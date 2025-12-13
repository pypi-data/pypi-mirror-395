pub fn decode_integer(data: &[u8]) -> Result<(isize, &[u8]), &'static str> {
    if data.is_empty() || data[0] != b'i' {
        return Err("Not an integer");
    }
    // Find the position of 'e'
    let end_pos = data
        .iter()
        .position(|&b| b == b'e')
        .ok_or("Missing 'e' for integer")?;

    // Slice out the integer part
    let int_bytes = &data[1..end_pos];

    // Check for empty integer
    if int_bytes.is_empty() {
        return Err("Empty integer");
    }

    // Leading zero check (except for '0')
    if int_bytes.len() > 1 && int_bytes[0] == b'0' {
        return Err("Leading zeros are not allowed");
    }
    // Negative zero check
    if int_bytes[0] == b'-' && int_bytes[1] == b'0' {
        return Err("Negative leading zeros are not allowed");
    }

    // Convert to string and parse
    let int_str = std::str::from_utf8(int_bytes).map_err(|_| "Invalid UTF-8")?;
    let value = int_str.parse::<isize>().map_err(|_| "Invalid integer")?;

    // Return the value and remaining slice
    Ok((value, &data[end_pos + 1..]))
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_integers() {
        // Simple integer
        let data = b"i42e";
        let (val, rest) = decode_integer(data).unwrap();
        assert_eq!(val, 42);
        assert_eq!(rest, b"");

        // Zero
        let data = b"i0e";
        let (val, rest) = decode_integer(data).unwrap();
        assert_eq!(val, 0);
        assert_eq!(rest, b"");

        // Integer with remaining data
        let data = b"i123e456";
        let (val, rest) = decode_integer(data).unwrap();
        assert_eq!(val, 123);
        assert_eq!(rest, b"456");
    }

    #[test]
    fn test_invalid_format() {
        // Not starting with 'i'
        let data = b"42e";
        assert!(decode_integer(data).is_err());

        // Missing 'e'
        let data = b"i42";
        assert!(decode_integer(data).is_err());

        // Empty integer
        let data = b"ie";
        assert!(decode_integer(data).is_err());

        // Leading zeros
        let data = b"i042e";
        assert!(decode_integer(data).is_err());
    }

    #[test]
    fn test_invalid_utf8() {
        // Invalid UTF-8 sequence
        let data = b"i\xff42e";
        assert!(decode_integer(data).is_err());
    }

    #[test]
    fn test_large_integer() {
        let data = b"i1234567890e";
        let (val, rest) = decode_integer(data).unwrap();
        assert_eq!(val, 1234567890);
        assert_eq!(rest, b"");
    }
}
