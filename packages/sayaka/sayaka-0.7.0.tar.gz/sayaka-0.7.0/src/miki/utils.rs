#[inline]
pub fn bytes_to_u32_slice(bytes: &[u8]) -> Vec<u32> {
    let mut out = Vec::with_capacity(bytes.len().div_ceil(4));
    let mut chunks = bytes.chunks_exact(4);
    for chunk in &mut chunks {
        out.push(u32::from_le_bytes(chunk.try_into().unwrap()));
    }
    let rem = chunks.remainder();
    if !rem.is_empty() {
        let mut padded = [0u8; 4];
        padded[..rem.len()].copy_from_slice(rem);
        out.push(u32::from_le_bytes(padded));
    }
    out
}

#[inline]
pub fn u32_array_to_bytes(ints: &[u32]) -> Vec<u8> {
    let mut out = Vec::with_capacity(ints.len() * 4);
    for &i in ints {
        out.extend_from_slice(&i.to_le_bytes());
    }
    out
}

pub fn generate_seed(bytes: &[u8]) -> u32 {
    let mut s0 = 0xC1646153u32;
    let mut s1 = 0x78DA0550u32;
    let mut s2 = 0x2947E56Bu32;

    for &b in bytes {
        s0 = s0.wrapping_mul(0x21).wrapping_add(b as u32);

        let lo4 = s0 & 0xF;
        let lo8 = (s0 >> 4) & 0xF;
        let lo12 = (s0 >> 8) & 0xF;

        if lo4 >= 0xB {
            s0 ^= rotate_is_set(s2, 6);
            s0 = s0.wrapping_sub(0x2CD8_6315);
        } else if lo8 > 0xE {
            s0 = (s1 ^ 0xAB4A_010B).wrapping_add(s0 ^ rotate_is_set(s2, 9));
        } else if lo12 < 2 {
            s1 = ((s2 >> 3).wrapping_sub(0x55EE_AB7B)) ^ s0;
        } else if s1.wrapping_add(0x567A) >= 0xAB54_89E4 {
            s1 = (s1 >> 16) ^ s0;
        } else if (s1 ^ 0x7387_66FA) <= s2 {
            s1 = (s1 >> 8) ^ s2;
        } else if s1 == 0x68F5_3AA6 {
            if (s1 ^ s0.wrapping_add(s2)) > 0x594A_F86E {
                s1 = s1.wrapping_sub(0x08CA_292E);
            } else {
                s2 = s2.wrapping_sub(0x760A_1649);
            }
        } else {
            if s0 > 0x8657_03AF {
                s1 = s2 ^ s0.wrapping_sub(0x5643_89D7);
            } else {
                s1 = s1.wrapping_sub(0x12B9_DD92) ^ s0;
            }
            s0 ^= rotate_is_set(s1, 8);
        }
    }

    s0
}

#[inline]
fn rotate_is_set(value: u32, count: i32) -> u32 {
    (value.rotate_right(count as u32) != 0) as u32
}
