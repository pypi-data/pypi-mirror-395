/// Impl for borrowed variants of an operation
#[doc(hidden)]
#[macro_export]
macro_rules! impl_dual_op_variants {
    ($trait:ident, $method:ident, $T:ty, $description:literal) => {
        // Owned + Owned
        // Must already be implemented

        // Owned + Reference
        impl<'a> $trait<&'a $T> for $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: &'a $T) -> $T {
                <$T as $trait>::$method(self, *other)
            }
        }

        // Reference + Owned
        impl<'a> $trait<$T> for &'a $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: $T) -> $T {
                <$T as $trait>::$method(*self, other)
            }
        }

        // Reference + Reference
        impl<'a, 'b> $trait<&'b $T> for &'a $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: &'b $T) -> $T {
                <$T as $trait>::$method(*self, *other)
            }
        }
    };
}

/// Comunicative impl for borrowed variants of an operation
#[doc(hidden)]
#[macro_export]
macro_rules! impl_single_op_variants_comm {
    ($trait:ident, $method:ident, $T:ty, $W:ty, $description:literal) => {
        // W first
        // Owned + Owned
        impl $trait<$T> for $W {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: $T) -> $T {
                <$T as $trait<$W>>::$method(other, self)
            }
        }

        // Owned + Reference
        impl<'a> $trait<&'a $T> for $W {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: &'a $T) -> $T {
                <$T as $trait<$W>>::$method(*other, self)
            }
        }

        // Reference + Owned
        impl<'a> $trait<$T> for &'a $W {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: $T) -> $T {
                <$T as $trait<$W>>::$method(other, *self)
            }
        }

        // Reference + Reference
        impl<'a, 'b> $trait<&'b $T> for &'a $W {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: &'b $T) -> $T {
                <$T as $trait<$W>>::$method(*other, *self)
            }
        }
    };
}

/// Impl for borrowed variants of an operation without communicative property
#[doc(hidden)]
#[macro_export]
macro_rules! impl_single_op_variants {
    ($trait:ident, $method:ident, $T:ty, $W:ty, $description:literal) => {
        // T first
        // Owned + Owned
        // Must already be implemented

        // Owned + Reference
        impl<'a> $trait<&'a $W> for $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: &'a $W) -> $T {
                <$T as $trait<$W>>::$method(self, *other)
            }
        }

        // Reference + Owned
        impl<'a> $trait<$W> for &'a $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: $W) -> $T {
                <$T as $trait<$W>>::$method(*self, other)
            }
        }

        // Reference + Reference
        impl<'a, 'b> $trait<&'b $W> for &'a $T {
            type Output = $T;

            #[doc = $description]
            fn $method(self, other: &'b $W) -> $T {
                <$T as $trait<$W>>::$method(*self, *other)
            }
        }
    };
}

/// Comunicative and normal impl for borrowed variants of an operation
#[doc(hidden)]
#[macro_export]
macro_rules! impl_single_op_comm {
    ($trait:ident, $method:ident, $op:tt, $T:ty, $W:ty, $description:literal) => {
        // Must be locally defined
        impl_single_op!($trait, $method, $op, $T, $W, $description);
        impl_single_op_variants_comm!($trait, $method, $T, $W, $description);
    };
}

/// Impl for borrowed variants of an operation without communicative property that produces the rhs
/// type
#[doc(hidden)]
#[macro_export]
macro_rules! impl_single_op_variants_other {
    ($trait:ident, $method:ident, $T:ty, $W:ty, $description:literal) => {
        // T first
        // Owned + Owned
        // Must already be implemented

        // Owned + Reference
        impl<'a> $trait<&'a $W> for $T {
            type Output = $W;

            #[doc = $description]
            fn $method(self, other: &'a $W) -> $W {
                <$T as $trait<$W>>::$method(self, *other)
            }
        }

        // Reference + Owned
        impl<'a> $trait<$W> for &'a $T {
            type Output = $W;

            #[doc = $description]
            fn $method(self, other: $W) -> $W {
                <$T as $trait<$W>>::$method(*self, other)
            }
        }

        // Reference + Reference
        impl<'a, 'b> $trait<&'b $W> for &'a $T {
            type Output = $W;

            #[doc = $description]
            fn $method(self, other: &'b $W) -> $W {
                <$T as $trait<$W>>::$method(*self, *other)
            }
        }
    };
}
