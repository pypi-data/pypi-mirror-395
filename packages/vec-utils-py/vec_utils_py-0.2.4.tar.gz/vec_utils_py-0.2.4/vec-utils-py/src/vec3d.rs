use pyo3::prelude::*;
use vec_utils::*;

use super::angle::AngleRadians;
use super::quat::Quat;

#[pyclass]
#[derive(Debug, Copy, Clone, PartialEq)]
pub struct Vec3d {
    pub inner: vec3d::Vec3d
}

#[pymethods]
impl Vec3d {
    #[new]
    pub fn new(x: f64, y: f64, z: f64) -> Self {
        Vec3d {
            inner: vec3d::Vec3d::new(x, y, z)
        }
    }

    #[staticmethod]
    pub fn zero() -> Self {
        Vec3d {
            inner: vec3d::Vec3d::zero()
        }
    }

    #[staticmethod]
    pub fn i() -> Self {
        Vec3d {
            inner: vec3d::Vec3d::i()
        }
    }

    #[staticmethod]
    pub fn j() -> Self {
        Vec3d {
            inner: vec3d::Vec3d::j()
        }
    }

    #[staticmethod]
    pub fn k() -> Self {
        Vec3d {
            inner: vec3d::Vec3d::k()
        }
    }

    #[staticmethod]
    pub fn new_from_to(from: &Vec3d, to: &Vec3d) -> Self {
        Vec3d {
            inner: vec3d::Vec3d::new_from_to(&from.inner, &to.inner)
        }
    }

    #[getter]
    pub fn x(&self) -> f64 {
        self.inner.x
    }

    #[getter]
    pub fn y(&self) -> f64 {
        self.inner.y
    }

    #[getter]
    pub fn z(&self) -> f64 {
        self.inner.z
    }

    #[setter]
    pub fn set_x(&mut self, value: f64) {
        self.inner.x = value;
    }

    #[setter]
    pub fn set_y(&mut self, value: f64) {
        self.inner.y = value;
    }

    #[setter]
    pub fn set_z(&mut self, value: f64) {
        self.inner.z = value;
    }

    pub fn to_quat(&self) -> Quat {
        Quat {
            inner: self.inner.to_quat()
        }
    }

    pub fn to_array(&self) -> [f64; 3] {
        self.inner.to_array()
    }

    pub fn magnitude(&self) -> f64 {
        self.inner.magnitude()
    }

    pub fn is_unit(&self) -> bool {
        self.inner.is_unit()
    }

    pub fn normalize(&self) -> Self {
        Vec3d {
            inner: self.inner.normalize()
        }
    }

    pub fn dot(&self, other: &Vec3d) -> f64 {
        self.inner.dot(&other.inner)
    }

    pub fn cross(&self, other: &Vec3d) -> Self {
        Vec3d {
            inner: self.inner.cross(&other.inner)
        }
    }

    pub fn angle_to(&self, other: &Vec3d) -> AngleRadians {
        AngleRadians {
            inner: self.inner.angle_to(&other.inner)
        }
    }

    pub fn scalar_triple_product(a: PyRef<Vec3d>, b: PyRef<Vec3d>, c: PyRef<Vec3d>) -> f64 {
        vec3d::Vec3d::scalar_triple_product(&a.inner, &b.inner, &c.inner)
    }

    pub fn distance_to(&self, other: &Vec3d) -> f64 {
        self.inner.distance_to(&other.inner)
    }

    pub fn distance_squared(&self, other: &Vec3d) -> f64 {
        self.inner.distance_squared(&other.inner)
    }

    pub fn distance_to_line(&self, a: &Vec3d, b: &Vec3d) -> f64 {
        self.inner.distance_to_line(&a.inner, &b.inner)
    }

    pub fn project_onto_plane(&self, normal: &Vec3d) -> Self {
        Vec3d {
            inner: self.inner.project_onto_plane(&normal.inner)
        }
    }

    pub fn project_onto_line(&self, line_r: &Vec3d, line_q: &Vec3d) -> Self {
        Vec3d {
            inner: self.inner.project_onto_line(&line_r.inner, &line_q.inner)
        }
    }

    pub fn __add__(&self, other: &Vec3d) -> Self {
        Vec3d {
            inner: self.inner + &other.inner
        }
    }

    pub fn __sub__(&self, other: &Vec3d) -> Self {
        Vec3d {
            inner: &self.inner - &other.inner
        }
    }

    pub fn __mul__(&self, rhs: f64) -> Self {
        Vec3d {
            inner: &self.inner * rhs
        }
    }

    pub fn __rmul__(&self, lhs: f64) -> Self {
        Vec3d {
            inner: lhs * self.inner
        }
    }

    pub fn __truediv__(&self, rhs: f64) -> Self {
        Vec3d {
            inner: self.inner / rhs
        }
    }

    pub fn __neg__(&self) -> Self {
        Vec3d { inner: -self.inner }
    }

    pub fn __getitem__(&self, index: usize) -> PyResult<f64> {
        if index > 2 {
            Err(pyo3::exceptions::PyIndexError::new_err(
                "Index out of bounds"
            ))
        } else {
            Ok(self.inner[index])
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "Vec3d({}, {}, {})",
            self.inner.x, self.inner.y, self.inner.z
        )
    }
}
