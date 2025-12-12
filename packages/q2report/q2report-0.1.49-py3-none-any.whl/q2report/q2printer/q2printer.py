#    Copyright © 2021 Andrei Puchko
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import os
from q2report.q2utils import num
import sys
import subprocess
from .calc_height import estimate_cell_height_cm

try:
    from PyQt6.QtGui import QTextDocument
    from PyQt6.QtWidgets import QApplication

    pyqt6_installed = True
except Exception:
    pyqt6_installed = False


def get_printer(output_file, output_type=None):
    if output_type is None and isinstance(output_file, str):
        output_type = os.path.splitext(output_file)[1].lower().replace(".", "")

    if output_type == "html":
        from q2report.q2printer.q2printer_html import Q2PrinterHtml as _printer
    elif output_type == "xlsx":
        from q2report.q2printer.q2printer_xlsx import Q2PrinterXlsx as _printer
    elif output_type == "docx":
        from q2report.q2printer.q2printer_docx import Q2PrinterDocx as _printer
    elif output_type == "pdf":
        from q2report.q2printer.q2printer_pdf import Q2PrinterPdf as _printer
    else:
        raise BaseException(f"format {output_type} is not supported")
    return _printer(output_file, output_type)


class Q2Printer:
    def __init__(self, output_file, output_type=None):
        self.output_file = self.checkOutputFileName(output_file)
        if output_type is None and isinstance(self.output_file, str):
            output_type = os.path.splitext(output_file)[1]
        self.output_type = output_type.lower().replace(".", "")
        self.xmlImageList = []
        # self._OF = None
        self._columns_count = None
        self._cm_columns_widths = []
        self.q2report = None
        self._pyqt6_app = None
        if pyqt6_installed:
            if QApplication.instance() is None:
                self._pyqt6_app = QApplication([])
            else:
                self._pyqt6_app = QApplication.instance()

    def checkOutputFileName(self, fileName=""):
        if not os.path.isdir(os.path.dirname(fileName)):
            os.mkdir(os.path.dirname(fileName))
        co = 0
        name, ext = os.path.splitext(fileName)
        while True:
            if os.path.isfile(fileName):
                try:
                    os.remove(fileName)
                except Exception as e:
                    co += 1
                    fileName = f"{name}{co:03d}{ext}"
                    continue
            break
        return fileName

    def open_output_file(self):
        # if not os.path.isdir(os.path.dirname(self.output_file)):
        #     os.mkdir(os.path.dirname(self.output_file))
        # self._OF = open(self.output_file, "w", encoding="utf8")
        pass

    def get_cell_height(self, cell_data):
        if pyqt6_installed:
            padding = cell_data["style"]["padding"].replace("cm", "").split(" ")
            while len(padding) < 4:
                padding += padding

            cm = num(96 / num(2.54))
            text_doc = QTextDocument()

            text_doc.setTextWidth((num(cell_data["width"]) - num(padding[1]) - num(padding[3])) * cm)

            style = cell_data["style"]
            style = "p {%s}" % ";".join([f"{x}:{style[x]}" for x in style])
            text_doc.setDefaultStyleSheet(style)
            text_doc.setHtml("<p>%s</p>" % cell_data["data"])
            height = round(num(text_doc.size().height()) / cm, 2)
            return height
        else:
            return num(estimate_cell_height_cm(cell_data))

    def calculate_real_sizes(self, rows_section, style):
        row_count = len(rows_section["heights"])
        spanned_cells = {}
        rows_section["row_height"] = []
        rows_section["min_row_height"] = []
        rows_section["max_row_height"] = []
        rows_section["auto_height_rows"] = []
        for row in range(row_count):
            spltd_heights = str(rows_section["heights"][row]).split("-")
            rows_section["min_row_height"].append(num(spltd_heights[0]))
            rows_section["max_row_height"].append(num(spltd_heights[1]) if len(spltd_heights) == 2 else 0)
            if rows_section["min_row_height"] == 0 and rows_section["max_row_height"] == 0:
                rows_section["auto_height_rows"].append(row)
            rows_section["row_height"].append(
                max(rows_section["max_row_height"][-1], rows_section["min_row_height"][-1])
            )

            for col in range(self._columns_count):
                key = f"{row},{col}"
                cell_data = rows_section.get("cells", {}).get(key, {})

                if not cell_data:
                    continue
                if cell_data.get("colspan", 0) > 1:
                    cell_data["width"] = sum(self._cm_columns_widths[col : col + cell_data["colspan"]])
                else:
                    cell_data["width"] = self._cm_columns_widths[col]
                if cell_data.get("data"):
                    cell_data["data"] = cell_data["data"].replace("\n", "<br>")
                    cell_data["height"] = self.get_cell_height(cell_data)
                    if key in spanned_cells:
                        spanned_cells[key] = cell_data["height"]
                    else:
                        if (
                            rows_section["min_row_height"][row] == 0
                            and rows_section["max_row_height"][row] == 0
                        ):
                            if rows_section["row_height"][row] < cell_data["height"]:
                                rows_section["row_height"][row] = cell_data["height"]

                if cell_data.get("rowspan", 0) > 1 or cell_data.get("colspan", 0) > 1:
                    spanned_cells[key] = 0

                # TODO: if background image (how to know?) - do not change height
                for image in cell_data.get("images", []):
                    w, h, i = self.prepare_image(image, cell_data.get("width"))
                    if image["height"] == 0:
                        image["height"] = max(image["height"], rows_section["row_height"][row])
                    if rows_section["row_height"][row] < h:
                        rows_section["row_height"][row] = h
            if (
                rows_section["min_row_height"][row] != 0
                and rows_section["row_height"][row] < rows_section["min_row_height"][row]
            ):
                rows_section["row_height"][row] = rows_section["min_row_height"][row]
            if (
                rows_section["max_row_height"][row] != 0
                and rows_section["row_height"][row] > rows_section["max_row_height"][row]
            ):
                rows_section["row_height"][row] = rows_section["max_row_height"][row]
            ##################
            if rows_section["min_row_height"][row] != 0 and rows_section["max_row_height"][row] == 0:
                rows_section["row_height"][row] = rows_section["min_row_height"][row]
            elif rows_section["min_row_height"][row] == 0 and rows_section["max_row_height"][row] != 0:
                rows_section["row_height"][row] = rows_section["max_row_height"][row]
            ##################
        # calculating height for spanned cells
        rows_section["hidden_rows"] = {i for i, h in enumerate(rows_section["row_height"]) if h == 0}
        for key in spanned_cells:
            start_row = int(key.split(",")[0])
            haha = 0
            for row in range(start_row, start_row + rows_section["cells"][key]["rowspan"]):
                haha += rows_section["row_height"][row] if rows_section["row_height"][row] else num(0)
                if row in rows_section["hidden_rows"]:
                    rows_section["hidden_rows"].remove(row)
            rest = spanned_cells[key] - haha
            for uprow in range(start_row, start_row + rows_section["cells"][key]["rowspan"]):
                if rows_section["row_height"][uprow] != 0:
                    continue
                if rest > rows_section["row_height"][uprow]:
                    if rows_section["max_row_height"][uprow] == 0:
                        rows_section["row_height"][uprow] += rest
                        break
        rows_section["section_height"] = sum(rows_section["row_height"])

    def render_rows_section(self, rows_section, style, outline_level):
        self.calculate_real_sizes(rows_section, style)

    def reset_page(
        self,
        page_width=21.0,
        page_height=29.0,
        page_margin_left=2.0,
        page_margin_top=1.0,
        page_margin_right=1.0,
        page_margin_bottom=1.0,
    ):
        self.page_width = num(page_width)
        self.page_height = num(page_height)
        self.page_margin_left = num(page_margin_left)
        self.page_margin_right = num(page_margin_right)
        self.page_margin_top = num(page_margin_top)
        self.page_margin_bottom = num(page_margin_bottom)
        self._current_width = self.page_width - self.page_margin_left - self.page_margin_right
        self._current_height = self.page_height - self.page_margin_top - self.page_margin_bottom

    def reset_columns(self, widths=[]):
        self._columns_count = len(widths)
        _cm_page_width = self._current_width

        self._cm_columns_widths = [0 for x in range(self._columns_count)]

        _fixed_columns_width = [num(x) if "%" not in x and num(x) != 0 else 0 for x in widths]
        _procent_columns_width = [num(x.replace("%", "").strip()) if "%" in x else 0 for x in widths]
        _float_columns_count = (
            self._columns_count
            - len([x for x in _procent_columns_width if x != 0])
            - len([x for x in _fixed_columns_width if x != 0])
        )
        _procent_width = num((_cm_page_width - num(sum(_fixed_columns_width))) / num(100))

        for x in range(self._columns_count):
            if _fixed_columns_width[x] != 0:
                self._cm_columns_widths[x] = _fixed_columns_width[x]
            else:
                prc = _procent_columns_width[x]
                if prc == 0:
                    prc = (num(100) - sum(_procent_columns_width)) / _float_columns_count
                self._cm_columns_widths[x] = round(_procent_width * prc, 2)
        self._cm_columns_widths = [round(x, 2) for x in self._cm_columns_widths]

    def prepare_image(self, image_dict, col_width):
        # col_width = self._cm_columns_widths[col]
        image = image_dict["image"]
        width = image_dict["width"]
        height = image_dict["height"]
        pixel_width = image_dict["pixel_width"]
        pixel_height = image_dict["pixel_height"]

        if image not in self.xmlImageList:
            self.xmlImageList.append(image)
            imageIndex = len(self.xmlImageList) - 1
        else:
            imageIndex = self.xmlImageList.index(image)
        if height == 0:
            if width == 0:
                width = num(col_width)
            height = width * pixel_height / pixel_width
        elif width == 0 and height != 0:
            width = height * pixel_width / pixel_height

        return width, height, imageIndex

    def save(self):
        # self._OF.close()
        pass

    def show(self):
        if isinstance(self.output_file, (str, bytes, os.PathLike, int)):
            if os.path.isfile(self.output_file):
                if sys.platform == "win32":
                    # os.startfile(os.path.abspath(self.output_file))
                    subprocess.Popen(
                        ["start", os.path.abspath(self.output_file)],
                        close_fds=True,
                        shell=True,
                        creationflags=subprocess.DETACHED_PROCESS,
                    )
                # elif sys.platform == 'darwin':
                #     subprocess.Popen(["open", self.output_file], close_fds=True, shell=False)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.Popen([opener, self.output_file], close_fds=True, shell=False)
