use crate::{dispatcher::bencode::encode_bencode, enums::bencode::BencodeValue};

pub fn encode_list(data: Vec<BencodeValue>) -> Result<Vec<u8>, &'static str> {
    let mut encoded = Vec::new();
    encoded.push(b'l');

    for item in data {
        let item_bytes = encode_bencode(item)?;
        encoded.extend(item_bytes);
    }

    encoded.push(b'e');
    Ok(encoded)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode_simple_list() {
        let list = vec![
            BencodeValue::Int(42),
            BencodeValue::Str("hello".as_bytes().to_vec()),
        ];

        let encoded = encode_list(list).unwrap();
        assert_eq!(encoded, b"li42e5:helloe".to_vec());
    }

    #[test]
    fn test_encode_nested_list() {
        let nested_list = vec![
            BencodeValue::Int(1),
            BencodeValue::List(vec![
                BencodeValue::Int(2),
                BencodeValue::Str("nested".as_bytes().to_vec()),
            ]),
            BencodeValue::Str("end".as_bytes().to_vec()),
        ];

        let encoded = encode_list(nested_list).unwrap();
        assert_eq!(encoded, b"li1eli2e6:nestede3:ende".to_vec());
    }

    #[test]
    fn test_empty_list() {
        let empty: Vec<BencodeValue> = vec![];
        let encoded = encode_list(empty).unwrap();
        assert_eq!(encoded, b"le".to_vec());
    }

    #[test]
    fn test_list_with_mixed_types() {
        // Renamed from "only_strings" to reflect actual content
        let list = vec![
            BencodeValue::Str("bencode".as_bytes().to_vec()),
            BencodeValue::Int(-20),
        ];
        let encoded = encode_list(list).unwrap();
        assert_eq!(encoded, b"l7:bencodei-20ee".to_vec());
    }
}
