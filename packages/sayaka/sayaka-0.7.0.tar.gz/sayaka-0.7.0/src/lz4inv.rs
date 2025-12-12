use std::fmt::Display;

use pyo3::PyErr;

#[derive(Debug)]
pub enum DecompressError {
    OutputTooSmall { expected: usize, actual: usize },
    LiteralOutOfBounds,
    OffsetOutOfBounds,
}

impl Display for DecompressError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::OutputTooSmall { expected, actual } => {
                write!(f, "Output too small: expected {expected}, actual {actual}")
            }
            Self::LiteralOutOfBounds => write!(f, "Literal out of bounds"),
            Self::OffsetOutOfBounds => write!(f, "Offset out of bounds"),
        }
    }
}

impl From<DecompressError> for PyErr {
    fn from(err: DecompressError) -> PyErr {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string())
    }
}

pub fn decompress_impl(src: &[u8], dst: &mut [u8]) -> Result<usize, DecompressError> {
    let mut src_pos = 0;
    let mut dst_pos = 0;

    let src_len = src.len();
    let dst_len = dst.len();

    while src_pos < src_len && dst_pos < dst_len {
        let (mut match_len, mut lit_len) = get_literal_token(src, &mut src_pos);
        lit_len = get_length(lit_len, src, &mut src_pos);

        if src_pos + lit_len > src_len {
            return Err(DecompressError::LiteralOutOfBounds);
        }
        if dst_pos + lit_len > dst_len {
            return Err(DecompressError::OutputTooSmall {
                expected: dst_pos + lit_len,
                actual: dst_len,
            });
        }

        dst[dst_pos..dst_pos + lit_len].copy_from_slice(&src[src_pos..src_pos + lit_len]);

        src_pos += lit_len;
        dst_pos += lit_len;

        if src_pos >= src_len {
            break;
        }

        let offset = get_chunk_end(src, &mut src_pos);
        match_len = get_length(match_len, src, &mut src_pos) + 4;

        let (enc_pos, overflow) = dst_pos.overflowing_sub(offset);
        if overflow {
            return Err(DecompressError::OffsetOutOfBounds);
        }
        if dst_pos + match_len > dst.len() {
            return Err(DecompressError::OutputTooSmall {
                expected: dst_pos + match_len,
                actual: dst.len(),
            });
        }

        if match_len <= offset {
            dst.copy_within(enc_pos..enc_pos + match_len, dst_pos);
            dst_pos += match_len;
        } else {
            let mut match_length_remain = match_len;
            let mut curr_enc_pos = enc_pos;
            let mut curr_dst_pos = dst_pos;

            while match_length_remain > 0 {
                dst[curr_dst_pos] = dst[curr_enc_pos];
                curr_enc_pos += 1;
                curr_dst_pos += 1;
                match_length_remain -= 1;
            }

            dst_pos = curr_dst_pos;
        }
    }

    Ok(dst_pos)
}

#[inline]
fn get_literal_token(src: &[u8], src_pos: &mut usize) -> (usize, usize) {
    let token = src[*src_pos];
    *src_pos += 1;

    let lit = token & 0x33;
    let enc = (token & 0xCC) >> 2;

    (
        ((enc & 0x3) | (enc >> 2)) as usize,
        ((lit & 0x3) | (lit >> 2)) as usize,
    )
}

#[inline]
fn get_chunk_end(src: &[u8], src_pos: &mut usize) -> usize {
    let high = src[*src_pos] as usize;
    *src_pos += 1;
    let low = src[*src_pos] as usize;
    *src_pos += 1;
    (high << 8) | low
}

#[inline]
fn get_length(mut length: usize, src: &[u8], src_pos: &mut usize) -> usize {
    if length == 0xf {
        loop {
            let v = src[*src_pos] as usize;
            *src_pos += 1;
            length += v;
            if v != 0xff {
                break;
            }
        }
    }
    length
}
