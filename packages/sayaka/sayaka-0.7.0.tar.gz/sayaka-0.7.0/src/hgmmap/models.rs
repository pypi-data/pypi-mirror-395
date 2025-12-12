use crate::hgmmap::errors::HgMmapError;
use crate::hgmmap::refs::RefValue;
use crate::hgmmap::types::{GuidProxy, RootCategory};
use crate::hgmmap::utils::{read_u32_le, read_u64_le};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Bundle {
    pub bundle_index: u32,
    pub name: String,
    pub hash_name_string: String,
    pub dependencies: Vec<u32>,
    pub direct_reverse_dependencies: Vec<u32>,
    pub direct_dependencies: Vec<u32>,
    pub bundle_flags: u32,
    pub hash_name: u64,
    pub hash_version: u64,
    pub category: RootCategory,
}

impl Bundle {
    pub fn from_bytes(
        data: &[u8],
    ) -> Result<(Self, RefValue, RefValue, RefValue, RefValue, RefValue), HgMmapError> {
        let bundle_index = read_u32_le(&data[0..4])?;
        let name_offset = read_u32_le(&data[4..8])?;
        let hash_name_string_offset = read_u32_le(&data[8..12])?;
        let dependencies_offset = read_u32_le(&data[12..16])?;
        let direct_reverse_dependencies_offset = read_u32_le(&data[16..20])?;
        let direct_dependencies_offset = read_u32_le(&data[20..24])?;
        let bundle_flags = read_u32_le(&data[24..28])?;
        let hash_name = read_u64_le(&data[28..36])?;
        let hash_version = read_u64_le(&data[36..44])?;
        let category_value = read_u32_le(&data[44..48])?;
        let category = RootCategory::try_from(category_value)?;

        let bundle = Bundle {
            bundle_index,
            name: String::new(),
            hash_name_string: String::new(),
            dependencies: Vec::new(),
            direct_reverse_dependencies: Vec::new(),
            direct_dependencies: Vec::new(),
            bundle_flags,
            hash_name,
            hash_version,
            category,
        };

        Ok((
            bundle,
            RefValue::new(name_offset),
            RefValue::new(hash_name_string_offset),
            RefValue::new(dependencies_offset),
            RefValue::new(direct_reverse_dependencies_offset),
            RefValue::new(direct_dependencies_offset),
        ))
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AssetInfo {
    pub path_hash_head: u64,
    pub path: String,
    pub guid: GuidProxy,
    pub sub_asset_name_hash: u32,
    pub file_id: u64,
    pub bundle_index: u32,
}

impl AssetInfo {
    pub fn from_bytes(data: &[u8]) -> Result<(Self, RefValue), HgMmapError> {
        let path_hash_head = read_u64_le(&data[0..8])?;
        let path_offset = read_u32_le(&data[8..12])?;

        let guid = GuidProxy::new(&data[12..28])?;

        let sub_asset_name_hash = read_u32_le(&data[28..32])?;
        let file_id = read_u64_le(&data[32..40])?;
        let bundle_index = read_u32_le(&data[40..44])?;

        let asset_info = AssetInfo {
            path_hash_head,
            path: String::new(),
            guid,
            sub_asset_name_hash,
            file_id,
            bundle_index,
        };

        Ok((asset_info, RefValue::new(path_offset)))
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ManifestData {
    pub bundles: Vec<Bundle>,
    pub asset_infos: Vec<AssetInfo>,
}
