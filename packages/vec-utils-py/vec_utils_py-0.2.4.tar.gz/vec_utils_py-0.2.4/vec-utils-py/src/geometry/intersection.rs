use pyo3::prelude::*;
use vec_utils::*;

use super::super::vec3d::Vec3d;
use super::circle::Circle;
use super::plane::Plane;

#[pyfunction]
pub fn circle_circle(circle1: &Circle, circle2: &Circle) -> Option<(Vec3d, Vec3d)> {
    let result = geometry::intersection::circle_circle(&circle1.inner, &circle2.inner);
    if let Some(i) = result {
        Some((Vec3d { inner: i.0 }, Vec3d { inner: i.1 }))
    } else {
        None
    }
}

#[pyfunction]
pub fn plane_line(plane: &Plane, a: &Vec3d, b: &Vec3d) -> Option<Vec3d> {
    let result = geometry::intersection::plane_line(&plane.inner, &a.inner, &b.inner);
    if let Some(i) = result {
        Some(Vec3d { inner: i })
    } else {
        None
    }
}

#[pyfunction]
pub fn circle_point(circle: &Circle, point: &Vec3d, inner: bool) -> bool {
    geometry::intersection::circle_point(&circle.inner, &point.inner, inner)
}

#[pyfunction]
pub fn circle_point_unchecked(circle: &Circle, point: &Vec3d, inner: bool) -> bool {
    geometry::intersection::circle_point_unchecked(&circle.inner, &point.inner, inner)
}
