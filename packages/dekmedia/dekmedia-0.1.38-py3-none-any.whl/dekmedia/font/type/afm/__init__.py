from ...const import weight_dict, font_props_default
from . import _afm


def get_afm_meta(font_path):
    with open(font_path, "rb") as fh:
        font = _afm.AFM(fh)
    name = font.get_familyname()
    fontname = font.get_fontname().lower()

    #  Styles are: italic, oblique, and normal (default)

    if font.get_angle() != 0 or 'italic' in name.lower():
        style = 'italic'
    elif 'oblique' in name.lower():
        style = 'oblique'
    else:
        style = font_props_default['style']

    #  Variants are: small-caps and normal (default)

    # !!!!  Untested
    if name.lower() in ['capitals', 'small-caps']:
        variant = 'small-caps'
    else:
        variant = font_props_default['variant']

    weight = font.get_weight().lower()
    if weight not in weight_dict:
        weight = font_props_default['weight']

    #  Stretch can be absolute and relative
    #  Absolute stretches are: ultra-condensed, extra-condensed, condensed,
    #    semi-condensed, normal, semi-expanded, expanded, extra-expanded,
    #    and ultra-expanded.
    #  Relative stretches are: wider, narrower
    #  Child value is: inherit
    if 'demi cond' in fontname:
        stretch = 'semi-condensed'
    elif any(word in fontname for word in ['narrow', 'cond']):
        stretch = 'condensed'
    elif any(word in fontname for word in ['wide', 'expanded', 'extended']):
        stretch = 'expanded'
    else:
        stretch = font_props_default['stretch']

    #  Sizes can be absolute and relative.
    #  Absolute sizes are: xx-small, x-small, small, medium, large, x-large,
    #    and xx-large.
    #  Relative sizes are: larger, smaller
    #  Length value is an absolute font size, e.g., 12pt
    #  Percentage values are in 'em's.  Most robust specification.

    #  All AFM fonts are apparently scalable.

    return {
        'name': name,
        'style': style,
        'weight': weight_dict.get(weight, weight),
        "size": font_props_default['size'],
        "stretch": stretch,
        "variant": variant,
    }
