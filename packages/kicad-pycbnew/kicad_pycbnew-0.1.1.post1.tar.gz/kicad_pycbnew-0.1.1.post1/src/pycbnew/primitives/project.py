import subprocess
from collections.abc import Iterable
from typing import Any
from importlib.metadata import version

from .footprint import KFootprint
from .gr_elements import KGrRect, KGrText, KGrLine, KGrPoly, KGrDimension
from .kicad import KiCadObject
from .layer import LayerCategory, KLayer
from .net import KNet
from .segment import KSegment, KArc
from .sexpressions import sexp_paper, sexp_layers_in_project, tree_to_sexp
from .via import KVia
from .zone import KZone

__version__ = version("kicad-pycbnew")

class KProject(KiCadObject):
    """
    Represents a KiCadObject PCB project object.

    The KProject class is designed to create and manipulate KiCadObject PCB projects programmatically.
    It allows for the creation, modification, and saving of PCB design files, using the KiCadObject PCB file format.
    The class facilitates various operations such as adding PCB elements, running design rule checks (DRC), exporting files
    in different formats (e.g., SVG or PDF), and organizing PCB layers.

    The class inherits from the KiCadObject base class.

    :param filename: The path to the PCB file to be created or modified. If `filename` does not end with ".kicad_pcb",
        ".kicad_pcb" will be appended to the filename.
    :type filename: str
    :param version: The KiCadObject version used to create the PCB file. Defaults to "20241229".
        KiCadObject will refuse to open a `.kicad_pcb` file whose version is newer than the one
        supported by the installed application. See:
        https://gitlab.com/kicad/code/kicad/-/blob/master/pcbnew/pcb_io/kicad_sexpr/pcb_io_kicad_sexpr.h
        for the mapping between *SEXPR_BOARD_FILE_VERSION* and KiCadObject versions.
        of KiCadObject used to open the PCB file, the PCB file will be saved with the latest version.
    :type version: str
    :param copper_layers: The number of copper layers in the PCB. Defaults to 2.
    :type copper_layers: int
    :param paper: The paper size of the PCB. Defaults to "A4".
        Accepted formats are: "A0", ..., "A5", "A", ..., "E", "USLetter", "USLegal" and "USLedger".
        Paper direction defaults to landscape. One can specify the paper orientation by appending " portrait"
        to the format string. For example, "A2 portrait" will set the paper orientation to portrait.
        For custom paper sizes, a tuple of (width, height) can be specified. For example, (1000, 1400)
         will set the paper size to 1000mm × 1400 mm.

    """
    def __init__(self,
                 filename: str,
                 version: str = '20241229',
                 copper_layers: int = 2,
                 paper: str|tuple[int, int] = 'A4'):
        super().__init__()
        self.filename = filename
        if not self.filename.endswith(".kicad_pcb"):
            self.filename += ".kicad_pcb"
        self.copper_layers = copper_layers
        self.paper = paper
        self.version = version

        # nets
        self.nets: list[KNet] = list()
        self._nets_set: set[KNet] = set()

        # rects
        self.rects: list[KGrRect] = list()

        # segments
        self.segments: list[KSegment] = list()

        # gr_lines
        self.gr_lines: list[KGrLine] = list()

        # gr_polys
        self.gr_polys: list[KGrPoly] = list()

        # arcs
        self.arcs: list[KArc] = list()

        # dimensions
        self.dimensions: list[KGrDimension] = list()

        # texts
        self.texts: list[KGrText] = list()

        # footprints
        self.footprints: list[KFootprint] = list()

        # vias
        self.vias: list[KVia] = list()

        # zones
        self.zones: list[KZone] = list()

        # Layers
        self.layers: dict[int, KLayer] = {
            0: KLayer(0, "F.Cu", LayerCategory.Signal)}
        for i in range(self.copper_layers - 2):
            self.layers[i + 1] = KLayer(i + 1, f"In{i + 1}.Cu", LayerCategory.Signal)
        self.layers.update({
            31: KLayer(31, "B.Cu", LayerCategory.Signal),
            32: KLayer(32, "B.Adhes", LayerCategory.User, "B.Adhesive"),
            33: KLayer(33, "F.Adhes", LayerCategory.User, "F.Adhesive"),
            34: KLayer(34, "B.Paste", LayerCategory.User),
            35: KLayer(35, "F.Paste", LayerCategory.User),
            36: KLayer(36, "B.SilkS", LayerCategory.User, "B.Silkscreen"),
            37: KLayer(37, "F.SilkS", LayerCategory.User, "F.Silkscreen"),
            38: KLayer(38, "B.Mask", LayerCategory.User),
            39: KLayer(39, "F.Mask", LayerCategory.User),
            40: KLayer(40, "Dwgs.User", LayerCategory.User, "User.Drawings"),
            41: KLayer(41, "Cmts.User", LayerCategory.User, "User.Comments"),
            42: KLayer(42, "Eco1.User", LayerCategory.User, "User.Eco1"),
            43: KLayer(43, "Eco2.User", LayerCategory.User, "User.Eco2"),
            44: KLayer(44, "Edge.Cuts", LayerCategory.User),
            45: KLayer(45, "Margin", LayerCategory.User),
            46: KLayer(46, "B.CrtYd", LayerCategory.User, "B.Courtyard"),
            47: KLayer(47, "F.CrtYd", LayerCategory.User, "F.Courtyard"),
            48: KLayer(48, "B.Fab", LayerCategory.User),
            49: KLayer(49, "F.Fab", LayerCategory.User)
        })

    def add(self, elements: Any):
        def flatten(obj):
            if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
                for x in obj:
                    yield from flatten(x)
            else:
                yield obj
        for elt in flatten(elements):
            match elt:
                case KNet():
                    if elt in self._nets_set:
                        raise ValueError(f"Net number {elt.number} already exists in the project.")
                    else:
                        self.nets.append(elt)
                        self._nets_set.add(elt)
                case KGrRect():
                    self.rects.append(elt)
                case KSegment():
                    self.segments.append(elt)
                case KGrLine():
                    self.gr_lines.append(elt)
                case KGrPoly():
                    self.gr_polys.append(elt)
                case KArc():
                    self.arcs.append(elt)
                case KGrDimension():
                    self.dimensions.append(elt)
                case KGrText():
                    self.texts.append(elt)
                case KFootprint():
                    self.footprints.append(elt)
                case KVia():
                    self.vias.append(elt)
                case KZone():
                    self.zones.append(elt)
                case _:
                    raise ValueError(f"Unknown element type: {type(elt)}")

    def sexp_tree(self) -> list[list | str]:
        ret: list[list|str] = ['kicad_pcb']
        ret.append(['version', f'{self.version}'])
        ret.append(['generator', '"pycbnew"'])
        ret.append(['generator_version', f'"{__version__}"'])
        ret.append(sexp_paper(self.paper))
        ret.append(sexp_layers_in_project(self.layers.values()))
        for primitive in (
            self.nets,
            self.zones,
            self.rects,
            self.segments,
            self.gr_lines,
            self.gr_polys,
            self.arcs,
            self.dimensions,
            self.texts,
            self.vias,
            self.footprints
        ):
            ret.extend(p.sexp_tree() for p in primitive)
        return ret

    def save(self):
        sexp = tree_to_sexp(self.sexp_tree())
        with open(self.filename, "w") as f:
            f.write(sexp)

    def higher_net_number(self):
        try:
            return max(net.number for net in self.nets)
        except ValueError:
            return 0

    def run_drc(self):
        try:
            # Regular KiCadObject CLI installation
            subprocess.run(["kicad-cli", "pcb", "drc", f"{self.filename}"])
        except FileNotFoundError:
            # KiCadObject installed via Snap package
            subprocess.run(["kicad.kicad-cli", "pcb", "drc", f"{self.filename}"])


    def export_svg(self):
        layers = ("F.Cu",)
        for i in range(self.copper_layers - 2):
            layers += (f"In{i + 1}.Cu",)
        layers += ("B.Cu",)
        args = [
            "pcb", "export", "svg", f"{self.filename}",
            "--layers", ",".join(layers),
            "--drill-shape-opt", '2'
        ]
        try:
            # Regular KiCadObject CLI installation
            subprocess.run(["kicad.kicad-cli"] + args)
        except FileNotFoundError:
            # KiCadObject installed via Snap package
            subprocess.run(["kicad-cli"] + args)

    def export_pdf(self):
        layers = ("F.Cu",)
        for i in range(self.copper_layers - 2):
            layers += (f"In{i + 1}.Cu",)
        layers += ("B.Cu",)
        args = [
            "pcb", "export", "pdf", f"{self.filename}",
            "--layers", ",".join(layers),
            "--mode-multipage",
            "--drill-shape-opt", '2'
        ]
        try:
            subprocess.run(["kicad.kicad-cli"] + args)
        except FileNotFoundError:
            subprocess.run(["kicad-cli"] + args)