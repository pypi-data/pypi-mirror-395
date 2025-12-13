#![feature(iter_intersperse)]
use pyo3::prelude::*;

mod angle;
mod geometry;
mod quat;
mod vec3d;
mod vec_list;

#[pymodule]
mod vec_utils_py {
    use super::*;
    #[pymodule_export]
    use crate::angle::AngleDegrees;
    #[pymodule_export]
    use crate::angle::AngleRadians;
    #[pymodule_export]
    use crate::quat::Quat;
    #[pymodule_export]
    use crate::vec_list::VecList;
    #[pymodule_export]
    use crate::vec3d::Vec3d;
    #[pymodule]
    mod geometry {
        #[pymodule_export]
        use crate::geometry::circle::Circle;
        #[pymodule_export]
        use crate::geometry::intersection::circle_circle;
        #[pymodule_export]
        use crate::geometry::intersection::circle_point;
        #[pymodule_export]
        use crate::geometry::intersection::circle_point_unchecked;
        #[pymodule_export]
        use crate::geometry::intersection::plane_line;
        #[pymodule_export]
        use crate::geometry::plane::Plane;
    }
}
