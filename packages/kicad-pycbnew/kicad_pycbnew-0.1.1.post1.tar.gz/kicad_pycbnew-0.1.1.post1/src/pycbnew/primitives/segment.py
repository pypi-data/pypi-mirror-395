from pycbnew.utils.geometry import Arc
from pycbnew.primitives.sexpressions import *
from .kicad import KiCadObject
from .net import KNet


class KSegment(KiCadObject):
    """
    Represents a segment in KiCadObject, including its connection details, dimensions, and layer
    information.

    A `KSegment` object is used to describe electrical or physical connections in a
    KiCadObject design. It contains details about its start and end points, layer, width, and
    the net it is associated with. This class also includes utility methods for converting
    the segment into a corresponding S-Expression representation used in KiCadObject.

    :ivar net: The net to which the segment is connected.
    :type net: KNet
    :ivar layer: The layer on which the segment exists.
    :type layer: str
    :ivar point1: The starting point of the segment.
    :type point1: Point
    :ivar point2: The ending point of the segment.
    :type point2: Point
    :ivar width: The width of the segment. Default is 0.2.
    :type width: float
    """
    def __init__(self, net: KNet, layer: str, point1: Point, point2: Point, width: float = 0.2, **kwargs):
        super().__init__()
        self.layer = layer
        self.point1 = point1
        self.point2 = point2
        self.width = width
        self.net = net

    @property
    def vector(self):
        return self.point2 - self.point1

    @property
    def length(self):
        return self.vector.norm

    def __repr__(self):
        return f"KSegment(net={self.net}, layer={self.layer}, point1={self.point1}, point2={self.point2}, width={self.width})"

    def sexp_tree(self) -> list[list | str]:
        ret: list[str | list] = ['segment']
        ret.append(sexp_start(self.point1))
        ret.append(sexp_end(self.point2))
        ret.append(sexp_width(self.width))
        ret.append(sexp_layer(self.layer))
        ret.append(sexp_net_number(self.net))
        ret.append(sexp_uuid(self.uuid))
        return ret


class KArc(KiCadObject):
    """
    Represents an arc object in KiCadObject with specific properties and methods for
    processing and serialization.

    The ``KArc`` class is used to represent and manipulate arc elements
    associated with KiCadObject. It stores the data required to define an arc's
    geometry, appearance, and association within its net and layer. This class is
    useful for creating and transforming KiCadObject-compatible data for arcs.

    :ivar arc: Geometric representation of the arc.
    :type arc: Arc
    :ivar layer: Name of the layer on which the arc resides.
    :type layer: str
    :ivar net: Optional KiCadNet associated with the arc.
    :type net: KNet | None
    :ivar width: Width of the arc's stroke.
    :type width: float
    """
    def __init__(self, arc: Arc, layer: str, net: KNet | None = None, width: float = 0.2):
        super().__init__()
        self.width = width
        self.layer = layer
        self.net = net
        self.arc = arc

    @property
    def length(self):
        return self.arc.length

    def __repr__(self):
        return f"KArc(net={self.net}, layer={self.layer}, p1={self.arc.p1}, p2={self.arc.p2}, p3={self.arc.p3}, angle={self.arc.angle}, width={self.width})"

    def sexp_tree(self) -> list[str | list]:
        ret: list[str | list] = ['gr_arc']
        ret.append(sexp_start(self.arc.p1))
        ret.append(sexp_mid(self.arc.p2))
        ret.append(sexp_end(self.arc.p3))
        ret.append(['stroke', sexp_width(self.width), ['type', 'default']])
        ret.append(sexp_layer(self.layer))
        ret.append(sexp_uuid(self.uuid))
        if self.net is not None:
            ret.append(sexp_net_number(self.net))
        return ret
