#![no_std]
#![deny(missing_docs)]
#![warn(clippy::pedantic)]
#![allow(
    clippy::must_use_candidate,
    clippy::many_single_char_names,
    clippy::return_self_not_must_use
)]
#![cfg_attr(not(feature = "std"), feature(core_float_math))]
#![doc(test(attr(deny(dead_code))))]
//! A crate for 3D vector, quaternion, geometry, and matrix operations
//! plus some miscellaneous other common things.
//! This library is not focused on performance although improvements are planned

#[cfg(feature = "std")]
#[macro_use]
extern crate std;

/// Angles and angle conversions
pub mod angle;
/// Complex number operations and functions
pub mod complex;
/// 3d geometry operations and functions
pub mod geometry;
/// Internal macros
pub(crate) mod macros;
/// Functions for working with matrices
/// currently only 2x2, 3x3, and 4x4 matrices are supported
/// with functions for calculating the determinant, minor, and cofactor
/// only available on std until i get around to fixing it or <https://github.com/rust-lang/rust/issues/137578> gets merged
#[cfg(feature = "std")]
pub mod matrix;
/// Quaternion operations and functions
pub mod quat;
/// Units and unit conversions
pub mod units;
/// 3D vector operations and functions
pub mod vec3d;
