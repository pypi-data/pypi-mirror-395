import os
from io import BytesIO
from PIL import Image
from dektools.file import sure_dir
from dektools.dict import is_list


def resize_image(image: Image, outputs, sizes=None):
    kwargs = {}
    if sizes:
        image = image.resize(max(sizes), Image.Resampling.LANCZOS)
        kwargs['sizes'] = sizes
    if not is_list(outputs):
        outputs = [outputs]
    for output in outputs:
        sure_dir(os.path.dirname(output))
        image.save(output, **kwargs)


def to_jpg(bs):
    image = Image.open(BytesIO(bs))
    image.convert('RGB')
    bi = BytesIO()
    image.save(bi, format='JPEG')
    return bi.getvalue()
