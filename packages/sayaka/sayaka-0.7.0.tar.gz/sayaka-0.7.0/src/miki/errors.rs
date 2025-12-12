use std::fmt::Display;

use pyo3::PyErr;

#[derive(Debug)]
pub enum MikiDecryptError {
    InvalidBlockIndex,
    InvalidTypeValue,
    BufferSizeMismatch { expected: usize, actual: usize },
}

impl Display for MikiDecryptError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidBlockIndex => write!(f, "Invalid block index"),
            Self::InvalidTypeValue => write!(f, "Invalid type value"),
            Self::BufferSizeMismatch { expected, actual } => {
                write!(
                    f,
                    "Buffer size mismatch: expected {expected}, actual {actual}"
                )
            }
        }
    }
}

impl From<MikiDecryptError> for PyErr {
    fn from(err: MikiDecryptError) -> PyErr {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string())
    }
}
