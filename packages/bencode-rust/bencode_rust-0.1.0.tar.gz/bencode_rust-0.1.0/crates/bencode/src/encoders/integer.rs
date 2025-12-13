pub fn encode_integer(data: isize) -> Result<Vec<u8>, &'static str> {
    let encoded = format!("i{}e", data);
    Ok(encoded.into_bytes())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode_integer() {
        // Test a normal integer
        assert_eq!(encode_integer(42).unwrap(), b"i42e".to_vec());

        // Test zero
        assert_eq!(encode_integer(0).unwrap(), b"i0e".to_vec());

        // Test a large number
        assert_eq!(encode_integer(123456789).unwrap(), b"i123456789e".to_vec());

        // Test Negative Number
        assert_eq!(encode_integer(-42).unwrap(), b"i-42e".to_vec());
    }
}
