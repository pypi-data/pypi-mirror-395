use crate::{dispatcher::bdecode::decode_bencode, enums::bencode::BencodeValue};
use std::collections::BTreeMap;

type DictionaryKey = Vec<u8>;
type DictionaryValue = BencodeValue;

type DictionaryOutput = BTreeMap<DictionaryKey, DictionaryValue>;

pub fn decode_dictionary(data: &[u8]) -> Result<(DictionaryOutput, &[u8]), &'static str> {
    if data.is_empty() || data[0] != b'd' {
        return Err("Not a dictionary");
    }

    let mut rest = &data[1..]; // skip 'd'
    let mut dict = BTreeMap::new();

    while !rest.is_empty() && rest[0] != b'e' {
        // Decode key
        let (key_value, new_rest) = decode_bencode(rest)?;
        let key_bytes = match key_value {
            BencodeValue::Str(bytes) => bytes,
            _ => return Err("Dictionary key must be a string"),
        };

        rest = new_rest;

        // Decode value
        let (value, new_rest) = decode_bencode(rest)?;
        rest = new_rest;

        // Insert into map (optionally check for duplicate keys)
        dict.insert(key_bytes, value);
    }

    if rest.is_empty() {
        return Err("Missing 'e' to terminate dictionary");
    }

    // Skip the terminating 'e'
    let rest = &rest[1..];
    Ok((dict, rest))
}
