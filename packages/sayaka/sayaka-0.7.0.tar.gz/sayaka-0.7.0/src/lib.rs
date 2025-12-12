mod chacha20;
mod chacha_decryptor;
mod hgmmap;
mod lz4inv;
mod miki;
mod utils;
mod xxtea;

use pyo3::{pyfunction, pymodule, types::PyAny};

#[pymodule]
mod sayaka {
    use pyo3::{ffi, types::PyBytes};

    use crate::lz4inv::decompress_impl;
    use crate::miki::{decrypt_old_to_impl, decrypt_to_impl};
    use crate::utils::get_python_buffer;

    #[pymodule_export]
    use crate::chacha20::ChaCha20;

    #[pymodule_export]
    use crate::hgmmap::ManifestDataBinary;

    #[pymodule_export]
    use crate::chacha_decryptor::ChaChaDecryptor;

    use super::*;

    #[pyfunction]
    fn miki_decrypt_and_decompress<'py>(
        py: pyo3::Python<'py>,
        encrypted: &pyo3::Bound<'py, PyAny>,
        decompressed_size: usize,
    ) -> pyo3::PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, decompressed_size, |decompressed| {
            if encrypted[..32].iter().filter(|&&b| b == 0xa6).count() > 5 {
                miki::decrypt_impl(encrypted)?;
            }

            decompress_impl(encrypted, decompressed)?;
            Ok(())
        });

        pyo3::Python::attach(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn miki_decrypt_old_and_decompress<'py>(
        py: pyo3::Python<'py>,
        encrypted: &pyo3::Bound<'py, PyAny>,
        decompressed_size: usize,
    ) -> pyo3::PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, decompressed_size, |decompressed| {
            if encrypted[..32].iter().filter(|&&b| b == 0xB7).count() > 5 {
                miki::decrypt_old_impl(encrypted)?;
            }

            decompress_impl(encrypted, decompressed)?;
            Ok(())
        });

        pyo3::Python::attach(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn miki_decrypt<'py>(
        py: pyo3::Python<'py>,
        encrypted: &pyo3::Bound<'py, PyAny>,
    ) -> pyo3::PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, encrypted.len(), |decrypted| {
            decrypt_to_impl(encrypted, decrypted)?;

            Ok(())
        });

        pyo3::Python::attach(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn miki_decrypt_old<'py>(
        py: pyo3::Python<'py>,
        encrypted: &pyo3::Bound<'py, PyAny>,
    ) -> pyo3::PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, encrypted.len(), |decrypted| {
            decrypt_old_to_impl(encrypted, decrypted)?;

            Ok(())
        });

        pyo3::Python::attach(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn decompress_buffer<'py>(
        py: pyo3::Python<'py>,
        compressed: &pyo3::Bound<'py, PyAny>,
        decompressed_size: usize,
    ) -> pyo3::PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(compressed)?;
        let compressed =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, decompressed_size, |decompressed| {
            decompress_impl(compressed, decompressed)?;
            Ok(())
        });

        pyo3::Python::attach(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn xxtea_decrypt<'py>(
        py: pyo3::Python<'py>,
        data: &pyo3::Bound<'py, PyAny>,
        key: &pyo3::Bound<'py, PyAny>,
    ) -> pyo3::PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut data_buf = get_python_buffer(data)?;
        let data_bytes = unsafe {
            std::slice::from_raw_parts_mut(data_buf.buf as *mut u8, data_buf.len as usize)
        };

        let mut key_buf = get_python_buffer(key)?;
        let key_bytes =
            unsafe { std::slice::from_raw_parts_mut(key_buf.buf as *mut u8, key_buf.len as usize) };

        let decrypted_data = xxtea::decrypt(data_bytes, key_bytes);

        let result = PyBytes::new_with(py, decrypted_data.len(), |decrypted| {
            decrypted.copy_from_slice(&decrypted_data);
            Ok(())
        });

        pyo3::Python::attach(|_| unsafe {
            ffi::PyBuffer_Release(&mut key_buf);
            ffi::PyBuffer_Release(&mut data_buf);
        });
        result
    }

    #[pyfunction]
    fn xxtea_encrypt<'py>(
        py: pyo3::Python<'py>,
        data: &pyo3::Bound<'py, PyAny>,
        key: &pyo3::Bound<'py, PyAny>,
    ) -> pyo3::PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut data_buf = get_python_buffer(data)?;
        let data_bytes = unsafe {
            std::slice::from_raw_parts_mut(data_buf.buf as *mut u8, data_buf.len as usize)
        };

        let mut key_buf = get_python_buffer(key)?;
        let key_bytes =
            unsafe { std::slice::from_raw_parts_mut(key_buf.buf as *mut u8, key_buf.len as usize) };

        let encrypted_data = xxtea::encrypt(data_bytes, key_bytes);

        let result = PyBytes::new_with(py, encrypted_data.len(), |encrypted| {
            encrypted.copy_from_slice(&encrypted_data);
            Ok(())
        });

        pyo3::Python::attach(|_| unsafe {
            ffi::PyBuffer_Release(&mut key_buf);
            ffi::PyBuffer_Release(&mut data_buf);
        });
        result
    }
}
