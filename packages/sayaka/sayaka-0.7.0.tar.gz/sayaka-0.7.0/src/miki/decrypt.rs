use super::crc::Crc;
use super::crypto::rc4;
use super::errors::MikiDecryptError;
use super::utils::{bytes_to_u32_slice, generate_seed, u32_array_to_bytes};

pub fn decrypt_to_impl(src: &mut [u8], dst: &mut [u8]) -> Result<(), MikiDecryptError> {
    if src.len() != dst.len() {
        return Err(MikiDecryptError::BufferSizeMismatch {
            expected: src.len(),
            actual: dst.len(),
        });
    }

    decrypt_impl(src)?;
    dst.copy_from_slice(src);

    Ok(())
}

pub fn decrypt_impl(bytes: &mut [u8]) -> Result<(), MikiDecryptError> {
    let encrypted_size = bytes.len().min(0x500);
    if encrypted_size < 0x20 {
        return Ok(());
    }

    let encrypted = &mut bytes[..encrypted_size];

    // Convert bytes to u32 slice for manipulation
    let encrypted_ints = bytes_to_u32_slice(encrypted);
    let es_u32 = encrypted_size as u32;

    // XOR first 0x20 bytes with 0xA6
    for b in &mut encrypted[..0x20] {
        *b ^= 0xA6;
    }

    // Generate seed parts
    let seed_ints_raw = [
        encrypted_ints[2] ^ encrypted_ints[6] ^ 0x226A61B9,
        encrypted_ints[3] ^ encrypted_ints[0] ^ 0x7A39D018 ^ es_u32,
        encrypted_ints[1] ^ encrypted_ints[5] ^ 0x18F6D8AA ^ es_u32,
        encrypted_ints[0] ^ encrypted_ints[7] ^ 0xAA255FB1,
        encrypted_ints[4] ^ encrypted_ints[7] ^ 0xF78DD8EB,
    ];

    let mut seed_bytes = u32_array_to_bytes(&seed_ints_raw);

    let seed = {
        let tmp = generate_seed(&seed_bytes).to_le_bytes();
        Crc::calculate_digest(&tmp, 0, tmp.len() as u32)
    };

    let key = seed_ints_raw.iter().fold(es_u32, |acc, v| acc ^ v);
    rc4(&mut seed_bytes, &key.to_le_bytes());

    let mut seed_ints = [0u32; 4];
    for (i, seed_int) in seed_ints.iter_mut().enumerate() {
        let o = i * 4;
        *seed_int = u32::from_le_bytes([
            seed_bytes[o],
            seed_bytes[o + 1],
            seed_bytes[o + 2],
            seed_bytes[o + 3],
        ]);
    }

    let key_seed = {
        let crc = Crc::calculate_digest(&seed_bytes, 0, seed_bytes.len() as u32);
        let buf = crc.to_le_bytes();
        generate_seed(&buf)
    };

    let key_vector = [
        seed_ints[3].wrapping_sub(0x1C26B82D) ^ key_seed,
        seed_ints[2].wrapping_add(0x3F72EAF3) ^ seed,
        seed_ints[0] ^ 0x82C57E3C ^ key_seed,
        seed_ints[1].wrapping_add(0x6F2A7347) ^ seed,
    ];

    if encrypted.len() > 0x20 {
        let block = &mut encrypted[0x20..];
        let seed_le = seed.to_le_bytes();

        if block.len() >= 0x80 {
            let (left, block) = block.split_at_mut(0x60);
            rc4(left, &seed_le);

            let byte_xor = (seed ^ 0x6E) as u8;
            for b in left {
                *b ^= byte_xor;
            }

            let block_len = block.len();

            let block_size = (encrypted_size - 0x80) / 4;

            if block_size > 0 {
                const BLOCK_KEYS: [u32; 4] = [0x6142756E, 0x62496E66, 0x1304B000, 0x6E8E30EC];

                for (i, &kv) in key_vector.iter().enumerate() {
                    let offset = i * block_size;
                    if offset >= block_len {
                        break;
                    }

                    let end = (offset + block_size).min(block_len);
                    let slice = &mut block[offset..end];

                    rc4(slice, &seed_le);

                    let xor_val = seed ^ kv ^ BLOCK_KEYS[i];
                    let limit = slice.len() & !3; // u32 对齐

                    let mut idx = 0;

                    while idx < limit {
                        let mut v = u32::from_le_bytes([
                            slice[idx],
                            slice[idx + 1],
                            slice[idx + 2],
                            slice[idx + 3],
                        ]);
                        v ^= xor_val;

                        slice[idx..idx + 4].copy_from_slice(&v.to_le_bytes());
                        idx += 4;
                    }
                }
            }
        } else {
            rc4(block, &seed.to_le_bytes());
        }
    }

    Ok(())
}
