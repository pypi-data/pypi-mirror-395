use super::string::encode_string;
use crate::{dispatcher::bencode::encode_bencode, enums::bencode::BencodeValue};

use std::collections::BTreeMap;

pub fn encode_dict(data: BTreeMap<Vec<u8>, BencodeValue>) -> Result<Vec<u8>, &'static str> {
    let mut encoded = Vec::new();
    encoded.push(b'd');

    for (key, value) in data.into_iter() {
        let encoded_key = encode_string(key)?;
        encoded.extend(encoded_key);

        let encoded_value = encode_bencode(value)?;
        encoded.extend(encoded_value);
    }

    encoded.push(b'e');
    Ok(encoded)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::enums::bencode::BencodeValue;
    use std::collections::BTreeMap;

    #[test]
    fn test_encode_empty_dict() {
        let dict = BTreeMap::new();
        let encoded = encode_dict(dict).unwrap();
        assert_eq!(encoded, b"de".to_vec());
    }

    #[test]
    fn test_encode_dict_with_int() {
        let mut dict = BTreeMap::new();
        dict.insert(
            b"wiki".to_vec(),
            BencodeValue::Str("bencode".as_bytes().to_vec()),
        );
        dict.insert(b"meaning".to_vec(), BencodeValue::Int(42));
        let encoded = encode_dict(dict).unwrap();
        assert_eq!(encoded, b"d7:meaningi42e4:wiki7:bencodee".to_vec());
    }

    #[test]
    fn test_encode_dict_with_string() {
        let mut dict = BTreeMap::new();
        dict.insert(
            b"name".to_vec(),
            BencodeValue::Str("Alice".as_bytes().to_vec()),
        );
        let encoded = encode_dict(dict).unwrap();
        assert_eq!(encoded, b"d4:name5:Alicee".to_vec());
    }

    #[test]
    fn test_encode_dict_with_list() {
        let mut dict = BTreeMap::new();
        let list = vec![
            BencodeValue::Int(1),
            BencodeValue::Str("two".as_bytes().to_vec()),
        ];
        dict.insert(b"numbers".to_vec(), BencodeValue::List(list));
        let encoded = encode_dict(dict).unwrap();
        assert_eq!(encoded, b"d7:numbersli1e3:twoee".to_vec());
    }

    #[test]
    fn test_nested_dict() {
        let mut dict: BTreeMap<Vec<u8>, BencodeValue> = BTreeMap::new();
        let mut nested_dict: BTreeMap<Vec<u8>, BencodeValue> = BTreeMap::new();
        nested_dict.insert(
            b"hello".to_vec(),
            BencodeValue::Str("world".as_bytes().to_vec()),
        );
        dict.insert(b"inner".to_vec(), BencodeValue::Dict(nested_dict));
        let encoded = encode_dict(dict).unwrap();
        assert_eq!(encoded, b"d5:innerd5:hello5:worldee".to_vec());
    }
}
