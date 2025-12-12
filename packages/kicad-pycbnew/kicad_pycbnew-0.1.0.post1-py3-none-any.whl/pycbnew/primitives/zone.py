from strenum import StrEnum

from pycbnew.utils.geometry import Point
from .kicad import KiCadObject, SExprSerializable
from .net import KNet
from .sexpressions import *


class KeepOutItems(SExprSerializable):
    """
    Represents a set of keep-out restrictions for PCB design elements.

    Each flag indicates whether a certain type of element is restricted.
    Multiple restrictions can be combined using bitwise operations.
    Provides a predefined combination `All` for convenience.

    This class behaves like a lightweight reimplementation of Python's
    ``enum.Flag`` but remains compatible with ``SExprSerializable``.
    The normal ``Flag`` class cannot be used here because it defines
    its own metaclass (``FlagMeta``), which is incompatible with the
    metaclass used by ``SExprSerializable``.

    To preserve the ergonomic syntax of Flag-based code while avoiding
    metaclass conflicts, each flag (e.g. ``Tracks`` or ``Vias``) is defined
    as an *instance* of ``KeepOutItems`` instead of a raw integer.
    These instances can be combined using bitwise operators (``|``, ``&``,
    ``~``) and support equality and reuse semantics similar to ``Flag``.

    Instances are memoized internally in ``_registry`` so that identical
    combinations return the same object (``KeepOutItems(3)`` always yields
    the same instance). This ensures consistency and keeps the memory
    footprint minimal.

    Static type checkers (e.g. PyCharm, mypy) cannot infer dynamically
    assigned attributes such as ``KeepOutItems.Tracks`` or ``KeepOutItems.Vias``.
    Therefore, we declare all expected attributes with forward type hints
    at class scope to silence "Unresolved attribute reference" warnings.
    These are overwritten with real instances immediately after the class
    definition.

    Example usage::

        self.keepoutitems = KeepOutItems.Tracks | KeepOutItems.Vias



    :param value: Integer representing the combination of keep-out flags.
    :type value: int

    :ivar Tracks: Restriction on tracks.
    :type Tracks: int
    :ivar Vias: Restriction on vias.
    :type Vias: int
    :ivar Pads: Restriction on pads.
    :type Pads: int
    :ivar CopperPours: Restriction on copper pours.
    :type CopperPours: int
    :ivar Footprints: Restriction on footprints.
    :type Footprints: int
    :ivar None_: No restrictions (default value).
    :type None_: int
    :ivar All: Combination of all restrictions.
    :type All: int
    """

    # --- Static type declarations (for IDEs and linters only) ---
    _registry = {}
    None_: 'KeepOutItems'
    Tracks: 'KeepOutItems'
    Vias: 'KeepOutItems'
    Pads: 'KeepOutItems'
    CopperPours: 'KeepOutItems'
    Footprints: 'KeepOutItems'
    All: 'KeepOutItems'

    # --- Core implementation ---
    def __new__(cls, value: int):
        # Reuse existing instance for identical values to mimic Flag behavior
        if value in cls._registry:
            return cls._registry[value]
        self = super().__new__(cls)
        self.value = value
        cls._registry[value] = self
        return self

    def __or__(self, other):
        return KeepOutItems(self.value | other.value)

    def __and__(self, other):
        return KeepOutItems(self.value & other.value)

    def __invert__(self):
        return KeepOutItems(~self.value & KeepOutItems.All.value)

    def sexp_tree(self) -> list[list | str]:
        return ['keepout',
                ['tracks', 'not_allowed' if self.value & KeepOutItems.Tracks.value else 'allowed'],
                ['vias', 'not_allowed' if self.value & KeepOutItems.Vias.value else 'allowed'],
                ['pads', 'not_allowed' if self.value & KeepOutItems.Pads.value else 'allowed'],
                ['copperpour', 'not_allowed' if self.value & KeepOutItems.CopperPours.value else 'allowed'],
                ['footprints', 'not_allowed' if self.value & KeepOutItems.Footprints.value else 'allowed']
                ]

# ---------------------------------------------------------------------------
# Flag definitions
# ---------------------------------------------------------------------------
# Flags are defined *after* the class body so that they are real instances
# of KeepOutItems (not integers). This allows direct calls like:
#   KeepOutItems.Pads.sexp_tree()
# while keeping the syntax as compact as with enum.Flag.
# ---------------------------------------------------------------------------

KeepOutItems.None_ = KeepOutItems(0)  # No restrictions
KeepOutItems.Tracks = KeepOutItems(1 << 0)
KeepOutItems.Vias = KeepOutItems(1 << 1)
KeepOutItems.Pads = KeepOutItems(1 << 2)
KeepOutItems.CopperPours = KeepOutItems(1 << 3)
KeepOutItems.Footprints = KeepOutItems(1 << 4)
KeepOutItems.All = (
        KeepOutItems.Tracks | KeepOutItems.Vias |
        KeepOutItems.Pads | KeepOutItems.CopperPours |
        KeepOutItems.Footprints
)


class KZone(KiCadObject):
    """
    Defines a KZone class that represents a zone in a KiCadObject PCB design.

    A KZone object is used to define properties and behaviors of a zone in a PCB.
    This includes attributes like layer assignment, net connection, hatching, and
    various clearance and thickness values. The class handles the representation
    and manipulation of its geometrical properties through points and supports
    exporting the zone's configuration in the s-expression format used by KiCadObject.

    :ivar connect_pads: Connection behavior of pads in the zone.
    :type connect_pads: ConnectPads
    :ivar priority: Priority level of the zone for filling.
    :type priority: int
    :ivar net: The net associated with the zone.
    :type net: KNet | None
    :ivar layer: Layer on which the zone is placed (default: F.Cu).
    :type layer: str
    :ivar layers: List of layers on which the zone is applied. Support wildcards (e.g. ["*.Cu"]).
                  If `layers` is defined, `layer` is ignored.
    :type layers: list[str] | None
    :ivar hatch_type: Defines the type of pattern used for zone hatching.
    :type hatch_type: str
    :ivar hatch_size: Size parameter defining the spacing of hatching pattern.
    :type hatch_size: float
    :ivar clearance: Specifies the clearance value surrounding zone objects.
    :type clearance: float
    :ivar min_thickness: Minimum material thickness allowed in the zone.
    :type min_thickness: float
    :ivar filled_areas_thickness: Configuration for filled areas' thickness.
    :type filled_areas_thickness: str
    :ivar thermal_gap: Gap in thermal relief connections.
    :type thermal_gap: float
    :ivar thermal_bridge_width: Width of thermal relief connection bridges.
    :type thermal_bridge_width: float
    :ivar island_removal_mode: Option defining the mode for island removal.
    :type island_removal_mode: any
    :ivar island_area_min: Minimum allowable area for an island in the zone.
    :type island_area_min: any
    :ivar points: List of points defining the zone's geometry.
    :type points: list[Point]
    """

    class ConnectPads(StrEnum):
        """
        Enumeration for specifying pad connection modes.

        This class represents the different options available for connecting pads in
        specific configurations or use cases. Each option corresponds to a distinct
        connection mode for pads and their associated characteristics.

        :ivar Solid: Represents a solid connection mode for pads.
        :type Solid: str
        :ivar No: Represents no connection mode for pads.
        :type No: str
        :ivar ThermalRelief: Represents a thermal relief connection mode for pads.
        :type ThermalRelief: str
        :ivar ReliefsForPTH: Represents thermal relief connection specifically for
            plated through holes.
        :type ReliefsForPTH: str
        """
        Solid = 'yes'
        No = 'no'
        ThermalRelief = ''
        ReliefsForPTH = 'thru_hole_only'

    def __init__(self, net: KNet | None = None, layer: str = "F.Cu", layers: list[str] = None, hatch_type="none",
                 hatch_size=0.5, clearance=0.5, min_thickness=0.25, filled_areas_thickness="no",
                 thermal_gap=0.5, thermal_bridge_width=0.5, points: list[Point] = None, island_removal_mode=None,
                 island_area_min=None, priority=0, connect_pads: ConnectPads = ConnectPads.ThermalRelief):
        super().__init__()
        self.connect_pads = connect_pads
        self.priority = priority
        self.net = net
        self.layer = layer
        self.layers = layers
        self.hatch_type = hatch_type
        self.hatch_size = hatch_size
        self.clearance = clearance
        self.min_thickness = min_thickness
        self.filled_areas_thickness = filled_areas_thickness
        self.thermal_gap = thermal_gap
        self.thermal_bridge_width = thermal_bridge_width
        self.island_removal_mode = island_removal_mode
        self.island_area_min = island_area_min
        self.points: list[Point] = points if points else []

    def __repr__(self):
        return f"Zone(net={self.net.name if self.net else 'None'}, layer={self.layer}, {len(self.points)} points)"

    def add_point(self, pt: Point):
        """
        Adds a new point to the collection of points maintained by the class.

        This method appends the provided Point object to the internal list of points,
        allowing the class to collect and manage a series of points for further
        processing or manipulation.

        :param pt: Point object to add to the collection.
        :type pt: Point
        """
        self.points.append(pt)

    def add_points(self, pts: list[Point]):
        """
        Adds a list of Point objects to the current collection of points.

        :param pts: A list of Point objects to append to the current collection.
        :type pts: list[Point]
        """
        self.points.extend(pts)

    def sexp_tree(self) -> list[list | str]:
        if not self.points:
            raise ValueError("Zone must have at least one point. If no points are provided, KiCad will "
                             "crash when trying to open the file.")
        ret: list[list | str] = ['zone']
        ret.append(sexp_net_number(self.net))
        ret.append(sexp_net_name(self.net))
        if self.layers:
            ret.append(sexp_layers(self.layers))
        else:
            ret.append(sexp_layer(self.layer))
        ret.append(sexp_uuid(self.uuid))
        ret.append(['hatch', f'{self.hatch_type}', f'{self.hatch_size}'])
        ret.append(['priority', f'{self.priority}'])
        ret.append(['connect_pads', ['clearance', f'{self.clearance}']])
        ret.append(['min_thickness', f'{self.min_thickness}'])
        ret.append(['filled_areas_thickness', f'{self.filled_areas_thickness}'])

        if self.island_removal_mode is not None and self.island_area_min is not None:
            island_removal_str = (f"(island_removal_mode {self.island_removal_mode}) "
                                  f"(island_area_min {self.island_area_min})")
        else:
            island_removal_str = ""
        ret.append(['fill',
                    ['thermal_gap', f'{self.thermal_gap}'],
                    ['thermal_bridge_width', f'{self.thermal_bridge_width}'],
                    island_removal_str
                    ])
        ret.append(['polygon', ['pts'] + [sexp_xy(pt) for pt in self.points]])
        return ret


class KKeepoutZone(KZone):
    """
    Represents a keepout zone in a KiCadObject design.

    This class is a specialized version of `KZone` that includes functionality for
    handling keepout zones based on specific items such as tracks, vias, pads, copper
    pours, and footprints. It provides a mechanism to specify whether certain PCB
    elements are allowed or not allowed within the keepout zone.

    :ivar keepout_items: Specifies the items (e.g., tracks, vias, pads, etc.) that
        are allowed or not allowed within the keepout zone.
    :type keepout_items: KeepOutItems
    """

    def __init__(self, keepout_items: KeepOutItems = KeepOutItems.All, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.keepout_items = keepout_items

    def sexp_tree(self) -> list[list | str]:
        sexp = super().sexp_tree()
        sexp.append(self.keepout_items.sexp_tree())
        return  sexp
