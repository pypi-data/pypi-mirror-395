pub fn encode_string(data: Vec<u8>) -> Result<Vec<u8>, &'static str> {
    let len = data.len();
    let mut result = Vec::new();

    // Convert length to ASCII bytes
    let len_str = len.to_string();
    result.extend_from_slice(len_str.as_bytes());

    // Add colon separator as raw byte
    result.push(b':');

    // Append raw data bytes directly
    result.extend_from_slice(&data);

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode_string() {
        // ASCII string
        assert_eq!(
            encode_string(b"bencode".to_vec()).unwrap(),
            b"7:bencode".to_vec()
        );

        // Empty string
        assert_eq!(encode_string(b"".to_vec()).unwrap(), b"0:".to_vec());

        // Unicode string (valid UTF-8)
        let unicode_str = "আসসালামু আলাইকুম";
        let expected = format!("{}:{}", unicode_str.len(), unicode_str).into_bytes();
        assert_eq!(
            encode_string(unicode_str.as_bytes().to_vec()).unwrap(),
            expected
        );

        // Non-UTF-8 bytes
        let input = vec![0xFF, 0xFE, 0xFD];
        let mut expected = b"3:".to_vec();
        expected.extend_from_slice(&input);
        assert_eq!(encode_string(input).unwrap(), expected);
    }
}
