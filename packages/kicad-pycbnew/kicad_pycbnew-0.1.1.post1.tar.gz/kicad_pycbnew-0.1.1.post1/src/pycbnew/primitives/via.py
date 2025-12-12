from enum import auto

from strenum import LowercaseStrEnum

from .kicad import KiCadObject
from .sexpressions import *
from .net import KNet


class KVia(KiCadObject):
    """
    Represents a via in KiCadObject design files.

    The KVia class is used to generate and manipulate via definitions in a PCB
    design, including their dimensions, net association, layer placement, and type.

    :ivar at: The coordinate position of the via.
    :type at: Point
    :ivar size: The size of the via in millimeters.
    :type size: float
    :ivar drill: The drill size of the via in millimeters.
    :type drill: float
    :ivar layers: The start and stop layers where the via is placed.
    :type layers: tuple[str, str]
    :ivar net: The KiCadNet object associated with the via.
    :type net: KNet
    :ivar via_type: The type of the via (e.g., through-hole, blind, or micro).
    :type via_type: KVia.Type
    """
    class Type(LowercaseStrEnum):
        """
        Enum class that categorizes different types of holes.

        This class is used to specify different types of holes commonly found in
        manufacturing or PCB designs. The types include Through_hole, Blind, and
        Micro. Each member of this enum can be used to represent a specific type
        of hole.

        :ivar Through_hole: Represents a through-hole, which is a hole that goes
            entirely through an object.
        :ivar Blind: Represents a blind hole, which does not fully penetrate an
            object.
        :ivar Micro: Represents a micro hole, often used in applications requiring
            extremely small holes.
        """
        Through_hole = ""
        Blind = auto()
        Micro = auto()

    def __init__(self, at: Point, net: KNet, size: float = 0.6, drill: float = 0.3,
                 layers: tuple[str, str] = ("F.Cu", "B.Cu"), via_type=Type.Through_hole):
        super().__init__()
        self.at = at
        self.size = size
        self.drill = drill
        self.layers = layers
        self.net = net
        self.via_type = via_type

    def __repr__(self):
        return f"KVia(at={self.at}, size={self.size}, drill={self.drill}, layers={self.layers}, net={self.net})"

    def sexp_tree(self) -> list[list | str]:
        return ['via',
                f'{self.via_type}',
                sexp_at(self.at),
                sexp_size(self.size),
                sexp_drill(self.drill),
                sexp_layers(self.layers),
                sexp_net_number(self.net),
                sexp_uuid(self.uuid)]
