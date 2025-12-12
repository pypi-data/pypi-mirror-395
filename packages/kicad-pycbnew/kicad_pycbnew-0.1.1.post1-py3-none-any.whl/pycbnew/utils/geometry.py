from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Iterable, TypeVar, Literal

from pycbnew.utils.bernstein import bernstein

T = TypeVar('T', bound='Coordinate')


class Coordinate(ABC):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def __copy__(self):
        return self.__class__(self.x, self.y)

    def __getitem__(self, item):
        return self.to_tuple()[item]

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise NotImplementedError('Index out of range')

    def __truediv__(self, other):
        if isinstance(other, float | int):
            return self.__class__(self.x / other, self.y / other)
        raise NotImplementedError

    def __mul__(self: T, other: float | int) -> T:
        if isinstance(other, float | int):
            return self.__class__(self.x * other, self.y * other)
        raise NotImplementedError

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def to_tuple(self):
        return self.x, self.y

    @classmethod
    def from_iterable(cls, iterable: Iterable[float]):
        if (isinstance(iterable, tuple | list) and
                len(iterable) == 2 and
                isinstance(iterable[0], float) and
                isinstance(iterable[1], float)):
            return cls(iterable[0], iterable[1])
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other):
        if (isinstance(other, tuple | list) and
                len(other) == 2 and
                isinstance(other[0], float | int) and
                isinstance(other[1], float | int)):
            return self.__class__(self.x + other[0], self.y + other[1])
        raise NotImplementedError

    def __radd__(self, other):
        return self.__add__(other)

    @abstractmethod
    def __sub__(self, other):
        if (isinstance(other, tuple | list) and
                len(other) == 2 and
                isinstance(other[0], float | int) and
                isinstance(other[1], float | int)):
            return self.__class__(self.x - other[0], self.y - other[1])
        raise NotImplementedError

    def __rsub__(self, other):
        if isinstance(other, list | tuple):
            return self.__class__(other[0] - self.x, other[1] - self.y)
        raise NotImplementedError

    def __hash__(self):
        return hash((self.__class__, self.x, self.y))

    def __len__(self):
        return 2


class Vector(Coordinate):
    def __add__(self, other):
        try:
            return super().__add__(other)
        except NotImplementedError:
            if isinstance(other, Vector):
                return Vector(self.x + other.x, self.y + other.y)
            raise NotImplementedError

    def __sub__(self, other):
        try:
            return super().__sub__(other)
        except NotImplementedError:
            if isinstance(other, Vector):
                return Vector(self.x - other.x, self.y - other.y)
            raise NotImplementedError

    def __mul__(self, other):
        try:
            return super().__mul__(other)
        except NotImplementedError:
            if isinstance(other, Vector):
                return self.x * other.x + self.y * other.y
            raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def rotate(self, angle, degrees: bool = False):
        """
        Rotate the vector by a given angle.

        This method returns a new `Vector` that is the result of rotating
        the current vector by the specified angle. The rotation is applied
        in the 2D plane using standard trigonometric formulas.

        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, the reference frame is indirect. Consequently, the
            rotation performed here corresponds to the opposite direction
            of a rotation in a standard (direct) Cartesian coordinate system.

        :param angle: The angle by which to rotate the vector.
        :type angle: float
        :param degrees: If True, interpret `angle` as degrees. Otherwise, radians.
        :type degrees: bool
        :return: A new `Vector` rotated by the given angle.
        :rtype: Vector
        """
        if degrees:
            angle = math.radians(angle)
        return Vector(+ self.x * math.cos(angle) + self.y * math.sin(angle),
                      - self.x * math.sin(angle) + self.y * math.cos(angle))

    def __xor__(self, other):
        """
        Compute the 2D pseudo-scalar (cross) product between two vectors.

        For two vectors a = (ax, ay) and b = (bx, by),
        this method returns the scalar value:

            a ^ b = ax * by - ay * bx

        This is equivalent to the determinant of the 2×2 matrix [a, b].
        It represents the signed area of the parallelogram spanned by the vectors.

        :param other: The other vector to compute the pseudo-scalar product with.
        :type other: Vector
        :return: The scalar result of the 2D cross product.
        :rtype: float
        """
        if isinstance(other, Vector):
            return self.x * other.y - self.y * other.x
        else:
            return NotImplemented

    def unit(self):
        """
        Calculates the unit vector of the current vector.

        The unit vector, also known as the normalized vector, is the vector with
        the same direction as the original vector but with a magnitude (or norm)
        of 1. This method achieves normalization by dividing the vector by its
        norm.

        :returns: A normalized version of the current vector.
        """
        return self / self.norm

    @property
    def norm(self):
        """
        Computes the Euclidean norm (magnitude) of the object.

        The norm property calculates the square root of the dot product
        functionality (self * self) to compute the sum of the squares.

        :return: The Euclidean norm of the object.
        :rtype: float
        """
        return math.sqrt(self * self)

    @staticmethod
    def angle(vector1: 'Vector', vector2: 'Vector'):
        """
        Calculate the signed angle between two vectors (from vector1 to vector2).

        This method computes the angle in radians between two `Vector` objects.
        The calculation is performed using the coordinates (x, y) of both vectors.
        The result is derived using the `math.atan2` function, which takes into
        account the cross-product and dot product of the vectors to return the
        angle in the range ]-π, π].


        Note:
            Since KiCad uses a coordinate system where the Y-axis is oriented
            downward, the reference frame is indirect. Consequently, the computed
            angles are the opposites of those obtained in a direct (standard)
            coordinate system.

        :param vector1: The first vector for the angle calculation
        :type vector1: Vector
        :param vector2: The second vector for the angle calculation
        :type vector2: Vector
        :return: The angle in radians between the two vectors
        :rtype: float
        """
        x1, y1 = vector1.x, vector1.y
        x2, y2 = vector2.x, vector2.y
        if x1 * y2 - x2 * y1 in (-0.0, 0.0):
            return math.pi
        return math.atan2(x2 * y1 - x1 * y2, x1 * x2 + y1 * y2)


class Point(Coordinate):
    def __add__(self, other: list | tuple | Vector):
        """
        Adds the given object to the current object. If the given object is not a compatible type as defined 
        (list, tuple, or Vector), raises a NotImplementedError. If the given object is an instance of Vector,
        it performs specific addition logic resulting in a Point object.

        :param other: The object to add, which must be a list, tuple, or Vector type.
        :return: A new object resulting from the addition. For a Vector type, returns a Point object.
        :rtype: Any
        :raises NotImplementedError: If the addition operation is not defined for the given type.
        """
        try:
            return super().__add__(other)
        except NotImplementedError:
            if isinstance(other, Vector):
                return Point(self.x + other.x, self.y + other.y)
            raise NotImplementedError

    def __sub__(self, other: list | tuple | Vector | Point):
        """
        Performs subtraction operation with different types of objects including `Vector` 
        or `Point`. Depending on the type of the `other` object, the function computes a 
        `Point` or `Vector` resulting from the subtraction. If the subtraction operation 
        for the given `other` type is not implemented, an exception is raised.

        :param other: The object to subtract. Can be of types `list`, `tuple`, `Vector`, 
           or `Point`.
        :return: A `Point` if `other` is a `Vector`, or a `Vector` if `other` is a `Point`.
        :raises NotImplementedError: If the subtraction operation with the given object type 
           is not supported.
        """
        try:
            return super().__sub__(other)
        except NotImplementedError:
            if isinstance(other, Vector):
                return Point(self.x - other.x, self.y - other.y)
            if isinstance(other, Point):
                return Vector(self.x - other.x, self.y - other.y)
            raise NotImplementedError

    def to_vector(self):
        """
        Converts the x and y attributes of the instance into a Vector object.

        :return: A new instance of the Vector class initialized with the x and y 
                 attributes from the current object.
        :rtype: Vector
        """
        return Vector(self.x, self.y)

    @classmethod
    def bottom_left(cls, points: list['Point']) -> 'Point':
        """
        Finds the bottom-left point among a list of points. 
        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, the bottom-left point is determined by the minimum x-coordinate and
            the maximum y-coordinate.

        :param points: A list of `Point` objects to evaluate. Each `Point` in the list 
            should have defined x and y coordinates.
        :return: A new `Point` object that represents the bottom-left point from the 
            provided list.
        """
        return Point(x=min(points, key=lambda pt: pt.x).x, y=max(points, key=lambda pt: pt.y).y)

    @classmethod
    def top_right(cls, points: list['Point']) -> 'Point':
        """
        Finds the top-right point among a list of points. 
        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, the top-right point is determined by the maximum x-coordinate and
            the minimum y-coordinate.

        :param points: A list of `Point` objects to evaluate. Each `Point` in the list 
            should have defined x and y coordinates.
        :return: A new `Point` object that represents the top-right point from the 
            provided list.
        """
        return Point(x=max(points, key=lambda pt: pt.x).x, y=min(points, key=lambda pt: pt.y).y)

    @classmethod
    def bottom_right(cls, points: list['Point']) -> 'Point':
        """
        Finds the bottom-right point among a list of points. 
        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, the bottom-right point is determined by the maximum x-coordinate and
            the maximum y-coordinate.

        :param points: A list of `Point` objects to evaluate. Each `Point` in the list 
            should have defined x and y coordinates.
        :return: A new `Point` object that represents the bottom-right point from the 
            provided list.
        """
        return Point(x=max(points, key=lambda pt: pt.x).x, y=max(points, key=lambda pt: pt.y).y)

    @classmethod
    def top_left(cls, points: list['Point']) -> 'Point':
        """
        Finds the top-left point among a list of points. 
        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, the top-left point is determined by the minimum x-coordinate and
            the minimum y-coordinate.

        :param points: A list of `Point` objects to evaluate. Each `Point` in the list 
            should have defined x and y coordinates.
        :return: A new `Point` object that represents the top-left point from the 
            provided list.
        """
        return Point(x=min(points, key=lambda pt: pt.x).x, y=min(points, key=lambda pt: pt.y).y)

    @classmethod
    def center(cls, points: list['Point'], method: Literal["bbox", "barycenter"] = "bbox"):
        """
        Calculates the center of a group of points on a 2D plane using the specified method.

        The center of the points can be calculated either based on the bounding box or the barycenter method.
        The bounding box method determines the center by averaging the top-left and bottom-right corners
        of the points' bounding box. The barycenter method calculates the center by averaging the x and y 
        coordinates of the points.

        :param points: A list of `Point` objects for which the center is to be calculated. It must contain
                       at least one point.
        :type points: list[Point]
        :param method: The method to use for calculating the center. It accepts either "bbox" (bounding box)
                       to calculate center based on bounding box corners, or "barycenter" to compute the
                       average of all points' coordinates. Defaults to "bbox".
        :type method: Literal["bbox", "barycenter"]
        :return: A new instance of the calling class that represents the calculated center.
        :rtype: cls
        :raises ValueError: If the list `points` is empty or if an unknown method is provided.
        """
        if not points:
            raise ValueError("points list cannot be empty")
        if method == "bbox":
            TL = cls.top_left(points)
            BR = cls.bottom_right(points)
            return cls((TL.x + BR.x) / 2, (TL.y + BR.y) / 2)
        elif method == "barycenter":
            x_mean = sum(p.x for p in points) / len(points)
            y_mean = sum(p.y for p in points) / len(points)
            return cls(x_mean, y_mean)
        else:
            raise ValueError(f"Unknown method: {method}")

    @classmethod
    def interpolate(cls, point1: Point, point2: Point, t: float):
        """
        Interpolates between two points using a parameter `t`.

        This function calculates a point along the line connecting
        `point1` and `point2` according to the weight `t`. The parameter
        `t` determines the relative position between the points.
        Values of `t` within [0, 1] produce points on the segment
        [point1, point2], while values outside this range yield points
        that lie beyond the segment, along the same line.

        :param point1: The starting point for interpolation.
        :type point1: Point
        :param point2: The end point for interpolation.
        :type point2: Point
        :param t: The interpolation factor. Should be between 0 and 1,
            where 0 returns `point1`, and 1 returns `point2`.
        :type t: float
        :return: The interpolated point.
        :rtype: Point
        """
        return point1 + t * (point2 - point1)

    @classmethod
    def bottom(cls, points: list['Point']):
        """
        Determines the bottom center point from a list of points by calculating 
        the bottom-left and bottom-right points and then finding the center point 
        between them.

        :param points: A list of 'Point' instances representing a set of 
            points in a 2D space.
        :type points: list[Point]
        :return: Returns a single 'Point' instance representing the bottom-center 
            point derived from the given input points.
        :rtype: Point
        """
        BL = cls.bottom_left(points)
        BR = cls.bottom_right(points)
        return cls.center([BL, BR])

    @classmethod
    def top(cls, points: list['Point']):
        """
        Determines the top center point from a list of points by calculating 
        the top-left and top-right points and then finding the center point 
        between them.

        :param points: A list of 'Point' instances representing a set of 
            points in a 2D space.
        :type points: list[Point]
        :return: Returns a single 'Point' instance representing the top-center 
            point derived from the given input points.
        :rtype: Point
        """
        TL = cls.top_left(points)
        TR = cls.top_right(points)
        return cls.interpolate(TL, TR, 0.5)

    @classmethod
    def right(cls, points: list['Point']):
        """
        Determines the right center point from a list of points by calculating 
        the top-right and bottom-right points and then finding the center point 
        between them.

        :param points: A list of 'Point' instances representing a set of 
            points in a 2D space.
        :type points: list[Point]
        :return: Returns a single 'Point' instance representing the right-center 
            point derived from the given input points.
        :rtype: Point
        """
        TR = cls.top_right(points)
        BR = cls.bottom_right(points)
        return cls.interpolate(TR, BR, 0.5)

    @classmethod
    def left(cls, points: list['Point']):
        """
        Determines the left center point from a list of points by calculating 
        the top-left and bottom-left points and then finding the center point 
        between them.

        :param points: A list of 'Point' instances representing a set of 
            points in a 2D space.
        :type points: list[Point]
        :return: Returns a single 'Point' instance representing the left-center 
            point derived from the given input points.
        :rtype: Point
        """
        TL = cls.top_left(points)
        BL = cls.bottom_left(points)
        return cls.interpolate(TL, BL, 0.5)

    def rotate(self, angle, center: 'Point' = None, degrees: bool = False) -> 'Point':
        """
        Rotates the point around a given center point by a specified angle.

        This function allows the point to be rotated either in radians or
        degrees. If the center point is not provided, the point will be rotated
        around the origin. The actual rotation is handled by the internal
        rotation logic of the vector.

        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, the reference frame is indirect. Consequently, the
            rotation performed here corresponds to the opposite direction
            of a rotation in a standard (direct) Cartesian coordinate system.

        :param angle: The angle to rotate the point. The interpretation (radians
            or degrees) is determined by the `degrees` parameter.
        :param center: The center point around which the rotation occurs. If
            None, the rotation occurs around the origin.
        :param degrees: Whether the angle is provided in degrees. By default,
            the angle is interpreted in radians.
        :return: A new point that is the result of the rotation.
        :rtype: Point
        """
        center = center or Point(0, 0)
        vec = self - center
        vec = vec.rotate(angle, degrees)
        return center + vec

    @classmethod
    def vertical_symmetry(cls, point: 'Point', x_mirror: float | int):
        """
        Computes the vertical symmetry of a given `Point` around a specified x-axis mirror
        line. The method creates and returns a new `Point` that is the symmetrical counterpart
        of the input `Point`.

        :param point: The `Point` instance to find the vertical symmetry for.
        :type point: Point
        :param x_mirror: The x-coordinate of the vertical axis of symmetry.
        :type x_mirror: float | int
        :return: A new `Point` instance that is the vertical symmetrical counterpart of
                 the input `point` with respect to the specified x-axis mirror line.
        :rtype: Point
        """
        return cls(2 * x_mirror - point.x, point.y)

    @classmethod
    def horizontal_symmetry(cls, point: 'Point', y_mirror: float | int):
        """
        Computes the horizontal symmetry of a given `Point` around a specified y-axis mirror
        line. The method creates and returns a new `Point` that is the symmetrical counterpart
        of the input `Point`.

        :param point: The `Point` instance to find the horizontal symmetry for.
        :type point: Point
        :param y_mirror: The x-coordinate of the horizontal axis of symmetry.
        :type y_mirror: float | int
        :return: A new `Point` instance that is the horizontal symmetrical counterpart of
                 the input `point` with respect to the specified y-axis mirror line.
        :rtype: Point
        """
        return cls(point.x, 2 * y_mirror - point.y)


class Arc:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.p1: Point = p1
        self.p2: Point = p2
        self.p3: Point = p3
        self._check_validity()

    def _check_validity(self):
        v12 = (self.p2 - self.p1)
        v23 = (self.p3 - self.p2)
        v31 = (self.p1 - self.p3)
        if any((v12.norm <= 1e-10,
                v31.norm <= 1e-10,
                v23.norm <= 1e-10)):
            raise ValueError("The three points must be distinct")
        if abs(v12 ^ v23) <= 1e-10:
            raise ValueError("The three points must not be aligned")

    def __repr__(self):
        return f"Arc({self.p1}, {self.p2}, {self.p3})"

    @property
    def chord(self):
        return (self.p3 - self.p1).norm

    @property
    def sagitta(self):
        return (Point.center([self.p1, self.p3]) - self.p2).norm

    @property
    def radius(self):
        if self.sagitta == 0:
            return self.chord
        return self.sagitta / 2 + self.chord ** 2 / (8 * self.sagitta)

    @property
    def center(self):
        if self.sagitta == 0:
            if self.chord == 0:
                return self.p1
            else:
                raise ValueError("Arc is degenerate")
        return self.p2 + (Point.center([self.p1, self.p3]) - self.p2).unit() * self.radius

    @property
    def angle(self):
        try:
            c = self.center
            return Vector.angle(self.p1 - c, self.p3 - c)
        except ValueError:
            return 0

    @property
    def length(self):
        if self.sagitta == 0:
            return self.chord
        return self.radius * abs(self.angle)

    @classmethod
    def from_center_radius(cls, center: Point, radius: float, angle1: float, angle2: float):
        """
        Construct an arc from a center point, radius, and two angles.

        The arc is drawn from angle1 to angle2 in the counterclockwise direction.
        The complementary arc (from angle2 to angle1) corresponds to the remaining part of the circle.

        :param center: The center point of the arc
        :param radius: The radius of the arc
        :param angle1: The starting angle in radians
        :param angle2: The ending angle in radians
        :return: An arc with the given properties
        """

        p1 = center + Vector(radius * math.cos(angle1), -radius * math.sin(angle1))
        p3 = center + Vector(radius * math.cos(angle2), -radius * math.sin(angle2))

        # Calculate middle point using the average angle
        if angle2 < angle1:
            angle2 += 2 * math.pi
        mid_angle = (angle1 + angle2) / 2
        p2 = center + Vector(radius * math.cos(mid_angle), -radius * math.sin(mid_angle))

        return cls(p1, p2, p3)

    @classmethod
    def from_vectors(cls, p: Point, v1: Vector, v3: Vector, s: float):
        """
        Constructs an arc from a reference point, two vectors, and a length.

        The arc is defined by three points:
            - `p1`: The start point, calculated as `p + s * unit(v1)`.
            - `p3`: The end point, calculated as `p + s * unit(v2)`.
            - `p2`: The midpoint of the arc, calculated based on the angle between `v1` and `v3`.

        Note: this will fail if:
            - the angle between `v1` and `v3` is π, the points `p1`, `p2`, and `p3` will be collinear
            - the angle between `v1` and `v3` is 0, the points `p1`, `p2`, and `p3` will coincide

        :param p: The reference point from which the arc is constructed.
        :type p: Point
        :param v1: The direction vector from `p` to the start point `p1`.
        :type v1: Vector
        :param v3: The direction vector from `p` to the end point `p3`.
        :type v3: Vector
        :param s: The scalar length used to scale the unit vectors for `p1` and `p3`.
        :type s: float
        :return: A new instance of the class constructed from the computed points `p1`,
            `p2`, and `p3`. Note that this will fail if the computed points become
            collinear (that is when the angle `alpha` equals 0 or π) or if either vector is a zero vector.
        :rtype: <class>
        :raises ZeroDivisionError: If either `v1` or `v3` is a zero vector (cannot compute unit vector).
        :raises ZeroDivisionError: If the angle between `v1` and `v2` is π (180 degrees) (cannot compute unit vector).
        :raises ValueError: If the angle between `v1` and `v2` is 0, resulting in collinear points.
        """
        u1 = v1.unit()  # This will fail if v1 is a zero vector
        u3 = v3.unit()  # This will fail if v3 is a zero vector
        u2 = (u1 + u3).unit()  # This will fail if alpha = π
        p1 = p + u1 * s
        p3 = p + u3 * s
        alpha = abs(Vector.angle(u1, u3)) / 2
        p2 = p + s * math.cos(alpha) / (1 + math.sin(alpha)) * u2
        return cls(p1, p2, p3)  # if alpha = 0, this will fail (p1, p2, p3 aligned)

    @staticmethod
    def radius_from_vectors(v1: Vector, v3: Vector, s: float) -> float:
        radius = s / math.tan(abs(Vector.angle(v1, v3)) / 2)
        return radius

    @staticmethod
    def s_from_vectors(v1: Vector, v3: Vector, radius: float) -> float:
        s = radius * math.tan(abs(Vector.angle(v1, v3)) / 2)
        return s

    @staticmethod
    def curvature_from_vectors(v1: Vector, v3: Vector, s: float) -> float:
        return math.tan(abs(Vector.angle(v1, v3)) / 2) / s


class Margins:
    def __init__(self, left: float, right: float, top: float, bottom: float):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def __repr__(self):
        return f"Margins(left={self.left}, right={self.right}, top={self.top}, bottom={self.bottom})"


class Polygon:
    def __init__(self, points: list[Point] = None):
        self._points = points if points else []

    @property
    def points(self) -> list[Point]:
        """
        Property that returns the list of the vertices of the polygon.

        :return: The value of points
        :rtype: Any
        """
        return self._points

    @points.setter
    def points(self, points: list[Point]):
        """
        Sets the list of vertices of the polygon.
        """
        self._points = points

    def add_point(self, point: Point):
        """
        Adds a vertex to the internal collection.

        :param point: A single instance of `Point` to be added to the
            internal list.
        :type point: Point
        :return: None
        """
        self._points.append(point)

    def add_points(self, points: list[Point]):
        """
        Extends the list of the polygon vertices.

        :param points: A list of Point objects to be added.
        :type points: list[Point]
        """
        self._points.extend(points)

    def remove_point(self, point: Point):
        """
        Removes the given point from the collection of points.

        This method removes a specific point from an existing collection
        of points, ensuring that the specified point is no longer part of
        the internal representation.

        :param point: The point to be removed
        :type point: Point
        :raises ValueError: If the given point is not part of the polygon's vertices.
        """
        self._points.remove(point)

    def remove_points(self, points: list[Point]):
        """
        Removes each of the points included in the list passed as an argument.

        :param points: The points to be removed
        :type points: list
        :raises ValueError: If a point is not part of the polygon's vertices.
        """
        for point in points:
            self._points.remove(point)

    def remove_all_points(self):
        """
        Removes all points (polygon's vertices) stored in the internal collection.

        This method clears the internal list of points, resetting it to an
        empty state. After calling this method, no points will remain
        stored in the collection.

        :return: None
        """
        self._points = []

    def bounding_box(self) -> Rectangle:
        """
        Returns the bounding box that encloses the points.

        :return: The rectangle bounding the points.
        :rtype: Rectangle
        """
        return Rectangle.from_points(self._points)

    def center(self, method: Literal["bbox", "barycenter"] = "bbox") -> Point:
        """
        Calculate the center of the points using the specified method.

        The method determines the way in which the center is computed for the set of
        points. The available methods are "bbox" and "barycenter":

        1. "bbox": Computes the center based on the bounding box of the points.
        2. "barycenter": Computes the center based on the average of the points.

        :param method: Specifies the method for computing the center. Must be one of
            "bbox" or "barycenter".
        :return: The center point of the points based on the specified method.
        :rtype: Point
        """
        return Point.center(self._points, method)

    def rotate(self, angle, center: Point = None, degrees: bool = False):
        """
        Rotates the polygon by the specified angle, either in degrees or radians,
        around a given center point. If no center is provided, the center
        of the bounding box (Rectangle) of the polygon is used.

        :param angle: The angle to rotate the polygon. The rotation is performed
                      in a counter-clockwise direction if the angle is positive.
                      Units are in radians unless the `degrees` parameter is set
                      to True.
        :type angle: float
        :param center: The center point around which to perform the rotation.
                       If None, the method will use the center of the polygon.
        :type center: Point or None
        :param degrees: A flag indicating whether the angle is specified in
                        degrees. If True, the angle is converted to radians.
                        Otherwise, it is assumed to be in radians.
        :type degrees: bool
        :return: None
        """
        if degrees:
            angle = math.radians(angle)
        if center is None:
            center = self.center()
        self._points = [point.rotate(angle, center) for point in self._points]

    def translate(self, vector: Vector):
        """
        Translates the coordinates of the Polygon object by a provided vector. The function adjusts
        the current position of the polygon's points using vector addition.

        :param vector: A vector representing the translation to apply.
        :type vector: Vector
        :return: None
        """
        for i, point in enumerate(self._points):
            self._points[i] = point + vector

    def scale(self, factor: float, center: Point = None):
        """
        Scales the polygon by the given factor relative to a specified center point.

        The method modifies the coordinates of the points in the polygon by scaling them 
        through multiplying their distances from the given center point by the specified 
        factor. If no center point is provided, the polygon is scaled relative to its 
        default center.

        :param factor: Scaling factor to enlarge or shrink the polygon. A factor greater 
            than 1 enlarges the polygon, less than 1 shrinks it, and equal to 1 does not 
            alter the size of the polygon.
        :type factor: float
        :param center: Optional. The center point relative to which the polygon is scaled. 
            If not provided, the default center of the polygon is used.
        :type center: Point, optional
        :return: None
        """
        if center is None:
            center = self.center()
        for i, point in enumerate(self._points):
            self._points[i] = center + (point - center) * factor

    def __repr__(self):
        return f"Polygon(points={self._points})"

    def __copy__(self):
        return Polygon(self._points)

    def __iter__(self):
        return iter(self._points)

    def __contains__(self, p: Point) -> bool:
        """
        Checks if a given point lies inside the polygon or on its edges.

        Uses the ray-casting algorithm to determine if the point is inside the polygon.
        Also returns True if the point lies exactly on any of the polygon's edges.

        :param p: The point to check.
        :type p: Point
        :return: True if the point is inside the polygon or on its edges, False otherwise.
        :rtype: bool
        :raises ValueError: If `p` is not a Point instance.
        """
        if not isinstance(p, Point):
            raise ValueError(f"p must be a Point, not {type(p)}")
        assert isinstance(p, Point)

        def on_segment(a: Point, b: Point, c: Point) -> bool:
            """Returns True if point c lies on the segment [ab]"""
            # Checks collinearity and bounds
            cross = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
            if abs(cross) > 1e-10:  # tolérance flottant
                return False
            dot = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)
            if dot < 0:
                return False
            squared_len = (b.x - a.x) ** 2 + (b.y - a.y) ** 2
            return dot <= squared_len

        n = len(self._points)
        inside = False
        j = n - 1
        for i in range(n):
            pi = self._points[i]
            pj = self._points[j]

            # Checks if the point is on the edge
            if on_segment(pi, pj, p):
                return True

            # Standard ray-casting
            if ((pi.y > p.y) != (pj.y > p.y)) and \
                    (p.x < (pj.x - pi.x) * (p.y - pi.y) / (pj.y - pi.y) + pi.x):
                inside = not inside
            j = i
        return inside


class Rectangle:
    """
    Represents a rectangle defined by its corner points.

    This class provides properties to access and manipulate the corner points of a
    rectangle: top-left, top-right, bottom-left, and bottom-right. Additionally,
    it allows access to derived properties such as the center, width, height, and
    side midpoints of the rectangle. The rectangle adjusts its corner points based
    on the specified inputs while conforming to KiCad's coordinate system where
    the Y-axis is oriented downward.

    :ivar points: A list of corner points of the rectangle provided in the following
        order: top-left, top-right, bottom-right, and bottom-left.
    :type points: list
    :ivar center: The center point of the rectangle.
    :type center: Point
    :ivar width: The width of the rectangle, derived from the difference between
        the x-coordinates of specific corner points.
    :type width: float
    :ivar height: The height of the rectangle, derived from the difference between
        the y-coordinates of specific corner points.
    :type height: float
    :ivar bottom: The center point of the rectangle's bottom side.
    :type bottom: Point
    :ivar top: The center point of the rectangle's top side.
    :type top: Point
    :ivar right: The center point of the rectangle's right side.
    :type right: Point
    :ivar left: The center point of the rectangle's left side.
    :type left: Point
    """

    def __init__(self, point1: Point, point2: Point):
        self._digest_points(point1, point2)

    def _digest_points(self, point1: Point, point2: Point):
        """
        Processes the given points to determine and assign the top-left,
        top-right, bottom-right, and bottom-left points based on their
        relative positions.

        :param point1: First point used for determining the corner``` positionspython.

        :type"""
        self._TL = Point.top_left([point1, point2])
        self._TR = Point.top_right([point1, point2])
        self._BR = Point.bottom_right([point1, point2])
        self._BL = Point.bottom_left([point1, point2])

    @property
    def top_left(self) -> Point:
        """
        Returns the top-left corner point of the rectangle.

        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, this method returns the corner with the minimum Y value and minimum X value.

        :return: A `Point` object representing the top-left corner.
        :rtype: Point
        """
        return self._TL

    @property
    def top_right(self) -> Point:
        """
        Returns the top-right corner point of the rectangle.

        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, this method returns the corner with the minimum Y value and maximum X value.

        :return: A `Point` object representing the top-right corner.
        :rtype: Point
        """
        return self._TR

    @property
    def bottom_right(self) -> Point:
        """
        Returns the bottom-right corner point of the rectangle.

        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, this method returns the corner with the maximum Y value and maximum X value.

        :return: A `Point` object representing the bottom-right corner.
        :rtype: Point
        """
        return self._BR

    @property
    def bottom_left(self) -> Point:
        """
        Returns the bottom-left corner point of the rectangle.

        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, this method returns the corner with the maximum Y value and minimum X value.

        :return: A `Point` object representing the bottom-left corner.
        :rtype: Point
        """
        return self._BL

    @top_left.setter
    def top_left(self, value: Point):
        """
        Sets the top-left point of the rectangle.

        Updates the rectangle from two points:
        the current bottom-right point and the new top-left point.

        Warning: the new top-left point may become any of the four corners,
        depending on its position relative to the current bottom-right point.

        :param value: The new top-left point.
        :type value: Point
        """
        self._digest_points(value, self._BR)

    @top_right.setter
    def top_right(self, value: Point):
        """
        Sets the bottom-right point of the rectangle.

        Updates the rectangle from two points:
        the current top-left point and the new bottom-right point.

        Warning: the new bottom-right point may become any of the four corners,
        depending on its position relative to the current top-left point.

        :param value: The new bottom-right point.
        :type value: Point
        """
        self._digest_points(value, self._BL)

    @bottom_right.setter
    def bottom_right(self, value: Point):
        """
        Sets the top-right point of the rectangle.

        Updates the rectangle from two points:
        the current bottom-left point and the new top-right point.

        Warning: the new top-right point may become any of the four corners,
        depending on its position relative to the current bottom-left point.

        :param value: The new top-right point.
        :type value: Point
        """
        self._digest_points(value, self._TL)

    @bottom_left.setter
    def bottom_left(self, value: Point):
        """
        Sets the bottom-left point of the rectangle.

        Updates the rectangle from two points:
        the current top-right point and the new bottom-left point.

        Warning: the new bottom-left point may become any of the four corners,
        depending on its position relative to the current top-right point.

        :param value: The new bottom-left point.
        :type value: Point
        """
        self._digest_points(value, self._TR)

    @property
    def points(self):
        """
        Get the corner points of a rectangular area.

        This property retrieves a list of the rectangular area's corner points,
        provided in the following order: top left, top right, bottom right,
        and bottom left.

        :return: A list of corner points of the rectangle in a sequential order.
        :rtype: list
        """
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]

    @property
    def center(self):
        """
        Returns the center point of the rectangle.

        :return: A `Point` object representing the center point of the rectangle.
        :rtype: Point
        :return:
        """
        return Point.center(self.points)

    @center.setter
    def center(self, center: Point):
        """
        Sets the center point of the rectangle.

        Translates the rectangle to the given center point,
        preserving its shape and dimensions.

        :param center: The new center point.
        :type center: Point
        """
        self.translate(center - self.center)

    @property
    def width(self):
        """
        Calculates and returns the width of a rectangle.

        The width is derived from the difference between the x-coordinates of the
        top-right and bottom-left corners.

        :returns: The width of the rectangle.
        :rtype: float
        """
        return self.top_right.x - self.bottom_left.x

    @property
    def height(self):
        """
        Calculates and returns the height of a rectangle.

        The height is derived from the difference between the y-coordinates of the
        top-right and bottom-left corners.

        :returns: The height of the rectangle.
        :rtype: float
        """
        return self.bottom_left.y - self.top_right.y

    @property
    def bottom(self) -> Point:
        """
        Gets the bottom center point based on the bottom left and bottom right points.

        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, this method returns the center point of the rectangle 
            side with the maximum Y value.

        :return: The center point between the bottom left and bottom right points.
        :rtype: Point
        """
        return Point.bottom(self.points)

    @property
    def top(self) -> Point:
        """
        Gets the top center point based on the top left and top right points.

        Note:
            Since KiCad uses a coordinate system with the Y-axis oriented
            downward, this method returns the center point of the rectangle 
            side with the minimum Y value.

        :return: The center point between the top left and top right points.
        :rtype: Point
        """
        return Point.top(self.points)

    @property
    def right(self) -> Point:
        """
        Gets the right center point based on the top right and bottom right points.

        :return: The center point between the top right and bottom right points.
        :rtype: Point
        """
        return Point.right(self.points)

    @property
    def left(self) -> Point:
        """
        Gets the left center point based on the top left and bottom left points.

        :return: The center point between the top left and bottom left points.
        :rtype: Point
        """
        return Point.left(self.points)

    def to_polygon(self) -> Polygon:
        """
        Create a new Polygon object from the Rectangle object.

        This method utilizes the `Polygon` class from the relevant library to create
        a polygonal representation of the existing points stored in the instance.

        :return: A `Polygon` object created using the instance's points.
        :rtype: Polygon
        """
        return Polygon(self.points)

    def translate(self, vector: Vector):
        """
        Translates the coordinates of the Rectangle obect by a provided vector. The function adjusts
        the current position of the rectangle's points using vector addition.

        :param vector: A vector representing the translation to apply.
        :type vector: Vector
        :return: None
        """
        self._digest_points(self.top_left + vector, self.bottom_right + vector)

    def add_margins(self, margin: Margins):
        """
        Expands the bounding box of this rectangle by the given margin.

        :param margin: The margin to add to the bounding box.
        :type margin: Margins
        """
        self._digest_points(self.top_left - Vector(margin.left, margin.top),
                            self.bottom_right + Vector(margin.right, margin.bottom))

    def remove_margins(self, margin: Margins):
        """
        Contracts the bounding box of this rectangle by the given margin.

        :param margin: The margin to add to the bounding box.
        :type margin: Margins
        """
        self._digest_points(self.top_left + Vector(margin.left, margin.top),
                            self.bottom_right - Vector(margin.right, margin.bottom))

    @classmethod
    def from_center(cls, center: Point, width: float, height: float):
        """
        Creates a new instance of the class by specifying the center point and dimensions.

        Constructs an instance of the class with the given center point, width, and height.
        The center is the geometric center of the rectangle, and the width and height specify
        the extent of the rectangle along horizontal and vertical directions respectively.

        :param center: The center point of the rectangle.
        :type center: Point
        :param width: The width of the rectangle.
        :type width: float
        :param height: The height of the rectangle.
        :type height: float
        :return: A new instance of the class representing the rectangle.
        :rtype: cls
        """
        return cls(center - (width / 2, height / 2), center + (width / 2, height / 2))

    @classmethod
    def from_points(cls, points: list[Point]):
        """
        Creates a new instance of the class using a list of points. The method
        derives the top-left and bottom-right points from the given list and
        uses them to instantiate the class.

        :param points: A list of `Point` objects to determine the defining corners.
        :type points: list[Point]
        :return: An instance of the class created from the provided points.
        :rtype: cls
        """
        return cls(Point.top_left(points), Point.bottom_right(points))

    @classmethod
    def from_x_y_limits(cls, x_limits: tuple[float, float], y_limits: tuple[float, float]):
        """
        Creates a new instance of the class using the specified x and y axis
        limits. This factory method helps to define the spatial bounds of the
        object by interpreting the specified x and y limits as the minimum and
        maximum points of a rectangular region.

        :param x_limits: A tuple containing the minimum and maximum values
            for the x-axis.
        :param y_limits: A tuple containing the minimum and maximum values
            for the y-axis.
        :return: A new instance of the class initialized with points representing
            the spatial bounds.
        """
        return cls(Point(min(x_limits), min(y_limits)), Point(max(x_limits), max(y_limits)))

    def __contains__(self, item):
        """
        Checks if a given Point is contained within the defined rectangular area.

        This method determines whether the specified Point lies within the bounds of
        the rectangle defined by its top-left and bottom-right corners.

        :param item: The Point to check for containment within the rectangle.
        :type item: Point
        :return: True if the Point lies within the bounds of the rectangle,
                 False otherwise.
        :rtype: bool
        """
        if not isinstance(item, Point):
            return False
        assert isinstance(item, Point)
        return self.top_left.x <= item.x <= self.bottom_right.x and self.top_left.y <= item.y <= self.bottom_right.y

    def __repr__(self):
        return f"Rectangle(TL({self.top_left.x},{self.top_left.y}) BR({self.bottom_right.x},{self.bottom_right.y}))"

    def __copy__(self):
        return Rectangle(self.top_left, self.bottom_right)


def bezier(geo: list[Coordinate], steps: int):
    """
    Computes a list of points approximating a Bezier curve based on the given control points 
    or vectors.

    The function calculates the curve following the Bezier formula using the provided control 
    geometry and divides it into the specified number of steps.

    :param geo: A list of control points or vectors defining the Bezier curve.
    :param steps: The number of steps or divisions for approximating the curve. 
                  Must be at least 2.
    :return: A list of points approximating the calculated Bézier curve.

    :raises ValueError: If the geometry list is empty, or if the geometry is not a list 
                        of points or vectors.
    """
    if not len(geo):
        raise ValueError(f"geometry cannot be empty")
    if steps < 2:
        steps = 2
    if isinstance(geo[0], Point):
        vectors = [pt - Point(0, 0) for pt in geo]
    elif isinstance(geo[0], Vector):
        vectors = geo
    else:
        raise ValueError("""geometry must be a list of points or vectors""")

    m = len(vectors) - 1
    points = []
    for s in range(steps):
        t = s / (steps - 1)
        points.append(sum([vec * (bernstein(i, m, t)) for i, vec in enumerate(vectors)], Point(0, 0)))
    return points


def intersection(p1: Point, v1: Vector, p2: Point, v2: Vector) -> Point:
    """
    Compute the intersection point between two lines in 2D.

    The first line passes through point point1 with direction vector u1.
    The second line passes through point point2 with direction vector u2.
    The intersection point P satisfies: point1 + t * u1 = point2 + s * u2.

    :param p1: A point on the first line.
    :type p1: Point
    :param v1: Direction vector of the first line.
    :type v1: Vector
    :param p2: A point on the second line.
    :type p2: Point
    :param v2: Direction vector of the second line.
    :type v2: Vector
    :return: The intersection point between the two lines.
    :rtype: Point
    :raises ZeroDivisionError: If the direction vectors are parallel (no unique intersection).
    """
    t = (p2 - p1) ^ v2 / (v1 ^ v2)
    return p1 + v1 * t


def same_side_of_line(point1: Point, point2: Point, line_point: Point, line_dir: Vector) -> bool:
    """
    Check if points p1 and p2 are on the same side of the line defined by line_point and line_dir.

    :param point1: First point
    :type point1: Point
    :param point2: Second point
    :type point2: Point
    :param line_point: A point on the line
    :type line_point: Point
    :param line_dir: Direction vector of the line
    :type line_dir: Vector
    :return: True if point1 and point2 are on the same side (or on the line), False otherwise
    :rtype: bool
    """
    v1 = point1 - line_point
    v2 = point2 - line_point

    side1 = v1 ^ line_dir
    side2 = v2 ^ line_dir

    return side1 * side2 >= 0


def find_equidistant_parallel_track_point(p1a: Point, p2a: Point, p3a: Point, p1b: Point) -> Point:
    """
    Compute the second point of track B such that its segments are parallel
    and equidistant to the corresponding segments of track A.

    The first segment of track B (P1B -> P2B) will be parallel to P1A -> P2A,
    and the second segment of track B (P2B -> next point) will be parallel
    to P2A -> P3A.

    The point P2B is chosen as the intersection of two lines:
    - one passing through P1B in the direction of the first segment of track A,
    - one passing through P2A in the direction of (P2A->P3A) - (P1A->P2A).

    This ensures that P2B is equidistant from the directions of both segments [P1A, P2A] and [P2A, P3A].

    :param p1a: First point of track A.
    :type p1a: Point
    :param p2a: Second point of track A.
    :type p2a: Point
    :param p3a: Third point of track A.
    :type p3a: Point
    :param p1b: First point of track B.
    :type p1b: Point
    :return: Second point of track B (P2B) such that the segments are parallel
             to track A and P2B is equidistant from the directions of the two segments.
    :rtype: Point
    """
    v1a = (p2a - p1a).unit()  # Direction of the first segment of track A
    v2a = (p3a - p2a).unit()  # Direction of the second segment of track A
    if abs(v1a ^ v2a) <= 1e-8:  # p1, p2, p3 aligned
        return intersection(p1b, v1a, p2a, v1a.rotate(math.pi / 2))
    elif same_side_of_line(p1a, p1b, p2a, v2a - v1a):
        return intersection(p1b, v1a, p2a, v2a - v1a)
    else:
        raise ValueError("Points p1a and p1b are not on the same side of the line of the bisector.")


def polygon_point_grid(area: Polygon, x_pitch: float = 0, y_pitch: float = 0, exclusion_polygons: list[Polygon] = None,
                       origin: Point = None, checkered: bool = False) -> list[Point]:
    """
    Generates a grid of points within a given polygon. This function calculates grid points
    based on provided pitch values (x and y directions), with optional exclusion zones,
    an origin point, and a parameter to skip certain grid points in a checkered pattern.

    :param area: The polygon within which the grid points will be generated.
    :param x_pitch: The horizontal spacing between grid points.
    :param y_pitch: The vertical spacing between grid points.
    :param exclusion_polygons: A list of polygons representing areas to exclude from the grid.
        Defaults to None, meaning no exclusions.
    :param origin: The origin point from where the grid is initiated. Defaults to None,
        which calculates an origin based on the top-left corner of the polygon's bounding box
        and aligns it to the grid pitch.
    :param checkered: A boolean flag that, if set to True, skips every alternate point in a
        checkered pattern. This provides a sparse grid. Defaults to False.
    :return: A list of points forming the grid within the polygon and adhering to all constraints.
    """
    bb = area.bounding_box()
    if origin is None:
        origin = bb.top_left
    else:
        x_offset = x_pitch * ((origin.x - bb.top_left.x) // x_pitch) if x_pitch > 0 else 0
        y_offset = y_pitch * ((origin.y - bb.top_left.y) // y_pitch) if y_pitch > 0 else 0
        origin = Point(origin.x - x_offset, origin.y - y_offset)
    column_count = int((bb.bottom_right.x - origin.x) / x_pitch) + 1 if x_pitch > 0 else 1
    row_count = int((bb.bottom_right.y - origin.y) / y_pitch) + 1 if y_pitch > 0 else 1

    points: list[Point] = list()
    for c in range(column_count):
        for r in range(row_count):
            if checkered and not (r + c) % 2:
                continue
            pt = origin + Vector(x_pitch * c, y_pitch * r)
            if not pt in area:
                continue
            if exclusion_polygons and any((pt in polygon for polygon in exclusion_polygons)):
                continue
            points.append(pt)
    return points
