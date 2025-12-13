use pyo3::prelude::*;
use rayon::prelude::*;
use vec_utils::*;

use super::quat::Quat;
use super::vec3d::Vec3d;

#[pyclass]
pub struct VecList {
    pub list: Vec<vec3d::Vec3d>
}

#[pymethods]
impl VecList {
    #[new]
    pub fn new(list: Vec<Vec3d>) -> Self {
        VecList {
            list: list.par_iter().map(|i| i.inner).collect()
        }
    }

    #[staticmethod]
    pub fn empty() -> Self {
        VecList {
            list: Vec::<vec3d::Vec3d>::new()
        }
    }

    #[getter]
    pub fn list(&self) -> Vec<Vec3d> {
        self.list.iter().map(|i| Vec3d { inner: *i }).collect()
    }

    pub fn rotate(&mut self, quat: &Quat) {
        let quat: quat::Quat = quat.inner;
        self.list = self.list.par_iter().map(|i| quat.rotate(i)).collect();
    }

    pub fn to_array(&self) -> Vec<[f64; 3]> {
        self.list.par_iter().map(|i| i.to_array()).collect()
    }

    pub fn magnitude(&self) -> Vec<f64> {
        self.list.par_iter().map(|i| i.magnitude()).collect()
    }

    pub fn extend(&mut self, other: &VecList) {
        self.list.extend(other.list.clone())
    }

    pub fn append(&mut self, vec: Vec3d) {
        self.list.push(vec.inner);
    }

    pub fn is_unit(&self) -> Vec<bool> {
        self.list.par_iter().map(|i| i.is_unit()).collect()
    }

    pub fn normalize(&self) -> Self {
        VecList {
            list: self.list.par_iter().map(|i| i.normalize()).collect()
        }
    }

    pub fn dot(&self, other: &Vec3d) -> Vec<f64> {
        self.list.par_iter().map(|i| i.dot(&other.inner)).collect()
    }

    pub fn cross(&self, other: &Vec3d) -> Self {
        VecList {
            list: self
                .list
                .par_iter()
                .map(|i| i.cross(&other.inner))
                .collect()
        }
    }

    pub fn collapse(&self, axis: usize) -> Self {
        assert!(axis <= 2);
        VecList {
            list: self
                .list
                .par_iter()
                .map(|i| i.collapse(axis).unwrap())
                .collect()
        }
    }

    // pub fn get_centroid(&self, axes: usize) -> (f64, f64) {
    //     let mut all_axes = vec![0, 1, 2];
    //     all_axes.remove(axes);
    //     let axes = (all_axes[0], all_axes[1]);
    //     self.list.iter()
    //         .circular_tuple_windows()
    //         .fold((0.0, 0.0), |acc, (i, j)| {
    //             let step = i[axes.0] * j[axes.1] - j[axes.0] * i[axes.1];
    //             (
    //                 acc.0 + (i[axes.0] + j[axes.0]) * step,
    //                 acc.1 + (i[axes.1] + j[axes.1]) * step
    //             )
    //         })
    // }

    // pub fn angle_to(&self, other: &Vec3d) -> AngleRadians {
    //     AngleRadians {
    //         inner: self.inner.angle_to(&other.inner)
    //     }
    // }
    //
    // pub fn scalar_triple_product(a: PyRef<Vec3d>, b: PyRef<Vec3d>, c: PyRef<Vec3d>) -> f64 {
    //     vec3d::Vec3d::scalar_triple_product(&a.inner, &b.inner, &c.inner)
    // }

    pub fn distance_to(&self, other: &Vec3d) -> Vec<f64> {
        self.list
            // .chunks(50)
            // .collect::<Vec<&vec3d::Vec3d>>()
            .par_iter()
            .map(|i| i.distance_to(&other.inner))
            .collect()
    }

    pub fn minimum_distance_to(&self, other: &Vec3d, stride: usize) -> (usize, f64) {
        assert!(stride != 0);
        let (close, _) = self
            .list
            .par_iter()
            .enumerate()
            .step_by(stride)
            // .map(|(j, i)| (j, i.distance_to(&other.inner)))
            .map(|(j, i)| (j, i.distance_squared(&other.inner)))
            .min_by(|a, b| a.1.total_cmp(&b.1))
            .unwrap();
        let window: &[vec3d::Vec3d];
        let offset: usize;
        if close < stride {
            window = &self.list[..(close + stride)];
            offset = 0;
        } else if close + stride > self.list.len() {
            window = &self.list[(close - stride)..];
            offset = close - stride;
        } else {
            window = &self.list[(close - stride)..(close + stride)];
            offset = close - stride;
        }
        let (index, distance) = window
            .par_iter()
            .enumerate()
            // .map(|(j, i)| (j, i.distance_to(&other.inner)))
            .map(|(j, i)| (j, i.distance_squared(&other.inner)))
            .min_by(|a, b| a.1.total_cmp(&b.1))
            .unwrap();
        (index + offset, distance.sqrt())
    }

    // pub fn distance_to_line(&self, a: &Vec3d, b: &Vec3d) -> f64 {
    //     self.inner.distance_to_line(&a.inner, &b.inner)
    // }
    //
    // pub fn project_onto_plane(&self, normal: &Vec3d) -> Self {
    //     Vec3d {
    //         inner: self.inner.project_onto_plane(&normal.inner)
    //     }
    // }
    //
    // pub fn project_onto_line(&self, line_r: &Vec3d, line_q: &Vec3d) -> Self {
    //     Vec3d {
    //         inner: self.inner.project_onto_line(&line_r.inner, &line_q.inner)
    //     }
    // }

    pub fn __add__(&self, other: &Vec3d) -> Self {
        VecList {
            list: self.list.par_iter().map(|i| i + other.inner).collect()
        }
    }

    pub fn __sub__(&self, other: &Vec3d) -> Self {
        VecList {
            list: self.list.par_iter().map(|i| i - other.inner).collect()
        }
    }

    pub fn __mul__(&self, rhs: f64) -> Self {
        VecList {
            list: self.list.par_iter().map(|i| i * rhs).collect()
        }
    }

    pub fn __rmul__(&self, lhs: f64) -> Self {
        VecList {
            list: self.list.par_iter().map(|i| i * lhs).collect()
        }
    }

    pub fn __truediv__(&self, rhs: f64) -> Self {
        VecList {
            list: self.list.par_iter().map(|i| *i / rhs).collect()
        }
    }

    pub fn __len__(&self) -> usize {
        self.list.len()
    }

    pub fn __iter__(&self) -> VecListIterator {
        VecListIterator {
            iter: self.list.clone().into_iter()
        }
    }

    pub fn __getitem__(&self, index: usize) -> PyResult<Vec3d> {
        if index > self.list.len() {
            Err(pyo3::exceptions::PyIndexError::new_err(
                "Index out of bounds"
            ))
        } else {
            Ok(Vec3d {
                inner: self.list[index]
            })
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "[{}]",
            self.list
                .par_iter()
                .map(|i| { format!("Vec3d({}, {}, {})", i.x, i.y, i.z) })
                .intersperse("\n".to_string())
                .collect::<String>()
        )
    }
}

#[pyclass]
pub struct VecListIterator {
    iter: std::vec::IntoIter<vec3d::Vec3d>
}

#[pymethods]
impl VecListIterator {
    pub fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    pub fn __next__(&mut self) -> Option<Vec3d> {
        Some(Vec3d {
            inner: self.iter.next()?
        })
    }
}
