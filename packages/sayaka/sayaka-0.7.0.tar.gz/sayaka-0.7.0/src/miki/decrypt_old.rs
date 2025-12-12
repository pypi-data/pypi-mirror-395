use super::crc::Crc;
use super::crypto::rc4;
use super::errors::MikiDecryptError;
use super::utils::{bytes_to_u32_slice, generate_seed, u32_array_to_bytes};

pub fn decrypt_old_to_impl(src: &mut [u8], dst: &mut [u8]) -> Result<(), MikiDecryptError> {
    if src.len() != dst.len() {
        return Err(MikiDecryptError::BufferSizeMismatch {
            expected: src.len(),
            actual: dst.len(),
        });
    }

    decrypt_old_impl(src)?;
    dst.copy_from_slice(src);

    Ok(())
}

pub fn decrypt_old_impl(bytes: &mut [u8]) -> Result<(), MikiDecryptError> {
    let encrypted_size = bytes.len().min(0x500);
    if encrypted_size < 0x20 {
        return Ok(());
    }

    let enc_data = &mut bytes[..encrypted_size];
    let enc_len = enc_data.len();
    let enc_data_int = bytes_to_u32_slice(&enc_data[..enc_len.min(32)]);

    let mut enc_block1 = [
        enc_data_int[2] ^ enc_data_int[5] ^ 0x3F72EAF3,
        enc_data_int[3] ^ enc_data_int[7] ^ (enc_len as u32),
        enc_data_int[1] ^ enc_data_int[4] ^ (enc_len as u32) ^ 0x753BDCAA,
        enc_data_int[0] ^ enc_data_int[6] ^ 0xE3D947D3,
    ];

    let mut enc_block1_bytes = [0u8; 16];
    for (i, v) in enc_block1.iter().enumerate() {
        enc_block1_bytes[i * 4..i * 4 + 4].copy_from_slice(&v.to_le_bytes());
    }

    let enc_block2_seed = generate_seed(&enc_block1_bytes);
    let enc_block2_key = enc_block2_seed.to_le_bytes();
    let enc_block2_key_int = enc_block2_seed;

    let enc_block1_key = (enc_len as u32)
        ^ enc_block1[0]
        ^ enc_block1[1]
        ^ enc_block1[2]
        ^ enc_block1[3]
        ^ 0x5E8BC918u32;
    rc4(&mut enc_block1_bytes, &enc_block1_key.to_le_bytes());

    // Update enc_block1 from the modified bytes
    for i in 0..4 {
        enc_block1[i] = u32::from_le_bytes([
            enc_block1_bytes[i * 4],
            enc_block1_bytes[i * 4 + 1],
            enc_block1_bytes[i * 4 + 2],
            enc_block1_bytes[i * 4 + 3],
        ]);
    }

    let crc =
        Crc::calculate_digest(&enc_block1_bytes, 0, enc_block1_bytes.len() as u32).wrapping_sub(2);

    // XOR first 32 bytes with 0xb7
    for b in &mut enc_data[..32] {
        *b ^= 0xB7;
    }

    if enc_len == 32 {
        return Ok(());
    }

    if enc_len < 0x9F {
        if enc_len > 32 {
            rc4(&mut enc_data[32..], &enc_block2_key);
        }
        return Ok(());
    }

    let key_material2 = [
        enc_block1[3].wrapping_add(0x6F1A36D8) ^ crc.wrapping_add(2),
        enc_block1[2].wrapping_sub(0x7E9A2C76) ^ enc_block2_key_int,
        enc_block1[0] ^ 0x840CF7D0 ^ crc.wrapping_add(2),
        enc_block1[1].wrapping_add(0x48D0E844) ^ enc_block2_key_int,
    ];

    let key_material2_bytes = u32_array_to_bytes(&key_material2);
    let key_block_seed = generate_seed(&key_material2_bytes);

    if enc_data.len() > 0x20 + 0x80 {
        let (enc_block2, rest) = enc_data[0x20..].split_at_mut(0x80);
        let mut key_block = [0u8; 0x80];
        key_block.copy_from_slice(enc_block2);

        rc4(&mut key_block, &key_block_seed.to_le_bytes());
        rc4(enc_block2, &key_material2_bytes[..12]);

        let key_table2 = [
            0x88558046u32,
            key_material2[3],
            0x5C7782C2u32,
            0x38922E17u32,
            key_material2[0],
            key_material2[1],
            0x44B38670u32,
            key_material2[2],
            0x6B07A514u32,
        ];

        let enc_block3 = rest;
        let rem_section = enc_len - 0xA0;
        let full_blocks = rem_section / 0x80;
        let rem_non_align = rem_section % 0x80;

        if full_blocks > 0 {
            let key_block_u32 = bytes_to_u32_slice(&key_block);

            for (block_idx, block) in enc_block3
                .chunks_exact_mut(0x80)
                .take(full_blocks)
                .enumerate()
            {
                let t = (key_table2[block_idx % 9] & 3) as u32;
                for idx in 0..32 {
                    let off = idx * 4;
                    let kbv = key_block_u32[idx];
                    let v = match t {
                        0 => {
                            kbv ^ key_table2[(key_material2[idx & 3] % 9) as usize]
                                ^ (32 - idx) as u32
                        }
                        1 => {
                            kbv ^ key_material2[(kbv & 3) as usize] ^ key_table2[(kbv % 9) as usize]
                        }
                        2 => kbv ^ key_material2[(kbv & 3) as usize] ^ (idx as u32),
                        _ => {
                            kbv ^ key_material2[(key_table2[idx % 9] & 3) as usize]
                                ^ (32 - idx) as u32
                        }
                    };
                    let mut cur = u32::from_le_bytes([
                        block[off],
                        block[off + 1],
                        block[off + 2],
                        block[off + 3],
                    ]);
                    cur ^= v;
                    let le = cur.to_le_bytes();
                    block[off..off + 4].copy_from_slice(&le);
                }
            }
        }

        if rem_non_align > 0 {
            let base = full_blocks * 0x80;
            for i in 0..rem_non_align {
                if base + i >= enc_block3.len() {
                    break;
                }

                let kb = key_block[i & 0x7F] as usize;
                let kt = (key_table2[(key_material2[i & 3] % 9) as usize] % 0xFF) as usize;
                enc_block3[base + i] ^= (i ^ kb ^ kt) as u8;
            }
        }
    }

    Ok(())
}
