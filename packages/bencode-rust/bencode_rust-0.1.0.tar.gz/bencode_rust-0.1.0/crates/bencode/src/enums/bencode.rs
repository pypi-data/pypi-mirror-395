use std::collections::BTreeMap;

#[derive(Debug, PartialEq, Eq, Clone)]
pub enum BencodeValue {
    Int(isize),
    Str(Vec<u8>),
    List(Vec<BencodeValue>),
    Dict(BTreeMap<Vec<u8>, BencodeValue>),
}
