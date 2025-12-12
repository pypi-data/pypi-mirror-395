from contextlib import redirect_stderr
from fontTools import ttLib
from ..const import weight_dict, weight_set, font_props_default


def get_ttf_meta(font_path):
    font = ttLib.TTFont(font_path, ignoreDecompileErrors=True, fontNumber=0)
    with redirect_stderr(None):
        names = font['name'].names
    details = {}
    for x in names:
        if x.langID == 0 or x.langID == 1033:
            try:
                details[x.nameID] = x.toUnicode()
            except UnicodeDecodeError:
                details[x.nameID] = x.string.decode(errors='ignore')
    sw = set(x.lower() for x in details[2].split())
    ws = weight_set & sw
    if ws:
        weight = next(iter(ws))
    else:
        weight = font_props_default['weight']
    ss = sw - ws
    if ss:
        style = next(iter(ss))
    else:
        style = font_props_default['style']
    return {
        **font_props_default,
        'name': details[1],
        'style': style,
        'weight': weight_dict.get(weight, weight),
    }
