import re
from .manager.default import font_manager


def is_font_family(s):
    return re.fullmatch(r'^[ 0-9a-zA-Z_-]+$', s)


def get_font_source(name):
    if name is None:
        name = 'SimSun'
    if isinstance(name, str):
        if is_font_family(name):
            with font_manager:
                font_path = font_manager.find_family(name)
            if font_path is None:
                raise FileNotFoundError(f"Can't find font path by name: {name}")
        else:
            font_path = name
        with open(font_path, 'rb') as f:
            return f.read()
    elif isinstance(name, bytes):
        return name
    else:
        return name.getvalue()
