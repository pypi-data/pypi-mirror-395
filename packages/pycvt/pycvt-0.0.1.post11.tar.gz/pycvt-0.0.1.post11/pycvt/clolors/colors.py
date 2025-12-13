import random
from functools import lru_cache

from distinctipy.distinctipy import get_colors, get_rgb256

_colors_map = {}
_rng = random.Random("default")


@lru_cache(maxsize=10000)
def getcolor(key="default", rng=_rng):
    if key in _colors_map:
        color = _colors_map[key]
    else:
        color = get_colors(1, exclude_colors=list(_colors_map.values()), rng=rng)[0]
        _colors_map[key] = color
    return get_rgb256(color)
