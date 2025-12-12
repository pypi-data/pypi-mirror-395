from html.parser import HTMLParser
import html
import re

HTML_COLOR_MAP = {
    "aliceblue": "f0f8ff",
    "antiquewhite": "faebd7",
    "aqua": "00ffff",
    "aquamarine": "7fffd4",
    "azure": "f0ffff",
    "beige": "f5f5dc",
    "bisque": "ffe4c4",
    "black": "000000",
    "blanchedalmond": "ffebcd",
    "blue": "0000ff",
    "blueviolet": "8a2be2",
    "brown": "a52a2a",
    "burlywood": "deb887",
    "cadetblue": "5f9ea0",
    "chartreuse": "7fff00",
    "chocolate": "d2691e",
    "coral": "ff7f50",
    "cornflowerblue": "6495ed",
    "cornsilk": "fff8dc",
    "crimson": "dc143c",
    "cyan": "00ffff",  # synonym of aqua
    "darkblue": "00008b",
    "darkcyan": "008b8b",
    "darkgoldenrod": "b8860b",
    "darkgray": "a9a9a9",
    "darkgreen": "006400",
    "darkgrey": "a9a9a9",
    "darkkhaki": "bdb76b",
    "darkmagenta": "8b008b",
    "darkolivegreen": "556b2f",
    "darkorange": "ff8c00",
    "darkorchid": "9932cc",
    "darkred": "8b0000",
    "darksalmon": "e9967a",
    "darkseagreen": "8fbc8f",
    "darkslateblue": "483d8b",
    "darkslategray": "2f4f4f",
    "darkslategrey": "2f4f4f",
    "darkturquoise": "00ced1",
    "darkviolet": "9400d3",
    "deeppink": "ff1493",
    "deepskyblue": "00bfff",
    "dimgray": "696969",
    "dimgrey": "696969",
    "dodgerblue": "1e90ff",
    "firebrick": "b22222",
    "floralwhite": "fffaf0",
    "forestgreen": "228b22",
    "fuchsia": "ff00ff",
    "gainsboro": "dcdcdc",
    "ghostwhite": "f8f8ff",
    "gold": "ffd700",
    "goldenrod": "daa520",
    "gray": "808080",
    "green": "008000",
    "greenyellow": "adff2f",
    "grey": "808080",  # synonym of gray
    "honeydew": "f0fff0",
    "hotpink": "ff69b4",
    "indianred": "cd5c5c",
    "indigo": "4b0082",
    "ivory": "fffff0",
    "khaki": "f0e68c",
    "lavender": "e6e6fa",
    "lavenderblush": "fff0f5",
    "lawngreen": "7cfc00",
    "lemonchiffon": "fffacd",
    "lightblue": "add8e6",
    "lightcoral": "f08080",
    "lightcyan": "e0ffff",
    "lightgoldenrodyellow": "fafad2",
    "lightgray": "d3d3d3",
    "lightgreen": "90ee90",
    "lightgrey": "d3d3d3",
    "lightpink": "ffb6c1",
    "lightsalmon": "ffa07a",
    "lightseagreen": "20b2aa",
    "lightskyblue": "87cefa",
    "lightslategray": "778899",
    "lightslategrey": "778899",
    "lightsteelblue": "b0c4de",
    "lightyellow": "ffffe0",
    "lime": "00ff00",
    "limegreen": "32cd32",
    "linen": "faf0e6",
    "magenta": "ff00ff",  # synonym of fuchsia
    "maroon": "800000",
    "mediumaquamarine": "66cdaa",
    "mediumblue": "0000cd",
    "mediumorchid": "ba55d3",
    "mediumpurple": "9370db",
    "mediumseagreen": "3cb371",
    "mediumslateblue": "7b68ee",
    "mediumspringgreen": "00fa9a",
    "mediumturquoise": "48d1cc",
    "mediumvioletred": "c71585",
    "midnightblue": "191970",
    "mintcream": "f5fffa",
    "mistyrose": "ffe4e1",
    "moccasin": "ffe4b5",
    "navajowhite": "ffdead",
    "navy": "000080",
    "oldlace": "fdf5e6",
    "olive": "808000",
    "olivedrab": "6b8e23",
    "orange": "ffa500",
    "orangered": "ff4500",
    "orchid": "da70d6",
    "palegoldenrod": "eee8aa",
    "palegreen": "98fb98",
    "paleturquoise": "afeeee",
    "palevioletred": "db7093",
    "papayawhip": "ffefd5",
    "peachpuff": "ffdab9",
    "peru": "cd853f",
    "pink": "ffc0cb",
    "plum": "dda0dd",
    "powderblue": "b0e0e6",
    "purple": "800080",
    "rebeccapurple": "663399",
    "red": "ff0000",
    "rosybrown": "bc8f8f",
    "royalblue": "4169e1",
    "saddlebrown": "8b4513",
    "salmon": "fa8072",
    "sandybrown": "f4a460",
    "seagreen": "2e8b57",
    "seashell": "fff5ee",
    "sienna": "a0522d",
    "silver": "c0c0c0",
    "skyblue": "87ceeb",
    "slateblue": "6a5acd",
    "slategray": "708090",
    "slategrey": "708090",
    "snow": "fffafa",
    "springgreen": "00ff7f",
    "steelblue": "4682b4",
    "tan": "d2b48c",
    "teal": "008080",
    "thistle": "d8bfd8",
    "tomato": "ff6347",
    "turquoise": "40e0d0",
    "violet": "ee82ee",
    "wheat": "f5deb3",
    "white": "ffffff",
    "whitesmoke": "f5f5f5",
    "yellow": "ffff00",
    "yellowgreen": "9acd32",
}


def css_color_to_rgb(color):
    color = color.strip().lower()
    if color.startswith("#"):
        hex_val = color.lstrip("#")
        if len(hex_val) == 3:
            hex_val = "".join([c * 2 for c in hex_val])
        return "FF" + hex_val.upper()
    elif color in HTML_COLOR_MAP:
        return "FF" + HTML_COLOR_MAP[color].upper()
    elif color.startswith("rgb("):
        match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", color)
        if match:
            r, g, b = map(int, match.groups())
            return f"FF{r:02X}{g:02X}{b:02X}"
    elif color == "":
        return "FF000000"
    else:
        return "FFFFFFFF"
    return None


class RichTextParser(HTMLParser):
    def __init__(self, fontfamily, base_fontsize):
        super().__init__()
        self.runs = []
        self.style_stack = []
        self.current_text = ""
        self.fontfamily = fontfamily
        self.base_fontsize = float(base_fontsize)

    def feed(self, cell_text, cell_style):
        cell_text = cell_text.strip()
        if cell_style.get("font-weight", "") == "bold":
            cell_text = f"<b>{cell_text}</b>"
        if cell_style.get("font-style", "") == "italic":
            cell_text = f"<i>{cell_text}</i>"
        if cell_style.get("text-decoration", "") == "underline":
            cell_text = f"<u>{cell_text}</u>"
        if color := cell_style.get("color", ""):
            cell_text = f"<font color=#{css_color_to_rgb(color)[2:]}>{cell_text}</font>"
        return super().feed(cell_text)

    def _get_current_style(self):
        return self.style_stack[-1] if self.style_stack else {}

    def _flush_current_text(self):
        if not self.current_text:
            return
        style = self._get_current_style()
        rPr = [f'<rFont val="{self.fontfamily}"/>']
        rPr.append(f'<sz val="{style.get("fontsize", self.base_fontsize)}"/>')
        if style.get("bold"):
            rPr.append("<b/>")
        if style.get("italic"):
            rPr.append("<i/>")
        if style.get("underline"):
            rPr.append("<u/>")
        if style.get("color"):
            rPr.append(f'<color rgb="{style["color"]}"/>')

        self.runs.append(
            "<r>"
            f"<rPr>{''.join(rPr)}</rPr>"
            f'<t xml:space="preserve">{html.escape(self.current_text)}</t>'
            "</r>"
        )
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        self._flush_current_text()
        style = self._get_current_style().copy()
        tag = tag.lower()

        if tag == "b":
            style["bold"] = True
        elif tag == "i":
            style["italic"] = True
        elif tag == "u":
            style["underline"] = True
        elif tag == "br":
            self._flush_current_text()
            self.runs.append("<br/>")
        elif tag == "font":
            for name, value in attrs:
                if name == "size":
                    try:
                        if value.startswith("+"):
                            style["fontsize"] = str(self.base_fontsize + 2 * int(value[1:]))
                        elif value.startswith("-"):
                            style["fontsize"] = str(self.base_fontsize - 2 * int(value[1:]))
                        else:
                            style["fontsize"] = value
                    except Exception:
                        pass
                elif name == "color":
                    rgb = css_color_to_rgb(value)
                    if rgb:
                        style["color"] = rgb
        self.style_stack.append(style)

    def handle_endtag(self, tag):
        self._flush_current_text()
        if self.style_stack:
            self.style_stack.pop()

    def handle_data(self, data):
        self.current_text += data

    def handle_entityref(self, name):
        self.current_text += html.unescape(f"&{name};")

    def handle_charref(self, name):
        self.current_text += html.unescape(f"&#{name};")

    def get_runs(self):
        self._flush_current_text()
        return self.runs
