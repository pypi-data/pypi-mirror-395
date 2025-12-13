use core::ops::{Add, Div, Index, Mul, Neg, Sub};
use core::{f64, fmt};
#[cfg(feature = "std")]
use std::vec::Vec;

use crate::angle::AngleRadians;
use crate::quat::Quat;
use crate::{
    impl_dual_op_variants, impl_single_op_comm, impl_single_op_variants,
    impl_single_op_variants_comm
};

/// A 3D vector
#[cfg_attr(feature = "serde", derive(serde::Deserialize, serde::Serialize))]
#[derive(Debug, Copy, Clone)]
pub struct Vec3d {
    /// The x component of the vector
    pub x: f64,
    /// The y component of the vector
    pub y: f64,
    /// The z component of the vector
    pub z: f64
}

impl Vec3d {
    /// Create a new Vec3d
    pub fn new(x: f64, y: f64, z: f64) -> Vec3d {
        Vec3d { x, y, z }
    }

    /// Create a new Vec3d from a start point to an end point
    pub fn new_from_to(from: &Vec3d, to: &Vec3d) -> Vec3d {
        Vec3d {
            x: to.x - from.x,
            y: to.y - from.y,
            z: to.z - from.z
        }
    }

    /// Create a new Vec3d with all components set to 0
    pub fn zero() -> Vec3d {
        Vec3d {
            x: 0.0,
            y: 0.0,
            z: 0.0
        }
    }

    /// Create a new Vec3d of the i unit vector
    pub fn i() -> Vec3d {
        Vec3d {
            x: 1.0,
            y: 0.0,
            z: 0.0
        }
    }

    /// Create a new Vec3d of the j unit vector
    pub fn j() -> Vec3d {
        Vec3d {
            x: 0.0,
            y: 1.0,
            z: 0.0
        }
    }

    /// Create a new Vec3d of the k unit vector
    pub fn k() -> Vec3d {
        Vec3d {
            x: 0.0,
            y: 0.0,
            z: 1.0
        }
    }

    /// Create a new Vec3d from a quaternion
    /// the imaginary components of the quaternion are used as the x, y, and z components of the vector
    /// the real component of the quaternion is ignored
    pub fn from_quat(q: &Quat) -> Vec3d {
        Vec3d {
            x: q.i,
            y: q.j,
            z: q.k
        }
    }

    /// Convert the Vec3d to an array
    pub fn to_array(&self) -> [f64; 3] {
        [self.x, self.y, self.z]
    }

    /// Convert the Vec3d to a quaternion
    /// the x, y, and z components of the vector are used as the imaginary components of the quaternion
    /// the real component of the quaternion is set to 0
    pub fn to_quat(&self) -> Quat {
        Quat {
            w: 0.0,
            i: self.x,
            j: self.y,
            k: self.z
        }
    }

    /// Create a new Vec3d from a slice of f64s
    /// the slice should have a length of 3
    /// any additional elements will be ignored
    pub fn from_slice(v: &[f64]) -> Vec3d {
        Vec3d {
            x: v[0],
            y: v[1],
            z: v[2]
        }
    }

    /// Convert the Vec3d to a Vec of f64 with length 3
    #[cfg(feature = "std")]
    pub fn to_vec(&self) -> Vec<f64> {
        vec![self.x, self.y, self.z]
    }

    /// Calculate the dot product of two Vec3d
    pub fn dot(&self, other: &Vec3d) -> f64 {
        self.x * other.x + self.y * other.y + self.z * other.z
    }

    /// Calculate the cross product of two Vec3d
    pub fn cross(&self, other: &Vec3d) -> Vec3d {
        Vec3d {
            x: self.y * other.z - self.z * other.y,
            y: self.z * other.x - self.x * other.z,
            z: self.x * other.y - self.y * other.x
        }
    }

    /// Calculate the magnitude of the Vec3d
    pub fn magnitude(&self) -> f64 {
        #[cfg(not(feature = "std"))]
        return core::f64::math::sqrt(self.x * self.x + self.y * self.y + self.z * self.z);
        #[cfg(feature = "std")]
        return (self.x * self.x + self.y * self.y + self.z * self.z).sqrt();
    }

    /// Check if the Vec3d is a unit vector
    pub fn is_unit(&self) -> bool {
        (self.magnitude() - 1.0).abs() < f64::EPSILON
    }

    /// Return a new Vec3d of the normalized vector
    pub fn normalize(&self) -> Vec3d {
        let magnitude = self.magnitude();
        Vec3d {
            x: self.x / magnitude,
            y: self.y / magnitude,
            z: self.z / magnitude
        }
    }

    /// Calculate the angle between two Vec3d's
    /// the result is in radians
    pub fn angle_to(&self, other: &Vec3d) -> AngleRadians {
        #[cfg(not(feature = "std"))]
        return AngleRadians::new(libm::acos(
            self.dot(other) / (self.magnitude() * other.magnitude())
        ));
        #[cfg(feature = "std")]
        return AngleRadians::new(
            (self.dot(other) / (self.magnitude() * other.magnitude())).acos()
        );
    }

    /// Calculate the scalar triple product of three Vec3d's
    pub fn scalar_triple_product(a: &Vec3d, b: &Vec3d, c: &Vec3d) -> f64 {
        a.dot(&b.cross(c))
    }

    /// Calculate the squared distance to another Vec3d
    /// This avoids a sqrt operation while being similarly useful
    pub fn distance_squared(&self, other: &Vec3d) -> f64 {
        let between = self - other;
        between.x * between.x + between.y * between.y + between.z * between.z
    }

    /// Calculate the distance to another Vec3d
    pub fn distance_to(&self, other: &Vec3d) -> f64 {
        (self - other).magnitude()
    }

    /// Calculate the distance from a point to a line
    /// the line is defined by two points
    /// the result is the shortest distance from the point to the line as a positive scalar
    /// the line is treated as infinite
    pub fn distance_to_line(&self, a: &Vec3d, b: &Vec3d) -> f64 {
        let ab = b - a;
        let ap = self - a;
        let t = ap.dot(&ab) / ab.dot(&ab);
        let projection = a + ab * t;
        (self - projection).magnitude()
    }

    /// Project a Vec3d onto a plane defined by a normal vector
    /// the normal vector should be a unit vector
    pub fn project_onto_plane(&self, normal: &Vec3d) -> Vec3d {
        self - normal * self.dot(normal)
    }

    /// Project a Vec3d onto a line
    /// returns the closest point on the line defined by two points
    /// to the point
    pub fn project_onto_line(&self, line_r: &Vec3d, line_q: &Vec3d) -> Vec3d {
        let t = (line_r - line_q).dot(&(line_q - self)) / (line_r - line_q).dot(&(line_r - line_q));
        line_q - t * (line_r - line_q)
    }

    // TODO: Benchmark this
    /// Collapse the vector
    /// sets the axis to zero
    /// similar to `project_onto_plane` but might be faster
    pub fn collapse(&self, axis: usize) -> Option<Vec3d> {
        match axis {
            0 => Some(Vec3d {
                x: 0.0,
                y: self.y,
                z: self.z
            }),
            1 => Some(Vec3d {
                x: self.x,
                y: 0.0,
                z: self.z
            }),
            2 => Some(Vec3d {
                x: self.x,
                y: self.y,
                z: 0.0
            }),
            _ => None
        }
    }
}

macro_rules! impl_dual_op {
    ($trait:ident, $method:ident, $op:tt, $T:ty, $description:literal) => {
        impl $trait for $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: $T) -> $T {
                Self { x: self.x $op other.x, y: self.y $op other.y, z: self.z $op other.z }
            }
        }

        impl_dual_op_variants!($trait, $method, $T, $description);
    }
}

macro_rules! impl_single_op {
    ($trait:ident, $method:ident, $op:tt, $T:ty, $W:ty, $description:literal) => {
        impl $trait<$W> for $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: $W) -> $T {
                Self { x: self.x $op other, y: self.y $op other, z: self.z $op other }
            }
        }

        impl_single_op_variants!($trait, $method, $T, $W, $description);
    }
}

impl_dual_op!(Add, add, +, Vec3d, "Add two Ved3ds together comonent-wise");
impl_dual_op!(Sub, sub, -, Vec3d, "Subtract one Vec3d from another component-wise");

// NOTE: I can't decide if it makes sense for addition to be communicative
impl_single_op!(Add, add, +, Vec3d, f64, "Add a scalar to each component of a Vec3d");
impl_single_op!(Sub, sub, -, Vec3d, f64, "Subtract a scalar from each component of a Vec3d");
impl_single_op_comm!(Mul, mul, *, Vec3d, f64, "Multiply a Vec3d by a scalar");
impl_single_op!(Div, div, /, Vec3d, f64, "Divide a Vec3d by a scalar");

impl Neg for Vec3d {
    type Output = Vec3d;

    fn neg(self) -> Vec3d {
        Vec3d::new(-self.x, -self.y, -self.z)
    }
}

impl PartialEq for Vec3d {
    fn eq(&self, other: &Self) -> bool {
        (self.x - other.x).abs() < f64::EPSILON
            && (self.y - other.y).abs() < f64::EPSILON
            && (self.z - other.z).abs() < f64::EPSILON
    }
}

impl Index<usize> for Vec3d {
    type Output = f64;

    /// Index into a Vec3d
    /// 0 is x, 1 is y, 2 is z
    /// Panics if the index is out of bounds
    fn index(&self, index: usize) -> &f64 {
        match index {
            0 => &self.x,
            1 => &self.y,
            2 => &self.z,
            _ => panic!("Index out of bounds")
        }
    }
}

impl fmt::Display for Vec3d {
    /// Format the Vec3d as a string
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {}, {})", self.x, self.y, self.z)
    }
}

#[cfg(test)]
mod tests {
    use assert_float_eq::assert_f64_near;
    use pretty_assertions::assert_eq;

    use super::*;

    #[test]
    fn test_new() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        assert_f64_near!(v.x, 1.0);
        assert_f64_near!(v.y, 2.0);
        assert_f64_near!(v.z, 3.0);
    }

    #[test]
    fn test_new_from_to() {
        let from = Vec3d::new(1.0, 1.0, 1.0);
        let to = Vec3d::new(2.0, 2.0, 2.0);
        let v = Vec3d::new_from_to(&from, &to);
        let good = Vec3d::new(1.0, 1.0, 1.0);
        assert_eq!(v, good);
    }

    #[test]
    fn test_zero() {
        let v = Vec3d::zero();
        let zero = Vec3d::new(0.0, 0.0, 0.0);
        assert_eq!(v, zero);
    }

    #[test]
    fn test_i() {
        let v = Vec3d::i();
        let i = Vec3d::new(1.0, 0.0, 0.0);
        assert_eq!(v, i);
    }

    #[test]
    fn test_j() {
        let v = Vec3d::j();
        let j = Vec3d::new(0.0, 1.0, 0.0);
        assert_eq!(v, j);
    }

    #[test]
    fn test_k() {
        let v = Vec3d::k();
        let k = Vec3d::new(0.0, 0.0, 1.0);
        assert_eq!(v, k);
    }

    #[test]
    fn test_from_quat() {
        let q = Quat::new(1.0, 2.0, 3.0, 4.0);
        let v = Vec3d::from_quat(&q);
        let good = Vec3d::new(2.0, 3.0, 4.0);
        assert_eq!(v, good);
    }

    #[test]
    fn test_to_array() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        let arr = v.to_array();
        let good = [1.0, 2.0, 3.0];
        assert_f64_near!(arr[0], good[0]);
        assert_f64_near!(arr[1], good[1]);
        assert_f64_near!(arr[2], good[2]);
    }

    #[test]
    fn test_to_quat() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        let q = v.to_quat();
        let good = Quat::new(0.0, 1.0, 2.0, 3.0);
        assert_eq!(q, good);
    }

    #[test]
    fn test_from_slice() {
        let v = Vec3d::from_slice(&[1.0, 2.0, 3.0]);
        let good = Vec3d::new(1.0, 2.0, 3.0);
        assert_eq!(v, good);
        let arr = [1.0, 2.0, 3.0];
        let v = Vec3d::from_slice(&arr);
        assert_eq!(v, good);
    }

    #[test]
    #[cfg(feature = "std")]
    fn test_to_vec() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        let vec = v.to_vec();
        let good = vec![1.0, 2.0, 3.0];
        assert_eq!(vec, good);
    }

    #[test]
    fn test_dot() {
        let v1 = Vec3d::new(1.0, 2.0, 3.0);
        let v2 = Vec3d::new(4.0, 5.0, 6.0);
        assert_f64_near!(v1.dot(&v2), 32.0);
    }

    #[test]
    fn test_cross() {
        let v1 = Vec3d::new(1.0, 2.0, 3.0);
        let v2 = Vec3d::new(4.0, 5.0, 6.0);
        let v = v1.cross(&v2);
        let good = Vec3d::new(-3.0, 6.0, -3.0);
        assert_eq!(v, good);
    }

    #[test]
    fn test_magnitude() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        assert_f64_near!(v.magnitude(), 3.741_657_386_773_941_3);
    }

    #[test]
    fn test_is_unit() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        assert_eq!(v.is_unit(), false);
    }

    #[test]
    fn test_normalize() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        let n = v.normalize();
        let good = Vec3d::new(
            0.267_261_241_912_424_4,
            0.534_522_483_824_848_8,
            0.801_783_725_737_273_2
        );
        assert_eq!(n, good);
    }

    #[test]
    fn test_angle_to() {
        let v1 = Vec3d::k();
        let v2 = Vec3d::i();
        assert_eq!(v1.angle_to(&v2), core::f64::consts::FRAC_PI_2.into());
    }

    #[test]
    fn test_scalar_triple_product() {
        let v1 = Vec3d::new(1.0, 2.0, 9.0);
        let v2 = Vec3d::new(7.0, 8.0, 9.0);
        let v3 = Vec3d::new(4.0, 5.0, 6.0);
        assert_f64_near!(Vec3d::scalar_triple_product(&v1, &v2, &v3), 18.0);
    }

    #[test]
    fn test_distance_to() {
        let v1 = Vec3d::new(1.0, 1.0, 1.0);
        let v2 = Vec3d::new(1.0, 1.0, 6.0);
        assert_f64_near!(v1.distance_to(&v2), 5.0);
    }

    #[test]
    fn test_distance_to_line() {
        let v1 = Vec3d::new(1.0, 1.0, 0.0);
        let v2 = Vec3d::new(1.0, 1.0, 6.0);
        let v3 = Vec3d::new(1.0, 0.0, 3.0);
        assert_f64_near!(v3.distance_to_line(&v1, &v2), 1.0);
    }

    #[test]
    fn test_project_onto_plane() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        let n = Vec3d::new(0.0, 0.0, 1.0);
        let p = v.project_onto_plane(&n);
        let good = Vec3d::new(1.0, 2.0, 0.0);
        assert_eq!(p, good);
    }

    #[test]
    fn collapse() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        let p = v.collapse(2).unwrap();
        let good = Vec3d::new(1.0, 2.0, 0.0);
        assert_eq!(p, good);
        assert_eq!(v.collapse(13), None);
    }

    #[test]
    #[allow(clippy::op_ref)]
    fn test_add() {
        let v1 = Vec3d::new(1.0, 2.0, 3.0);
        let v2 = Vec3d::new(4.0, 5.0, 6.0);
        let v = v1 + v2;
        let good = Vec3d::new(5.0, 7.0, 9.0);
        assert_eq!(v, good);
        let v = &v1 + v2;
        assert_eq!(v, good);
        let v = v1 + &v2;
        assert_eq!(v, good);
        let v = &v1 + &v2;
        assert_eq!(v, good);
        let good = Vec3d::new(5.0, 6.0, 7.0);
        let v = v1 + 4.0;
        assert_eq!(v, good);
        let v = &v1 + 4.0;
        assert_eq!(v, good);
        let v = v1 + &4.0;
        assert_eq!(v, good);
        let v = &v1 + &4.0;
        assert_eq!(v, good);
    }

    #[test]
    #[allow(clippy::op_ref)]
    fn test_sub() {
        let v1 = Vec3d::new(1.0, 2.0, 3.0);
        let v2 = Vec3d::new(4.0, 5.0, 6.0);
        let v = v1 - v2;
        let good = Vec3d::new(-3.0, -3.0, -3.0);
        assert_eq!(v, good);
        let v = &v1 - v2;
        assert_eq!(v, good);
        let v = v1 - &v2;
        assert_eq!(v, good);
        let v = &v1 - &v2;
        assert_eq!(v, good);
        let good = Vec3d::new(-3.0, -2.0, -1.0);
        let v = v1 - 4.0;
        assert_eq!(v, good);
        let v = &v1 - 4.0;
        assert_eq!(v, good);
        let v = v1 - &4.0;
        assert_eq!(v, good);
        let v = &v1 - &4.0;
        assert_eq!(v, good);
    }

    #[test]
    #[allow(clippy::op_ref)]
    fn test_mul() {
        let v1 = Vec3d::new(1.0, 2.0, 3.0);
        let v = v1 * 2.0;
        let good = Vec3d::new(2.0, 4.0, 6.0);
        assert_eq!(v, good);
        let v = &v1 * 2.0;
        assert_eq!(v, good);
        let v = v1 * &2.0;
        assert_eq!(v, good);
        let v = &v1 * &2.0;
        assert_eq!(v, good);
    }

    #[test]
    #[allow(clippy::op_ref)]
    fn test_div() {
        let v1 = Vec3d::new(1.0, 2.0, 3.0);
        let v = v1 / 2.0;
        let good = Vec3d::new(0.5, 1.0, 1.5);
        assert_eq!(v, good);
        let v = &v1 / 2.0;
        assert_eq!(v, good);
        let v = v1 / &2.0;
        assert_eq!(v, good);
        let v = &v1 / &2.0;
        assert_eq!(v, good);
    }

    #[test]
    fn test_index() {
        let v = Vec3d::new(1.0, 2.0, 3.0);
        assert_f64_near!(v[0], 1.0);
        assert_f64_near!(v[1], 2.0);
        assert_f64_near!(v[2], 3.0);
    }
}
