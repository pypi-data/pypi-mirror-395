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


from q2report.q2printer.q2printer import Q2Printer
from q2report.q2printer.xlsx_parts import xlsx_parts
from q2report.q2utils import num, int_, reMultiSpaceDelete, reDecimal, reNumber
from .rich_text_parser import RichTextParser, css_color_to_rgb

import zipfile
import re
import base64

reHtmlTagBr = re.compile(r"<\s*/*BR\s*/*\s*>\s*", re.IGNORECASE)

cm_2_inch = num(2.5396)
points_in_mm = num(2.834645669)
points_in_cm = num(points_in_mm) * num(10)
twip_in_cm = num(points_in_cm) * num(20)


class Q2PrinterXlsx(Q2Printer):
    def __init__(self, output_file, output_type=None):
        super().__init__(output_file, output_type)
        self.xlsx_sheets = []
        self.current_sheet = {}
        self.sheet_current_row = 1

        self.fonts = ["""<sz val="10"/><name val="Calibri"/>"""]
        self.fills = [
            """<fill><patternFill patternType="none"/></fill>""",
            """<fill><patternFill patternType="none"/></fill>""",
        ]
        self.borders = ["""<left/><right/><top/><bottom/><diagonal/>"""]
        self.cell_xfs = ["""<xf borderId="0" fillId="0" fontId="0" numFmtId="0" xfId="0"/>"""]
        self.num_fmts = []
        self.xmlImageList = []
        self.images_size_list = []

        self.cellStyleXfs = []
        self.cellStyles = []
        self.sharedStrings = []

        self.html = []
        self.style = {}

    def save(self):
        self.close_xlsx_sheet()
        super().save()

        # zipf = zipfile.ZipFile(self.output_file + ".zip", "w", zipfile.ZIP_DEFLATED)
        zipf = zipfile.ZipFile(self.output_file, "w", zipfile.ZIP_DEFLATED)
        zipf.writestr(
            "xl/sharedStrings.xml",
            (
                xlsx_parts["xl/sharedStrings.xml"]
                % (
                    len(self.sharedStrings),
                    len(self.sharedStrings),
                    "".join("""<si>%s</si>\n""" % st for st in self.sharedStrings),
                )
            ).encode("utf8"),
        )
        zipf.writestr("_rels/.rels", xlsx_parts["_rels/.rels"].encode("utf8"))
        self.save_styles(zipf)

        wb_sheets = []
        wb_workbook_rels = []
        wb_images = []
        wb_content_types = []

        for img in range(0, len(self.xmlImageList)):
            zipf.writestr("xl/media/image%s.png" % (img + 1), base64.b64decode(self.xmlImageList[img]))
            wb_images.append(xlsx_parts["images"] % ((img + 1), (img + 1)))

        for x in range(0, len(self.xlsx_sheets)):
            wb_content_types.append(xlsx_parts["wb_content_types_sheet"] % (x + 1))
            drawing_det = []
            if self.xlsx_sheets[x]["drawing"]:
                for img in range(0, len(self.xlsx_sheets[x]["drawing"])):
                    drawing_det.append(
                        xlsx_parts["xl/drawings/drawing.xml(png)"] % self.xlsx_sheets[x]["drawing"][img]
                    )

            zipf.writestr(
                "xl/drawings/_rels/drawing%s.xml.rels" % (x + 1),
                xlsx_parts["xl/drawings/_rels/drawing.xml.rels"] % "".join(wb_images),
            )
            zipf.writestr(
                "xl/drawings/drawing%s.xml" % (x + 1),
                (xlsx_parts["xl/drawings/drawing.xml"] % "".join(drawing_det)),
            )

            if drawing_det:
                wb_content_types.append(xlsx_parts["wb_content_types_image"] % (x + 1))
                zipf.writestr(
                    "xl/worksheets/_rels/sheet%s.xml.rels" % (x + 1),
                    (xlsx_parts["xl/worksheets/_rels/sheet.xml.rels"] % (x + 1)),
                )
                drawing = '<drawing r:id="rId1"/>'
            else:
                drawing = ""

            wb_sheets.append(
                """\
                    <sheet name="Sheet%s" sheetId="%s" r:id="rId%s"/>"""
                % (x + 1, x + 1, x + 9)
            )
            wb_workbook_rels.append(xlsx_parts["xl/_rels/workbook.xml.rels-line"] % (x + 9, x + 1))

            sheet_data = ""
            for z in range(len(self.xlsx_sheets[x]["sheetData"])):
                sheet_data += f'\t<row r="{z+1}" '
                sheet_data += f'\t customHeight="1" ht="{self.xlsx_sheets[x]["sheetData"][z]["height"]}" '
                sheet_data += f"""\n\t{"hidden='true'" if self.xlsx_sheets[x]["sheetData"][z]["height"] == 0 else "hidden='false'"} """
                sheet_data += f'\n\toutlineLevel="{self.xlsx_sheets[x]["sheetData"][z]["outline_level"]}" '
                sheet_data += ' collapsed="false" >'
                sheet_data += f'{"".join(self.xlsx_sheets[x]["sheetData"][z]["cells"])}'
                sheet_data += "</row>"

            merges = "".join(self.xlsx_sheets[x]["spans"])
            if merges:
                merges = """<mergeCells count="%s">%s\n</mergeCells>""" % (
                    len(self.xlsx_sheets[x]["spans"]),
                    merges,
                )
            zipf.writestr(
                "xl/worksheets/sheet%s.xml" % (x + 1),
                (
                    xlsx_parts["xl/worksheets/sheet.xml"]
                    % (self.xlsx_sheets[x]["cols"], sheet_data, merges, self.xlsx_sheets[x]["page"], drawing)
                ),
            )

        zipf.writestr(
            "xl/_rels/workbook.xml.rels",
            (xlsx_parts["xl/_rels/workbook.xml.rels"] % "".join(wb_workbook_rels)).encode("utf8"),
        )

        zipf.writestr("xl/workbook.xml", (xlsx_parts["xl/workbook.xml"] % "".join(wb_sheets)).encode("utf8"))

        zipf.writestr(
            "[Content_Types].xml",
            (xlsx_parts["[Content_Types].xml"] % "".join(wb_content_types)).encode("utf8"),
        )

        zipf.close()

    def reset_columns(self, widths):
        super().reset_columns(widths)
        self.close_xlsx_sheet()

        self.sheet_current_row = 1
        self.current_sheet = {}
        self.current_sheet["drawing"] = []

        cols = ["<cols>"]
        for col_index, col in enumerate(self._cm_columns_widths):
            cols.append(
                f'\n\t<col min="{col_index+1}" max="{col_index+1}" '
                f' width="{col * num(5.105)}" bestFit="0" customWidth="1"/>'
            )
        cols.append("\n</cols>")
        self.current_sheet["cols"] = "".join(cols)

        self.current_sheet["page"] = (
            f"<pageMargins "
            f'\nleft="{round(self.page_margin_left / cm_2_inch,4)}" '
            f'\nright="{round((self.page_margin_right-num(0.01)) / cm_2_inch,4)}" '
            f'\ntop="{round(self.page_margin_top / cm_2_inch,4)}" '
            f'\nbottom="{round(self.page_margin_bottom / cm_2_inch,4)}" '
            f'\nheader="0.3" '
            f'\nfooter="0.3"/> '
            f'\n\n<pageSetup paperSize="0" '
            f' paperHeight="{self.page_height}cm" paperWidth="{self.page_width}cm" '
            f"""orientation="{'landscape' if self.page_width > self.page_height else 'portrait'}"/>"""
        )
        self.current_sheet["sheetData"] = []
        self.current_sheet["spans"] = []

    def close_xlsx_sheet(self):
        if self.current_sheet:
            self.xlsx_sheets.append(self.current_sheet)

    def render_rows_section(self, rows_section, style, outline_level):
        super().render_rows_section(rows_section, style, outline_level)
        row_count = len(rows_section["heights"])
        spanned_cells = {}

        sheet_row = {}
        for row in range(row_count):  # вывод - по строкам
            height = rows_section["row_height"][row]
            if row in rows_section["auto_height_rows"]:
                height = 0

            sheet_row["height"] = height * points_in_cm

            sheet_row["cells"] = []
            sheet_row["outline_level"] = outline_level
            for col in range(self._columns_count):  # цикл по клеткам строки
                key = f"{row},{col}"
                if key in spanned_cells:
                    sheet_row["cells"].append(spanned_cells[key])
                    continue
                cell_address = self.get_cell_address(self.sheet_current_row, col)
                cell_data = rows_section.get("cells", {}).get(key, {})

                row_span = cell_data.get("rowspan", 1)
                col_span = cell_data.get("colspan", 1)

                cell_style = cell_data.get("style", {})
                if cell_style == {}:
                    cell_style = dict(style)
                    # cell_data["style"] = cell_style

                self.make_image(cell_data, row, col)
                cell_xml = self.make_xlsx_cell(cell_address, cell_style, cell_data)
                sheet_row["cells"].append(cell_xml)
                if row_span > 1 or col_span > 1:
                    merge_str = ":".join(
                        (
                            self.get_cell_address(self.sheet_current_row, col),
                            self.get_cell_address(self.sheet_current_row + row_span - 1, col + col_span - 1),
                        )
                    )
                    self.current_sheet["spans"].append(f'\n\t<mergeCell ref="{merge_str}"/>')
                    for span_row in range(int_(row_span)):
                        for span_col in range(int_(col_span)):
                            cell_address = self.get_cell_address(
                                self.sheet_current_row + span_row, span_col + col
                            )
                            spanned_cells[f"{span_row+row},{span_col+col}"] = self.make_xlsx_cell(
                                cell_address, cell_style
                            )
            self.current_sheet["sheetData"].append(dict(sheet_row))
            self.sheet_current_row += 1

    def save_styles(self, zipf):
        borders = """<borders count="%s">%s</borders>\n""" % (
            len(self.borders),
            "".join("\n<border>%s</border>" % x for x in self.borders),
        )
        fonts = """<fonts count="%s">%s</fonts>\n""" % (
            len(self.fonts),
            "".join("\n<font>%s</font>" % font for font in self.fonts),
        )
        cellXfs = """\n<cellXfs count="%s">%s\n</cellXfs>""" % (
            len(self.cell_xfs),
            "".join("\n%s" % style for style in self.cell_xfs),
        )
        fills = """\n<fills count="%s">%s</fills>""" % (
            len(self.fills),
            "\n".join(self.fills),
        )

        self.convert_num_fmt()
        num_fmts = f"""<numFmts count="{len(self.num_fmts)}">
                        {''.join(['<numFmt numFmtId="%s" formatCode="%s"/>' % (index+164, fmt)
                        for index, fmt in enumerate(self.num_fmts)])}
                    </numFmts>
        """

        zipf.writestr("xl/styles.xml", (xlsx_parts["xl/styles.xml"] % locals()).encode("utf8"))

    def convert_num_fmt(self):
        for idx, fmt in enumerate(self.num_fmts):
            if fmt.startswith("N"):
                dec = int_(_.group()) if (_ := reNumber.search(fmt)) else None
                if dec is not None:
                    efmt = "0."
                    efmt += "0" * dec
                    zero = efmt if "Z" in fmt else ""
                    self.num_fmts[idx] = f"{efmt};-{efmt};{zero};@"
                else:
                    if "Z" in fmt:
                        self.num_fmts[idx] = "General"
                    else:
                        self.num_fmts[idx] = "[=0]" ";General"
            elif fmt.startswith("F"):
                dec = int_(_.group()) if (_ := reNumber.search(fmt)) else None
                if dec is not None:
                    efmt = "#,###0."
                    efmt += "0" * dec
                    zero = efmt if "Z" in fmt else ""
                    self.num_fmts[idx] = f"{efmt};-{efmt};{zero};@"
                elif dec is None:
                    efmt = "#,###0.############"
                    zero = efmt if "Z" in fmt else ""
                    self.num_fmts[idx] = f"{efmt};-{efmt};{zero};@"
                else:
                    if "Z" in fmt:
                        self.num_fmts[idx] = "General"
                    else:
                        self.num_fmts[idx] = "[=0]" ";General"

    def get_cell_xf_id(self, style, numFmtId=0):
        border = f'borderId="{self.get_cell_borders(style)}"'
        fill = f'fillId="{self.get_fills_id(style)}"'
        font = f'fontId="{self.get_font_id(style)}"'
        num_fmt = f'numFmtId="{numFmtId}"'
        align = self.get_cell_align(style)

        cell_xfs = f'<xf {border} {fill} {font} {num_fmt} xfId="0" applyAlignment="true"> {align} </xf>'
        if cell_xfs not in self.cell_xfs:
            self.cell_xfs.append(cell_xfs)
        xf_id = self.cell_xfs.index(cell_xfs)

        return xf_id

    def get_font_id(self, style):
        # font_size = num(str(style["font-size"]).replace("pt", ""))
        font_size = num(str(style["font-size"]).replace("pt", "")) * num(0.93)
        font_family = style["font-family"]
        font_weight = "<b/>" if style.get("font-weight", "") == "bold" else ""
        font_color = f'<color rgb="{css_color_to_rgb(color)}"/>' if (color := style.get("color", "")) else ""
        font_style = f'<name val="{font_family}"/> <sz val="{font_size}"/> {font_color} {font_weight}'
        if font_style not in self.fonts:
            self.fonts.append(font_style)
        font_id = self.fonts.index(font_style)
        return font_id

    def get_fills_id(self, style):
        color = style.get("background")
        if color is None:
            return 0
        fill = (
            '<fill><patternFill patternType="solid">'
            f'<fgColor rgb="{css_color_to_rgb(color)}"/>'
            f'<bgColor rgb="{css_color_to_rgb(color)}"/>'
            "</patternFill></fill>"
        )

        if fill not in self.fills:
            self.fills.append(fill)
        return self.fills.index(fill)

    def get_num_fmt_id(self, numFormat):
        if numFormat not in self.num_fmts:
            self.num_fmts.append(numFormat)
        return self.num_fmts.index(numFormat) + 164

    def make_image(self, cell_data, row, col):
        for x in cell_data.get("images", []):
            width, height, imageIndex = self.prepare_image(x, cell_data.get("width"))

            width = num(width) * num(12700) * points_in_cm
            height = num(height) * num(12700) * points_in_cm

            tmp_drawing = {}
            tmp_drawing["_id"] = imageIndex + 1
            tmp_drawing["_row"] = self.sheet_current_row - 1
            tmp_drawing["_col"] = col
            tmp_drawing["_height"] = int(height)
            tmp_drawing["_width"] = int(width)
            self.current_sheet["drawing"].append(tmp_drawing)

    def make_xlsx_cell(self, cell_address, cell_style, cell_data: dict = {}):
        raw_text = cell_data.get("xlsx_data", "")
        cell_format = cell_data.get("format", "")

        isNumber = reDecimal.match(raw_text)
        if isNumber and (cell_format or cell_style.get("text-align") == "right"):
            numFmtId = self.get_num_fmt_id(cell_format) if cell_format else 0

            xf_id = self.get_cell_xf_id(cell_style, numFmtId)
            return f"""\n\t <c r="{cell_address}" s="{xf_id}" t="n">
                                    <v>{raw_text}</v>
                                </c>"""
        else:
            xf_id = self.get_cell_xf_id(cell_style)
            cell_text = cell_data.get("data", "")
            # Normalize cell text
            cell_text = (cell_text or "").replace("\r", "").replace("\n", "")
            cell_text = reMultiSpaceDelete.sub(" ", cell_text)
            cell_text = reHtmlTagBr.sub("\n", cell_text)

            # Parse inline formatting
            fontsize = str(cell_style.get("font-size", "10pt")).replace("pt", "")
            fontfamily = cell_style.get("font-family", "Calibri")
            parser = RichTextParser(fontfamily, fontsize)
            parser.feed(cell_text, cell_style)
            runs = parser.get_runs()

            if len(runs) == 1:
                cell_content = f"<t>{cell_text}</t>"
            else:
                cell_content = "".join(runs)

            if cell_content:
                if cell_content not in self.sharedStrings:
                    self.sharedStrings.append(cell_content)
                    shared_strings_id = len(self.sharedStrings) - 1
                else:
                    shared_strings_id = self.sharedStrings.index(cell_content)
                return f"""\n\t <c r="{cell_address}" s="{xf_id}" t="s">
                                    <v>{shared_strings_id}</v>
                                </c>"""
            else:
                return f'\n\t<c r="{cell_address}" s="{xf_id}"/>'

    def get_cell_align(self, cell_style):

        if cell_style["vertical-align"] == "middle":
            vertical = 'vertical="center"'
        elif cell_style["vertical-align"] == "top":
            vertical = 'vertical="top"'
        else:
            vertical = ""

        padding = cell_style["padding"].replace("cm", "").split(" ")
        while len(padding) < 4:
            padding += padding

        if cell_style["text-align"] == "center":
            horizontal = 'horizontal="center"'
        elif cell_style["text-align"] == "right":
            horizontal = 'horizontal="right"'
            if padding[1]:
                horizontal += f""" indent="{int(round(num(padding[1]) / num(0.25)))}" """
        elif cell_style["text-align"] == "justify":
            horizontal = 'horizontal="justify"'
        else:
            horizontal = ""
            if padding[3]:
                horizontal = f""" horizontal="left" indent="{int(round((num(padding[3])) / num(0.25)))}" """
        return f'\n\t<alignment {horizontal} {vertical} wrapText="true"/>\n'

    def get_cell_borders(self, cell_style):
        border_width = cell_style["border-width"].split(" ")
        while len(border_width) < 4:
            border_width += border_width
        border = []

        border_color = 'auto="1"'
        if color := cell_style.get("border-color"):
            border_color = f' rgb="{css_color_to_rgb(color)}"'

        border_width_dict = {
            side: int_(border_width[index]) for index, side in enumerate(("top", "right", "bottom", "left"))
        }

        for side in ("left", "right", "top", "bottom"):
            if int_(border_width_dict[side]):
                bw = self.get_border_width(border_width_dict[side])
                border.append(f'<{side} style="{bw}"><color {border_color}/></{side}>')
        border.append("<diagonal/>")

        borders = "\n".join(border)

        if borders not in self.borders:
            self.borders.append(borders)
            border_id = len(self.borders) - 1
        else:
            border_id = self.borders.index(borders)
        return border_id

    def get_border_width(self, borderWidth):
        borderWidth = num(borderWidth)
        if borderWidth == 1:
            return "thin"
        elif borderWidth <= 3:
            return "medium"
        elif borderWidth > 3:
            return "thick"

    def get_cell_address(self, row, col):
        return self.get_xls_column_letter(col + 1) + str(row)

    def get_xls_column_letter(self, col):
        rez = ""
        while col:
            part = col % 26
            if part == 0:
                part = 26
            col = int((col - 1) / 26)
            rez = chr(ord("A") + part - 1) + rez
        return rez
