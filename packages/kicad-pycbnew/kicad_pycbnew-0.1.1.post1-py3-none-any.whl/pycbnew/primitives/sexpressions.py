from typing import Iterable

from pycbnew.utils.geometry import Point


def fnum(x: float | int) -> str:
    """Return a string with value rounded to 4 decimals, without trailing zeros."""
    rounded = round(float(x), 4)
    s = f"{rounded:.10g}"  # compact format, withdraw trailing zeros0
    return s


def sexp_at(at: Point) -> list[str]:
    return ['at', fnum(at.x), fnum(at.y)]


def sexp_at_angle(at: Point, angle: float) -> list[str]:
    return ['at', fnum(at.x), fnum(at.y), fnum(angle)]


def sexp_drill(drill: float) -> list[str]:
    return ['drill', fnum(drill)]


def sexp_size(size: float) -> list[str]:
    return ['size', fnum(size)]


def sexp_paper(val: str | tuple[int, int]) -> list[str]:
    if isinstance(val, tuple):
        return ['paper', '"User"', f'{int(val[0])} {int(val[1])}']
    else:
        if val.endswith(" portrait"):
            val = val.rstrip(" portrait")
            val = f'"{val}" portrait'
        else:
            val = f'"{val}"'
        return ['paper', val]


def sexp_size2(size1: float, size2: float) -> list[str]:
    return ['size', fnum(size1), fnum(size2)]


def sexp_width(size: float) -> list[str]:
    return ['width', fnum(size)]


def sexp_layer(layer: str) -> list[str]:
    return ['layer', f'"{layer}"']


def sexp_layers(layers: Iterable[str]) -> list[str]:
    return ['layers'] + [f'"{layer}"' for layer in layers]


def sexp_layers_in_project(layers: Iterable['KLayer']) -> list[str]:
    from .layer import KLayer
    layers: Iterable[KLayer] = layers
    return ['layers'] + [layer.sexp_tree() for layer in layers]


def sexp_net_number(net: 'KNet') -> list[str]:
    if net is None:
        return ['net', '0']
    else:
        return ['net', f'{net.number}']


def sexp_net_name(net: 'KNet') -> list[str]:
    if net is None:
        return ['net_name', '""']
    else:
        return ['net_name', f'"{net.name}"']


def sexp_net_full(net: 'KNet') -> list[str]:
    if net is None:
        return ['net', '0', '""']
    else:
        return ['net', f'{net.number}', f'"{net.name}"']


def sexp_uuid(uuid: str) -> list[str]:
    return ['uuid', f'"{uuid}"']


def sexp_xy(point: Point) -> list[str]:
    return ['xy', fnum(point.x), fnum(point.y)]


def sexp_xyz(xyz: tuple[float, float, float]) -> list[str]:
    return ['xyz', fnum(xyz[0]), fnum(xyz[1]), fnum(xyz[2])]


def sexp_start(point: Point) -> list[str]:
    return ['start', fnum(point.x), fnum(point.y)]


def sexp_end(point: Point) -> list[str]:
    return ['end', fnum(point.x), fnum(point.y)]


def sexp_mid(point: Point) -> list[str]:
    return ['mid', fnum(point.x), fnum(point.y)]


def tree_to_sexp(obj, depth: int = 0) -> str:
    indent = '    ' * depth
    if isinstance(obj, list):
        try:
            first_list_index = [isinstance(o, list) for o in obj].index(True)
            head = obj[:first_list_index]
            tail = obj[first_list_index:]
            inner = []
            for o in tail:
                if isinstance(o, list):
                    inner.append(tree_to_sexp(o, depth + 1))
                else:
                    inner.append('    ' * (depth + 1) + str(o))
            return f"{indent}({' '.join(head)}\n" + "\n".join(inner) + f"\n{indent})"
        except ValueError:
            return indent + "(" + " ".join(str(x) for x in obj) + ")"
    else:
        return indent + str(obj)

