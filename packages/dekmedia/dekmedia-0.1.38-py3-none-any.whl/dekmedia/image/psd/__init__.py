import os
import re
import json
from dataclasses import dataclass
from collections import OrderedDict
from PIL import Image, ImageDraw
from psd_tools import PSDImage
from psd_tools.api.layers import Layer, TypeLayer
from dektools.file import sure_dir, write_file
from dektools.str import slugify, replace, Unicode
from dektools.dict import dict_merge, assign
from ...font.const import font_props_default
from ...font.manager.default import font_manager
from ..text import text_in_box, Text, get_font, generate_image, get_text_box_height


@dataclass
class Rect:
    left: int
    top: int
    width: int
    height: int

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height


class Node:
    default_options = {}

    def __init__(self, rect: Rect, content, options=None):
        self.rect = rect
        self.content = content
        self.options = assign(self.default_options, {} if options is None else options)

    def update(self, content):
        self.content = content

    def update_options(self, options):
        dict_merge(self.options, options)

    def render(self, canvas: 'PsdCanvas', draw: ImageDraw, image: Image):
        raise NotImplementedError()

    def dump(self, canvas: 'PsdCanvas', name, path):
        raise NotImplementedError()

    @staticmethod
    def _save(image: Image, path, name):
        sure_dir(path)
        image.save(os.path.join(path, name + '.png'))


class ImageNode(Node):
    def update(self, content):
        if isinstance(content, str):
            from ..qr import make_qr
            content = make_qr(text=content)
        self.content = content.resize(self.content.size, Image.Resampling.LANCZOS)

    def render(self, canvas: 'PsdCanvas', draw: ImageDraw, image: Image):
        image.paste(self.content, (self.rect.left, self.rect.top), self.content.convert('RGBA'))

    def dump(self, canvas: 'PsdCanvas', name, path):
        self._save(self.content, path, name)


class TextNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = self._get_args()

    def _get_args(self):
        data = self.content[0]
        text, font, color = data['text'], data['font'], data['color']
        wrap = re.search(r'\S+[\r\n]+\S+', text)
        fp = font_manager.find_family(font['name'], weight=font['weight'], style=font['style'])
        font = get_font(fp, font['size'])
        return wrap, font, color

    @property
    def text(self):
        return replace(self.content[0]['text'], {'\r': '', '\n': ''})

    def update(self, content):
        self.content[0]['text'] = content

    def render(self, canvas: 'PsdCanvas', draw: ImageDraw, image: Image):
        text, (wrap, font, color) = self.text, self.args
        if wrap:
            text_in_box(draw, Text(text).block, (self.rect.left, self.rect.top), self.rect.width, font=font,
                        color=color)
        else:
            draw.text((self.rect.left, self.rect.top), text=text, fill=color, font=font)

    def dump(self, canvas: 'PsdCanvas', name, path):
        text, (wrap, font, color) = self.text, self.args
        if wrap:
            texts = Text(text).block
            height = get_text_box_height(font, texts, self.rect.width)
            image = Image.new('RGBA', (self.rect.width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            text_in_box(draw, texts, (0, 0), self.rect.width, font=font, color=color)
        else:
            image = generate_image(text, font=font, color=color, bgc=(0, 0, 0, 0))
        self._save(image, path, name)
        write_file(os.path.join(path, name + '.txt'), s=text)


class PsdCanvas:
    image_node_cls = ImageNode
    text_node_cls = TextNode

    def __init__(self, width, height, nodes: OrderedDict):
        self.width = width
        self.height = height
        self.nodes = nodes

    def __str__(self):
        return self.__class__.__name__ + str(json.dumps(
            {k: f"<{v.__class__.__name__}>" for k, v in self.nodes.items()},
            indent=2, ensure_ascii=False))

    def update(self, data):
        for name, content in data.items():
            self.nodes[name].update(content)

    def update_options(self, data):
        for name, options in data.items():
            self.nodes[name].update_options(options)

    def render(self):
        image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        for node in self.nodes.values():
            node.render(self, draw, image)
        return image

    def dump(self, path):
        for name, node in self.nodes.items():
            node.dump(self, name, path)
        path = os.path.join(path, 'meta', 'index.png')
        sure_dir(os.path.dirname(path))
        self.render().save(path)

    @classmethod
    def load(cls, file, short = 15, suffix: str = '-'): # short: int | None
        psd = PSDImage.open(file)
        names = get_psd_names(psd, short, suffix)
        nodes = OrderedDict()
        for layer in psd:
            layer: Layer
            name = names[layer.layer_id]
            rect = Rect(layer.left, layer.top, layer.width, layer.height)
            if isinstance(layer, TypeLayer):
                yy = layer.transform[3]  # https://github.com/psd-tools/psd-tools/issues/176#issuecomment-718514769
                data_list = []
                text = layer.engine_dict['Editor']['Text'].value
                fs = layer.resource_dict['FontSet']
                run_length = layer.engine_dict['StyleRun']['RunLengthArray']
                run_data = layer.engine_dict['StyleRun']['RunArray']
                index = 0
                for length, style in zip(run_length, run_data):
                    sub_text = text[index:index + length]
                    stylesheet = style['StyleSheet']['StyleSheetData']
                    color = get_font_color(stylesheet)
                    font = dict(
                        name=fs[stylesheet['Font']]['Name'].value,
                        size=stylesheet['FontSize'] * yy,
                        weight='bold' if stylesheet.get('FauxBold') else font_props_default['weight'],
                        style='italic' if stylesheet.get('FauxItalic') else font_props_default['style'],
                    )
                    if data_list and (data_list[-1]['font'], color) == (font, color):
                        data_list[-1]['text'] += sub_text
                    else:
                        data_list.append(dict(
                            text=sub_text,
                            font=font,
                            color=color
                        ))
                    index += length
                nodes[name] = cls.text_node_cls(rect, data_list)
            else:
                nodes[name] = cls.image_node_cls(rect, layer.composite())
        return cls(psd.width, psd.height, nodes)


def get_font_color(stylesheet):
    if 'FillColor' in stylesheet:
        values = stylesheet['FillColor']['Values']
    else:
        values = stylesheet['StrokeColor']['Values']
    values = [int(x * 255) for x in values]
    return tuple([*values[1:], values[0]])


def get_psd_names(psd, short, suffix):
    lid_map = {}
    for name, lid in sorted(((slugify(layer.name, True), layer.layer_id) for layer in psd), key=lambda x: x[0]):
        _short = len(name) if short is None else short
        ss = ""
        while True:
            _name = Unicode(name)[:_short] + ss
            if _name not in lid_map:
                break
            _short += 1
            ss += suffix
        lid_map[_name] = lid
    return {v: k for k, v in lid_map.items()}
