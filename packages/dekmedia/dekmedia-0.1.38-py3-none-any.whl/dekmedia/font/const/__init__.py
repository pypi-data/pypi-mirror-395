weight_dict = {
    'ultralight': 100,
    'light': 200,
    'normal': 400,
    'regular': 400,
    'book': 400,
    'medium': 500,
    'roman': 500,
    'semibold': 600,
    'demibold': 600,
    'demi': 600,
    'bold': 700,
    'heavy': 800,
    'extra bold': 800,
    'black': 900,
}

weight_set = set(weight_dict)

font_props_default = {
    'style': 'normal',
    'weight': weight_dict['normal'],
    "size": "scalable",
    "stretch": "normal",
    "variant": "normal",
}
