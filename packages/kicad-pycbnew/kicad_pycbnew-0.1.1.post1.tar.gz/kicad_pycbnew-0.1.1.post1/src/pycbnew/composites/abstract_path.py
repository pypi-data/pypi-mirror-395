import math
import sys
from abc import ABC, abstractmethod
from typing import Type

from pycbnew.primitives.gr_elements import Stroke, KGrLine
from pycbnew.primitives.net import KNet
from pycbnew.primitives.segment import KSegment, KArc
from pycbnew.utils.geometry import Point, Vector, Arc, find_equidistant_parallel_track_point


class KAbstractPath(ABC):
    def __init__(self, layer: str, origin: Point, width: float,
                 stroke: Stroke = Stroke.Default, closed: bool = False, net: KNet | None = None):
        self.net = net
        self.closed = closed
        self.stroke = stroke
        self.layer = layer
        self.width = width
        self._length: float = 0
        self._points: list[Point] = [origin]
        self._vectors: list[Vector] = list()
        self._straight_element_type: Type[KSegment] | Type[KGrLine] | None = None
        self._angular_path_elements: list[KSegment | KGrLine] = list()
        self._arced_path_elements: list[KSegment | KGrLine | KArc] = list()

    @property
    def vectors(self):
        return self._vectors

    @property
    def points(self):
        return self._points

    @property
    def origin(self):
        return self._points[0]

    @property
    def end(self):
        return self._points[-1]

    def __add__(self, other):
        if not isinstance(other, KAbstractPath):
            raise TypeError(f"Cannot add {other.__class__.__name__} to {self.__class__.__name__}")
        self.add_points(other.points)
        return self

    def invert(self):
        self._points.reverse()
        self._vectors = [-v for v in self._vectors[::-1]]
        self._angular_path_elements.reverse()
        self._arced_path_elements.reverse()

    @classmethod
    def from_points(cls, points: list[Point], layer: str, width: float,
                    stroke: Stroke = Stroke.Default, closed: bool = False, net: KNet | None = None):
        path = cls(layer=layer, origin=points[0], width=width, stroke=stroke, closed=closed, net=net)
        path.add_points(points[1:])
        return path

    @classmethod
    def from_vectors(cls, origin: Point, vectors: list[Vector], layer: str, width: float,
                     stroke: Stroke = Stroke.Default, closed: bool = False, net: KNet | None = None):
        path = cls(layer=layer, origin=origin, width=width, stroke=stroke, closed=closed, net=net)
        path.add_vectors(vectors)
        return path

    def add_vector(self, vector: Vector):
        if vector.norm < 1e-4:
            return
        self._angular_path_elements.clear()
        self._arced_path_elements.clear()
        self._vectors.append(vector)
        self._points.append(self._points[-1] + vector)

    def add_vectors(self, vectors: list[Vector]):
        for vector in vectors:
            self.add_vector(vector)

    def add_point(self, point: Point):
        if len(self._points) and (point - self._points[-1]).norm < 1e-4:
            return
        self._angular_path_elements.clear()
        self._arced_path_elements.clear()
        self._points.append(point)
        self._vectors.append(self._points[-1] - self._points[-2])

    def add_points(self, points: list[Point]):
        for point in points:
            self.add_point(point)

    def add_vertical_line(self, y: float):
        self.add_point(Point(self.end.x, y))

    def add_horizontal_line(self, x: float):
        self.add_point(Point(x, self.end.y))

    @staticmethod
    def _vectors_45_0_from_vector(vector: Vector) -> list[Vector]:
        """
        Splits a vector into two vectors: one aligned diagonally at a 45-degree angle (vec_45)
        and the other aligned horizontally or vertically (vec_0).

        The function computes a segment along the diagonal (45 degrees) with the largest
        length possible while ensuring the remaining part of the vector is either purely
        horizontal or vertical. The method returns a list containing the diagonal segment
        and the remaining segment.

        :param vector: The vector to be split into diagonal and horizontal/vertical segments.
        :type vector: Vector
        :return: A list of two vectors - the first one is a 45-degree diagonal vector (vec_45), and
            the second one is the remaining horizontal or vertical vector (vec_0) of the original vector.
        :rtype: list[Vector]
        """
        dx, dy = vector.to_tuple()
        d = min(abs(dx), abs(dy))
        if dx != 0 and dy != 0:
            sgn_dx = math.copysign(1, dx)
            sgn_dy = math.copysign(1, dy)
            vec_45 = Vector(d * sgn_dx, d * sgn_dy)
        else:
            vec_45 = Vector(0, 0)
        vec_0 = vector - vec_45
        return [vec_45, vec_0]

    def add_3segments_45_0_45_by_vector(self, vector: Vector, pos: float = 0.5):
        """
        Adds three segments to the object based on the given vector.
        The first and last segments are aligned diagonally at a 45-degree angle.
        The middle segment is aligned horizontally or vertically and passes through the
        intermediate point defined by the position parameter.

        :param vector: The vector that determines the direction and magnitude for the
            segments to be added.
        :type vector: Vector
        :param pos: A float between 0 and 1 that defines the position along the 45-
            degree vector where intermediate points are calculated. Defaults to 0.5.
        :type pos: float
        :return: None
        """
        if vector.norm == 0:
            return
        p1 = self.points[-1]
        p4 = p1 + vector
        v_45, v_0 = self._vectors_45_0_from_vector(vector)
        p2 = p1 + pos * v_45
        p3 = p4 + (pos - 1) * v_45
        self.add_points([p2, p3, p4])

    def add_3segments_0_45_0_by_vector(self, vector: Vector, pos: float = 0.5):
        """
        Adds three segments to the object based on the given vector.
        The first and last segments are aligned horizontally or vertically.
        The middle segment is aligned diagonally at a 45-degree angle and passes through the
        intermediate point defined by the position parameter.

        :param vector: Directional vector used to determine the segments
        :type vector: Vector
        :param pos: A float between 0 and 1 that defines the position along the horizontal or vertical
            vector where intermediate points are calculated. Defaults to 0.5.
        :type pos: float
        :return: None
        """
        if vector.norm == 0:
            return
        p1 = self.points[-1]
        p4 = p1 + vector
        v_45, v_0 = self._vectors_45_0_from_vector(vector)
        p2 = p1 + pos * v_0
        p3 = p4 + (pos - 1) * v_0
        self.add_points([p2, p3, p4])

    def add_3segments_45_0_45_by_point(self, point: Point, pos: float = 0.5):
        """
        Adds three segments to the object based on the given point.
        The first and last segments are aligned diagonally at a 45-degree angle.
        The middle segment is aligned horizontally or vertically and passes through the
        intermediate point defined by the position parameter.

        :param point: The point that determines the end of the last segment.
        :type point: Point
        :param pos: A float between 0 and 1 that defines the position along the 45-
            degree vector where intermediate points are calculated. Defaults to 0.5.
        :type pos: float
        :return: None
        """
        self.add_3segments_45_0_45_by_vector(point - self._points[-1], pos)

    def add_3segments_0_45_0_by_point(self, point: Point, pos: float = 0.5):
        """
        Adds three segments to the object based on the given point.
        The first and last segments are aligned horizontally or vertically.
        The middle segment is aligned diagonally at a 45-degree angle and passes through the
        intermediate point defined by the position parameter.

        :param point: The point that determines the end of the last segment.
        :type point: Point
        :param pos: A float between 0 and 1 that defines the position along the 45-
            degree vector where intermediate points are calculated. Defaults to 0.5.
        :type pos: float
        :return: None
        """
        self.add_3segments_0_45_0_by_vector(point - self._points[-1], pos)

    def add_2segments_by_vector_45_0(self, vector: Vector):
        """
        Adds two segments to the object based on the given vector.

        This method processes the vector to generate specific segment additions.
        The first segment is aligned diagonally at a 45-degree angle.
        The last segment is aligned horizontally or vertically.

        If the norm of the vector is zero, this method does nothing.

        :param vector: An instance of Vector used to define the segments to be added
        :return: None
        """
        if vector.norm == 0:
            return
        self.add_vectors(self._vectors_45_0_from_vector(vector))

    def add_2segments_by_vector_0_45(self, vector: Vector):
        """
        Adds two segments to the object based on the given vector.

        This method processes the vector to generate specific segment additions.
        The first segment is aligned horizontally or vertically.
        The last segment is aligned diagonally at a 45-degree angle.

        If the norm of the vector is zero, this method does nothing.

        :param vector: An instance of Vector used to define the segments to be added
        :return: None
        """
        if vector.norm == 0:
            return
        self.add_vectors(self._vectors_45_0_from_vector(vector)[::-1])

    def add_2segments_by_point_45_0(self, point: Point):
        """
        Adds two segments to the object based on the given point.

        This method processes the vector to generate specific segment additions.
        The first segment is aligned diagonally at a 45-degree angle.
        The last segment is aligned horizontally or vertically.

        If the last point of the path and the point passed as an argument are the same,
        this method does nothing.

        :param point: The point that determines the end of the last segment.
        :type point: Point
        :return: None
        """
        self.add_2segments_by_vector_45_0(point - self._points[-1])

    def add_2segments_by_point_0_45(self, point: Point):
        """
        Adds two segments to the object based on the given vector.

        This method processes the vector to generate specific segment additions.
        The first segment is aligned horizontally or vertically.
        The last segment is aligned diagonally at a 45-degree angle.

        If the last point of the path and the point passed as an argument are the same,
        this method does nothing.

        :param point: The point that determines the end of the last segment.
        :type point: Point
        :return: None
        """
        self.add_2segments_by_vector_0_45(point - self._points[-1])

    @property
    def length(self) -> float:
        if self._angular_path_elements:
            return sum([elt.length for elt in self._angular_path_elements])
        elif self._arced_path_elements:
            s = 0.0
            for elt in self._arced_path_elements:
                if isinstance(elt, (KSegment, KGrLine)):
                    s += elt.length
                elif isinstance(elt, KArc):
                    s += elt.arc.length
            return s
        else:
            raise ValueError("Path is empty or segments not computed")

    @abstractmethod
    def angular_path_elements(self) -> list[KSegment | KGrLine]:
        if self._straight_element_type is None:
            raise TypeError(f"{__class__.__name__} must define '_straight_element_type'")
        self._arced_path_elements.clear()
        self._angular_path_elements.clear()
        pts = self._points
        if self.closed:
            pts.append(self._points[0])
        for i in range(len(pts) - 1):
            _start_point = pts[i]
            _end_point = pts[i + 1]
            self._angular_path_elements.append(self._straight_element_type(point1=_start_point,
                                                                           point2=_end_point,
                                                                           layer=self.layer,
                                                                           width=self.width,
                                                                           stroke=self.stroke,
                                                                           net=self.net))
        return self._angular_path_elements

    @abstractmethod
    def curved_path_elements(self, max_radius: float = None) -> list[KSegment | KArc] | list[KGrLine | KArc]:
        """
        Generate a sequence of path elements (straight segments and arcs) for a polyline,
        replacing each vertex with a circular arc where possible, respecting a maximum
        curvature radius.

        :param max_radius: Maximum allowed radius for arcs; defaults to the largest
                           representable float if None.
        :return: List of path elements (straight lines and arcs) forming the curved path.

        Process:
        1. Initialize vertex parameters:
           - Compute the half-tangent of each internal angle.
           - Compute the s-parameter: distance along each adjacent segment where the arc starts.
        2. Iteratively fit the s-parameters to avoid overlap of arcs on short segments.
        3. For each internal vertex, attempt to create an arc tangent to adjacent segments.
           - If arcs cannot be placed (degenerate or zero-length vectors), fall back to straight segments.
        4. Append straight segments between arcs as needed to maintain connectivity.
        5. Return the list of all path elements.
        """
        if self._straight_element_type is None:
            raise TypeError(f"{__class__.__name__} must define '_straight_element_type'")

        if max_radius is None:
            max_radius = sys.float_info.max

        # Clear previous path elements
        self._arced_path_elements.clear()
        self._angular_path_elements.clear()

        common_kwargs = {
            "layer": self.layer,
            "width": self.width,
            "net": self.net
        }

        # Step 1: Initialize vertices parameters
        vertices_params = self._init_vertices_params(max_radius)

        # Step 2: Iteratively fit s-parameters to avoid arc overlaps
        self._fit_s_param(vertices_params)
        self._fit_s_param(vertices_params, force=True)

        # Round s-values for numerical stability
        the_s = [round(dic['s'], 5) for dic in vertices_params]

        # Track the current endpoint for straight segments
        _end_point = self._points[0]

        # Step 3: Build arcs and optional straight segments for each internal vertex
        for i, pt in enumerate(self._points[1:-1]):
            v1, v2 = self._vectors[i], self._vectors[i + 1]
            try:
                arc = Arc.from_vectors(pt, -v1, v2, the_s[i + 1])
                if arc.radius < self.width / 2:
                    raise ValueError("Arc radius too small")
            except (ZeroDivisionError, ValueError):
                arc = None  # Cannot form an arc: points coincide or are collinear, or radius is too small.

            # Decide if a straight segment is needed before the arc
            tol = self.width / 20  # minimum straight segment length is 1/10 of the half-width
            target = pt if arc is None else arc.p1
            straight_pts = (_end_point, target) if (_end_point - target).norm > tol else None

            # Append a straight segment if needed
            if straight_pts is not None:
                self._arced_path_elements.append(
                    self._straight_element_type(
                        point1=straight_pts[0],
                        point2=straight_pts[1],
                        stroke=self.stroke,
                        **common_kwargs
                    )
                )

            # Append arc if created
            if arc is not None:
                self._arced_path_elements.append(KArc(arc=arc, **common_kwargs))

            # Update endpoint for next segment
            if arc is not None:
                _end_point = arc.p3
            elif straight_pts is not None:
                _end_point = straight_pts[1]
            else:
                _end_point = pt

        # Step 4: Append last straight segment if necessary
        if (self.points[-1] - _end_point).norm > self.width / 2 / 10:
            self._arced_path_elements.append(
                self._straight_element_type(
                    point1=_end_point,
                    point2=self.points[-1],
                    stroke=self.stroke,
                    **common_kwargs
                )
            )

        # Step 5: Return the completed curved path
        return self._arced_path_elements

    def _init_vertices_params(self, max_radius: float) -> list[dict[str, float]]:
        """
        Initialize geometric parameters for each vertex in the point set.

        For each vertex (except the first and last), this method calculates:
        - `h_tan`: the tangent of half the internal angle formed by adjacent vectors
                   (-v_prev, v_next)
        - `s`: the initial attachment distance for an arc centered at the vertex,
               respecting the maximum radius constraint

        The first and last vertices are considered endpoints, so both `h_tan` and `s` are 0.

        :param max_radius: Maximum radius allowed for arcs when computing s-parameter
        :type max_radius: float
        :return: List of dictionaries with keys:
            - 'h_tan': half-angle tangent for the vertex
            - 's': initial s-parameter for the vertex
        :rtype: list[dict[str, float]]
        """
        vertices_params: list[dict[str, float]] = []
        for i, point in enumerate(self._points):
            if i in (0, len(self._points) - 1):
                h_tan = 0.0
                s = 0.0
            else:
                v_prv = self._vectors[i - 1]
                v_nxt = self._vectors[i]
                # Tangent of half the internal angle at this vertex
                h_tan = abs(math.tan(Vector.angle(-v_prv, v_nxt) / 2))
                # Initial s-parameter constrained by vector lengths and maximum radius
                s = min(v_prv.norm, v_nxt.norm, Arc.s_from_vectors(v_prv, v_nxt, max_radius))
            vertices_params.append({'h_tan': h_tan, 's': s})
        return vertices_params

    def _fit_s_param(self,
                     vertices_params: list[dict[str, float]],
                     loop_max: int = 10_000,
                     convergence_limit: float = 1e-6,
                     relax: float = 0.01,
                     force: bool = False) -> None:
        """
        Iteratively adjust the s-parameters of all vertices using a forward-backward
        sweep to reduce arc overlaps more efficiently.

        Here, the s-parameter represents the attachment distance of an arc at a vertex:
        it is the length along each adjacent segment from the vertex to the start of
        the circular arc that replaces the original sharp corner. Adjusting s-parameters
        ensures that arcs from consecutive vertices do not overlap.

        Each iteration performs:
        1. Forward sweep: adjusts consecutive vertex pairs from start to end.
        2. Backward sweep: adjusts consecutive vertex pairs from end to start.

        The relaxation factor limits the per-step adjustment to avoid overshoot.

        Convergence is reached when the maximum s-parameter change across all pairs
        falls below `convergence_limit`.

        :param vertices_params: List of dictionaries containing vertex parameters
            ('h_tan' and 's') for each vertex.
        :param loop_max: Maximum number of full sweeps (forward + backward)
        :param convergence_limit: Threshold below which changes are considered converged
        :param relax: Fraction of overlap reduced per relaxation step
        :param force: If True, force relaxation to consume all overlap (default True)
        :return: None (modifies vertices_params in place)
        """
        n = len(vertices_params)
        if force:
            relax_params = {'min_relax': 1.0, 'max_relax': 1.0, 'base_relax': 1.0}
        else:
            relax_params = {'base_relax': relax}
        for _ in range(loop_max):
            evol_max = 0.0
            # Forward sweep
            for i in range(n - 1):
                s_i = vertices_params[i]['s']
                s_j = vertices_params[i + 1]['s']
                d_ij = (self._points[i + 1] - self._points[i]).norm
                htan_i = vertices_params[i]['h_tan']
                htan_j = vertices_params[i + 1]['h_tan']

                new_s_i, new_s_j = self._relax_s_pair(s_i, s_j, d_ij, htan_i, htan_j, **relax_params)
                vertices_params[i]['s'] = new_s_i
                vertices_params[i + 1]['s'] = new_s_j
                evol_max = max(evol_max, abs(new_s_i - s_i), abs(new_s_j - s_j))

            # Backward sweep
            for i in reversed(range(n - 1)):
                s_i = vertices_params[i]['s']
                s_j = vertices_params[i + 1]['s']
                d_ij = (self._points[i + 1] - self._points[i]).norm
                htan_i = vertices_params[i]['h_tan']
                htan_j = vertices_params[i + 1]['h_tan']

                new_s_i, new_s_j = self._relax_s_pair(s_i, s_j, d_ij, htan_i, htan_j, **relax_params)
                vertices_params[i]['s'] = new_s_i
                vertices_params[i + 1]['s'] = new_s_j
                evol_max = max(evol_max, abs(new_s_i - s_i), abs(new_s_j - s_j))

            if evol_max < convergence_limit:
                break

    @staticmethod
    def _relax_s_pair(s_i: float, s_j: float,
                      d_ij: float,
                      htan_i: float, htan_j: float,
                      base_relax: float = 0.01,
                      min_relax: float = 1e-20,
                      max_relax: float = 0.5) -> tuple[float, float]:
        """
        Adjust the attachment distances (s_i, s_j) for a pair of consecutive vertices
        using a dynamic relaxation factor that depends on segment overlap and angles.

        :param s_i: attachment distance from vertex Pi
        :param s_j: attachment distance from vertex Pj
        :param d_ij: length of the segment [Pi Pj]
        :param htan_i: tangent of half the angle at Pi
        :param htan_j: tangent of half the angle at Pj
        :param base_relax: base relaxation factor (default 0.01)
        :param max_relax: maximum allowed relaxation (default 0.5)
        :param min_relax: minimum allowed relaxation (default 1e-20)
        :return: tuple (new_s_i, new_s_j) adjusted distances
        """
        if s_i + s_j <= d_ij:
            return s_i, s_j  # no overlap

        overlap = (s_i + s_j) - d_ij

        # Compute the radii of curvature (the larger the radius, the more s will decrease)
        r_i =  s_i / htan_i if htan_i > 0 else 1e10
        r_j =  s_j / htan_j if htan_j > 0 else 1e10

        denom = r_i + r_j
        if denom == 0:
            return s_i, s_j  # degenerate geometry

        # Dynamic relaxation factor
        # - proportional to relative overlap
        # - reduced for sharp angles (htan large)
        angle_factor = 1 / (1 + max(htan_i, htan_j))  # 0 < factor <= 1
        relax = max(min_relax, min(max_relax, base_relax * (overlap / d_ij) * angle_factor))

        # Apply weighted relaxation
        # Retreats (delta_i, delta_j) are proportional to the radius of curvature of the opposite vertex:
        #   - A larger-radius (flatter) arc at the neighboring vertex will push the current s-parameter more,
        #     while a sharper arc (smaller radius) moves less to avoid further steepening.
        #   - This is why delta_i uses r_j and delta_j uses r_i.
        delta_i = relax * overlap * r_j / denom
        delta_j = relax * overlap * r_i / denom
        s_i = max(0.0, s_i - delta_i)
        s_j = max(0.0, s_j - delta_j)

        return s_i, s_j

    def _parallel_path_points(self, start_point: Point, end_point: Point) -> list[Point]:
        ret: list[Point] = [start_point]
        for i in range(1, len(self._points) - 1):
            pt = find_equidistant_parallel_track_point(*self._points[i - 1:i + 2], ret[-1])
            ret.append(pt)
        ret.append(end_point)
        return ret
