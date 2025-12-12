use crate::hgmmap::errors::HgMmapError;
use crate::hgmmap::utils::{Reader, utf16le_to_string};

#[derive(Debug)]
pub struct RefString {
    pub length: u32,
}

impl RefString {
    pub fn new(reader: &Reader, offset: usize) -> Result<Self, HgMmapError> {
        let length = reader.read_u32_at(offset)?;
        Ok(RefString { length })
    }

    pub fn to_string(&self, reader: &Reader, value_offset: usize) -> Result<String, HgMmapError> {
        let string_data = reader.get_slice(value_offset + 4, self.length as usize)?;
        utf16le_to_string(string_data)
    }
}

#[derive(Debug)]
pub struct RefArray {
    pub length: u32,
    pub offset: usize,
}

impl RefArray {
    pub fn new(reader: &Reader, value_offset: usize) -> Result<Self, HgMmapError> {
        let length = reader.read_u32_at(value_offset)?;
        Ok(RefArray {
            length,
            offset: value_offset + 4,
        })
    }

    pub fn at<'a>(
        &self,
        reader: &Reader<'a>,
        index: usize,
        item_size: usize,
    ) -> Result<&'a [u8], HgMmapError> {
        if index >= self.length as usize {
            return Err(HgMmapError::IndexOutOfRange);
        }

        let index_offset = item_size * index;
        let start = self.offset + index_offset;
        reader.get_slice(start, item_size)
    }

    pub fn to_list_int(
        &self,
        reader: &Reader,
        value_offset: Option<usize>,
    ) -> Result<Vec<u32>, HgMmapError> {
        let mut result = Vec::with_capacity(self.length as usize);
        let offset = value_offset.map(|v| v + 4).unwrap_or(self.offset);

        for i in 0..self.length as usize {
            let value = reader.read_u32_at(offset + i * 4)?;
            result.push(value);
        }

        Ok(result)
    }
}

#[derive(Debug)]
pub struct RefValue {
    pub offset: u32,
}

impl RefValue {
    pub fn new(offset: u32) -> Self {
        RefValue { offset }
    }

    pub fn get_value<'a>(
        &self,
        reader: &Reader<'a>,
        data_offset: usize,
        size: usize,
    ) -> Result<(&'a [u8], usize), HgMmapError> {
        let value_offset = data_offset + self.offset as usize;
        let value_data = reader.get_slice(value_offset, size)?;
        Ok((value_data, value_offset))
    }
}

#[derive(Debug)]
pub struct RefHashSlot {
    pub offset: usize,
    pub buckets_size: u32,
}

impl RefHashSlot {
    pub fn read(reader: &Reader, pos: &mut usize) -> Result<Self, HgMmapError> {
        let offset = reader.read_u32(pos)?;
        let buckets_size = reader.read_u32(pos)?;
        Ok(RefHashSlot {
            offset: offset as usize,
            buckets_size,
        })
    }
}

#[derive(Debug)]
pub struct RefMultiHashTable {
    pub offset: usize,
    slots: Vec<RefHashSlot>,
}

impl RefMultiHashTable {
    pub fn new(reader: &Reader, position: usize) -> Result<Self, HgMmapError> {
        let capacity = reader.read_u32_at(position)?;
        let slot_offset = position + 4;

        let mut slots = Vec::with_capacity(capacity as usize);
        for i in 0..capacity as usize {
            let mut slot_pos = slot_offset + i * 8;
            let slot = RefHashSlot::read(reader, &mut slot_pos)?;
            slots.push(slot);
        }

        Ok(RefMultiHashTable {
            offset: position,
            slots,
        })
    }

    pub fn get_enumerator(&'_ self) -> RefEnumerator<'_> {
        RefEnumerator::new(self)
    }
}

#[derive(Debug)]
pub struct RefEnumerator<'a> {
    table: &'a RefMultiHashTable,
    current_index: i32,
    slot_index: usize,
    reader: Option<&'a Reader<'a>>,
}

impl<'a> RefEnumerator<'a> {
    pub fn new(table: &'a RefMultiHashTable) -> RefEnumerator<'a> {
        RefEnumerator {
            table,
            current_index: -1,
            slot_index: 0,
            reader: None,
        }
    }

    pub fn with_reader(mut self, reader: &'a Reader<'a>) -> Self {
        self.reader = Some(reader);
        self
    }

    pub fn get_current(&self, item_size: usize) -> Result<&[u8], HgMmapError> {
        let reader = self.reader.ok_or(HgMmapError::NotInitialized)?;

        if self.slot_index >= self.table.slots.len() {
            return Err(HgMmapError::RefEnumeratorIndexOutOfRange);
        }

        let slot = &self.table.slots[self.slot_index];

        if self.current_index as u32 >= slot.buckets_size {
            return Err(HgMmapError::RefEnumeratorIndexOutOfRange);
        }

        let value_offset =
            self.table.offset + slot.offset + item_size * self.current_index as usize;
        reader.get_slice(value_offset, item_size)
    }

    pub fn move_next(&mut self) -> Result<bool, HgMmapError> {
        if self.reader.is_none() {
            return Err(HgMmapError::NotInitialized);
        }

        self.current_index += 1;

        if self.slot_index >= self.table.slots.len() {
            return Ok(false);
        }

        // Use precomputed slot information
        loop {
            if self.slot_index >= self.table.slots.len() {
                return Ok(false);
            }

            let slot = &self.table.slots[self.slot_index];

            if (self.current_index as u32) < slot.buckets_size {
                break;
            }

            self.slot_index += 1;
            self.current_index = 0;
        }

        Ok(true)
    }
}
