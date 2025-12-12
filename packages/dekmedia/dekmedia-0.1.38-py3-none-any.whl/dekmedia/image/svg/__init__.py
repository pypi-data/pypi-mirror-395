import fitz
from copy import deepcopy
from PIL import Image
from lxml import etree
from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPDF
from svglib.fonts import FontMap
from ...font.const import font_props_default
from ...font.manager.default import font_manager


def get_svg_meta(root, fonts=None):
    def walk(node):
        ff = node.attrib.get('font-family')
        if ff and ff not in fonts:
            kwargs = {}
            for attr in ('style', 'weight', 'stretch', 'variant'):
                kwargs[attr] = node.attrib.get(f'font-{attr}') or font_props_default[attr]
            with font_manager:
                font_path = font_manager.find_family(ff, **kwargs)
            fonts[ff] = dict(
                font_path=font_path,
                weight=kwargs['weight'],
                style=kwargs['style'])
        for child in node.getchildren():
            walk(child)

    vb = root.attrib.get('viewBox')
    if vb:
        _, _, w, h = vb.split()
    else:
        w, h = root.attrib['width'], root.attrib['height']
    if fonts:
        fonts = deepcopy(fonts)
    else:
        fonts = {}
    walk(root)
    return (int(w), int(h)), fonts


# https://github.com/lovell/sharp/issues/1996#issuecomment-561656817
# No support `dominant-baseline``alignment-baseline`, use `dy=".25em"` to shift the <text/> along the y-axis
def load_svg(
        content, width=None, height=None,
        fonts=None):  # content: str | bytes # Remove <?xml ...> when `content` is a string
    parser = etree.XMLParser(resolve_entities=False, strip_cdata=False, recover=True)
    svg_root = etree.XML(content, parser=parser)
    size, fonts = get_svg_meta(svg_root, fonts)
    dpi = None
    k = 0.013889
    if width is not None:
        dpi = width / (size[0] * k)
    if height is not None and dpi is not None:
        dpi = height / (size[1] * k)
    if dpi is not None:
        dpi = round(dpi)
    font_map = FontMap()
    for ff, kwargs in fonts.items():
        font_map.register_font(ff, **kwargs)
    drawing = SvgRenderer('', font_map=font_map).render(svg_root)
    pdf = renderPDF.drawToString(drawing)
    doc = fitz.Document(stream=pdf)
    pix = doc.load_page(0).get_pixmap(alpha=True, dpi=dpi)
    cspace = pix.colorspace
    if cspace is None:
        mode = "L"
    elif cspace.n == 1:
        mode = "L" if pix.alpha == 0 else "LA"
    elif cspace.n == 3:
        mode = "RGB" if pix.alpha == 0 else "RGBA"
    else:
        mode = "CMYK"
    return Image.frombytes(mode, (pix.width, pix.height), pix.samples)
