use core::f64;

use crate::vec3d::Vec3d;

/// A plane in 3D space
#[derive(Copy, Clone, Debug)]
pub struct Plane {
    /// The normal vector of the plane
    pub normal: Vec3d,
    /// The distance from the origin to the plane
    pub distance: f64
}

impl Plane {
    /// Create a new plane
    pub fn new(normal: &Vec3d, distance: f64) -> Plane {
        Plane {
            normal: normal.normalize(),
            distance
        }
    }

    /// Create a new plane from a normal and a point on the plane
    /// The normal points outward from the origin
    pub fn from_point(normal: &Vec3d, point: &Vec3d) -> Plane {
        let dot = normal.dot(point);
        // if dot >= 0.0 {
        //     Plane {
        //         normal: normal.normalize(),
        //         distance: dot
        //     }
        // } else {
        //     Plane {
        //         normal: -normal.normalize(),
        //         distance: -dot
        //     }
        // }
        Plane {
            normal: normal.normalize(),
            distance: -dot
        }
    }

    /// The XY plane
    pub fn xy() -> Plane {
        Plane::new(&Vec3d::k(), 0.0)
    }

    /// The XZ plane
    pub fn xz() -> Plane {
        Plane::new(&Vec3d::j(), 0.0)
    }

    /// The YZ plane
    pub fn yz() -> Plane {
        Plane::new(&Vec3d::i(), 0.0)
    }

    /// Create a plane from three points
    pub fn from_points(point1: &Vec3d, point2: &Vec3d, point3: &Vec3d) -> Plane {
        let normal = (point2 - point1).cross(&(point3 - point1));
        Plane::from_point(&normal, point1)
    }

    /// Get the unsigned distance from a point to the plane
    pub fn distance_to_point(&self, point: &Vec3d) -> f64 {
        self.normal.x * point.x + self.normal.y * point.y + self.normal.z * point.z + self.distance
    }

    /// Calculate if a point lies on the plane
    pub fn contains_point(&self, point: &Vec3d) -> bool {
        self.distance_to_point(point) < f64::EPSILON
    }
}

impl PartialEq for Plane {
    fn eq(&self, other: &Self) -> bool {
        if self.normal == other.normal {
            self.distance == other.distance
        } else if self.normal == -other.normal {
            self.distance == -other.distance
        } else {
            false
        }
    }
}

#[cfg(test)]
mod tests {
    use assert_float_eq::assert_f64_near;
    use pretty_assertions::assert_eq;

    use super::*;
    use crate::angle::AngleRadians;
    use crate::vec3d::Vec3d;

    #[test]
    fn test_new() {
        let plane = Plane::new(&Vec3d::i(), 5.0);
        assert_f64_near!(plane.distance, 5.0);
        assert_eq!(plane.normal, Vec3d::i());
    }

    #[test]
    fn test_from_point() {
        let point = Vec3d::k();
        let plane = Plane::from_point(&Vec3d::j(), &point);
        let good = Plane::new(&Vec3d::j(), 0.0);
        assert_eq!(plane, good);
    }

    #[test]
    fn test_xy_yz_xz() {
        assert_eq!(Plane::xy(), Plane::new(&Vec3d::k(), 0.0));
        assert_eq!(Plane::xz(), Plane::new(&Vec3d::j(), 0.0));
        assert_eq!(Plane::yz(), Plane::new(&Vec3d::i(), 0.0));
    }

    #[test]
    fn test_from_points() {
        let v1 = Vec3d::zero();
        let v2 = Vec3d::j();
        let v3 = Vec3d::i();
        let plane = Plane::from_points(&v1, &v2, &v3);
        let good = Plane::new(&Vec3d::k(), 0.0);
        assert_eq!(plane, good);
    }

    #[test]
    fn test_distance_to_point() {
        let plane = Plane::xy();
        let v1 = Vec3d::i();
        let v2 = Vec3d::k();
        let v3 = Vec3d::new(3.0, -56.0, -5.0);
        assert_f64_near!(plane.distance_to_point(&v1), 0.0);
        assert_f64_near!(plane.distance_to_point(&v2), 1.0);
        assert_f64_near!(plane.distance_to_point(&v3), -5.0);
        let v = Vec3d::new(1.0, 1.0, 0.0);
        let plane = Plane::new(&v, 1.0);
        let v1 = Vec3d::zero();
        let v2 = Vec3d::new(
            (AngleRadians::quarter_pi() + AngleRadians::half_pi()).cos(),
            (AngleRadians::quarter_pi() + AngleRadians::half_pi()).sin(),
            0.0
        );
        assert_f64_near!(plane.distance_to_point(&v1), 1.0);
        assert_f64_near!(plane.distance_to_point(&v2), 1.0);
        assert_f64_near!(plane.distance_to_point(&v.normalize()), 0.0);
    }

    #[test]
    fn test_contains_point() {
        let plane = Plane::xz();
        let v1 = Vec3d::i();
        let v2 = Vec3d::j();
        let v3 = Vec3d::k();
        assert_eq!(plane.contains_point(&v1), true);
        assert_eq!(plane.contains_point(&v2), false);
        assert_eq!(plane.contains_point(&v3), true);
    }
}
