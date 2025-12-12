import re
from html.parser import HTMLParser

FONT_SIZE_ADJUST = {
    "+1": 2,
    "-1": -2,
    "+2": 4,
    "-2": -4,
}


def parse_padding(padding_str):
    # Converts "0.05cm 0.05cm 0.05cm 0.05cm" → [top, right, bottom, left]
    sizes = [float(x.replace("cm", "")) for x in padding_str.strip().split()]
    if len(sizes) == 1:
        return [sizes[0]] * 4
    elif len(sizes) == 2:
        return [sizes[0], sizes[1], sizes[0], sizes[1]]
    elif len(sizes) == 3:
        return [sizes[0], sizes[1], sizes[2], sizes[1]]
    elif len(sizes) == 4:
        return sizes
    else:
        return [0.0, 0.0, 0.0, 0.0]


class HTMLStyledTextExtractor(HTMLParser):
    def __init__(self, base_font_size):
        super().__init__()
        self.base_font_size = base_font_size
        self.result = []  # list of (word, effective_font_size, style_factor)
        self.font_stack = [base_font_size]
        self.bold = False
        self.italic = False
        self.underline = False

    def handle_starttag(self, tag, attrs):
        if tag == "font":
            attr_dict = dict(attrs)
            size = attr_dict.get("size")
            if size in FONT_SIZE_ADJUST:
                self.font_stack.append(self.font_stack[-1] + FONT_SIZE_ADJUST[size])
            else:
                self.font_stack.append(self.font_stack[-1])
        elif tag == "b":
            self.bold = True
        elif tag == "i":
            self.italic = True
        elif tag == "u":
            self.underline = True

    def handle_endtag(self, tag):
        if tag == "font" and len(self.font_stack) > 1:
            self.font_stack.pop()
        elif tag == "b":
            self.bold = False
        elif tag == "i":
            self.italic = False
        elif tag == "u":
            self.underline = False

    def handle_data(self, data):
        words = data.split()
        for word in words:
            style_factor = 1.0
            if self.bold:
                style_factor += 0.10
            if self.italic:
                style_factor += 0.05
            # underline could affect height slightly, not width
            self.result.append((word, self.font_stack[-1], style_factor))


def estimate_cell_height_cm(cell_data):
    text = cell_data["data"]
    style = cell_data["style"]
    width_cm = float(cell_data["width"])
    padding_cm = parse_padding(style.get("padding", "0cm 0cm 0cm 0.0cm"))
    font_size_pt = int(re.search(r"\d+", str(style.get("font-size", "10pt"))).group())

    # Available text width in cm
    available_width_cm = width_cm - padding_cm[1] - padding_cm[3]
    if available_width_cm <= 0:
        return 0.0

    # Extract styled words
    parser = HTMLStyledTextExtractor(base_font_size=font_size_pt)
    parser.feed(text)
    styled_words = parser.result  # list of (word, font_size, style_factor)

    # Simulate text layout
    lines = []
    current_line_width = 0.0
    current_line = []

    for word, size_pt, style_factor in styled_words:
        avg_char_width_cm = 0.45 * size_pt * 0.0352778 * style_factor
        word_width_cm = len(word) * avg_char_width_cm

        if current_line_width + word_width_cm <= available_width_cm:
            current_line.append(word)
            current_line_width += word_width_cm + avg_char_width_cm  # add space
        else:
            lines.append(current_line)
            current_line = [word]
            current_line_width = word_width_cm + avg_char_width_cm
    if current_line:
        lines.append(current_line)

    # Estimate line height (slightly increased if underline was used)
    underline_used = any(parser.underline for (_, _, _) in styled_words)
    max_font_size = max((size for (_, size, _) in styled_words), default=font_size_pt)
    line_height_cm = max_font_size * 0.0352778 * (1.2 + (0.1 if underline_used else 0))

    total_text_height_cm = len(lines) * line_height_cm
    total_height_cm = total_text_height_cm + padding_cm[0] + padding_cm[2]

    return round(total_height_cm, 2)
