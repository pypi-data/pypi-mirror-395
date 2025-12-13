/// Functions for working with 2x2 matrices
pub mod matrix2x2 {
    use crate::complex::Complex;

    /// Calculate the determinant of a 2x2 matrix
    pub fn determinant(matrix: &[[f64; 2]; 2]) -> f64 {
        matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    }

    /// Calculate the eigenvalues of a 2x2 matrix
    /// returns a tuple of the eigenvalues as complex numbers
    pub fn eigenvalues(matrix: &[[f64; 2]; 2]) -> (Complex, Complex) {
        let mean = f64::midpoint(matrix[0][0], matrix[1][1]);
        let determinant = determinant(matrix);
        let discriminant = mean.powi(2) - determinant;
        let eigenvalue1 = Complex::new(mean, 0.0) + Complex::sqrt(discriminant);
        let eigenvalue2 = Complex::new(mean, 0.0) - Complex::sqrt(discriminant);
        (eigenvalue1, eigenvalue2)
    }

    /// Calculate the eigenvectors of a 2x2 matrix
    /// returns a tuple of the eigenvectors as 2D arrays
    pub fn eigenvectors(matrix: &[[f64; 2]; 2]) -> ([f64; 2], [f64; 2]) {
        let (eigenvalue1, eigenvalue2) = eigenvalues(matrix);
        let mut eigenvector1 = [0.0; 2];
        let mut eigenvector2 = [0.0; 2];
        if eigenvalue1.imaginary == 0.0 {
            if matrix[0][0] - eigenvalue1.real != 0.0 {
                eigenvector1[0] = matrix[0][1] / (matrix[0][0] - eigenvalue1.real);
                eigenvector1[1] = 1.0;
            } else if matrix[1][0] != 0.0 {
                eigenvector1[0] = 1.0;
                eigenvector1[1] = matrix[1][1] / (matrix[1][0] - eigenvalue1.real);
            }
        }
        if eigenvalue2.imaginary == 0.0 {
            if matrix[0][0] - eigenvalue2.real != 0.0 {
                eigenvector2[0] = matrix[0][1] / (matrix[0][0] - eigenvalue2.real);
                eigenvector2[1] = 1.0;
            } else if matrix[1][0] != 0.0 {
                eigenvector2[0] = 1.0;
                eigenvector2[1] = matrix[1][1] / (matrix[1][0] - eigenvalue2.real);
            }
        }
        (eigenvector1, eigenvector2)
    }
}

/// Functions for working with 3x3 matrices
pub mod matrix3x3 {
    use crate::vec3d::Vec3d;

    /// Calculate the determinant of a 3x3 matrix
    pub fn determinant(matrix: &[[f64; 3]; 3]) -> f64 {
        matrix[0][0] * matrix[1][1] * matrix[2][2]
            + matrix[0][1] * matrix[1][2] * matrix[2][0]
            + matrix[0][2] * matrix[1][0] * matrix[2][1]
            - matrix[0][2] * matrix[1][1] * matrix[2][0]
            - matrix[0][1] * matrix[1][0] * matrix[2][2]
            - matrix[0][0] * matrix[1][2] * matrix[2][1]
    }

    /// Calculate the minor of a 3x3 matrix given a row and column index
    pub fn minor(matrix: &[[f64; 3]; 3], row: usize, col: usize) -> f64 {
        let mut minor = [[0.0; 2]; 2];
        for i in 0..3 {
            for j in 0..3 {
                if i != row && j != col {
                    let mut m = i;
                    let mut n = j;
                    if i > row {
                        m -= 1;
                    }
                    if j > col {
                        n -= 1;
                    }
                    minor[m][n] = matrix[i][j];
                }
            }
        }
        super::matrix2x2::determinant(&minor)
    }

    /// Calculate the cofactor of a 3x3 matrix given a row and column index
    pub fn cofactor(matrix: &[[f64; 3]; 3], row: usize, col: usize) -> f64 {
        let minor = minor(matrix, row, col);
        let factor = [[1.0, -1.0, 1.0], [-1.0, 1.0, -1.0], [1.0, -1.0, 1.0]];
        factor[row][col] * minor
    }

    /// Get the cofactor matrix of a 3x3 matrix
    pub fn cofactor_matrix(matrix: &[[f64; 3]; 3]) -> [[f64; 3]; 3] {
        let mut cofactor_matrix = [[0.0; 3]; 3];
        for i in 0..3 {
            for j in 0..3 {
                cofactor_matrix[i][j] = cofactor(matrix, i, j);
            }
        }
        cofactor_matrix
    }

    /// Transpose a 3x3 matrix
    /// i.e. swap the rows and columns
    pub fn transpose(matrix: &[[f64; 3]; 3]) -> [[f64; 3]; 3] {
        let mut transpose = [[0.0; 3]; 3];
        for i in 0..3 {
            for j in 0..3 {
                transpose[i][j] = matrix[j][i];
            }
        }
        transpose
    }

    /// Calculate the adjoint of a 3x3 matrix
    /// i.e. the transpose of the cofactor matrix
    pub fn adjoint(matrix: &[[f64; 3]; 3]) -> [[f64; 3]; 3] {
        let cofactor_matrix = cofactor_matrix(matrix);
        let transpose_matrix = transpose(&cofactor_matrix);
        dbg!(cofactor_matrix);
        dbg!(transpose_matrix);
        transpose_matrix
    }

    /// Vector multiplication of a matrix with a Vec3d
    pub fn mul(matrix: &[[f64; 3]; 3], vector: &Vec3d) -> Vec3d {
        let mut result: [f64; 3] = [0.0; 3];
        for (i, j) in matrix.iter().enumerate() {
            // result[i] = vector.dot(Vec3d::from_slice(j));
            result[i] = Vec3d::from_slice(j).dot(vector);
        }
        Vec3d::from_slice(&result)
    }

    // Calculate the eigenvalues of a 3x3 matrix
    // returns a tuple of the eigenvalues as complex numbers
    // pub fn eigenvalues(matrix: &[[f64; 3]; 3]) -> (Complex, Complex, Complex) {
    //
    // }
}

/// Functions for working with 4x4 matrices
pub mod matrix4x4 {
    /// Calculate the determinant of a 4x4 matrix
    pub fn determinant(matrix: &[[f64; 4]; 4]) -> f64 {
        matrix[0][0] * matrix[1][1] * matrix[2][2] * matrix[3][3]
            + matrix[0][0] * matrix[1][2] * matrix[2][3] * matrix[3][1]
            + matrix[0][0] * matrix[1][3] * matrix[2][1] * matrix[3][2]
            + matrix[0][1] * matrix[1][0] * matrix[2][3] * matrix[3][2]
            + matrix[0][1] * matrix[1][2] * matrix[2][0] * matrix[3][3]
            + matrix[0][1] * matrix[1][3] * matrix[2][2] * matrix[3][0]
            + matrix[0][2] * matrix[1][0] * matrix[2][1] * matrix[3][3]
            + matrix[0][2] * matrix[1][1] * matrix[2][3] * matrix[3][0]
            + matrix[0][2] * matrix[1][3] * matrix[2][0] * matrix[3][1]
            + matrix[0][3] * matrix[1][0] * matrix[2][2] * matrix[3][1]
            + matrix[0][3] * matrix[1][1] * matrix[2][0] * matrix[3][2]
            + matrix[0][3] * matrix[1][2] * matrix[2][1] * matrix[3][0]
            - matrix[0][0] * matrix[1][1] * matrix[2][3] * matrix[3][2]
            - matrix[0][0] * matrix[1][2] * matrix[2][1] * matrix[3][3]
            - matrix[0][0] * matrix[1][3] * matrix[2][2] * matrix[3][1]
            - matrix[0][1] * matrix[1][0] * matrix[2][2] * matrix[3][3]
            - matrix[0][1] * matrix[1][2] * matrix[2][3] * matrix[3][0]
            - matrix[0][1] * matrix[1][3] * matrix[2][0] * matrix[3][2]
            - matrix[0][2] * matrix[1][0] * matrix[2][3] * matrix[3][1]
            - matrix[0][2] * matrix[1][1] * matrix[2][0] * matrix[3][3]
            - matrix[0][2] * matrix[1][3] * matrix[2][1] * matrix[3][0]
            - matrix[0][3] * matrix[1][0] * matrix[2][1] * matrix[3][2]
            - matrix[0][3] * matrix[1][1] * matrix[2][2] * matrix[3][0]
            - matrix[0][3] * matrix[1][2] * matrix[2][0] * matrix[3][1]
    }

    /// Calculate the minor of a 4x4 matrix given a row and column index
    pub fn minor(matrix: &[[f64; 4]; 4], row: usize, col: usize) -> f64 {
        let mut minor = [[0.0; 3]; 3];
        for i in 0..4 {
            for j in 0..4 {
                if i != row && j != col {
                    let mut m = i;
                    let mut n = j;
                    if i > row {
                        m -= 1;
                    }
                    if j > col {
                        n -= 1;
                    }
                    minor[m][n] = matrix[i][j];
                }
            }
        }
        super::matrix3x3::determinant(&minor)
    }

    /// Calculate the cofactor of a 4x4 matrix given a row and column index
    pub fn cofactor(matrix: &[[f64; 4]; 4], row: usize, col: usize) -> f64 {
        let minor = minor(matrix, row, col);
        let factor = [
            [1.0, -1.0, 1.0, -1.0],
            [-1.0, 1.0, -1.0, 1.0],
            [1.0, -1.0, 1.0, -1.0],
            [-1.0, 1.0, -1.0, 1.0]
        ];
        factor[row][col] * minor
    }
}

#[cfg(test)]
mod tests {
    mod tests2x2 {
        use super::super::matrix2x2;

        #[test]
        fn test_matrix2x2_determinant() {
            let matrix = [[1.0, 2.0], [3.0, 4.0]];
            assert_eq!(matrix2x2::determinant(&matrix), -2.0);
        }

        #[test]
        fn test_matrix2x2_eigenvalues() {
            let matrix = [[8.0, 4.0], [4.0, 8.0]];
            let (eigenvalue1, eigenvalue2) = matrix2x2::eigenvalues(&matrix);
            assert_eq!(eigenvalue1.real, 12.0);
            assert_eq!(eigenvalue1.imaginary, 0.0);
            assert_eq!(eigenvalue2.real, 4.0);
            assert_eq!(eigenvalue2.imaginary, 0.0);
        }

        #[test]
        fn test_matrix2x2_eigenvectors() {
            let matrix = [[8.0, 4.0], [4.0, 8.0]];
            let (eigenvector1, eigenvector2) = matrix2x2::eigenvectors(&matrix);
            assert_eq!(eigenvector1[0], -1.0);
            assert_eq!(eigenvector1[1], 1.0);
            assert_eq!(eigenvector2[0], 1.0);
            assert_eq!(eigenvector2[1], 1.0);
        }
    }

    mod tests3x3 {
        use super::super::matrix3x3;

        #[test]
        fn test_matrix3x3_determinant() {
            let matrix = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]];
            assert_eq!(matrix3x3::determinant(&matrix), 0.0);
        }

        #[test]
        fn test_matrix3x3_minor() {
            let matrix = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]];
            assert_eq!(matrix3x3::minor(&matrix, 0, 0), -3.0);
        }

        #[test]
        fn test_matrix3x3_cofactor() {
            let matrix = [[1.0, 4.0, 7.0], [3.0, 0.0, 5.0], [-1.0, 9.0, 11.0]];
            assert_eq!(matrix3x3::cofactor(&matrix, 1, 2), -13.0);
            assert_eq!(matrix3x3::cofactor(&matrix, 2, 0), 20.0);
        }

        #[test]
        fn test_matrix3x3_cofactor_matrix() {
            let matrix = [[1.0, 4.0, 7.0], [3.0, 0.0, 5.0], [-1.0, 9.0, 11.0]];
            let cofactor = [
                [-45.0, -38.0, 27.0],
                [19.0, 18.0, -13.0],
                [20.0, 16.0, -12.0]
            ];
            let cofactor_matrix = matrix3x3::cofactor_matrix(&matrix);
            assert_eq!(cofactor_matrix[0][0], cofactor[0][0]);
            assert_eq!(cofactor_matrix[0][1], cofactor[0][1]);
            assert_eq!(cofactor_matrix[0][2], cofactor[0][2]);
            assert_eq!(cofactor_matrix[1][0], cofactor[1][0]);
            assert_eq!(cofactor_matrix[1][1], cofactor[1][1]);
            assert_eq!(cofactor_matrix[1][2], cofactor[1][2]);
            assert_eq!(cofactor_matrix[2][0], cofactor[2][0]);
            assert_eq!(cofactor_matrix[2][1], cofactor[2][1]);
            assert_eq!(cofactor_matrix[2][2], cofactor[2][2]);
        }

        #[test]
        fn test_matrix3x3_transpose() {
            let matrix = [[1.0, 4.0, 7.0], [3.0, 0.0, 5.0], [-1.0, 9.0, 11.0]];
            let transpose = [[1.0, 3.0, -1.0], [4.0, 0.0, 9.0], [7.0, 5.0, 11.0]];
            let transpose_matrix = matrix3x3::transpose(&matrix);
            assert_eq!(transpose_matrix[0][0], transpose[0][0]);
            assert_eq!(transpose_matrix[0][1], transpose[0][1]);
            assert_eq!(transpose_matrix[0][2], transpose[0][2]);
            assert_eq!(transpose_matrix[1][0], transpose[1][0]);
            assert_eq!(transpose_matrix[1][1], transpose[1][1]);
            assert_eq!(transpose_matrix[1][2], transpose[1][2]);
            assert_eq!(transpose_matrix[2][0], transpose[2][0]);
            assert_eq!(transpose_matrix[2][1], transpose[2][1]);
            assert_eq!(transpose_matrix[2][2], transpose[2][2]);
        }

        #[test]
        fn test_matrix3x3_adjoint() {
            let matrix = [[1.0, 4.0, 7.0], [3.0, 0.0, 5.0], [-1.0, 9.0, 11.0]];
            let adjoint = [
                [-45.0, 19.0, 20.0],
                [-38.0, 18.0, 16.0],
                [27.0, -13.0, -12.0]
            ];
            let adjoint_matrix = matrix3x3::adjoint(&matrix);
            dbg!(adjoint_matrix);
            assert_eq!(adjoint_matrix[0][0], adjoint[0][0]);
            assert_eq!(adjoint_matrix[0][1], adjoint[0][1]);
            assert_eq!(adjoint_matrix[0][2], adjoint[0][2]);
            assert_eq!(adjoint_matrix[1][0], adjoint[1][0]);
            assert_eq!(adjoint_matrix[1][1], adjoint[1][1]);
            assert_eq!(adjoint_matrix[1][2], adjoint[1][2]);
            assert_eq!(adjoint_matrix[2][0], adjoint[2][0]);
            assert_eq!(adjoint_matrix[2][1], adjoint[2][1]);
            assert_eq!(adjoint_matrix[2][2], adjoint[2][2]);
        }
    }

    mod tests4x4 {
        use super::super::matrix4x4;

        #[test]
        fn test_matrix4x4_determinant() {
            let matrix = [
                [1.0, 2.0, 3.0, 4.0],
                [5.0, 6.0, 7.0, 8.0],
                [9.0, 10.0, 11.0, 12.0],
                [13.0, 14.0, 15.0, 16.0]
            ];
            assert_eq!(matrix4x4::determinant(&matrix), 0.0);
        }

        #[test]
        fn test_matrix4x4_minor() {
            let matrix = [
                [1.0, 2.0, 3.0, 4.0],
                [5.0, 6.0, 7.0, 8.0],
                [9.0, 10.0, 11.0, 12.0],
                [13.0, 14.0, 15.0, 16.0]
            ];
            assert_eq!(matrix4x4::minor(&matrix, 0, 0), 0.0);
        }

        #[test]
        fn test_matrix4x4_cofactor() {
            let matrix = [
                [1.0, 2.0, 3.0, 4.0],
                [5.0, 6.0, 7.0, 8.0],
                [9.0, 10.0, 11.0, 12.0],
                [13.0, 14.0, 15.0, 16.0]
            ];
            assert_eq!(matrix4x4::cofactor(&matrix, 0, 0), 0.0);
        }
    }
}
