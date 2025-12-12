use std::fmt::Display;
use std::io;

use pyo3::PyErr;

#[derive(Debug)]
pub enum HgMmapError {
    InvalidHeader,
    InvalidVersion,
    InvalidRootCategory(u32),
    InvalidDataLength { expected: usize, actual: usize },
    MemoryMapError(io::Error),
    Utf16ConversionError(std::string::FromUtf16Error),
    NotInitialized,
    IndexOutOfRange,
    GuidCreationError(String),
    RefEnumeratorIndexOutOfRange,
    SerializationError(String),
}

impl Display for HgMmapError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidHeader => write!(f, "Invalid header"),
            Self::InvalidVersion => write!(f, "Invalid version"),
            Self::InvalidRootCategory(id) => write!(f, "Invalid root category: {id}"),
            Self::InvalidDataLength { expected, actual } => {
                write!(
                    f,
                    "Invalid data length: expected {expected} bytes, got {actual}"
                )
            }
            Self::MemoryMapError(err) => write!(f, "Memory map error: {err}"),
            Self::Utf16ConversionError(err) => write!(f, "UTF-16 conversion error: {err}"),
            Self::NotInitialized => write!(f, "Not initialized"),
            Self::IndexOutOfRange => write!(f, "Index out of range"),
            Self::GuidCreationError(err) => {
                write!(f, "GUID creation error: {err}")
            }
            Self::RefEnumeratorIndexOutOfRange => {
                write!(f, "RefEnumerator index out of range")
            }
            Self::SerializationError(err) => write!(f, "Serialization error: {err}"),
        }
    }
}

impl From<HgMmapError> for PyErr {
    fn from(err: HgMmapError) -> PyErr {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string())
    }
}

impl From<std::string::FromUtf16Error> for HgMmapError {
    fn from(err: std::string::FromUtf16Error) -> Self {
        Self::Utf16ConversionError(err)
    }
}
