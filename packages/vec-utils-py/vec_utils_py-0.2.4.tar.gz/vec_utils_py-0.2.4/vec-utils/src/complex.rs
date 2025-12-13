use core::fmt;
use core::ops::{Add, Div, Index, Mul, Sub};

use crate::{
    impl_dual_op_variants, impl_single_op_comm, impl_single_op_variants,
    impl_single_op_variants_comm, impl_single_op_variants_other
};

/// A complex number
#[cfg_attr(feature = "serde", derive(serde::Deserialize, serde::Serialize))]
#[derive(Debug, Copy, Clone, PartialEq)]
pub struct Complex {
    /// The real part of the complex number
    pub real: f64,
    /// The imaginary part of the complex number
    pub imaginary: f64
}

impl Complex {
    /// Create a new complex number
    pub fn new(real: f64, imaginary: f64) -> Complex {
        Complex { real, imaginary }
    }

    /// Create a new complex number from the square root of a real number
    pub fn sqrt(num: f64) -> Complex {
        if num < 0.0 {
            #[cfg(not(feature = "std"))]
            return Complex::new(0.0, core::f64::math::sqrt(num.abs()));
            #[cfg(feature = "std")]
            return Complex::new(0.0, num.abs().sqrt());
        }
        #[cfg(not(feature = "std"))]
        return Complex::new(core::f64::math::sqrt(num), 0.0);
        #[cfg(feature = "std")]
        return Complex::new(num.sqrt(), 0.0);
    }

    /// Get the magnitude of the complex number
    pub fn magnitude(&self) -> f64 {
        #[cfg(not(feature = "std"))]
        return core::f64::math::sqrt(
            core::f64::math::powi(self.real, 2) + core::f64::math::powi(self.imaginary, 2)
        );
        #[cfg(feature = "std")]
        return (self.real.powi(2) + self.imaginary.powi(2)).sqrt();
    }

    /// Get the conjugate of the complex number
    pub fn conjugate(&self) -> Complex {
        Complex {
            real: self.real,
            imaginary: -self.imaginary
        }
    }
}

macro_rules! impl_dual_op {
    ($trait:ident, $method:ident, $op:tt, $T:ty, $description:literal) => {
        impl $trait for $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: $T) -> $T {
                Self { real: self.real $op other.real, imaginary: self.imaginary $op other.imaginary }
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
                Self { real: self.real $op other, imaginary: self.imaginary }
            }
        }

        impl_single_op_variants!($trait, $method, $T, $W, $description);
    }
}

impl_dual_op!(Add, add, +, Complex, "Add two complex numbers together");
impl_dual_op!(Sub, sub, -, Complex, "Subtract one complex number from another");

impl_single_op_comm!(Add, add, +, Complex, f64, "Add a scalar to a complex number");
impl_single_op!(Sub, sub, -, Complex, f64, "Subtract a scalar from a complex number");

impl Mul<Complex> for Complex {
    type Output = Complex;

    /// Multiply a complex number by another complex number
    fn mul(self, other: Complex) -> Complex {
        Complex {
            real: self.real * other.real - self.imaginary * other.imaginary,
            imaginary: self.real * other.imaginary + self.imaginary * other.real
        }
    }
}

impl_dual_op_variants!(
    Mul,
    mul,
    Complex,
    "Multiply a complex number by another complex number"
);

impl Mul<f64> for Complex {
    type Output = Complex;

    /// Multiply a complex by a real number
    fn mul(self, other: f64) -> Complex {
        Complex {
            real: self.real * other,
            imaginary: self.imaginary * other
        }
    }
}

impl_single_op_variants!(
    Mul,
    mul,
    Complex,
    f64,
    "Multiply a complex number by a real number"
);

impl Mul<Complex> for f64 {
    type Output = Complex;

    /// Multiply a real number by a complex number
    fn mul(self, other: Complex) -> Complex {
        Complex {
            real: self * other.real,
            imaginary: self * other.imaginary
        }
    }
}

impl_single_op_variants_other!(
    Mul,
    mul,
    f64,
    Complex,
    "Multiply a real number by a complex number"
);

impl Div<Complex> for Complex {
    type Output = Complex;

    /// Divide a complex number by another complex number
    fn div(self, other: Complex) -> Complex {
        #[cfg(not(feature = "std"))]
        return Complex {
            real: (self.real * other.real + self.imaginary * other.imaginary)
                / (core::f64::math::powi(other.real, 2)
                    + core::f64::math::powi(other.imaginary, 2)),
            imaginary: (self.imaginary * other.real - self.real * other.imaginary)
                / (core::f64::math::powi(other.real, 2)
                    + core::f64::math::powi(other.imaginary, 2))
        };
        #[cfg(feature = "std")]
        return Complex {
            real: (self.real * other.real + self.imaginary * other.imaginary)
                / (other.real.powi(2) + other.imaginary.powi(2)),
            imaginary: (self.imaginary * other.real - self.real * other.imaginary)
                / (other.real.powi(2) + other.imaginary.powi(2))
        };
    }
}

impl_dual_op_variants!(
    Div,
    div,
    Complex,
    "Divide a complex number by another complex number"
);

impl Div<f64> for Complex {
    type Output = Complex;

    /// Divide a complex number by a real number
    fn div(self, other: f64) -> Complex {
        #[cfg(not(feature = "std"))]
        return Complex {
            real: self.real * other / core::f64::math::powi(other, 2),
            imaginary: self.imaginary * other / core::f64::math::powi(other, 2)
        };
        #[cfg(feature = "std")]
        return Complex {
            real: self.real * other / other.powi(2),
            imaginary: self.imaginary * other / other.powi(2)
        };
    }
}

impl_single_op_variants!(
    Div,
    div,
    Complex,
    f64,
    "Divide a complex number by a real number"
);

impl Div<Complex> for f64 {
    type Output = Complex;

    /// Divide a real number by a complex number
    fn div(self, other: Complex) -> Complex {
        #[cfg(not(feature = "std"))]
        return Complex {
            real: self * other.real
                / (core::f64::math::powi(other.real, 2)
                    + core::f64::math::powi(other.imaginary, 2)),
            imaginary: -self * other.imaginary
                / (core::f64::math::powi(other.real, 2)
                    + core::f64::math::powi(other.imaginary, 2))
        };
        #[cfg(feature = "std")]
        return Complex {
            real: self * other.real / (other.real.powi(2) + other.imaginary.powi(2)),
            imaginary: -self * other.imaginary / (other.real.powi(2) + other.imaginary.powi(2))
        };
    }
}

impl_single_op_variants_other!(
    Div,
    div,
    f64,
    Complex,
    "Divide a real number by a complex number"
);

impl Index<usize> for Complex {
    type Output = f64;

    fn index(&self, index: usize) -> &f64 {
        match index {
            0 => &self.real,
            1 => &self.imaginary,
            _ => panic!("Index out of range")
        }
    }
}

impl fmt::Display for Complex {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if self.real == 0.0 {
            write!(f, "{}i", self.imaginary)
        } else if self.imaginary < 0.0 {
            write!(f, "{} - {}i", self.real, self.imaginary.abs())
        } else {
            write!(f, "{} + {}i", self.real, self.imaginary)
        }
    }
}

#[cfg(test)]
mod tests {
    use assert_float_eq::assert_f64_near;

    use super::*;

    #[test]
    fn test_new() {
        let c = Complex::new(1.0, 2.0);
        assert_f64_near!(c.real, 1.0);
        assert_f64_near!(c.imaginary, 2.0);
    }

    #[test]
    fn test_sqrt() {
        let c = Complex::sqrt(-16.0);
        assert_f64_near!(c.real, 0.0);
        assert_f64_near!(c.imaginary, 4.0);
    }

    #[test]
    fn test_magnitude() {
        let c = Complex::new(3.0, 4.0);
        assert_f64_near!(c.magnitude(), 5.0);
    }

    #[test]
    fn test_conjugate() {
        let c = Complex::new(1.0, 2.0);
        let conjugate = c.conjugate();
        assert_f64_near!(conjugate.real, 1.0);
        assert_f64_near!(conjugate.imaginary, -2.0);
    }

    #[test]
    fn test_add() {
        let c1 = Complex::new(1.0, 2.0);
        let c2 = Complex::new(3.0, 4.0);
        let sum = c1 + c2;
        assert_f64_near!(sum.real, 4.0);
        assert_f64_near!(sum.imaginary, 6.0);
    }

    #[test]
    fn test_sub() {
        let c1 = Complex::new(1.0, 2.0);
        let c2 = Complex::new(3.0, 4.0);
        let diff = c1 - c2;
        assert_f64_near!(diff.real, -2.0);
        assert_f64_near!(diff.imaginary, -2.0);
    }
}
