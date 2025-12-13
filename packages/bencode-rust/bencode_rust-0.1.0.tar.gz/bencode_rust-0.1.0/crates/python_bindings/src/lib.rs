use std::collections::BTreeMap;

use bencode::enums::bencode::BencodeValue;
use pyo3::{
    IntoPyObjectExt,
    prelude::*,
    types::{PyDict, PyList, PyTuple},
};

fn py_to_bencode_tokens(obj: Bound<PyAny>, decode_utf: Option<bool>) -> PyResult<BencodeValue> {
    let decode = decode_utf.unwrap_or(false);

    // List (PyList)
    if let Ok(list) = obj.cast::<PyList>() {
        let mut items = Vec::new();
        for item in list.iter() {
            items.push(py_to_bencode_tokens(item, Some(decode))?);
        }
        return Ok(BencodeValue::List(items));
    }

    // Tuple -> treat exactly like a list
    if let Ok(tuple) = obj.cast::<PyTuple>() {
        let mut items = Vec::new();
        for item in tuple.iter() {
            items.push(py_to_bencode_tokens(item, Some(decode))?);
        }
        return Ok(BencodeValue::List(items));
    }

    // Integers
    if let Ok(int_val) = obj.extract::<isize>() {
        return Ok(BencodeValue::Int(int_val));
    }

    // Strings -> UTF-8 bytes
    if let Ok(s) = obj.extract::<String>() {
        return Ok(BencodeValue::Str(s.into_bytes()));
    }

    // Bytes
    if let Ok(bytes) = obj.extract::<Vec<u8>>() {
        return Ok(BencodeValue::Str(bytes));
    }

    // Dict
    if let Ok(dict) = obj.cast::<PyDict>() {
        let mut map = BTreeMap::<Vec<u8>, BencodeValue>::new();

        for (key, value) in dict.iter() {
            let key_bytes: Vec<u8> = if decode {
                // Keys must be byte-like and valid UTF-8
                if let Ok(s) = key.extract::<String>() {
                    // Python str -> UTF-8 bytes
                    s.into_bytes()
                } else if let Ok(b) = key.extract::<Vec<u8>>() {
                    // Ensure bytes are valid UTF-8 then return raw bytes
                    String::from_utf8(b).map(|s| s.into_bytes()).map_err(|_| {
                        PyErr::new::<pyo3::exceptions::PyValueError, _>(
                            "Dictionary key bytes are not valid UTF-8",
                        )
                    })?
                } else {
                    return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                        "Dictionary keys must be str or bytes",
                    ));
                }
            } else {
                // Convert Python key → Vec<u8>
                if let Ok(py_str) = key.extract::<&str>() {
                    // Python str → UTF-8 bytes
                    py_str.as_bytes().to_vec()
                } else if let Ok(py_bytes) = key.extract::<&[u8]>() {
                    // Python bytes → raw bytes
                    py_bytes.to_vec()
                } else {
                    return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                        "Dictionary keys must be str or bytes",
                    ));
                }
            };

            // Convert value recursively
            let val = py_to_bencode_tokens(value, Some(decode))?;
            map.insert(key_bytes, val);
        }

        return Ok(BencodeValue::Dict(map));
    }

    // Unsupported type
    Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
        "Unsupported type: {}",
        obj.get_type().name()?
    )))
}

fn bencode_tokens_to_py(
    py: Python,
    tokens: BencodeValue,
    decode_utf: Option<bool>,
) -> PyResult<Bound<PyAny>> {
    let decoded = decode_utf.unwrap_or(false);

    match tokens {
        BencodeValue::Int(i) => Ok(i.into_bound_py_any(py)?),
        BencodeValue::Str(bytes) => {
            // Attempt UTF-8 decoding
            match String::from_utf8(bytes) {
                Ok(utf8_string) => Ok(utf8_string.into_bound_py_any(py)?),
                Err(e) => {
                    // Fall back to bytes for invalid UTF-8
                    let raw_bytes = e.into_bytes();
                    Ok(raw_bytes.into_bound_py_any(py)?)
                }
            }
        }
        BencodeValue::List(list) => {
            let py_list = PyList::empty(py);
            for item in list {
                py_list.append(bencode_tokens_to_py(py, item, Some(decoded))?)?;
            }
            Ok(py_list.into_any())
        }
        BencodeValue::Dict(dict) => {
            let py_dict = PyDict::new(py);
            for (key, value) in dict {
                // Handle dict key: decode as UTF-8 if requested and valid
                let key_obj = if decoded {
                    match String::from_utf8(key) {
                        Ok(s) => s.into_bound_py_any(py)?,
                        Err(e) => e.into_bytes().into_bound_py_any(py)?,
                    }
                } else {
                    key.into_bound_py_any(py)?
                };
                py_dict.set_item(key_obj, bencode_tokens_to_py(py, value, Some(decoded))?)?;
            }
            Ok(py_dict.into_any())
        }
    }
}

#[pymodule(name = "bencode_rs")]
mod python_bindings {
    use ::bencode::dispatcher::{bdecode::decode_bencode, bencode::encode_bencode};
    use pyo3::exceptions::PyValueError;
    use pyo3::prelude::*;

    use super::{bencode_tokens_to_py, py_to_bencode_tokens};

    #[pyfunction]
    #[pyo3(signature = (obj, decode_utf=false))]
    fn bencode(obj: Bound<PyAny>, decode_utf: Option<bool>) -> PyResult<Vec<u8>> {
        let objects = py_to_bencode_tokens(obj, decode_utf)?;
        let encoded = encode_bencode(objects).unwrap();
        Ok(encoded)
    }

    #[pyfunction]
    #[pyo3(signature = (string, decode_utf=false))]
    fn bdecode<'py>(
        py: Python<'py>,
        string: &[u8],
        decode_utf: Option<bool>,
    ) -> PyResult<Bound<'py, PyAny>> {
        let (decoded_objects, _rest) = decode_bencode(string).map_err(PyValueError::new_err)?;
        let python_objects = bencode_tokens_to_py(py, decoded_objects, decode_utf)?;
        Ok(python_objects)
    }
}
