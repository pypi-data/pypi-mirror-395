from pycbnew.composites.abstract_path import KAbstractPath
from pycbnew.primitives.gr_elements import KGrLine
from pycbnew.primitives.segment import KArc


class KGrLinePath(KAbstractPath):
    def angular_path_elements(self) -> list[KGrLine]:
        self._straight_element_type = KGrLine
        return super().angular_path_elements()

    def curved_path_elements(self, max_radius: float = None) -> list[KGrLine | KArc]:
        self._straight_element_type = KGrLine
        return super().curved_path_elements(max_radius)
