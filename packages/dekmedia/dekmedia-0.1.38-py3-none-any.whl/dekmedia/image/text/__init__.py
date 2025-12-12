import string
from typing import Iterable, Literal
from io import BytesIO
from PIL import Image as PilImage, ImageDraw, ImageFont
from dektools.func import FuncAnyArgs
from ...font import get_font_source


def get_spacing(font, spacing=None):
    if spacing is None:
        spacing = 1.0
    if isinstance(spacing, float):
        spacing = font.font.descent * spacing
    return spacing


def get_font(src, size):
    return ImageFont.truetype(BytesIO(get_font_source(src)), size)


def generate_image(text: str, font, angle=0, color=None, bgc=None, spacing=None):
    color = color or (0, 0, 0)
    bgc = bgc or (255, 255, 255)
    spacing = get_spacing(font, spacing)
    image = PilImage.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
    image = PilImage.new('RGBA' if len(bgc) == 4 else 'RGB', (box[2], int(box[3] + font.font.descent)), bgc)
    draw = ImageDraw.Draw(image)
    draw.text(box[:2], text, font=font, fill=color, spacing=spacing)
    if angle:
        image = image.rotate(angle, expand=True, fillcolor=bgc)
    return image


def get_text_size(font, text):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


whitespace = set(string.whitespace)


def get_text_box_info(font, texts: Iterable[str], width):
    def append(_w, _h, _word):
        check_the_last()
        widths.append(_w)
        heights.append(_h)
        lines.append(_word)

    def check_the_last():
        if heights and heights[-1] == 0:
            heights[-1] = jh

    lines = ['']
    widths = [0]
    heights = [0]
    jw, jh = get_text_size(font, 'j')
    for word in texts:
        w, h = get_text_size(font, lines[-1] + word)
        if word == '\n':
            append(w, h, word)
        elif w > width + jw / 2:
            append(w, h, word)
        else:
            if lines[-1] == '\n':
                append(0, 0, '')
            lines[-1] += word
            widths[-1] = w
            heights[-1] = h
    check_the_last()
    return lines, widths, heights


def get_text_box_height(font, texts: Iterable[str], width, spacing=None):
    spacing = get_spacing(font, spacing)
    lines, _, heights = get_text_box_info(font, texts, width)
    cursor = 0
    for i in range(len(lines)):
        cursor += heights[i] + spacing
    return int(cursor)


def text_in_box(draw: ImageDraw, texts: Iterable[str], xy, width, font, spacing=None, color=None,
                align: Literal['left', 'right', 'middle'] = 'left', hidden=None):
    if color is None:
        color = (0, 0, 0)
    spacing = get_spacing(font, spacing)
    lines, widths, heights = get_text_box_info(font, texts, width)
    x, y = xy
    cursor = 0
    hidden = FuncAnyArgs(hidden) if hidden else None
    for i, line in enumerate(lines):
        if align == 'left':
            offset = 0
        elif align == 'right':
            offset = width - widths[i]
        else:
            offset = (width - widths[i]) // 2
        if not hidden or not hidden(cursor + heights[i], cursor, i, len(lines)):
            draw.text((x + offset, y + cursor), line, font=font, fill=color)
        cursor += heights[i] + spacing


class Text:
    def __init__(self, s: str):
        self.content = s

    @property
    def block(self):
        return list(self.content)

    @property
    def words(self):
        result = []
        last_ascii = False
        for c in self.content:
            if c.isascii():
                if c.isalpha():
                    if last_ascii:
                        result[-1] += c
                    else:
                        result.append(c)
                    last_ascii = True
                else:
                    result.append(c)
                    last_ascii = False
            else:
                result.append(c)
                last_ascii = False
        return result
