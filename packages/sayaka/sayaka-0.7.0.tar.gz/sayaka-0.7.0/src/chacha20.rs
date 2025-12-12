use std::fmt::Display;

use pyo3::{Bound, PyAny, PyErr, PyResult, Python, ffi, pyclass, pymethods, types::PyBytes};

use crate::utils::get_python_buffer;

const ALLOWED_KEY_LENGTH: usize = 32;
const ALLOWED_NONCE_LENGTH: usize = 12;
const STATE_LENGTH: usize = 16;
const KEYSTREAM_SIZE: usize = STATE_LENGTH * 4;

#[derive(Debug)]
pub enum ChaCha20Error {
    InvalidKeyLength { expected: usize, actual: usize },
    InvalidNonceLength { expected: usize, actual: usize },
}

impl Display for ChaCha20Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidKeyLength { expected, actual } => {
                write!(
                    f,
                    "Invalid key length: expected {expected}, actual {actual}"
                )
            }
            Self::InvalidNonceLength { expected, actual } => {
                write!(
                    f,
                    "Invalid nonce length: expected {expected}, actual {actual}"
                )
            }
        }
    }
}

impl From<ChaCha20Error> for PyErr {
    fn from(err: ChaCha20Error) -> PyErr {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string())
    }
}

#[derive(Copy, Clone)]
#[pyclass]
pub struct ChaCha20 {
    state: [u32; STATE_LENGTH],
    keystream: [u8; KEYSTREAM_SIZE],
    keystream_block_idx: usize,
}

#[pymethods]
impl ChaCha20 {
    #[new]
    pub fn new(key: &[u8], nonce: &[u8], counter: u32) -> PyResult<Self> {
        let key: &[u8; 32] = key
            .try_into()
            .map_err(|_| ChaCha20Error::InvalidKeyLength {
                expected: ALLOWED_KEY_LENGTH,
                actual: key.len(),
            })?;
        let nonce: &[u8; 12] = nonce
            .try_into()
            .map_err(|_| ChaCha20Error::InvalidNonceLength {
                expected: ALLOWED_NONCE_LENGTH,
                actual: nonce.len(),
            })?;

        let mut state = [0u32; STATE_LENGTH];
        init_state(&mut state, key, nonce, counter);
        let keystream = chacha20_block(&mut state);

        Ok(ChaCha20 {
            state,
            keystream,
            keystream_block_idx: 0,
        })
    }

    pub fn work_bytes<'py>(
        &mut self,
        py: pyo3::Python<'py>,
        encrypted: &Bound<'py, PyAny>,
    ) -> PyResult<Bound<'py, PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, encrypted.len(), |data| {
            self.work_bytes_impl(encrypted);
            data.copy_from_slice(encrypted);
            Ok(())
        });

        Python::attach(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }
}

impl ChaCha20 {
    pub fn work_bytes_impl(&mut self, data: &mut [u8]) {
        let mut offset = 0;
        let len = data.len();

        unsafe {
            while offset < len {
                if self.keystream_block_idx == 64 {
                    self.keystream = chacha20_block(&mut self.state);
                    self.keystream_block_idx = 0;
                }

                let available = 64 - self.keystream_block_idx;
                let block_len = (len - offset).min(available);

                let ks_ptr = self.keystream.as_ptr().add(self.keystream_block_idx);
                let data_ptr = data.as_mut_ptr().add(offset);

                for i in 0..block_len {
                    *data_ptr.add(i) ^= *ks_ptr.add(i);
                }

                self.keystream_block_idx += block_len;
                offset += block_len;
            }
        }
    }
}

impl std::fmt::Debug for ChaCha20 {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ChaCha20")
            .field("state", &self.state)
            .field("keystream", &self.keystream)
            .field("keystream_block_idx", &self.keystream_block_idx)
            .finish()
    }
}

fn init_state(state: &mut [u32; STATE_LENGTH], key: &[u8; 32], nonce: &[u8; 12], counter: u32) {
    state[0] = 0x61707865;
    state[1] = 0x3320646e;
    state[2] = 0x79622d32;
    state[3] = 0x6b206574;

    for i in 0..8 {
        let b = &key[i * 4..i * 4 + 4];
        state[4 + i] = u32::from_le_bytes([b[0], b[1], b[2], b[3]]);
    }

    state[12] = counter;

    for i in 0..3 {
        let b = &nonce[i * 4..i * 4 + 4];
        state[13 + i] = u32::from_le_bytes([b[0], b[1], b[2], b[3]]);
    }
}

fn chacha20_block(s: &mut [u32; STATE_LENGTH]) -> [u8; KEYSTREAM_SIZE] {
    let mut x = *s;

    for _ in 0..10 {
        quarter_round(&mut x, 0, 4, 8, 12);
        quarter_round(&mut x, 1, 5, 9, 13);
        quarter_round(&mut x, 2, 6, 10, 14);
        quarter_round(&mut x, 3, 7, 11, 15);

        quarter_round(&mut x, 0, 5, 10, 15);
        quarter_round(&mut x, 1, 6, 11, 12);
        quarter_round(&mut x, 2, 7, 8, 13);
        quarter_round(&mut x, 3, 4, 9, 14);
    }

    let mut out = [0u8; KEYSTREAM_SIZE];
    for i in 0..16 {
        let v = s[i].wrapping_add(x[i]).to_le_bytes();
        out[i * 4..i * 4 + 4].copy_from_slice(&v);
    }

    let counter = s[12].wrapping_add(1);
    s[12] = counter;
    if counter == 0 {
        s[13] = s[13].wrapping_add(1);
    }

    out
}

#[inline]
fn quarter_round(x: &mut [u32], a: usize, b: usize, c: usize, d: usize) {
    x[a] = x[a].wrapping_add(x[b]);
    x[d] = (x[d] ^ x[a]).rotate_left(16);

    x[c] = x[c].wrapping_add(x[d]);
    x[b] = (x[b] ^ x[c]).rotate_left(12);

    x[a] = x[a].wrapping_add(x[b]);
    x[d] = (x[d] ^ x[a]).rotate_left(8);

    x[c] = x[c].wrapping_add(x[d]);
    x[b] = (x[b] ^ x[c]).rotate_left(7);
}
