use std::fmt::Display;

use serde::{Deserialize, Serialize};

use crate::hgmmap::errors::HgMmapError;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[repr(u32)]
pub enum RootCategory {
    Main = 0,
    Initial = 1,
    ENum = 2,
}

impl TryFrom<u32> for RootCategory {
    type Error = HgMmapError;

    fn try_from(value: u32) -> Result<Self, Self::Error> {
        match value {
            0 => Ok(RootCategory::Main),
            1 => Ok(RootCategory::Initial),
            2 => Ok(RootCategory::ENum),
            _ => Err(HgMmapError::InvalidRootCategory(value)),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GuidProxy {
    pub val0: u32,
    pub val1: u32,
    pub val2: u32,
    pub val3: u32,
}

impl Display for GuidProxy {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{:08x}-{:04x}-{:04x}-{:04x}-{:04x}{:08x}",
            self.val0,
            self.val1 >> 16,
            self.val1 & 0xFFFF,
            self.val2 >> 16,
            self.val2 & 0xFFFF,
            self.val3
        )
    }
}

impl GuidProxy {
    pub fn new(data: &[u8]) -> Result<Self, HgMmapError> {
        if data.len() != 16 {
            return Err(HgMmapError::GuidCreationError(
                "GUID must be 16 bytes".to_string(),
            ));
        }

        let val0 = u32::from_le_bytes([data[0], data[1], data[2], data[3]]);
        let val1 = u32::from_le_bytes([data[4], data[5], data[6], data[7]]);
        let val2 = u32::from_le_bytes([data[8], data[9], data[10], data[11]]);
        let val3 = u32::from_le_bytes([data[12], data[13], data[14], data[15]]);

        Ok(GuidProxy {
            val0,
            val1,
            val2,
            val3,
        })
    }
}
