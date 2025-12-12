import os.path
import platform
from enum import auto, Enum
from typing import Literal

from pyparsing import nested_expr
from strenum import LowercaseStrEnum, StrEnum

from pycbnew.utils.geometry import Point, Vector
from .kicad import KiCadObject, SExprSerializable
from .net import KNet
from .sexpressions import *


def is_number_str(s: str) -> bool:
    """Check if a string represents an int or float."""
    try:
        float(s)
        return True
    except ValueError:
        return False


class KPad(KiCadObject):
    """
    Represents a KiCadObject pad used in electronic design automation software.

    The KPad class is responsible for parsing and handling the properties of
    a pad, which is an essential component in PCB (Printed Circuit Board) design.
    The pad can have various attributes such as shape, type, position, size,
    drill, and associated net. It also supports serialization into a list
    format for further processing or exporting. The class provides functionality
    to interpret raw input data and extract the relevant attributes for the pad.

    :ivar footprint: The KiCadObject footprint instance associated with this pad.
    :type footprint: KFootprint
    :ivar net: The associated net of the pad or None if no net is assigned.
    :type net: KNet or None
    :ivar raw_code_list: The raw list of extracted code data related to the pad.
    :type raw_code_list: list
    :ivar non_parsed_code_list: The list of code lines not parsed yet.
    :type non_parsed_code_list: list
    :ivar id: The identifier or name of the pad.
    :type id: str or None
    :ivar shape: The shape of the pad.
    :type shape: KPad.Shape or None
    :ivar type: The type of the pad.
    :type type: KPad.Type or None
    :ivar at: The position of the pad as an instance of a Point.
    :type at: Point or None
    :ivar angle: The rotation angle of the pad in degrees.
    :type angle: float
    :ivar size: The dimensions of the pad as a vector.
    :type size: Vector or None
    :ivar drill: The drill size or parameters of the pad.
    :type drill: str or None
    :ivar layers: The list of layers associated with the pad.
    :type layers: list[str]
    :ivar solder_mask_margins: The solder mask margins for the pad.
    :type solder_mask_margins: float or None
    """
    class Shape(LowercaseStrEnum):
        Circle = auto()
        Rect = auto()
        Oval = auto()
        Trapezoid = auto()
        Roundrect = auto()
        Custom = auto()

    class Type(LowercaseStrEnum):
        Thru_hole = auto()
        Smd = auto()
        Connect = auto()
        Np_thru_hole = auto()

    def __init__(self, footprint: 'KFootprint', data: list, net: KNet | None = None, angle: float = 0.0):
        super().__init__()
        self.footprint = footprint
        self.net: KNet | None = net
        self.raw_code_list = data
        self.non_parsed_code_list = data

        self.id: str | None = None
        self.shape: KPad.Shape | None = None
        self.type: KPad.Type | None = None
        self.at: Point | None = None
        self.angle: float = angle
        self.size: Vector | None = None
        self.drill: str | None = None
        self.layers: list[str] = []
        self.solder_mask_margins: float | None = None

        self.parse()

    @property
    def absolute_at(self) -> Point:
        """
        Calculates the absolute position by rotating the given position and adding
        it to the footprint position. The method takes into account the rotation angle
        specified in degrees.

        :return: The absolute position after rotation, in a tuple (x, y).
        :rtype: Point
        """
        return self.footprint.at + Vector(*self.at.rotate(self.footprint.angle, degrees=True))

    def parse(self):
        to_be_removed: list[int] = list()
        assert (self.raw_code_list[0] == 'pad')
        # pad name
        self.id = self.raw_code_list[1].strip('"')
        to_be_removed.append(1)
        # pad type
        self.type = KPad.Type(self.raw_code_list[2])
        to_be_removed.append(2)
        # pad shape
        self.shape = KPad.Shape(self.raw_code_list[3])
        to_be_removed.append(3)
        # pad position and angle identifier
        self.at = Point(float(self.raw_code_list[4][1]), float(self.raw_code_list[4][2]))
        self.angle = float(self.raw_code_list[4][3]) if len(self.raw_code_list[4]) == 4 else 0.0
        to_be_removed.append(4)
        for i, item in enumerate(self.raw_code_list[5:], start=5):
            to_be_removed.append(i)
            match item:
                case ['size', x, y]:
                    self.size = Vector(float(x), float(y))
                case ['drill', *params]:
                    self.drill = ' '.join(params)
                case ['layers', *layers]:
                    self.layers = [l.strip('"') for l in layers]
                case ['solder_mask_margin', margin]:
                    self.solder_mask_margins = float(margin)
                case _:
                    to_be_removed.pop()
        for i in reversed(to_be_removed):
            self.non_parsed_code_list.pop(i)

    def sexp_tree(self):
        ret: list[str | list] = ["pad"]
        ret.append(f'"{self.id}"')
        ret.append(str(self.type))
        ret.append(str(self.shape))
        if self.net is not None:
            ret.append(["net", str(self.net.number), f'"{self.net.name}"'])
        ret.append(sexp_at_angle(self.at, self.angle))
        ret.append(sexp_size2(*self.size.to_tuple()))
        if self.drill is not None:
            ret.append(["drill", str(self.drill)])
        ret.append(sexp_layers(self.layers))
        if self.non_parsed_code_list:
            ret.extend(self.non_parsed_code_list[1:])
        return ret

    def __repr__(self):
        return f"KPad(id={self.id}, at={self.at}, size={self.size}, layers={self.layers}, net={self.net}, footprint={self.footprint})"


class Footprint3DModel(SExprSerializable):
    def __init__(self, path: str, scale: tuple[float, float, float] = None, rotate: tuple[float, float, float] = None,
                 offset: tuple[float, float, float] = None):
        self.path = path
        self.scale = scale or (1.0, 1.0, 1.0)
        self.offset = offset or (0.0, 0.0, 0.0)
        self.rotate = rotate or (0.0, 0.0, 0.0)

    @classmethod
    def from_sexp_list(cls, sexp_list: list) -> 'Footprint3DModel':
        assert sexp_list[0] == 'model'
        path = sexp_list[1].strip('"')
        offset = None
        scale = None
        rotate = None
        for item in sexp_list[2:]:
            try:
                xyz, x, y, z = item[1]
                assert xyz == 'xyz'
            except (ValueError, AssertionError):
                continue
            match item[0]:
                case 'offset':
                    offset = (float(x), float(y), float(z))
                case 'scale':
                    scale = (float(x), float(y), float(z))
                case 'rotate':
                    rotate = (float(x), float(y), float(z))
        return cls(path, scale, rotate, offset)

    def __repr__(self):
        return f"KFootprint3DModel(path={self.path}, offset={self.offset}, scale={self.scale}, rotate={self.rotate})"

    def sexp_tree(self) -> list[str | list]:
        ret: list[str | list] = ['model', f'"{self.path}"']
        ret.append(['scale', sexp_xyz(self.scale)])
        ret.append(['offset', sexp_xyz(self.offset)])
        ret.append(['rotate', sexp_xyz(self.rotate)])
        return ret


class KFootprintProperty(KiCadObject):
    """
    Handles and represents properties within a KiCadObject footprint.

    This class is designed to parse, modify, and manage specific properties related
    to a footprint in KiCadObject. It supports operations for parsing raw data into
    structured attributes, generating a serialized list representation of a property
    for KiCadObject, and other property-related operations. Instances of this class are
    instantiated with initial data representing the property and include support for
    various types of properties and modifications in their attributes.

    :ivar footprint: The KiCadObject footprint to which this property belongs.
    :type footprint: KFootprint
    :ivar type: The type of the property (e.g., reference, value, footprint, etc.). Must correspond to values in the `Type` enum.
    :type type: Type
    :ivar value: The value associated with the property.
    :type value: str
    :ivar at: The positional coordinates of the property in the footprint.
    :type at: Point
    :ivar angle: The angle of rotation to apply to the property, in degrees.
    :type angle: float
    :ivar layer: The specific KiCadObject layer on which the property exists.
    :type layer: str
    :ivar hide: Indicates whether the property is hidden in the KiCadObject footprint.
    :type hide: Literal['yes', 'no']
    :ivar unlocked: Indicates whether the property is locked or unlocked for editing.
    :type unlocked: Literal['yes', 'no']
    :ivar raw_code_list: The raw data used to initialize or define the property, usually from KiCadObject serialization.
    :type raw_code_list: list
    :ivar non_parsed_code_list: A list of code elements that were not parsed or assigned during initialization.
    :type non_parsed_code_list: list
    """

    class Type(StrEnum):
        Reference = auto()
        Value = auto()
        Footprint = auto()
        Datasheet = auto()
        Description = auto()

    def __init__(self, footprint: 'KFootprint', data: list, type=None, value: str = "",
                 at: Point = Point(0, 0), angle: float = 0.0, hide: Literal['yes', 'no'] = 'no',
                 unlocked: Literal['yes', 'no'] = 'yes', layer: str = ""):
        super().__init__()
        self.footprint = footprint
        self.type = type
        self.value = value
        self._at = at
        self.angle = angle
        self.layer = layer
        self.hide = hide
        self.unlocked = unlocked
        self.raw_code_list: list = data
        self.non_parsed_code_list: list = data

        if self.raw_code_list:
            self.parse()

    def parse(self):
        to_be_removed: list[int] = list()
        assert (self.raw_code_list[0] == 'property')
        # property type
        self.type = KFootprintProperty.Type(self.raw_code_list[1].strip('"'))
        to_be_removed.append(1)
        # property value
        self.value = self.raw_code_list[2].strip('"')
        to_be_removed.append(2)
        for i, item in enumerate(self.raw_code_list[3:], start=3):
            to_be_removed.append(i)
            match item:
                case ['at', x, y, angle]:
                    self._at = Point(float(x), float(y))
                    self.angle = float(angle)
                case ['at', x, y]:
                    self._at = Point(float(x), float(y))
                case ['unlocked', val]:
                    self.unlocked = val
                case ['layer', val]:
                    self.layer = val.strip('"')
                case ['hide', val]:
                    self.hide = val
                case ['uuid', val]:
                    # original uuid will be replaced by a unique one
                    pass
                case _:
                    to_be_removed.pop()
        for i in reversed(to_be_removed):
            self.non_parsed_code_list.pop(i)

    @property
    def at(self) -> Point:
        return self._at

    @at.setter
    def at(self, new_at: Point):  # Strangely, pcbnew GUI shows an inverted y offset value (a bug?)
        self._at = Point(new_at.x, -new_at.y)

    def sexp_tree(self):
        ret: list[str | list] = ["property"]
        ret.append(f'"{self.type}"')
        ret.append(f'"{self.value}"')
        ret.append(sexp_at_angle(self._at, self.angle))
        ret.append(['unlocked', self.unlocked])
        ret.append(sexp_layer(self.layer))
        ret.append(['hide', self.hide])
        ret.append(sexp_uuid(self.uuid))
        if self.non_parsed_code_list:
            ret.extend(self.non_parsed_code_list[1:])
        return ret

    def __repr__(self):
        return f'KiCadFootprintProperty(type={self.type}, value="{self.value}", at={self.at}, angle={self.angle}'


class KFootprint(KiCadObject):
    """
    Represents a KiCad footprint (.kicad_mod file) as a manipulable Python object.

    A `KFootprint` encapsulates the structure and attributes of a KiCad footprint,
    including its pads, properties, 3D models, and placement information.
    It can load footprints from absolute file paths or from library-style
    references (e.g. "Resistors_SMD:R_0603"), automatically resolving their
    location using known KiCad footprint folders.

    The class also handles coordinate flipping for back-side placement and
    manages mapping between pads and electrical nets.

    Notes
    -----
    - Footprints are resolved either from an absolute path or from KiCad-style
      library references using the form "LibraryName:FootprintName".
    - The default search paths depend on the operating system (Windows, macOS, Linux).
    - Angle normalization ensures consistency between front and back layers.
    - If the footprint cannot be found, a FileNotFoundError is raised.

    :param footprint: Path to a `.kicad_mod` file or a KiCad library reference
                      (e.g. "LibraryName:FootprintName").
    :type footprint: str
    :param at: Placement point of the footprint on the PCB.
    :type at: Point
    :param pad_net_mapping: Optional mapping between pad names and electrical nets.
    :type pad_net_mapping: dict[str, KNet] | None
    :param side: Indicates whether the footprint is placed on the front or back copper layer.
    :type side: KFootprint.Side
    :param default_net: Default net assigned to pads without explicit mapping.
    :type default_net: KNet | None
    :param angle: Rotation angle in degrees.
    :type angle: float
    :param fp_3dmodel: Optional associated 3D model of the footprint.
    :type fp_3dmodel: Footprint3DModel | None
    """


    class Side(Enum):
        Front = auto()
        Back = auto()

    folders = []

    @classmethod
    def _init_default_folders(cls):
        system = platform.system()
        if system == "Windows":
            cls.folders = [
                r'C:\Program Files\KiCad\7.0\share\kicad\footprints',
                os.path.expanduser(r'~\AppData\Roaming\kicad\7.0\footprints'),
            ]
        elif system == "Darwin":  # macOS
            cls.folders = [
                '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints',
                os.path.expanduser('~/Library/Preferences/kicad/7.0/footprints'),
            ]
        else:  # Linux and others
            cls.folders = [
                '/usr/share/kicad/footprints/',
                '/snap/kicad/15/usr/share/kicad/footprints/',
            ]

    @classmethod
    def set_footprint_folders(cls, new_folders: Iterable[str]):
        cls.folders = list(new_folders)

    @classmethod
    def append_to_footprint_folders(cls, new_folder: str):
        cls.folders.append(new_folder)

    @classmethod
    def extend_footprint_folders(cls, new_folders: Iterable[str]):
        cls.folders.extend(list(new_folders))

    def default_footprint_folders(self):
        return self.folders

    @classmethod
    def reset_footprint_folders(cls):
        cls._init_default_folders()

    def __init__(self, footprint: str, at=Point(0, 0), pad_net_mapping=None, side: Side = Side.Front,
                 default_net: KNet = None, angle: float = 0, fp_3dmodel: Footprint3DModel = None):
        if not self.folders:
            self._init_default_folders()

        super().__init__()
        if os.path.isfile(footprint):
            self.filepath = footprint
        elif ':' in footprint:
            try:
                lib, ftprnt = footprint.split(':')
                lib += '.pretty'
                ftprnt += '.kicad_mod'
                for folder in self.folders:
                    if os.path.isfile(os.path.join(folder, lib, ftprnt)):
                        self.filepath = os.path.join(folder, lib, ftprnt)
                        break
            except ValueError:
                raise FileNotFoundError(f"Footprint {footprint} not found")
        try:
            assert os.path.isfile(self.filepath)
        except (AttributeError, AssertionError):
            raise FileNotFoundError(f"Footprint {footprint} not found")

        self.at = at
        angle = round(angle, 3)
        self.angle = angle if side == KFootprint.Side.Front else 180 - angle
        self.angle = ((self.angle + 180) % 360) - 180
        self.angle = 180 if self.angle == -180 else self.angle
        self.layer = "F.Cu" if side == KFootprint.Side.Front else "B.Cu"
        self._pad_net_mapping = dict()
        self.pads: list[KPad] = list()
        self.pad_net_mapping: dict[str, KNet] = pad_net_mapping if isinstance(pad_net_mapping, dict) else dict()
        self.default_net = default_net
        self.properties: dict[str, KFootprintProperty] = dict()
        self.side = side
        self.fp_3dmodel = fp_3dmodel

        self.sexp_list = self.parse_sexpr()
        if side == KFootprint.Side.Back:
            self._flip_footprint(self.sexp_list)
        self.find_pads(self.sexp_list)
        self.find_properties(self.sexp_list)
        if self.fp_3dmodel is None:
            self.find_fp_3dmodel(self.sexp_list)

    @property
    def pad_net_mapping(self):
        return self._pad_net_mapping

    @pad_net_mapping.setter
    def pad_net_mapping(self, mapping: dict[str, KNet]):
        raise NotImplementedError("pad_net_mapping cannot be set after initialization")

    @staticmethod
    def _flip_footprint(data):
        if isinstance(data, list):
            # Check if the current list matches a <layer[s]> pattern
            if (
                    len(data) > 1
                    and data[0] in ('layer', 'layers')
            ):
                for i, item in enumerate(data[1:], start=1):
                    if isinstance(item, str):
                        if item.startswith('"F'):
                            item = '"B' + item[2:]
                        elif item.startswith('"B'):
                            item = '"F' + item[2:]
                        else:
                            continue
                        data[i] = item
            # Check if the current list matches a <coordinates [angle]> pattern
            if (
                    len(data) in (3, 4)
                    and data[0] in ('at', 'start', 'end', 'center', 'mid', 'xy')
                    and all(isinstance(v, str) and is_number_str(v) for v in data[1:])
            ):
                data[2] = str(-float(data[2]))
            # Check if the current list is an 'effects' list and update or add 'mirror' status
            if len(data) > 1 and data[0] == 'effects':
                for item in data[1:]:
                    if isinstance(item, list) and item[0] == 'justify':
                        if item[-1] == 'mirror':
                            del item[-1]
                        else:
                            item.append('mirror')
                        break
                else:
                    data.append(['justify', 'mirror'])
            # Recurse into all sub-elements
            for item in data:
                KFootprint._flip_footprint(item)

    @pad_net_mapping.setter
    def pad_net_mapping(self, mapping: dict[str, KNet]):
        for key, value in mapping.items():
            if not isinstance(value, KNet | None):
                raise TypeError("pad_net_mapping must be a dict of KNet objects")
        self._pad_net_mapping = mapping

    def _read_kicad_mod(self):
        """Reads the .kicad_mod file and returns its content as a string."""
        with open(self.filepath, 'r') as file:
            return file.read()

    def find_pads(self, data):
        self.pads.clear()
        to_be_removed: list[int] = list()
        for i, item in enumerate(data):
            if isinstance(item, list) and item[0] == 'pad':
                pad = KPad(footprint=self, data=item)
                pad.net = self.pad_net_mapping.get(pad.id, self.default_net)
                self.pads.append(pad)
                to_be_removed.append(i)
        for i in reversed(to_be_removed):
            del data[i]

    def find_properties(self, data):
        self.properties.clear()
        to_be_removed: list[int] = list()
        for i, item in enumerate(data):
            if isinstance(item, list) and item[0] == 'property':
                property = KFootprintProperty(footprint=self, data=item)
                self.properties[property.type] = property
                to_be_removed.append(i)
        for i in reversed(to_be_removed):
            del data[i]

    def find_fp_3dmodel(self, data):
        for i, item in enumerate(data):
            if isinstance(item, list) and item[0] == 'model':
                self.fp_3dmodel = Footprint3DModel.from_sexp_list(item)
                del data[i]
                break

    def parse_sexpr(self):
        """
        Parses a KiCadObject footprint file and converts it into a nested list
        structure (S-expression tree) representing the hierarchical format of the data.
        This function uses a basic parser to process the text content
        of a KiCadObject footprint and returns the parsed data as a Python list.

        :return: A nested list structure reflecting the hierarchical content
            of the KiCadObject footprint file
        :rtype: list
        """
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        parsed = nested_expr('(', ')').parse_string(content)
        return parsed.asList()[0]

    def sexp_tree(self) -> list[list | str]:
        ret: list = self.sexp_list[:]
        for pad in self.pads:
            ret.append(pad.sexp_tree())
        for property in self.properties.values():
            ret.append(property.sexp_tree())
        if self.fp_3dmodel is not None:
            ret.append(self.fp_3dmodel.sexp_tree())
        ret.insert(2, sexp_at_angle(self.at, self.angle))
        return ret

    def __repr__(self):
        return f"KFootprint(filepath={self.filepath}, at={self.at}, angle={self.angle})"


# populates the default folder list (platform dependant)
KFootprint._init_default_folders()