use memmap2::Mmap;

use crate::hgmmap::errors::HgMmapError;

#[derive(Debug)]
pub struct Reader<'a> {
    mmap: &'a Mmap,
}

impl<'a> Reader<'a> {
    pub fn new(mmap: &'a Mmap) -> Self {
        Reader { mmap }
    }

    #[inline]
    pub fn read_u32(&self, pos: &mut usize) -> Result<u32, HgMmapError> {
        let value = self.read_u32_at(*pos)?;
        *pos += 4;
        Ok(value)
    }

    #[inline]
    pub fn read_u32_at(&self, pos: usize) -> Result<u32, HgMmapError> {
        self.mmap
            .get(pos..pos + 4)
            .and_then(|bytes| bytes.try_into().ok())
            .map(u32::from_le_bytes)
            .ok_or(HgMmapError::InvalidDataLength {
                expected: 4,
                actual: self.mmap.len().saturating_sub(pos),
            })
    }

    #[inline]
    pub fn read_utf16(&self, pos: &mut usize) -> Result<String, HgMmapError> {
        let length = self.read_u32(pos)? as usize;
        let byte_length = length * 2;

        let data = self.get_slice(*pos, byte_length)?;
        *pos += byte_length;

        utf16le_to_string(data)
    }

    #[inline]
    pub fn get_slice(&self, pos: usize, length: usize) -> Result<&'a [u8], HgMmapError> {
        self.mmap
            .get(pos..pos + length)
            .ok_or(HgMmapError::InvalidDataLength {
                expected: length,
                actual: self.mmap.len().saturating_sub(pos),
            })
    }
}

#[inline]
pub fn read_u32_le(data: &[u8]) -> Result<u32, HgMmapError> {
    data.get(..4)
        .and_then(|bytes| bytes.try_into().ok())
        .map(u32::from_le_bytes)
        .ok_or(HgMmapError::InvalidDataLength {
            expected: 4,
            actual: data.len(),
        })
}

#[inline]
pub fn read_u64_le(data: &[u8]) -> Result<u64, HgMmapError> {
    data.get(..8)
        .and_then(|bytes| bytes.try_into().ok())
        .map(u64::from_le_bytes)
        .ok_or(HgMmapError::InvalidDataLength {
            expected: 8,
            actual: data.len(),
        })
}

#[inline]
pub fn utf16le_to_string(data: &[u8]) -> Result<String, HgMmapError> {
    let utf16_data: Vec<u16> = data
        .chunks_exact(2)
        .map(|chunk| u16::from_le_bytes([chunk[0], chunk[1]]))
        .collect();
    String::from_utf16(&utf16_data).map_err(HgMmapError::from)
}
