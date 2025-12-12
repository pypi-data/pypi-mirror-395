import os
from pathlib import Path
from find_system_fonts_filename import get_system_fonts_filename, FindSystemFontsFilenameException
from dektools.ext.font import font_extensions

path_res = Path(__file__).resolve().parent.parent / 'res'


def iter_dir_fonts(*paths):
    for path in paths:
        if os.path.isdir(path):
            for root, _, filenames in os.walk(path):
                for name in filenames:
                    if os.path.splitext(name)[-1].lower() in font_extensions:
                        yield os.path.join(root, name)


def iter_sys_fonts():
    try:
        yield from get_system_fonts_filename()
    except FindSystemFontsFilenameException:
        pass


def iter_res_fonts():
    yield from iter_dir_fonts(path_res)


def iter_all_fonts():
    yield from iter_res_fonts()
    yield from iter_sys_fonts()
