from enum import auto, Flag, IntEnum

from strenum import LowercaseStrEnum

from pycbnew.utils.geometry import Rectangle, Point
from .kicad import KiCadObject, SExprSerializable
from .sexpressions import *
from .sexpressions import sexp_layer, sexp_uuid, sexp_xy


class Stroke(LowercaseStrEnum):
    """
    Enumeration for different types of stroke patterns.

    This class provides an enumeration of various stroke styles that
    can be used for graphical representation or styling. Each member
    of this enumeration represents a unique stroke pattern.
    """
    Default = auto()
    Dash = auto()
    Dot = auto()
    Dash_Dot = auto()
    Dash_Dot_Dot = auto()
    Solid = auto()


class TextJustify(SExprSerializable):
    """
    Represents text justification flags and their combinations.

    This class behaves like a lightweight reimplementation of Python's
    ``enum.Flag`` but remains compatible with ``SExprSerializable``.
    The normal ``Flag`` class cannot be used here because it defines
    its own metaclass (``FlagMeta``), which is incompatible with the
    metaclass used by ``SExprSerializable``.

    To preserve the ergonomic syntax of Flag-based code while avoiding
    metaclass conflicts, each flag (e.g. ``Left`` or ``Top``) is defined
    as an *instance* of ``TextJustify`` instead of a raw integer.
    These instances can be combined using bitwise operators (``|``, ``&``,
    ``~``) and support equality and reuse semantics similar to ``Flag``.

    Instances are memoized internally in ``_registry`` so that identical
    combinations return the same object (``TextJustify(3)`` always yields
    the same instance). This ensures consistency and keeps the memory
    footprint minimal.

    Static type checkers (e.g. PyCharm, mypy) cannot infer dynamically
    assigned attributes such as ``TextJustify.Left`` or ``TextJustify.Top``.
    Therefore, we declare all expected attributes with forward type hints
    at class scope to silence "Unresolved attribute reference" warnings.
    These are overwritten with real instances immediately after the class
    definition.

    Example usage::

        self.justify = TextJustify.TopLeft
        print(self.justify.sexp_tree())
        # → ['justify', 'left', 'top']

    :param value: Bitwise combination representing justification flags.
    :type value: int

    :ivar Left: Align text to the left.
    :ivar Right: Align text to the right.
    :ivar Top: Align text to the top.
    :ivar Bottom: Align text to the bottom.
    :ivar Mirror: Apply a mirror effect to the text (useful for back-side layers).
    :ivar Default: Default alignment (no special alignment).
    :ivar TopLeft: Combination of Left and Top.
    :ivar BottomLeft: Combination of Left and Bottom.
    :ivar TopRight: Combination of Right and Top.
    :ivar BottomRight: Combination of Right and Bottom.
    """

    # --- Static type declarations (for IDEs and linters only) ---
    _registry = {}
    Left: 'TextJustify'
    Right: 'TextJustify'
    Top: 'TextJustify'
    Bottom: 'TextJustify'
    Mirror: 'TextJustify'
    Default: 'TextJustify'
    TopLeft: 'TextJustify'
    BottomLeft: 'TextJustify'
    TopRight: 'TextJustify'
    BottomRight: 'TextJustify'
    All: 'TextJustify'

    # --- Core implementation ---
    def __new__(cls, value: int):
        # Reuse existing instance for identical values to mimic Flag behavior
        if value in cls._registry:
            return cls._registry[value]
        self = super().__new__(cls)
        self.value = value
        cls._registry[value] = self
        return self

    def __or__(self, other: 'TextJustify') -> 'TextJustify':
        """Bitwise OR (combine flags)."""
        return TextJustify(self.value | other.value)

    def __and__(self, other: 'TextJustify') -> 'TextJustify':
        """Bitwise AND (intersection of flags)."""
        return TextJustify(self.value & other.value)

    def __invert__(self) -> 'TextJustify':
        """Bitwise NOT (invert all active flags)."""
        return TextJustify(~self.value & TextJustify.All.value)

    def sexp_tree(self) -> list[str | list]:
        """Serialize the justification configuration as an S-expression."""
        ret = ['justify']
        if self.value & TextJustify.Left.value:
            ret.append("left")
        elif self.value & TextJustify.Right.value:
            ret.append("right")

        if self.value & TextJustify.Top.value:
            ret.append("top")
        elif self.value & TextJustify.Bottom.value:
            ret.append("bottom")

        if self.value & TextJustify.Mirror.value:
            ret.append("mirror")

        return ret


# ---------------------------------------------------------------------------
# Flag definitions
# ---------------------------------------------------------------------------
# Flags are defined *after* the class body so that they are real instances
# of TextJustify (not integers). This allows direct calls like:
#   TextJustify.Left.sexp_tree()
# while keeping the syntax as compact as with enum.Flag.
# ---------------------------------------------------------------------------

TextJustify.Default = TextJustify(0)
TextJustify.Left = TextJustify(1 << 0)
TextJustify.Right = TextJustify(1 << 1)
TextJustify.Top = TextJustify(1 << 2)
TextJustify.Bottom = TextJustify(1 << 3)
TextJustify.Mirror = TextJustify(1 << 4)
TextJustify.TopLeft = TextJustify.Left | TextJustify.Top
TextJustify.BottomLeft = TextJustify.Left | TextJustify.Bottom
TextJustify.TopRight = TextJustify.Right | TextJustify.Top
TextJustify.BottomRight = TextJustify.Right | TextJustify.Bottom
TextJustify.All = (
    TextJustify.Left | TextJustify.Right |
    TextJustify.Top | TextJustify.Bottom |
    TextJustify.Mirror
)


class Font(SExprSerializable):
    """
    Represents a font configuration including size, face, style, and thickness.

    This class provides functionality to manage font properties such as size,
    typeface, boldness, italicization, and thickness. It also generates serialized
    representations of these font properties.

    :ivar size: Tuple representing the font size in horizontal and vertical dimensions.
    :type size: tuple[float, float]
    :ivar face: Typeface name of the font. None indicates no specific typeface.
    :type face: str
    :ivar bold: Indicates whether the font is bold.
    :type bold: bool
    :ivar italic: Indicates whether the font is italic.
    :type italic: bool
    :ivar thickness: Thickness of the font.
    :type thickness: float
    """
    def __init__(self, size: tuple[float, float] = (1.5, 1.5), face: str = None, bold: bool = False,
                 italic: bool = False, thickness: float = None):
        super().__init__()
        self.size = size
        self.face = face
        self.bold = bold
        self.italic = italic
        self._thickness = thickness

    @property
    def thickness(self):
        if self._thickness is not None:
            return self._thickness
        else:
            return round(max(*self.size) / (5 if self.bold else 8), 2)

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    def sexp_tree(self) -> list[str | list]:
        ret: list[str | list] = ['font']
        ret.append(['size', fnum(self.size[0]), fnum(self.size[1])])
        if self.face:
            ret.append(['face', f'"{self.face}"'])
        if self.bold:
            ret.append(['bold'])
        if self.italic:
            ret.append(['italic'])
        else:
            ret.append([f'thickness', f"{self.thickness}"])
        return ret


class KGrText(KiCadObject):
    """
    Represents graphical text in KiCadObject.

    This class serves as a representation of graphical text objects within KiCadObject.
    It provides functionality to manage properties such as text content, position,
    layer assignment, font details, angle adjustment, and justification settings.

    :ivar justify: The justification of the text.
    :type justify: TextJustify
    :ivar angle: The angle of rotation for the text.
    :type angle: float
    :ivar layer: The layer on which the text is located.
    :type layer: str
    :ivar text: The content of the text.
    :type text: str
    :ivar at: The position of the text as a Point object.
    :type at: Point
    :ivar font: The font details of the text.
    :type font: Font
    """
    def __init__(self, layer: str, text: str, at: Point, font: Font = None, angle: float = 0,
                 justify: TextJustify = TextJustify.Default, knockout=False):
        super().__init__()
        if not isinstance(justify, TextJustify):
            self.justify = TextJustify.Default
        else:
            self.justify = justify
        self.angle = angle
        self.layer = layer
        self.text = text.replace('\n', r'\n')
        self.at = at
        self.font = font if font else Font()
        self.knockout = knockout

    def sexp_tree(self) -> list[list | str]:
        ret: list[list|str] = ['gr_text', f'"{self.text}"']
        ret.append(sexp_at_angle(self.at, self.angle))
        ret.append(sexp_layer(self.layer) + (['knockout'] if self.knockout else []))
        ret.append(sexp_uuid(self.uuid))
        ret.append(['effects', self.justify.sexp_tree(), self.font.sexp_tree()])
        return ret


class KGrRect(KiCadObject):
    """
    Represents a graphic rectangle in KiCadObject.

    This class is designed to model a graphic rectangle in KiCadObject, including its
    layer, dimensions, stroke width and type, and fill properties. It provides tools
    to output the rectangle's representation in S-Expressions, which is a part of
    KiCadObject's design file format.

    :ivar layer: The name of the layer in which the rectangle is placed.
    :type layer: str
    :ivar rect: The dimensions of the rectangle, including its top-left and bottom-right coordinates.
    :type rect: Rectangle
    :ivar width: The stroke width of the rectangle, defining the line thickness (default is 0.2).
    :type width: float
    :ivar stroke: The stroke type of the rectangle, such as solid, dash, etc.
    :type stroke: Stroke
    :ivar fill: Indicates whether the rectangle is filled (True) or unfilled (False).
    :type fill: bool
    """
    def __init__(self, layer: str, rect: Rectangle, width: float = 0.2, stroke: Stroke = Stroke.Default,
                 fill: bool = False):
        super().__init__()
        self.layer = layer
        self.rect = rect
        self.width = width
        self.stroke = stroke
        self.fill = fill

    def sexp_tree(self) -> list[list | str]:
        ret: list[list | str] = ['gr_rect']
        ret.append(sexp_start(self.rect.top_left))
        ret.append(sexp_end(self.rect.bottom_right))
        ret.append(['stroke', sexp_width(self.width), ['type', f"{self.stroke}"]])
        ret.append(['fill', 'yes' if self.fill else 'no'])
        ret.append(sexp_layer(self.layer))
        ret.append(sexp_uuid(self.uuid))
        return ret


class KGrPoly(KiCadObject):
    """
    Represents a graphical polygon in a KiCadObject layout.

    The KGrPoly class defines a polygon that can be used in KiCadObject PCB designs.
    It supports customization of the polygon's layer, points, width, stroke type, and
    fill property. This class provides functionality to add points to the polygon and
    generate a corresponding S-Expression representation.

    :ivar layer: The layer on which the polygon is drawn.
    :type layer: str
    :ivar points: List of Point objects representing the vertices of the polygon.
    :type points: list[Point]
    :ivar width: The thickness of the polygon's outline.
    :type width: float
    :ivar stroke: The stroke type of the polygon (e.g., solid, dashed).
    :type stroke: Stroke
    :ivar fill: Indicates whether the polygon is filled or not.
    :type fill: bool
    """
    def __init__(self, layer: str, points: list[Point] = None, width: float = 0.1,
                 stroke: Stroke = Stroke.Solid, fill: bool = False):
        super().__init__()
        self.layer = layer
        self.points: list[Point] = points if points else []
        self.width = width
        self.stroke = stroke
        self.fill = fill

    def __repr__(self):
        return f"GrPoly(net=layer={self.layer}, {len(self.points)} points)"

    def add_point(self, pt: Point):
        """Ajoute un sommet au polygone."""
        self.points.append(pt)

    def add_points(self, pts: list[Point]):
        """Ajoute des sommets au polygone."""
        self.points.extend(pts)

    def sexp_tree(self) -> list[list | str]:
        ret: list[list | str] = ['gr_poly']
        ret.append(['pts'] + [sexp_xy(pt) for pt in self.points])
        ret.append(['stroke', sexp_width(self.width), ['type', f"{self.stroke}"]])
        ret.append(['fill', 'yes' if self.fill else 'no'])
        ret.append(sexp_layer(self.layer))
        ret.append(sexp_uuid(self.uuid))
        return ret


class KGrLine(KiCadObject):
    """
    Represents a graphic line in KiCadObject design files.

    This class is used to define and manipulate graphic lines in KiCadObject designs.
    It includes attributes for the line's endpoints, layer, width, and stroke
    type. The class inherits from `KiCadObject` and allows for conversion to an S-expression
    list for KiCadObject file generation.

    :ivar layer: The layer of the graphic line in the KiCadObject design.
    :type layer: str
    :ivar point1: The starting point of the graphic line.
    :type point1: Point
    :ivar point2: The ending point of the graphic line.
    :type point2: Point
    :ivar width: The width of the graphic line, with a default value of 0.2.
    :type width: float
    :ivar stroke: The stroke type of the graphic line, with a default value of `Stroke.Default`.
    :type stroke: Stroke
    """
    def __init__(self, point1: Point, point2: Point, layer: str, width: float = 0.2, stroke: Stroke = Stroke.Default,
                 **kwargs):
        super().__init__()
        self.layer = layer
        self.point1 = point1
        self.point2 = point2
        self.width = width
        self.stroke = stroke

    def sexp_tree(self) -> list[list | str]:
        ret: list[list | str] = ['gr_line']
        ret.append(sexp_start(self.point1))
        ret.append(sexp_end(self.point2))
        ret.append(['stroke', sexp_width(self.width), ['type', f"{self.stroke}"]])
        ret.append(sexp_layer(self.layer))
        ret.append(sexp_uuid(self.uuid))
        return ret


class DimensionStyle(SExprSerializable):
    """
    Represents a KiCadObject dimension style configuration.

    This class encapsulates various parameters for defining a dimension style in KiCadObject,
    including thickness, arrow length, text position, and other related properties. It is
    designed primarily to standardize the representation and manipulation of dimension
    styles in the KiCadObject environment.

    :ivar thickness: Line thickness of the dimension style.
    :type thickness: float
    :ivar arrow_length: Length of the arrow used in the dimension style.
    :type arrow_length: float
    :ivar text_position_mode: Indicates the mode of text positioning, such as outside or inline.
    :type text_position_mode: DimensionStyle.TextPositionMode
    :ivar extension_height: Height of extensions associated with the dimension style.
    :type extension_height: float
    :ivar extension_offset: Offset distance for extension lines in the dimension style.
    :type extension_offset: float
    :ivar keep_text_aligned: Specifies whether to keep the dimension text aligned.
    :type keep_text_aligned: bool
    """
    class TextPositionMode(IntEnum):
        Outside = 0
        Inline = 1

    def __init__(self, thickness: float = 0.2, arrow_length: float = 1.27,
                 text_position_mode: TextPositionMode = TextPositionMode.Outside,
                 extension_height: float = 0.6, extension_offset: float = 0.5, keep_text_aligned: bool = True):
        super().__init__()
        self.thickness = thickness
        self.arrow_length = arrow_length
        self.text_position_mode = text_position_mode
        self.extension_height = extension_height
        self.extension_offset = extension_offset
        self.keep_text_aligned = keep_text_aligned

    def sexp_tree(self) -> list[list | str]:
        ret: list[list | str] = ['style']
        ret.append(['thickness', f'{self.thickness}'])
        ret.append(['arrow_length', f'{self.arrow_length}'])
        ret.append(['text_position_mode', f'{self.text_position_mode}'])
        ret.append(['extension_height', f'{self.extension_height}'])
        ret.append(['extension_offset', f'{self.extension_offset}'])
        if self.keep_text_aligned:
            ret.append(['keep_text_aligned', 'yes'])
        return ret


class DimensionFormat(SExprSerializable):
    """
    Represents a KiCadObject-specific dimension formatting configuration.

    This class is used to define formatting parameters for dimensions in KiCadObject,
    including prefix, suffix, units, units format, precision, and an optional
    override value. It provides functionality to generate these parameters in
    a structured format for further processing or serialization.

    :ivar prefix: The prefix string to be appended before the dimension value.
    :type prefix: str
    :ivar suffix: The suffix string to be appended after the dimension value.
    :type suffix: str
    :ivar units: The unit type for the dimension value.
    :type units: DimensionFormat.Units
    :ivar units_format: The format of how units are displayed alongside the dimension.
    :type units_format: DimensionFormat.UnitsFormat
    :ivar precision: The number of decimal places for the dimension value.
    :type precision: int
    :ivar override_value: An optional override value for the dimension. If specified,
        this value will replace the calculated dimension value.
    :type override_value: str or None
    """
    class Units(IntEnum):
        """
        Enumeration of measurement units.

        This class provides a set of predefined units for measurement conversions or
        unit specification purposes. It supports enums for common measures used in
        engineering, design, and automation industries.

        :ivar Inches: Represents the unit of inches.
        :ivar Mils: Represents the unit of mils, which is a thousandth of an inch.
        :ivar Millimeter: Represents the unit of millimeters.
        :ivar Automatic: Represents an automatic unit detection mode.
        """
        Inches = 0
        Mils = 1
        Millimeter = 2
        Automatic = 3

    class UnitsFormat(IntEnum):
        """
        Represents enumeration for formatting units in various styles.

        This class provides integer values corresponding to different formatting
        styles that can be applied to textual representations of units. These
        formats can be utilized where unit designations in textual or visual
        output must adhere to specific formatting.

        :ivar No_suffix: Represents a format where there is no suffix appended to
            the unit representation.
        :type No_suffix: int
        :ivar Bare_suffix: Represents a format where a bare suffix is appended to
            the unit representation without any additional symbols.
        :type Bare_suffix: int
        :ivar Wrap_suffix_in_parenthesis: Represents a format where the suffix is
            wrapped in parentheses in the unit representation.
        :type Wrap_suffix_in_parenthesis: int
        """
        No_suffix = 0
        Bare_suffix = 1
        Wrap_suffix_in_parenthesis = 2

    def __init__(self, prefix: str = "", suffix: str = "",
                 units: Units = Units.Millimeter,
                 units_format: UnitsFormat = UnitsFormat.Bare_suffix,
                 precision: int = 7,
                 override_value: str = None):
        super().__init__()
        self.prefix = prefix
        self.suffix = suffix
        self.units = units
        self.units_format = units_format
        self.precision = precision
        self.override_value = override_value

    def sexp_tree(self) -> list[list | str]:
        ret: list[list | str] = ['format']
        if self.prefix:
            ret.append(['prefix', f'"{self.prefix}"'])
        if self.suffix:
            ret.append(['suffix', f'"{self.suffix}"'])
        ret.append(['units', f'{self.units}'])
        ret.append(['units_format', f'{self.units_format}'])
        ret.append(['precision', f'{self.precision}'])
        if self.override_value is not None:
            ret.append(['override_value', f'"{self.override_value}"'])
        return ret


class KGrDimension(KiCadObject):
    """
    Represents a KiCadObject graphical dimension object.

    This class encapsulates the functionality and data needed for defining and working
    with graphical dimensions in KiCadObject. It supports various dimension types and associated
    attributes like format, style, layer, and font size. The class provides methods to
    manipulate and represent dimension data in the KiCadObject compatible format.

    :ivar dimension_style: The style settings for the dimension.
    :type dimension_style: DimensionStyle
    :ivar dimension_format: The formatting settings for the dimension.
    :type dimension_format: DimensionFormat
    :ivar height: The height of the dimension line or text.
    :type height: float
    :ivar type: The type of the dimension (e.g., Aligned, Leader, etc.).
    :type type: Type
    :ivar point1: The first anchor point of the dimension.
    :type point1: Point
    :ivar point2: The second anchor point of the dimension.
    :type point2: Point
    :ivar layer: The layer on which the dimension will be placed.
    :type layer: str
    :ivar font: The font for the dimension text.
    :type font: Font
    """
    class Type(LowercaseStrEnum):
        """
        Represents alignment and orientation types.

        This enumeration class defines various types of alignments and
        orientations, such as Aligned, Leader, Center, Orthogonal, and
        Radial. It is primarily used to categorize or specify the type
        of orientation-related state in a given context.

        These values are auto-generated using the `auto()` method.
        """
        Aligned = auto()
        Leader = auto()
        Center = auto()
        Orthogonal = auto()
        Radial = auto()

    def __init__(self, point1: Point, point2: Point, height: float, layer: str = "Cmts.User",
                 type: Type = Type.Aligned, dimension_format: DimensionFormat | None = None,
                 dimension_style: DimensionStyle | None = None, font: Font | None = None):
        super().__init__()
        self.dimension_style = dimension_style or DimensionStyle()
        self.dimension_format = dimension_format or DimensionFormat()
        self.height = height
        self.type = type
        self.point1 = point1
        self.point2 = point2
        self.layer = layer
        self.font = font or Font()

    @property
    def length(self):
        return (self.point1 - self.point2).norm

    def sexp_tree(self) -> list[list | str]:
        ret: list[list | str] = ['dimension']
        ret.append(['type', f'{self.type}'])
        ret.append(sexp_layer(self.layer))
        ret.append(sexp_uuid(self.uuid))
        ret.append(['pts', sexp_xy(self.point1), sexp_xy(self.point2)])
        ret.append(['height', f'{self.height}'])
        ret.append(['gr_text', '""', sexp_layer(self.layer), ['effects', self.font.sexp_tree()]])
        ret.append(self.dimension_format.sexp_tree())
        ret.append(self.dimension_style.sexp_tree())
        return ret
