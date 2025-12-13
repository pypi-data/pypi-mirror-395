from typing import overload, Any, List, Optional, Tuple
from .. import Vec3d

class Plane:
    """
    A class representing an infinite plane in 3D space.

    Attributes:
        normal (Vec3d): The normal vector of the plane.
        distance (float): The distance of the plane from the origin along its normal.
    """
    def __init__(self, normal: "Vec3d", distance: float) -> None:
        """
        Creates a new Plane instance.

        :param normal: The normal vector of the plane.
        :param distance: The distance of the plane from the origin.
        """
        ...

    @staticmethod
    def from_point(normal: "Vec3d", point: "Vec3d") -> "Plane":
        """
        Creates a new plane from a normal vector and a point on the plane.

        :param normal: The normal vector of the plane.
        :param point: A point on the plane.
        :return: A new Plane instance.
        """
        ...

    @staticmethod
    def xy() -> "Plane":
        """
        Returns a plane representing the XY-plane (normal along the Z-axis).

        :return: The XY-plane.
        """
        ...

    @staticmethod
    def xz() -> "Plane":
        """
        Returns a plane representing the XZ-plane (normal along the Y-axis).

        :return: The XZ-plane.
        """
        ...

    @staticmethod
    def yz() -> "Plane":
        """
        Returns a plane representing the YZ-plane (normal along the X-axis).

        :return: The YZ-plane.
        """
        ...

    @staticmethod
    def from_points(point1: "Vec3d", point2: "Vec3d", point3: "Vec3d") -> "Plane":
        """
        Creates a new plane from three non-collinear points.

        :param point1: The first point on the plane.
        :param point2: The second point on the plane.
        :param point3: The third point on the plane.
        :return: A new Plane instance.
        """
        ...

    @property
    def normal(self) -> "Vec3d":
        """
        Get or set the normal vector of the plane.

        :return: The normal vector as a Vec3d instance.
        """
        ...

    @normal.setter
    def normal(self, value: "Vec3d") -> None:
        ...

    @property
    def distance(self) -> float:
        """
        Get or set the distance of the plane from the origin.

        :return: The distance value as a float.
        """
        ...

    @distance.setter
    def distance(self, value: float) -> None:
        ...

    def distance_to_point(self, point: "Vec3d") -> float:
        """
        Calculates the signed distance from the plane to a point.

        :param point: The point to measure the distance to.
        :return: The distance as a float.
        """
        ...

    def contains_point(self, point: "Vec3d") -> bool:
        """
        Checks if a point lies on the plane.

        :param point: The point to check.
        :return: True if the point is on the plane, False otherwise.
        """
        ...


class Circle:
    """
    A class representing a circle in 3D space.

    Attributes:
        center (Vec3d): The center point of the circle.
        radius (float): The radius of the circle.
        normal (Vec3d): The normal vector of the circle's plane.
    """
    def __init__(self, center: "Vec3d", radius: float, normal: "Vec3d") -> None:
        """
        Creates a new Circle instance.

        :param center: The center point of the circle.
        :param radius: The radius of the circle.
        :param normal: The normal vector of the circle's plane.
        """
        ...

    @staticmethod
    def none() -> "Circle":
        """
        Creates an 'empty' Circle instance with all values zeroed

        :return: The empty Circle instance.
        """
        ...

    @property
    def center(self) -> "Vec3d":
        """
        Get or set the center point of the circle.

        :return: The center point as a Vec3d instance.
        """
        ...

    @center.setter
    def center(self, value: "Vec3d") -> None:
        ...

    @property
    def normal(self) -> "Vec3d":
        """
        Get or set the normal vector of the circle's plane.

        :return: The normal vector as a Vec3d instance.
        """
        ...

    @normal.setter
    def normal(self, value: "Vec3d") -> None:
        ...

    @property
    def radius(self) -> float:
        """
        Get or set the radius of the circle.

        :return: The radius value as a float.
        """
        ...

    @radius.setter
    def radius(self, value: float) -> None:
        ...

    @property
    def area(self) -> float:
        """
        Get the area of the circle.

        :return: The area as a float.
        """
        ...

    def get_plane(self) -> "Plane":
        """
        Returns the plane on which the circle lies.

        :return: A Plane instance.
        """
        ...

    def in_same_plane(self, other: "Circle") -> bool:
        """
        Checks if this circle lies in the same plane as another.

        :param other: The other Circle instance.
        :return: True if both circles are in the same plane, False otherwise.
        """
        ...

    def is_degenerate(self) -> bool:
        """
        Checks if the circle is degenerate (i.e., has a radius of zero).

        :return: True if the radius is zero, False otherwise.
        """
        ...

    def __eq__(self, other: "Circle") -> bool:
        """
        Checks if this circle is equal to another.

        :param other: The other Circle instance.
        :return: True if both circles have the same center, radius, and normal, False otherwise.
        """
        ...

# --- Intersection Functions ---

def circle_circle(circle1: "Circle", circle2: "Circle") -> Optional[Tuple["Vec3d", "Vec3d"]]:
    """
    Finds the intersection points of two circles.

    :param circle1: The first circle.
    :param circle2: The second circle.
    :return: A tuple of two Vec3d instances representing the intersection points, or None if they do not intersect.
    """
    ...

def plane_line(plane: "Plane", a: "Vec3d", b: "Vec3d") -> Optional["Vec3d"]:
    """
    Calculates the intersection point of a plane and a line defined by two points.

    :param plane: The plane.
    :param a: The first point on the line.
    :param b: The second point on the line.
    :return: The intersection point as a Vec3d instance, or None if the line is parallel to the plane.
    """
    ...

def circle_point(circle: "Circle", point: "Vec3d", inner: bool) -> bool:
    """
    Checks if a point is on the circumference or within a circle.

    :param circle: The circle to check against.
    :param point: The point to check.
    :param inner: If True, also checks for points inside the circle; otherwise, checks only the circumference.
    :return: True if the point meets the criteria, False otherwise.
    """
    ...

def circle_point_unchecked(circle: "Circle", point: "Vec3d", inner: bool) -> bool:
    """
    Checks if a point is on the circumference or within a circle without performing some checks.

    This function may have performance benefits but assumes the inputs are valid.

    :param circle: The circle to check against.
    :param point: The point to check.
    :param inner: If True, also checks for points inside the circle; otherwise, checks only the circumference.
    :return: True if the point meets the criteria, False otherwise.
    """
    ...

