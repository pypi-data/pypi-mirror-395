mod errors;
mod models;
mod refs;
mod types;
mod utils;

use std::fs::File;
use std::io::{BufWriter, Write};

use memmap2::Mmap;
use pyo3::{PyResult, pyclass, pymethods};

use errors::HgMmapError;
use models::{AssetInfo, Bundle, ManifestData};
use refs::{RefArray, RefMultiHashTable, RefString};
use utils::Reader;

#[pyclass]
#[derive(Debug, Default)]
pub struct ManifestDataBinary {
    bundles: Option<RefArray>,
    asset_info_dictionary: Option<RefMultiHashTable>,
    hash: String,
    perforce_cl: String,
    memory_map: Option<Mmap>,
    _file: Option<File>,
    offset: usize,
    asset_info_offset: usize,
    bundle_offset: usize,
    data_offset: usize,
}

#[pymethods]
impl ManifestDataBinary {
    #[new]
    pub fn new() -> Self {
        ManifestDataBinary::default()
    }

    pub fn init_binary(&mut self, file_path: &str) -> PyResult<bool> {
        Ok(self.init_binary_impl(file_path)?)
    }

    pub fn save_to_json_file(&self, output_path: &str) -> PyResult<bool> {
        Ok(self.save_to_json_file_impl(output_path)?)
    }
}

impl ManifestDataBinary {
    const HEAD1: u32 = 4279369489;
    const HEAD2: u32 = 4059231220;
    const _VERSION: &'static str = "1.0.1";

    fn init_binary_impl(&mut self, file_path: &str) -> Result<bool, HgMmapError> {
        let file = File::open(file_path).map_err(HgMmapError::MemoryMapError)?;
        let mmap = unsafe { Mmap::map(&file).map_err(HgMmapError::MemoryMapError)? };
        let reader = Reader::new(&mmap);

        let mut position = 0;
        self.offset = position;

        // Read header 1
        let head1 = reader.read_u32(&mut position)?;
        if head1 != ManifestDataBinary::HEAD1 {
            return Ok(false);
        }

        // Read version hash
        let version_hash = reader.read_utf16(&mut position)?;
        drop(version_hash); // Not used, just validate

        // Read header 2
        let head2 = reader.read_u32(&mut position)?;
        if head2 != ManifestDataBinary::HEAD2 {
            return Ok(false);
        }

        // Read hash
        self.hash = reader.read_utf16(&mut position)?;

        // Read Perforce CL
        self.perforce_cl = reader.read_utf16(&mut position)?;

        // Read asset info dictionary
        let asset_info_dictionary_size = reader.read_u32(&mut position)? as usize;

        self.asset_info_offset = position;
        self.asset_info_dictionary = Some(RefMultiHashTable::new(&reader, self.asset_info_offset)?);
        position += asset_info_dictionary_size;

        // Read Bundle array
        let bundles_size = reader.read_u32(&mut position)? as usize;

        self.bundle_offset = position;
        self.bundles = Some(RefArray::new(&reader, self.bundle_offset)?);
        position += bundles_size;

        // Read data size
        let _data_size = reader.read_u32(&mut position)? as usize;

        self.data_offset = position;

        self.memory_map = Some(mmap);
        self._file = Some(file);

        Ok(true)
    }

    fn save_to_json_file_impl(&self, output_path: &str) -> Result<bool, HgMmapError> {
        let manifest_data = self.to_manifest_data()?;
        let file = File::create(output_path).map_err(HgMmapError::MemoryMapError)?;
        let mut writer = BufWriter::new(file);
        serde_json::to_writer_pretty(&mut writer, &manifest_data).map_err(|e| {
            HgMmapError::SerializationError(format!("Failed to serialize JSON: {e}"))
        })?;
        writer.flush().map_err(HgMmapError::MemoryMapError)?;
        Ok(true)
    }

    fn to_manifest_data(&self) -> Result<ManifestData, HgMmapError> {
        let mmap = self
            .memory_map
            .as_ref()
            .ok_or(HgMmapError::NotInitialized)?;
        let reader = Reader::new(mmap);
        let bundles_ref = self.bundles.as_ref().ok_or(HgMmapError::NotInitialized)?;
        let asset_info_dict = self
            .asset_info_dictionary
            .as_ref()
            .ok_or(HgMmapError::NotInitialized)?;

        let mut result_bundles = Vec::with_capacity(bundles_ref.length as usize);

        for i in 0..bundles_ref.length as usize {
            let bundle_data = bundles_ref.at(&reader, i, 48)?;
            let (
                mut bundle,
                name_ref,
                hash_name_ref,
                deps_ref,
                direct_reverse_deps_ref,
                direct_deps_ref,
            ) = Bundle::from_bytes(bundle_data)?;

            // Get string values
            let (_, name_offset) = name_ref.get_value(&reader, self.data_offset, 4)?;
            let name_str_ref = RefString::new(&reader, name_offset)?;
            bundle.name = name_str_ref.to_string(&reader, name_offset)?;

            let (_, hash_name_offset) = hash_name_ref.get_value(&reader, self.data_offset, 4)?;
            let hash_name_str_ref = RefString::new(&reader, hash_name_offset)?;
            bundle.hash_name_string = hash_name_str_ref.to_string(&reader, hash_name_offset)?;

            // Get dependency arrays (using the optimized RefArray::to_list_int)
            let (_, deps_offset) = deps_ref.get_value(&reader, self.data_offset, 4)?;
            let deps_array = RefArray::new(&reader, deps_offset)?;
            bundle.dependencies = deps_array.to_list_int(&reader, Some(deps_offset))?;

            let (_, direct_reverse_deps_offset) =
                direct_reverse_deps_ref.get_value(&reader, self.data_offset, 4)?;
            let direct_reverse_deps_array = RefArray::new(&reader, direct_reverse_deps_offset)?;
            bundle.direct_reverse_dependencies =
                direct_reverse_deps_array.to_list_int(&reader, Some(direct_reverse_deps_offset))?;

            let (_, direct_deps_offset) =
                direct_deps_ref.get_value(&reader, self.data_offset, 4)?;
            let direct_deps_array = RefArray::new(&reader, direct_deps_offset)?;
            bundle.direct_dependencies =
                direct_deps_array.to_list_int(&reader, Some(direct_deps_offset))?;

            result_bundles.push(bundle);
        }

        // Process AssetInfo data
        let mut result_assets = Vec::new();
        let mut enumerator = asset_info_dict.get_enumerator().with_reader(&reader);
        while enumerator.move_next()? {
            let asset_data = enumerator.get_current(48)?;
            let (mut asset_info, path_ref) = AssetInfo::from_bytes(asset_data)?;

            // Get path string
            let (_, path_offset) = path_ref.get_value(&reader, self.data_offset, 4)?;
            let path_str_ref = RefString::new(&reader, path_offset)?;
            asset_info.path = path_str_ref.to_string(&reader, path_offset)?;

            result_assets.push(asset_info);
        }

        Ok(ManifestData {
            bundles: result_bundles,
            asset_infos: result_assets,
        })
    }

    #[allow(dead_code)]
    fn to_json(&self) -> Result<String, HgMmapError> {
        let manifest_data = self.to_manifest_data()?;
        serde_json::to_string(&manifest_data)
            .map_err(|e| HgMmapError::SerializationError(format!("Failed to serialize JSON: {e}")))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test() -> Result<(), Box<dyn std::error::Error>> {
        let mut manifest = ManifestDataBinary::default();

        let file_path = "manifest.hgmmap";

        match manifest.init_binary_impl(file_path) {
            Ok(true) => {
                println!("Successfully loaded manifest binary");
                println!("Hash: {}", manifest.hash);

                manifest
                    .save_to_json_file_impl("manifest.hgmmap.json")
                    .unwrap();
                println!("Manifest data saved to manifest.hgmmap.json");
            }
            Ok(false) => {
                println!("Failed to load manifest binary");
            }
            Err(e) => {
                println!("Error loading manifest binary: {e}");
            }
        }

        Ok(())
    }
}
