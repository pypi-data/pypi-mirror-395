use crate::{
    encoders::{
        dictionary::encode_dict, integer::encode_integer, list::encode_list, string::encode_string,
    },
    enums::bencode::BencodeValue,
};

pub fn encode_bencode(value: BencodeValue) -> Result<Vec<u8>, &'static str> {
    match value {
        BencodeValue::Int(n) => encode_integer(n),
        BencodeValue::Str(s) => encode_string(s),
        BencodeValue::List(l) => encode_list(l),
        BencodeValue::Dict(d) => encode_dict(d),
    }
}
