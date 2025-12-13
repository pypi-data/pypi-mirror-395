use pyo3::prelude::*;
use vec_utils::*;

use super::super::vec3d::Vec3d;
use super::plane::Plane;

#[pyclass]
#[derive(Debug, Clone, Copy)]
pub struct Circle {
    pub inner: geometry::circle::Circle
}

#[pymethods]
impl Circle {
    #[new]
    fn new(center: &Vec3d, radius: f64, normal: &Vec3d) -> Self {
        Circle {
            inner: geometry::circle::Circle::new(&center.inner, radius, &normal.inner)
        }
    }

    #[staticmethod]
    pub fn none() -> Self {
        Circle {
            inner: geometry::circle::Circle::new(&vec3d::Vec3d::zero(), 0.0, &vec3d::Vec3d::zero())
        }
    }

    #[getter]
    pub fn center(&self) -> Vec3d {
        Vec3d {
            inner: self.inner.center
        }
    }

    #[getter]
    pub fn normal(&self) -> Vec3d {
        Vec3d {
            inner: self.inner.normal
        }
    }

    #[getter]
    pub fn radius(&self) -> f64 {
        self.inner.radius
    }

    #[setter]
    pub fn set_radius(&mut self, value: f64) {
        self.inner.radius = value;
    }

    #[setter]
    pub fn set_center(&mut self, value: Vec3d) {
        self.inner.center = value.inner;
    }

    #[setter]
    pub fn set_normal(&mut self, value: Vec3d) {
        self.inner.normal = value.inner;
    }

    #[getter]
    pub fn area(&self) -> f64 {
        self.inner.get_area()
    }

    fn get_plane(&self) -> Plane {
        Plane {
            inner: self.inner.get_plane()
        }
    }

    fn in_same_plane(&self, other: &Circle) -> bool {
        self.inner.in_same_plane(&other.inner)
    }

    fn is_degenerate(&self) -> bool {
        self.inner.is_degenerate()
    }

    fn __eq__(&self, other: &Circle) -> bool {
        self.inner == other.inner
    }
}
