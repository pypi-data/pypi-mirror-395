pub fn decode_string(data: &[u8]) -> Result<(Vec<u8>, &[u8]), &'static str> {
    // Find the colon separating length from content
    let colon_pos = data.iter().position(|&b| b == b':').ok_or("Missing ':'")?;

    // Parse length as bytes, no UTF-8 conversion
    if colon_pos == 0 {
        return Err("Empty length");
    }
    let mut len: usize = 0;
    for &b in &data[..colon_pos] {
        if !b.is_ascii_digit() {
            return Err("Invalid digit in length");
        }
        len = len * 10 + (b - b'0') as usize;
    }

    // Check if enough bytes remain
    let start = colon_pos + 1;
    if data.len() < start + len {
        return Err("Not enough bytes for string");
    }

    let string_bytes = data[start..start + len].to_vec();
    let rest = &data[start + len..];

    Ok((string_bytes, rest))
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_strings() {
        let data = b"5:hello";
        let (val, rest) = decode_string(data).unwrap();
        assert_eq!(val, b"hello");
        assert_eq!(rest, b"");

        let data = b"0:";
        let (val, rest) = decode_string(data).unwrap();
        assert_eq!(val, b"");
        assert_eq!(rest, b"");

        let data = b"3:abc123";
        let (val, rest) = decode_string(data).unwrap();
        assert_eq!(val, b"abc");
        assert_eq!(rest, b"123");

        // Arbitrary bytes
        let data = b"4:\xff\x00\xaa\xbb";
        let (val, rest) = decode_string(data).unwrap();
        assert_eq!(val, vec![0xff, 0x00, 0xaa, 0xbb]);
        assert_eq!(rest, b"");

        let data = b"1:\xff";
        let (val, _rest) = decode_string(data).unwrap();
        assert_eq!(val, vec![0xff])
    }

    #[test]
    fn test_invalid_format() {
        let data = b"5hello"; // missing colon
        assert!(decode_string(data).is_err());

        let data = b":hello"; // empty length
        assert!(decode_string(data).is_err());

        let data = b"a:hello"; // non-digit
        assert!(decode_string(data).is_err());

        let data = b"10:short"; // not enough bytes
        assert!(decode_string(data).is_err());
    }
}
