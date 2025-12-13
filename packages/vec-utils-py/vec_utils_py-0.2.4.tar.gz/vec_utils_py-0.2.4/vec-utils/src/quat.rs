use core::fmt;
use core::ops::{Add, Div, Index, Mul, Sub};
#[cfg(feature = "std")]
use std::vec::Vec;

use crate::angle::AngleRadians;
use crate::vec3d::Vec3d;
use crate::{
    impl_dual_op_variants, impl_single_op_comm, impl_single_op_variants,
    impl_single_op_variants_comm
};

/// A quaternion
#[cfg_attr(feature = "serde", derive(serde::Deserialize, serde::Serialize))]
#[derive(Debug, Copy, Clone)]
pub struct Quat {
    /// The real component of the quaternion
    pub w: f64,
    /// The i component of the quaternion
    pub i: f64,
    /// The j component of the quaternion
    pub j: f64,
    /// The k component of the quaternion
    pub k: f64
}

impl Quat {
    /// Create a new quaternion
    pub fn new(w: f64, i: f64, j: f64, k: f64) -> Quat {
        Quat { w, i, j, k }
    }

    /// Create a new identity quaternion
    /// i.e. a quaternion with a real component of 1 and imaginary components of 0
    pub fn identity() -> Quat {
        Quat {
            w: 1.0,
            i: 0.0,
            j: 0.0,
            k: 0.0
        }
    }

    /// Create a new quaternion from an axis and an angle
    /// representing a rotation of the given angle around the given axis
    /// the resulting quaternion is definitionally a unit quaternion
    /// the angle is positive for a counter-clockwise rotation
    pub fn from_axis_angle(axis: &Vec3d, angle: impl Into<AngleRadians>) -> Quat {
        let angle: AngleRadians = -angle.into();
        let half_angle: AngleRadians = angle / 2.0;
        let s = half_angle.sin();
        Quat {
            w: half_angle.cos(),
            i: axis[0] * s,
            j: axis[1] * s,
            k: axis[2] * s
        }
    }

    /// Create a new quaternion from a rotation matrix
    pub fn from_rotation_matrix(m: &[[f64; 3]; 3]) -> Quat {
        #[cfg(not(feature = "std"))]
        let w = core::f64::math::sqrt(1.0 + m[0][0] + m[1][1] + m[2][2]) / 2.0;
        #[cfg(feature = "std")]
        let w = (1.0 + m[0][0] + m[1][1] + m[2][2]).sqrt() / 2.0;
        #[cfg(not(feature = "std"))]
        let i = core::f64::math::sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) / 2.0;
        #[cfg(feature = "std")]
        let i = (1.0 + m[0][0] - m[1][1] - m[2][2]).sqrt() / 2.0;
        #[cfg(not(feature = "std"))]
        let j = core::f64::math::sqrt(1.0 - m[0][0] + m[1][1] - m[2][2]) / 2.0;
        #[cfg(feature = "std")]
        let j = (1.0 - m[0][0] + m[1][1] - m[2][2]).sqrt() / 2.0;
        #[cfg(not(feature = "std"))]
        let k = core::f64::math::sqrt(1.0 - m[0][0] - m[1][1] + m[2][2]) / 2.0;
        #[cfg(feature = "std")]
        let k = (1.0 - m[0][0] - m[1][1] + m[2][2]).sqrt() / 2.0;
        if w > i && w > j && w > k {
            Quat {
                w,
                i: (m[2][1] - m[1][2]) / (4.0 * w),
                j: (m[0][2] - m[2][0]) / (4.0 * w),
                k: (m[1][0] - m[0][1]) / (4.0 * w)
            }
        } else if i > j && i > k {
            Quat {
                w: (m[2][1] - m[1][2]) / (4.0 * i),
                i,
                j: (m[0][1] + m[1][0]) / (4.0 * i),
                k: (m[0][2] + m[2][0]) / (4.0 * i)
            }
        } else if j > k {
            Quat {
                w: (m[0][2] - m[2][0]) / (4.0 * j),
                i: (m[0][1] + m[1][0]) / (4.0 * j),
                j,
                k: (m[1][2] + m[2][1]) / (4.0 * j)
            }
        } else {
            Quat {
                w: (m[1][0] - m[0][1]) / (4.0 * k),
                i: (m[0][2] + m[2][0]) / (4.0 * k),
                j: (m[1][2] + m[2][1]) / (4.0 * k),
                k
            }
        }
    }

    /// Calculate the conjugate of the quaternion
    /// i.e. the quaternion with the same real component and negated imaginary components
    pub fn conjugate(&self) -> Quat {
        Quat {
            w: self.w,
            i: -self.i,
            j: -self.j,
            k: -self.k
        }
    }

    /// Calculate the magnitude of the quaternion
    pub fn magnitude(&self) -> f64 {
        #[cfg(not(feature = "std"))]
        return core::f64::math::sqrt(
            self.w * self.w + self.i * self.i + self.j * self.j + self.k * self.k
        );
        #[cfg(feature = "std")]
        return (self.w * self.w + self.i * self.i + self.j * self.j + self.k * self.k).sqrt();
    }

    /// Return a new Quat of the normalized quaternion
    pub fn normalize(&self) -> Quat {
        let magnitude = self.magnitude();
        Quat {
            w: self.w / magnitude,
            i: self.i / magnitude,
            j: self.j / magnitude,
            k: self.k / magnitude
        }
    }

    /// Check if the quaternion is a unit quaternion
    pub fn is_unit(&self) -> bool {
        (self.magnitude() - 1.0).abs() < f64::EPSILON
    }

    /// Convert the quaternion to an axis and an angle
    pub fn to_axis_angle(&self) -> (Vec3d, AngleRadians) {
        if (self.w - 1.0).abs() < f64::EPSILON {
            (Vec3d::i(), 0.0.into())
        } else {
            #[cfg(not(feature = "std"))]
            let angle = 2.0 * libm::acos(self.w);
            #[cfg(feature = "std")]
            let angle = 2.0 * self.w.acos();
            #[cfg(not(feature = "std"))]
            let s = libm::sin(angle / 2.0);
            #[cfg(feature = "std")]
            let s = (angle / 2.0).sin();
            let x = self.i / s;
            let y = self.j / s;
            let z = self.k / s;
            (Vec3d::new(x, y, z), angle.into())
        }
    }

    /// Convert the quaternion to a vector
    /// the real component of the quaternion is discarded
    /// the imaginary components of the quaternion are used as the vector components
    pub fn to_vec3d(&self) -> Vec3d {
        Vec3d::new(self.i, self.j, self.k)
    }

    /// Convert the quaternion to a rotation matrix
    pub fn to_rotation_matrix(&self) -> [[f64; 3]; 3] {
        [
            [
                1.0 - 2.0 * (self.j * self.j + self.k * self.k),
                2.0 * (self.i * self.j - self.k * self.w),
                2.0 * (self.i * self.k + self.j * self.w)
            ],
            [
                2.0 * (self.i * self.j + self.k * self.w),
                1.0 - 2.0 * (self.i * self.i + self.k * self.k),
                2.0 * (self.j * self.k - self.i * self.w)
            ],
            [
                2.0 * (self.i * self.k - self.j * self.w),
                2.0 * (self.j * self.k + self.i * self.w),
                1.0 - 2.0 * (self.i * self.i + self.j * self.j)
            ]
        ]
    }

    /// Rotate a vector by the quaternion
    /// this is an active rotation
    pub fn rotate(&self, v: &Vec3d) -> Vec3d {
        let qv = Quat {
            w: 0.0,
            i: v.x,
            j: v.y,
            k: v.z
        };
        (self.conjugate() * qv * self).to_vec3d()
    }

    /// Convert the Quat to a Vec of f64 with length 4
    #[cfg(feature = "std")]
    pub fn to_vec(&self) -> Vec<f64> {
        vec![self.w, self.i, self.j, self.k]
    }
}

macro_rules! impl_dual_op {
    ($trait:ident, $method:ident, $op:tt, $T:ty, $description:literal) => {
        impl $trait for $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: $T) -> $T {
                Self { w: self.w $op other.w, i: self.i $op other.i, j: self.j $op other.j, k: self.k $op other.k }
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
                Self { w: self.w $op other, i: self.i $op other, j: self.j $op other, k: self.k $op other }
            }
        }

        impl_single_op_variants!($trait, $method, $T, $W, $description);
    }
}

impl_dual_op!(Add, add, +, Quat, "Add two Quats together comonent-wise");
impl_dual_op!(Sub, sub, -, Quat, "Subtract one Quat from another component-wise");

// NOTE: I can't decide if it makes sense for addition to be communicative
impl_single_op!(Add, add, +, Quat, f64, "Add a scalar to each component of a Quat");
impl_single_op!(Sub, sub, -, Quat, f64, "Subtract a scalar from each component of a Quat");
impl_single_op_comm!(Mul, mul, *, Quat, f64, "Multiply a Quat by a scalar");
impl_single_op!(Div, div, /, Quat, f64, "Divide a Quat by a scalar");

impl Mul<Quat> for Quat {
    type Output = Quat;

    /// Multiply two quaternions
    /// also known as a Hamilton product
    fn mul(self, other: Quat) -> Quat {
        Quat {
            w: self.w * other.w - self.i * other.i - self.j * other.j - self.k * other.k,
            i: self.w * other.i + self.i * other.w + self.j * other.k - self.k * other.j,
            j: self.w * other.j + self.j * other.w + self.k * other.i - self.i * other.k,
            k: self.w * other.k + self.k * other.w + self.i * other.j - self.j * other.i
        }
    }
}

impl_dual_op_variants!(
    Mul,
    mul,
    Quat,
    "Multiply two quaternions, also known as a Hamilton product"
);

impl Index<usize> for Quat {
    type Output = f64;

    /// Index into a quaternion
    /// 0 is w, 1 is x, 2 is y, 3 is z
    /// Panics if the index is out of bounds
    fn index(&self, index: usize) -> &f64 {
        match index {
            0 => &self.w,
            1 => &self.i,
            2 => &self.j,
            3 => &self.k,
            _ => panic!("Index out of range")
        }
    }
}

impl fmt::Display for Quat {
    /// Format the quaternion as a string
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {}, {}, {})", self.w, self.i, self.j, self.k)
    }
}

impl PartialEq for Quat {
    fn eq(&self, other: &Self) -> bool {
        (self.w - other.w).abs() < f64::EPSILON
            && (self.i - other.i).abs() < f64::EPSILON
            && (self.j - other.j).abs() < f64::EPSILON
            && (self.k - other.k).abs() < f64::EPSILON
    }
}

#[cfg(test)]
mod tests {
    use assert_float_eq::assert_f64_near;
    use pretty_assertions::assert_eq;

    use super::*;

    #[test]
    fn test_new() {
        let q = Quat::new(1.0, 2.0, 3.0, 4.0);
        assert_f64_near!(q.w, 1.0);
        assert_f64_near!(q.i, 2.0);
        assert_f64_near!(q.j, 3.0);
        assert_f64_near!(q.k, 4.0);
    }

    #[test]
    fn test_identity() {
        let q = Quat::identity();
        let good = Quat::new(1.0, 0.0, 0.0, 0.0);
        assert_eq!(q, good);
    }

    #[test]
    fn test_from_axis_angle() {
        let axis = Vec3d::i();
        let q = Quat::from_axis_angle(&axis, 0.0);
        let good = Quat::new(1.0, 0.0, 0.0, 0.0);
        assert_eq!(q, good);
    }

    #[test]
    fn test_from_rotation_matrix() {
        let m = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]];
        let q = Quat::from_rotation_matrix(&m);
        let good = Quat::new(1.0, 0.0, 0.0, 0.0);
        assert_eq!(q, good);
    }

    #[test]
    fn test_conjugate() {
        let q = Quat::new(1.0, 2.0, 3.0, 4.0);
        let c = q.conjugate();
        let good = Quat::new(1.0, -2.0, -3.0, -4.0);
        assert_eq!(c, good);
    }

    #[test]
    fn test_magnitude() {
        let q = Quat::new(1.0, 2.0, 3.0, 4.0);
        assert_f64_near!(q.magnitude(), 5.477_225_575_051_661);
    }

    #[test]
    fn test_is_unit() {
        let q = Quat::new(1.0, 2.0, 3.0, 4.0);
        assert_eq!(q.is_unit(), false);
    }

    #[test]
    fn test_to_axis_angle() {
        let q = Quat::new(1.0, 0.0, 0.0, 0.0);
        let (axis, angle) = q.to_axis_angle();
        let good = Vec3d::new(1.0, 0.0, 0.0);
        assert_eq!(axis, good);
        assert_eq!(angle, 0.0.into());
    }

    #[test]
    fn test_to_vec3d() {
        let q = Quat::new(1.0, 2.0, 3.0, 4.0);
        let v = q.to_vec3d();
        let good = Vec3d::new(2.0, 3.0, 4.0);
        assert_eq!(v, good);
    }

    #[test]
    fn test_to_rotation_matrix() {
        let q = Quat::new(1.0, 0.0, 0.0, 0.0);
        let m = q.to_rotation_matrix();
        assert_f64_near!(m[0][0], 1.0);
        assert_f64_near!(m[0][1], 0.0);
        assert_f64_near!(m[0][2], 0.0);
        assert_f64_near!(m[1][0], 0.0);
        assert_f64_near!(m[1][1], 1.0);
        assert_f64_near!(m[1][2], 0.0);
        assert_f64_near!(m[2][0], 0.0);
        assert_f64_near!(m[2][1], 0.0);
        assert_f64_near!(m[2][2], 1.0);
    }

    #[test]
    fn test_rotate() {
        let q = Quat::new(1.0, 0.0, 0.0, 0.0);
        let v = Vec3d::new(1.0, 0.0, 0.0);
        let r = q.rotate(&v);
        let good = Vec3d::new(1.0, 0.0, 0.0);
        assert_eq!(r, good);
    }

    #[test]
    fn test_mul() {
        let q1 = Quat::new(1.0, 2.0, 3.0, 4.0);
        let q2 = Quat::new(5.0, 6.0, 7.0, 8.0);
        let q = q1 * q2;
        let good = Quat::new(-60.0, 12.0, 30.0, 24.0);
        assert_eq!(q, good);
    }

    #[test]
    fn test_index() {
        let q = Quat::new(1.0, 2.0, 3.0, 4.0);
        assert_f64_near!(q[0], 1.0);
        assert_f64_near!(q[1], 2.0);
        assert_f64_near!(q[2], 3.0);
        assert_f64_near!(q[3], 4.0);
    }
}
