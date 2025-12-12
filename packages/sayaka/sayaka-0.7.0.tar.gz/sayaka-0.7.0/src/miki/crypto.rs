pub fn rc4(data: &mut [u8], key: &[u8]) {
    assert!(!key.is_empty());

    let mut s = [0u8; 256];
    for (i, v) in s.iter_mut().enumerate() {
        *v = i as u8;
    }

    let mut j = 0u8;
    let key_len = key.len();
    for i in 0..=255u8 {
        let ki = key[(i as usize) % key_len];
        j = j.wrapping_add(s[i as usize]).wrapping_add(ki);
        s.swap(i as usize, j as usize);
    }

    let mut i = 0u8;
    j = 0;
    for byte in data.iter_mut() {
        i = i.wrapping_add(1);
        j = j.wrapping_add(s[i as usize]);
        s.swap(i as usize, j as usize);

        let idx = s[j as usize].wrapping_add(s[i as usize]);
        let k_val = s[idx as usize];

        let k = k_val.rotate_left(1).wrapping_sub(0x61);

        *byte ^= k;
    }
}
