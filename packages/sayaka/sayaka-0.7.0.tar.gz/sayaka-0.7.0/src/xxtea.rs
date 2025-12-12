use std::mem::MaybeUninit;

const DELTA: u32 = 0x9E3779B9;

/// Convert a slice of u32 values to bytes
/// If `w` is true, the last element is treated as the original length
#[inline(always)]
fn long2str(v: &[u32], w: bool) -> Vec<u8> {
    if v.is_empty() {
        return Vec::new();
    }

    let total_bytes = v.len() * 4;
    let n = (v.len() - 1) << 2;

    let m = if w {
        let m = v[v.len() - 1] as usize;
        if m < n.saturating_sub(3) || m > n {
            return Vec::new();
        }
        m
    } else {
        total_bytes
    };

    let mut result = vec![0u8; total_bytes];

    unsafe {
        let src = v.as_ptr() as *const u8;
        std::ptr::copy_nonoverlapping(src, result.as_mut_ptr(), total_bytes);
    }

    result.truncate(m);
    result
}

/// Convert bytes to a vector of u32 values
/// If `add_len` is true, append the original length as the last element
#[inline(always)]
pub fn str2long(s: &[u8], add_len: bool) -> Vec<u32> {
    let n = s.len();
    let pad = (4 - (n & 3)) & 3;
    let m = n + pad; // padded bytes
    let words = m / 4;
    let extra = add_len as usize; // 0 or 1

    let mut v: Vec<MaybeUninit<u32>> = Vec::with_capacity(words + extra);

    // SAFETY: v is uninitialized but we will write all m bytes
    unsafe {
        let dst_u32 = v.as_mut_ptr(); // *mut MaybeUninit<u32>
        let dst_u8 = dst_u32 as *mut u8; // view as u8 buffer

        // 2) Copy full original bytes
        std::ptr::copy_nonoverlapping(s.as_ptr(), dst_u8, n);

        // 3) Zero padding bytes (only up to 3 bytes)
        if pad != 0 {
            std::ptr::write_bytes(dst_u8.add(n), 0, pad);
        }

        // 4) Set length of initialized words
        v.set_len(words);

        // 5) Convert Vec<MaybeUninit<u32>> → Vec<u32>
        let v = std::mem::transmute::<Vec<MaybeUninit<u32>>, Vec<u32>>(v);

        // 6) Optionally push original length
        if add_len {
            let mut v = v;
            v.push(n as u32);
            return v;
        }

        v
    }
}

/// XXTEA encrypt function
pub fn encrypt(data: &[u8], key: &[u8]) -> Vec<u8> {
    let mut v = str2long(data, true);

    // Pad key to 16 bytes
    let mut key_padded = key.to_vec();
    key_padded.resize(16, 0);
    let k = str2long(&key_padded, false);

    let n = v.len() - 1;
    if n < 1 {
        return long2str(&v, false);
    }

    let mut z = v[n];
    let mut sum: u32 = 0;
    let q = 6 + 52 / (n + 1);

    for _ in 0..q {
        sum = sum.wrapping_add(DELTA);
        let e = ((sum >> 2) & 3) as usize;

        for p in 0..n {
            let y = v[p + 1];
            let mx = ((z >> 5) ^ (y << 2)).wrapping_add((y >> 3) ^ (z << 4))
                ^ (sum ^ y).wrapping_add(k[(p & 3) ^ e] ^ z);
            v[p] = v[p].wrapping_add(mx);
            z = v[p];
        }

        let y = v[0];
        let mx = ((z >> 5) ^ (y << 2)).wrapping_add((y >> 3) ^ (z << 4))
            ^ (sum ^ y).wrapping_add(k[(n & 3) ^ e] ^ z);
        v[n] = v[n].wrapping_add(mx);
        z = v[n];
    }

    long2str(&v, false)
}

/// XXTEA decrypt function
pub fn decrypt(data: &[u8], key: &[u8]) -> Vec<u8> {
    let mut v = str2long(data, false);

    // Pad key to 16 bytes
    let mut key_padded = key.to_vec();
    key_padded.resize(16, 0);
    let k = str2long(&key_padded, false);

    let n = v.len() - 1;
    if n < 1 {
        return long2str(&v, true);
    }

    let mut y = v[0];
    let q = 6 + 52 / (n + 1);
    let mut sum: u32 = (q as u32).wrapping_mul(DELTA);

    while sum != 0 {
        let e = ((sum >> 2) & 3) as usize;

        for p in (1..=n).rev() {
            let z = v[p - 1];
            let mx = ((z >> 5) ^ (y << 2)).wrapping_add((y >> 3) ^ (z << 4))
                ^ (sum ^ y).wrapping_add(k[(p & 3) ^ e] ^ z);
            v[p] = v[p].wrapping_sub(mx);
            y = v[p];
        }

        let z = v[n];
        let mx = ((z >> 5) ^ (y << 2)).wrapping_add((y >> 3) ^ (z << 4))
            ^ (sum ^ y).wrapping_add(k[e] ^ z);
        v[0] = v[0].wrapping_sub(mx);
        y = v[0];

        sum = sum.wrapping_sub(DELTA);
    }

    long2str(&v, true)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encrypt_decrypt() {
        let key = b"1234567890123456";
        let data = b"Hello, XXTEA!";

        let encrypted = encrypt(data, key);
        let decrypted = decrypt(&encrypted, key);

        assert_eq!(decrypted, data);
    }

    #[test]
    fn test_encrypt_decrypt_short_key() {
        let key = b"short";
        let data = b"Test data with short key";

        let encrypted = encrypt(data, key);
        let decrypted = decrypt(&encrypted, key);

        assert_eq!(decrypted, data);
    }

    #[test]
    fn test_encrypt_decrypt_empty() {
        let key = b"testkey";
        let data = b"";

        let encrypted = encrypt(data, key);
        let decrypted = decrypt(&encrypted, key);

        assert_eq!(decrypted, data);
    }

    #[test]
    fn test_encrypt_decrypt_long_data() {
        let key = b"longtestkey12345";
        let data = b"This is a longer piece of data that we want to encrypt and decrypt using XXTEA algorithm.";

        let encrypted = encrypt(data, key);
        let decrypted = decrypt(&encrypted, key);

        assert_eq!(decrypted, data);
    }
}
