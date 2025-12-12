import math
from svg.path import parse_path, Path
from dektools.num import near_zero


def radian_to_degree(radian):
    return radian * 180 / math.pi


def calc_text_attrs(pp: Path, percent):
    if percent == 0:
        percent = near_zero
    point = pp.point(percent)
    tangent = pp.tangent(percent)
    degree = radian_to_degree(math.atan2(tangent.imag, tangent.real))
    return point.real, point.imag, degree


def path_text(path: str, text: str, cursor: float, anchor: float, gap):
    pp = parse_path(path)
    path_length = pp.length()
    result = []
    if path_length == 0:
        return result
    text_length = max(len(text) - 1, 1)
    for i, c in enumerate(text):
        percent = (cursor * path_length - (text_length * anchor - i) * gap) / path_length
        if 0 <= percent <= 1:
            result.append([c, calc_text_attrs(pp, percent)])
    return result
