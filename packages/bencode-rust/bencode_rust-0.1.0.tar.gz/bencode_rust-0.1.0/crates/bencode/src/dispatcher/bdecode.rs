use crate::{
    decoders::{
        dictionary::decode_dictionary, integer::decode_integer, list::decode_list,
        string::decode_string,
    },
    enums::bencode::BencodeValue,
};

pub fn decode_bencode(data: &[u8]) -> Result<(BencodeValue, &[u8]), &'static str> {
    if data.is_empty() {
        return Err("Empty input");
    }

    match data[0] {
        b if b.is_ascii_digit() => {
            let (bytes, rest) = decode_string(data)?;
            Ok((BencodeValue::Str(bytes), rest))
        }
        b'i' => {
            let (num, rest) = decode_integer(data)?;
            Ok((BencodeValue::Int(num), rest))
        }
        b'l' => {
            let (list, rest) = decode_list(data)?;
            Ok((BencodeValue::List(list), rest))
        }
        b'd' => {
            let (dict, rest) = decode_dictionary(data)?;
            Ok((BencodeValue::Dict(dict), rest))
        }
        _ => {
            println!("{:?}", data[0]);
            Err("Unknown type prefix")
        }
    }
}
