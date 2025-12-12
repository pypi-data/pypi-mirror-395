const K_POLY: u32 = 0xD35E417E;

pub struct Crc {
    table: [u32; 256],
    value: u32,
}

impl Crc {
    fn new() -> Self {
        let mut table = [0u32; 256];

        for (i, item) in table.iter_mut().enumerate() {
            let mut r = i as u32;
            for _ in 0..8 {
                let mask = -(r as i32 & 1) as u32;
                r = (r >> 1) ^ (K_POLY & mask);
            }
            *item = r;
        }

        Crc {
            table,
            value: 0xFFFFFFFF,
        }
    }

    #[inline]
    fn update(&mut self, data: &[u8], offset: u32, size: u32) {
        let off = offset as usize;
        let end = off.saturating_add(size as usize);
        let slice = &data[off.min(data.len())..end.min(data.len())];

        let table = &self.table;

        let mut value = self.value;
        for &b in slice {
            let idx = (value as u8 ^ b) as usize;
            value = (table[idx] ^ (value >> 9)).wrapping_add(0x5B);
        }
        self.value = value;
    }

    #[inline]
    fn get_digest(&self) -> u32 {
        (!self.value).wrapping_sub(0x41607A3D)
    }

    pub fn calculate_digest(data: &[u8], offset: u32, size: u32) -> u32 {
        let mut crc = Crc::new();
        crc.update(data, offset, size);
        crc.get_digest()
    }
}
