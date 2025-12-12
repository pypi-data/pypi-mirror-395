from pycbnew.composites.abstract_path import KAbstractPath
from pycbnew.primitives.net import KNet
from pycbnew.primitives.segment import KSegment, KArc
from pycbnew.utils.geometry import Point


class KSegmentPath(KAbstractPath):
    def angular_path_elements(self) -> list[KSegment]:
        self._straight_element_type = KSegment
        return super().angular_path_elements()

    def curved_path_elements(self, max_radius: float = None) -> list[KSegment | KArc]:
        self._straight_element_type = KSegment
        return super().curved_path_elements(max_radius)

    def parallel_path(self, start_point: Point, end_point: Point, net: KNet = None,
                      layer: str = None, width: float = None) -> 'KSegmentPath':
        p_path = KSegmentPath.from_points(points = self._parallel_path_points(start_point, end_point),
                                          layer=layer or self.layer,
                                          width=width or self.width,
                                          net=net or self.net)
        return p_path
