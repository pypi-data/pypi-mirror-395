use pyo3::prelude::*;
use vec_utils::*;

#[pyclass]
#[derive(Debug, PartialOrd, PartialEq, Clone, Copy)]
pub struct AngleRadians {
    pub inner: angle::AngleRadians
}

#[pyclass]
#[derive(Debug, PartialOrd, PartialEq, Clone, Copy)]
pub struct AngleDegrees {
    pub inner: angle::AngleDegrees
}

#[pymethods]
impl AngleDegrees {
    #[new]
    pub fn new(angle: f64) -> Self {
        AngleDegrees {
            inner: angle::AngleDegrees::new(angle)
        }
    }

    pub fn __repr__(&self) -> String {
        format!("{}", self.inner)
    }

    #[getter]
    pub fn angle(&self) -> f64 {
        self.inner.angle
    }

    #[setter]
    pub fn set_angle(&mut self, value: f64) {
        self.inner.angle = value;
    }

    pub fn to_radians(&self) -> AngleRadians {
        AngleRadians {
            inner: self.inner.to_radians()
        }
    }
}

#[pymethods]
impl AngleRadians {
    #[new]
    pub fn new(angle: f64) -> Self {
        AngleRadians {
            inner: angle::AngleRadians::new(angle)
        }
    }

    #[staticmethod]
    pub fn zero() -> Self {
        AngleRadians {
            inner: angle::AngleRadians::zero()
        }
    }

    #[staticmethod]
    pub fn pi() -> Self {
        AngleRadians {
            inner: angle::AngleRadians::pi()
        }
    }

    #[staticmethod]
    pub fn two_pi() -> Self {
        AngleRadians {
            inner: angle::AngleRadians::two_pi()
        }
    }

    #[staticmethod]
    pub fn half_pi() -> Self {
        AngleRadians {
            inner: angle::AngleRadians::half_pi()
        }
    }

    #[staticmethod]
    pub fn quarter_pi() -> Self {
        AngleRadians {
            inner: angle::AngleRadians::quarter_pi()
        }
    }

    #[staticmethod]
    pub fn third_pi() -> Self {
        AngleRadians {
            inner: angle::AngleRadians::third_pi()
        }
    }

    #[staticmethod]
    pub fn sixth_pi() -> Self {
        AngleRadians {
            inner: angle::AngleRadians::sixth_pi()
        }
    }

    #[getter]
    pub fn angle(&self) -> f64 {
        self.inner.angle
    }

    #[setter]
    pub fn set_angle(&mut self, value: f64) {
        self.inner.angle = value;
    }

    pub fn to_degrees(&self) -> AngleDegrees {
        AngleDegrees {
            inner: self.inner.to_degrees()
        }
    }

    pub fn sin(&self) -> f64 {
        self.inner.sin()
    }

    pub fn cos(&self) -> f64 {
        self.inner.cos()
    }

    pub fn tan(&self) -> f64 {
        self.inner.tan()
    }

    pub fn sec(&self) -> f64 {
        self.inner.sec()
    }

    pub fn csc(&self) -> f64 {
        self.inner.csc()
    }

    pub fn cot(&self) -> f64 {
        self.inner.cot()
    }

    pub fn __add__(&self, other: &AngleRadians) -> AngleRadians {
        AngleRadians {
            inner: self.inner + other.inner
        }
    }

    pub fn __sub__(&self, other: &AngleRadians) -> AngleRadians {
        AngleRadians {
            inner: self.inner - other.inner
        }
    }

    pub fn __mul__(&self, rhs: f64) -> AngleRadians {
        AngleRadians {
            inner: self.inner * rhs
        }
    }

    pub fn __truediv__(&self, rhs: f64) -> AngleRadians {
        AngleRadians {
            inner: self.inner / rhs
        }
    }

    pub fn __neg__(&self) -> AngleRadians {
        AngleRadians { inner: -self.inner }
    }

    pub fn __lt__(&self, other: &AngleRadians) -> bool {
        self.inner < other.inner
    }

    pub fn __le__(&self, other: &AngleRadians) -> bool {
        self.inner <= other.inner
    }

    pub fn __gt__(&self, other: &AngleRadians) -> bool {
        self.inner > other.inner
    }

    pub fn __ge__(&self, other: &AngleRadians) -> bool {
        self.inner >= other.inner
    }

    pub fn __eq__(&self, other: &AngleRadians) -> bool {
        self.inner == other.inner
    }

    pub fn __repr__(&self) -> String {
        format!("{}", self.inner)
    }
}
