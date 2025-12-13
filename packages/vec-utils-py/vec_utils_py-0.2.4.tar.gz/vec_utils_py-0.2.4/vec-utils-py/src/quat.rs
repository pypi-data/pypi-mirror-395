use pyo3::prelude::*;
use vec_utils::*;

use super::angle::AngleRadians;
use super::vec3d::Vec3d;

#[pyclass]
#[derive(Debug, Copy, Clone, PartialEq)]
pub struct Quat {
    pub inner: quat::Quat
}

#[pymethods]
impl Quat {
    #[new]
    fn new(w: f64, i: f64, j: f64, k: f64) -> Self {
        Quat {
            inner: quat::Quat::new(w, i, j, k)
        }
    }

    #[staticmethod]
    fn identity() -> Self {
        Quat {
            inner: quat::Quat::identity()
        }
    }

    #[staticmethod]
    fn from_axis_angle(axis: &Vec3d, angle: AngleRadians) -> Self {
        Quat {
            inner: quat::Quat::from_axis_angle(&axis.inner, angle.inner)
        }
    }

    #[getter]
    pub fn w(&self) -> f64 {
        self.inner.w
    }

    #[getter]
    pub fn i(&self) -> f64 {
        self.inner.i
    }

    #[getter]
    pub fn j(&self) -> f64 {
        self.inner.j
    }

    #[getter]
    pub fn k(&self) -> f64 {
        self.inner.k
    }

    #[setter]
    pub fn set_w(&mut self, value: f64) {
        self.inner.w = value;
    }

    #[setter]
    pub fn set_i(&mut self, value: f64) {
        self.inner.i = value;
    }

    #[setter]
    pub fn set_j(&mut self, value: f64) {
        self.inner.j = value;
    }

    #[setter]
    pub fn set_k(&mut self, value: f64) {
        self.inner.k = value;
    }

    fn conjugate(&self) -> Self {
        Quat {
            inner: self.inner.conjugate()
        }
    }

    fn magnitude(&self) -> f64 {
        self.inner.magnitude()
    }

    fn normalize(&self) -> Quat {
        Quat {
            inner: self.inner.normalize()
        }
    }

    fn to_vec3d(&self) -> (f64, f64, f64) {
        let v = self.inner.to_vec3d();
        (v.x, v.y, v.z)
    }

    fn is_unit(&self) -> bool {
        self.inner.is_unit()
    }

    fn to_axis_angle(&self) -> (Vec3d, AngleRadians) {
        let result = self.inner.to_axis_angle();
        (Vec3d { inner: result.0 }, AngleRadians { inner: result.1 })
    }

    fn to_rotation_matrix(&self) -> [[f64; 3]; 3] {
        self.inner.to_rotation_matrix()
    }

    fn rotate(&self, v: &Vec3d) -> Vec3d {
        Vec3d {
            inner: self.inner.rotate(&v.inner)
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "Quat({}, {}, {}, {})",
            self.inner.w, self.inner.i, self.inner.j, self.inner.k
        )
    }
}
