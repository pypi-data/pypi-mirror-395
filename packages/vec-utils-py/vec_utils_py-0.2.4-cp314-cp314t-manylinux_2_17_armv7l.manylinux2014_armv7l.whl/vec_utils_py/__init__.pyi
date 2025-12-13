from typing import Any, Iterator, overload

class Vec3d:
    """
    A 3D vector.

    Attributes:
        x (float): The x-component of the vector.
        y (float): The y-component of the vector.
        z (float): The z-component of the vector.
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Creates a new 3D vector.

        :param x: The x-component.
        :param y: The y-component.
        :param z: The z-component.
        """
        ...

    @staticmethod
    def zero() -> "Vec3d":
        """
        Returns a new vector with all components set to 0.0.

        :return: A zero vector.
        """
        ...

    @staticmethod
    def i() -> "Vec3d":
        """
        Returns the unit vector along the x-axis (1, 0, 0).

        :return: The x-axis unit vector.
        """
        ...

    @staticmethod
    def j() -> "Vec3d":
        """
        Returns the unit vector along the y-axis (0, 1, 0).

        :return: The y-axis unit vector.
        """
        ...

    @staticmethod
    def k() -> "Vec3d":
        """
        Returns the unit vector along the z-axis (0, 0, 1).

        :return: The z-axis unit vector.
        """
        ...

    @staticmethod
    def new_from_to(from_vec: "Vec3d", to_vec: "Vec3d") -> "Vec3d":
        """
        Creates a new vector from one point to another.

        :param from_vec: The starting point.
        :param to_vec: The ending point.
        :return: The new vector from `from_vec` to `to_vec`.
        """
        ...

    @property
    def x(self) -> float:
        """
        Get or set the x-component of the vector.

        :return: The value of the x-component.
        """
        ...

    @x.setter
    def x(self, value: float) -> None: ...
    @property
    def y(self) -> float:
        """
        Get or set the y-component of the vector.

        :return: The value of the y-component.
        """
        ...

    @y.setter
    def y(self, value: float) -> None: ...
    @property
    def z(self) -> float:
        """
        Get or set the z-component of the vector.

        :return: The value of the z-component.
        """
        ...

    @z.setter
    def z(self, value: float) -> None: ...
    def to_quat(self) -> "Quat":
        """
        Converts the vector to a quaternion.
        The x, y, and z components of the vector are used as the imaginary components of the quaternion.
        The real component of the quaternion is set to 0.

        :return: The resulting quaternion.
        """
        ...

    def to_array(self) -> list[float]:
        """
        Returns the vector components as a Python list.

        :return: A list containing the x, y, and z components.
        """
        ...

    def magnitude(self) -> float:
        """
        Calculates the magnitude (length) of the vector.

        :return: The magnitude of the vector.
        """
        ...

    def is_unit(self) -> bool:
        """
        Checks if the vector is a unit vector.

        :return: True if the magnitude is within f64 epsilon of 1.0, False otherwise.
        """
        ...

    def normalize(self) -> "Vec3d":
        """
        Returns a new normalized vector.

        :return: The normalized vector.
        """
        ...

    def dot(self, other: "Vec3d") -> float:
        """
        Calculates the dot product with another vector.

        :param other: The other vector.
        :return: The dot product.
        """
        ...

    def cross(self, other: "Vec3d") -> "Vec3d":
        """
        Calculates the cross product with another vector.

        :param other: The other vector.
        :return: The resulting vector.
        """
        ...

    def angle_to(self, other: "Vec3d") -> AngleRadians:
        """
        Calculates the angle between this vector and another.

        :param other: The other vector.
        :return: The angle in radians.
        """
        ...

    @staticmethod
    def scalar_triple_product(a: "Vec3d", b: "Vec3d", c: "Vec3d") -> float:
        """
        Calculates the scalar triple product of three vectors.

        :param a: The first vector.
        :param b: The second vector.
        :param c: The third vector.
        :return: The scalar triple product.
        """
        ...

    def distance_to(self, other: "Vec3d") -> float:
        """
        Calculates the distance to another vector.

        :param other: The other vector.
        :return: The distance.
        """
        ...

    def distance_squared(self, other: "Vec3d") -> float:
        """
        Calculates the squared distance to another vector. This avoids a sqrt while being similarly useful.

        :param other: The other vector.
        :return: The distance squared.
        """
        ...

    def distance_to_line(self, a: "Vec3d", b: "Vec3d") -> float:
        """
        Calculates the distance to a line defined by two points.

        :param a: A point on the line.
        :param b: Another point on the line.
        :return: The distance to the line.
        """
        ...

    def project_onto_plane(self, normal: "Vec3d") -> "Vec3d":
        """
        Projects the vector onto a plane with a given normal.

        :param normal: The normal vector of the plane.
        :return: The projected vector.
        """
        ...

    def project_onto_line(self, line_r: "Vec3d", line_q: "Vec3d") -> "Vec3d":
        """
        Projects the vector onto a line defined by two vectors.

        :param line_r: The origin of the line.
        :param line_q: The direction vector of the line.
        :return: The projected vector.
        """
        ...

    @overload
    def __add__(self, other: "Vec3d") -> "Vec3d": ...
    @overload
    def __add__(self, other: Any) -> Any:
        """
        Adds another vector to this one.

        :param other: The vector to add.
        :return: A new vector representing the sum.
        """
        ...

    @overload
    def __sub__(self, other: "Vec3d") -> "Vec3d": ...
    @overload
    def __sub__(self, other: Any) -> Any:
        """
        Subtracts another vector from this one.

        :param other: The vector to subtract.
        :return: A new vector representing the difference.
        """
        ...

    @overload
    def __mul__(self, other: float) -> "Vec3d": ...
    @overload
    def __mul__(self, other: Any) -> Any:
        """
        Multiplies the vector by a scalar.

        :param other: The scalar to multiply by.
        :return: A new scaled vector.
        """
        ...

    @overload
    def __rmul__(self, other: float) -> "Vec3d": ...
    @overload
    def __rmul__(self, other: Any) -> Any:
        """
        Allows for scalar multiplication from the left (e.g., `2 * vector`).

        :param other: The scalar to multiply by.
        :return: A new scaled vector.
        """
        ...

    @overload
    def __truediv__(self, other: float) -> "Vec3d": ...
    @overload
    def __truediv__(self, other: Any) -> Any:
        """
        Divides the vector by a scalar.

        :param other: The scalar to divide by.
        :return: A new scaled vector.
        """
        ...

    def __neg__(self) -> "Vec3d":
        """
        Negates the vector.

        :return: The new negated vector.
        """
        ...

    def __getitem__(self, index: int) -> float:
        """
        Accesses the components of the vector by index (0, 1, 2).

        :param index: The index of the component.
        :return: The value of the component.
        :raises IndexError: If the index is out of bounds.
        """
        ...

    def __repr__(self) -> str:
        """
        Provides an official string representation of the vector.

        :return: A string like "Vec3d(x, y, z)".
        """
        ...

class Quat:
    """
    A quaternion

    Attributes:
        w (float): The w-component (scalar part) of the quaternion.
        i (float): The i-component (x part) of the quaternion.
        j (float): The j-component (y part) of the quaternion.
        k (float): The k-component (z part) of the quaternion.
    """

    def __init__(self, w: float, i: float, j: float, k: float) -> None:
        """
        Creates a new quaternion.

        :param w: The w-component.
        :param i: The i-component.
        :param j: The j-component.
        :param k: The k-component.
        """
        ...

    @staticmethod
    def identity() -> "Quat":
        """
        Returns an identity quaternion.
        i.e. a quaternion with a real component of 1 and imaginary components of 0.

        :return: An identity quaternion.
        """
        ...

    @staticmethod
    def from_axis_angle(axis: "Vec3d", angle: "AngleRadians") -> "Quat":
        """
        Creates a quaternion from an axis and an angle.
        Representing a rotation of the given angle around the given axis.
        The resulting quaternion is definitionally a unit quaternion.
        The angle is positive for a counter-clockwise rotation.

        :param axis: The axis of rotation.
        :param angle: The angle of rotation.
        :return: The new quaternion.
        """
        ...

    @property
    def w(self) -> float:
        """
        Get or set the w-component of the quaternion.

        :return: The w-component.
        """
        ...

    @w.setter
    def w(self, value: float) -> None: ...
    @property
    def i(self) -> float:
        """
        Get or set the i-component (x part) of the quaternion.

        :return: The i-component.
        """
        ...

    @i.setter
    def i(self, value: float) -> None: ...
    @property
    def j(self) -> float:
        """
        Get or set the j-component (y part) of the quaternion.

        :return: The j-component.
        """
        ...

    @j.setter
    def j(self, value: float) -> None: ...
    @property
    def k(self) -> float:
        """
        Get or set the k-component (z part) of the quaternion.

        :return: The k-component.
        """
        ...

    @k.setter
    def k(self, value: float) -> None: ...
    def conjugate(self) -> "Quat":
        """
        Returns the conjugate of the quaternion.

        :return: The conjugate quaternion.
        """
        ...

    def magnitude(self) -> float:
        """
        Calculates the magnitude of the quaternion.

        :return: The magnitude.
        """
        ...

    def normalize(self) -> "Quat":
        """
        Returns a new normalized quaternion.

        :return: The normalized quaternion.
        """
        ...

    def to_vec3d(self) -> "Vec3d":
        """
        Converts the vector part of the quaternion to a Vec3d

        :return: A Vec3d of the (i, j, k) components.
        """
        ...

    def is_unit(self) -> bool:
        """
        Checks if the quaternion is a unit quaternion.

        :return: True if the magnitude is approximately 1.0, False otherwise.
        """
        ...

    def to_axis_angle(self) -> tuple["Vec3d", "AngleRadians"]:
        """
        Converts the quaternion to an axis and an angle.

        :return: A tuple containing the axis (`Vec3d`) and angle (`AngleRadians`).
        """
        ...

    def to_rotation_matrix(self) -> list[list[float]]:
        """
        Converts the quaternion to a 3x3 rotation matrix.

        :return: A list of lists representing the matrix.
        """
        ...

    def rotate(self, v: "Vec3d") -> "Vec3d":
        """
        Rotates a vector by the quaternion.

        :param v: The vector to rotate.
        :return: The rotated vector.
        """
        ...

    def __repr__(self) -> str:
        """
        Provides an official string representation of the quaternion.

        :return: A string like "Quat(w, i, j, k)".
        """
        ...

class AngleRadians:
    """
    A class representing an angle in radians.

    Attributes:
        angle (float): The angle value in radians.
    """

    def __init__(self, angle: float) -> None:
        """
        Creates a new AngleRadians instance.

        :param angle: The initial angle value in radians.
        """
        ...

    @staticmethod
    def zero() -> "AngleRadians":
        """
        Returns a new angle with a value of 0.0 radians.

        :return: A new AngleRadians instance representing zero radians.
        """
        ...

    @staticmethod
    def pi() -> "AngleRadians":
        """
        Returns a new angle with a value of pi radians.

        :return: A new AngleRadians instance representing pi radians.
        """
        ...

    @staticmethod
    def two_pi() -> "AngleRadians":
        """
        Returns a new angle with a value of 2*pi radians.

        :return: A new AngleRadians instance representing 2*pi radians.
        """
        ...

    @staticmethod
    def half_pi() -> "AngleRadians":
        """
        Returns a new angle with a value of pi/2 radians.

        :return: A new AngleRadians instance representing pi/2 radians.
        """
        ...

    @staticmethod
    def quarter_pi() -> "AngleRadians":
        """
        Returns a new angle with a value of pi/4 radians.

        :return: A new AngleRadians instance representing pi/4 radians.
        """
        ...

    @staticmethod
    def third_pi() -> "AngleRadians":
        """
        Returns a new angle with a value of pi/3 radians.

        :return: A new AngleRadians instance representing pi/3 radians.
        """
        ...

    @staticmethod
    def sixth_pi() -> "AngleRadians":
        """
        Returns a new angle with a value of pi/6 radians.

        :return: A new AngleRadians instance representing pi/6 radians.
        """
        ...

    @property
    def angle(self) -> float:
        """
        Get or set the angle value in radians.

        :return: The angle value.
        """
        ...

    @angle.setter
    def angle(self, value: float) -> None: ...
    def to_degrees(self) -> "AngleDegrees":
        """
        Converts the angle to degrees.

        :return: The angle as an AngleDegrees instance.
        """
        ...

    def sin(self) -> float:
        """
        Calculates the sine of the angle.

        :return: The sine of the angle.
        """
        ...

    def cos(self) -> float:
        """
        Calculates the cosine of the angle.

        :return: The cosine of the angle.
        """
        ...

    def tan(self) -> float:
        """
        Calculates the tangent of the angle.

        :return: The tangent of the angle.
        """
        ...

    def sec(self) -> float:
        """
        Calculates the secant of the angle.

        :return: The secant of the angle.
        """
        ...

    def csc(self) -> float:
        """
        Calculates the cosecant of the angle.

        :return: The cosecant of the angle.
        """
        ...

    def cot(self) -> float:
        """
        Calculates the cotangent of the angle.

        :return: The cotangent of the angle.
        """
        ...

    @overload
    def __add__(self, other: "AngleRadians") -> "AngleRadians": ...
    @overload
    def __add__(self, other: Any) -> Any:
        """
        Adds another AngleRadians instance to this one.

        :param other: The other AngleRadians instance.
        :return: A new AngleRadians instance representing the sum.
        """
        ...

    @overload
    def __sub__(self, other: "AngleRadians") -> "AngleRadians": ...
    @overload
    def __sub__(self, other: Any) -> Any:
        """
        Subtracts another AngleRadians instance from this one.

        :param other: The other AngleRadians instance.
        :return: A new AngleRadians instance representing the difference.
        """
        ...

    @overload
    def __mul__(self, rhs: float) -> "AngleRadians": ...
    @overload
    def __mul__(self, rhs: Any) -> Any:
        """
        Multiplies the angle by a scalar.

        :param rhs: The scalar to multiply by.
        :return: A new scaled AngleRadians instance.
        """
        ...

    @overload
    def __truediv__(self, rhs: float) -> "AngleRadians": ...
    @overload
    def __truediv__(self, rhs: Any) -> Any:
        """
        Divides the angle by a scalar.

        :param rhs: The scalar to divide by.
        :return: A new scaled AngleRadians instance.
        """
        ...

    def __neg__(self) -> "AngleRadians":
        """
        Negates the angle.

        :return: The new negated AngleRadians instance.
        """
        ...

    def __lt__(self, other: "AngleRadians") -> bool:
        """
        Checks if this angle is less than another.

        :param other: The other AngleRadians instance.
        :return: True if this angle is less than `other`, False otherwise.
        """
        ...

    def __le__(self, other: "AngleRadians") -> bool:
        """
        Checks if this angle is less than or equal to another.

        :param other: The other AngleRadians instance.
        :return: True if this angle is less than or equal to `other`, False otherwise.
        """
        ...

    def __gt__(self, other: "AngleRadians") -> bool:
        """
        Checks if this angle is greater than another.

        :param other: The other AngleRadians instance.
        :return: True if this angle is greater than `other`, False otherwise.
        """
        ...

    def __ge__(self, other: "AngleRadians") -> bool:
        """
        Checks if this angle is greater than or equal to another.

        :param other: The other AngleRadians instance.
        :return: True if this angle is greater than or equal to `other`, False otherwise.
        """
        ...

    @overload
    def __eq__(self, other: "AngleRadians") -> bool: ...
    @overload
    def __eq__(self, rhs: Any) -> Any:
        """
        Checks if this angle is equal to another.

        :param other: The other AngleRadians instance.
        :return: True if this angle is equal to `other`, False otherwise.
        """
        ...

    def __repr__(self) -> str:
        """
        Provides a string representation of the angle.

        :return: A string like "AngleRadians(3.14159)".
        """
        ...

class AngleDegrees:
    """
    A class representing an angle in degrees.

    Attributes:
        angle (float): The angle value in degrees.
    """

    def __init__(self, angle: float) -> None:
        """
        Creates a new AngleDegrees instance.

        :param angle: The initial angle value in degrees.
        """
        ...

    def to_radians(self) -> "AngleRadians":
        """
        Converts the angle to radians.

        :return: The angle as an AngleRadians instance.
        """
        ...

    @property
    def angle(self) -> float:
        """
        Get or set the angle value in degrees.

        :return: The angle value.
        """
        ...

    @angle.setter
    def angle(self, value: float) -> None: ...
    def __repr__(self) -> str:
        """
        Provides a string representation of the angle.

        :return: A string like "360°".
        """
        ...

class VecList:
    """
    A class for managing a list of 3D vectors.

    Attributes:
        list (list[Vec3d]): The internal list of Vec3d objects.
    """

    def __init__(self, list: list[Vec3d]) -> None:
        """
        Creates a new VecList instance.

        :param list: An initial list of Vec3d objects.
        """
        ...

    @staticmethod
    def empty() -> "VecList":
        """
        Returns a new empty VecList.

        :return: An empty VecList instance.
        """
        ...

    def append(self, vec: "Vec3d") -> None:
        """
        Appends the vector to the list.

        :param vec: The vector to append
        """

    @property
    def list(self) -> list[Vec3d]:
        """
        The internal list of Vec3d objects.

        :return: The list of vectors.
        """
        ...

    def rotate(self, quat: "Quat") -> None:
        """
        Rotates every vector in the list by a given quaternion.

        :param quat: The quaternion to rotate by.
        """
        ...

    def to_array(self) -> list[list[float]]:
        """
        Converts all vectors in the list to a list of lists.

        :return: A list of lists, where each inner list represents a vector's components.
        """
        ...

    def magnitude(self) -> list[float]:
        """
        Calculates the magnitude of each vector in the list.

        :return: A list of magnitudes for each vector.
        """
        ...

    def extend(self, other: "VecList") -> None:
        """
        Extends the current list with the vectors from another VecList.

        :param other: The other VecList instance.
        """
        ...

    def is_unit(self) -> list[bool]:
        """
        Checks if each vector in the list is a unit vector.

        :return: A list of booleans, where each boolean indicates if the corresponding vector is a unit vector.
        """
        ...

    def normalize(self) -> "VecList":
        """
        Normalizes each vector in the list.

        :return: A new VecList instance containing the normalized vectors.
        """
        ...

    def dot(self, other: "Vec3d") -> list[float]:
        """
        Calculates the dot product of each vector in the list with a given vector.

        :param other: The other Vec3d instance.
        :return: A list of dot products.
        """
        ...

    def cross(self, other: "Vec3d") -> "VecList":
        """
        Calculates the cross product of each vector in the list with a given vector.

        :param other: The other Vec3d instance.
        :return: A new VecList instance containing the resulting vectors.
        """
        ...

    def collapse(self, axis: int) -> "VecList":
        """
        Collapses a vector along a given axis.

        :param axis: The axis to collapse along (0 for x, 1 for y, 2 for z).
        :return: A new VecList with the vectors collapsed.
        """
        ...

    def distance_to(self, other: "Vec3d") -> list[float]:
        """
        Calculates the distance from each vector in the list to another vector.

        :param other: The other Vec3d instance.
        :return: A list of distances.
        """
        ...

    def minimum_distance_to(self, other: "Vec3d", stride: int) -> tuple[int, float]:
        """
        Calculates the vector with the minimum distance to another vector.

        :param stride: The stride size to take, if stride is 1 all points are checked
        :return: A tuple of the index of the closest point and its corresponding distance
        """

    @overload
    def __add__(self, other: "Vec3d") -> "VecList": ...
    @overload
    def __add__(self, other: Any) -> Any:
        """
        Adds a single vector to every vector in the list.

        :param other: The Vec3d instance to add.
        :return: A new VecList with the results.
        """
        ...

    @overload
    def __sub__(self, other: "Vec3d") -> "VecList": ...
    @overload
    def __sub__(self, other: Any) -> Any:
        """
        Subtracts a single vector from every vector in the list.

        :param other: The Vec3d instance to subtract.
        :return: A new VecList with the results.
        """
        ...

    @overload
    def __mul__(self, rhs: float) -> "VecList": ...
    @overload
    def __mul__(self, rhs: Any) -> Any:
        """
        Multiplies every vector in the list by a scalar.

        :param rhs: The scalar to multiply by.
        :return: A new VecList with the results.
        """
        ...

    @overload
    def __rmul__(self, lhs: float) -> "VecList": ...
    @overload
    def __rmul__(self, lhs: Any) -> Any:
        """
        Allows for scalar multiplication from the left.

        :param lhs: The scalar to multiply by.
        :return: A new VecList with the results.
        """
        ...

    @overload
    def __truediv__(self, rhs: float) -> "VecList": ...
    @overload
    def __truediv__(self, rhs: Any) -> Any:
        """
        Divides every vector in the list by a scalar.

        :param rhs: The scalar to divide by.
        :return: A new VecList with the results.
        """
        ...

    def __len__(self) -> int:
        """
        Returns the number of vectors in the list.

        :return: The length of the list.
        """
        ...

    def __iter__(self) -> "VecListIterator":
        """
        Returns an iterator for the list of vectors.

        :return: A VecListIterator.
        """
        ...

    def __getitem__(self, index: int) -> Vec3d:
        """
        Retrieves a vector by index.

        :param index: The index of the vector.
        :return: The Vec3d instance at the given index.
        :raises IndexError: If the index is out of bounds.
        """
        ...

    def __repr__(self) -> str:
        """
        Provides a developer-friendly string representation of the list.

        :return: A string representation of the VecList.
        """
        ...

class VecListIterator(Iterator[Vec3d]):
    """
    An iterator for a VecList instance.
    """

    def __iter__(self) -> "VecListIterator":
        """
        Returns the iterator itself.

        :return: The VecListIterator.
        """
        ...

    def __next__(self) -> Vec3d:
        """
        Returns the next item in the iterator.

        :return: The next Vec3d instance.
        :raises StopIteration: When the iteration is exhausted.
        """
        ...
