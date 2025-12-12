import qrcode
from qrcode.image.styledpil import StyledPilImage
from dektools.dict import assign

default_props = {
    'version': 1,
    'error': qrcode.constants.ERROR_CORRECT_L,
    'box': 10,
    'border': 0,
    'color': 'black',
    'bgc': 'white',
    'embed': None,
    'fit': True
}


def make_qr(**kwargs):
    props = assign(default_props, kwargs)
    qr = qrcode.QRCode(
        version=props['version'],
        error_correction=props['error'],
        box_size=props['box'],
        border=props['border'],
    )
    qr.add_data(props['text'])
    qr.make(fit=props['fit'])
    return qr.make_image(
        fill_color=props['color'],
        back_color=props['bgc'],
        image_factory=StyledPilImage,
        embeded_image=props['embed'] or None
    )
