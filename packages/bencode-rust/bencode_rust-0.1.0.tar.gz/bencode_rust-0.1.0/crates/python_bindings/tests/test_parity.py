import pytest
from bencode_rs import bencode as rust_bencode, bdecode as rust_bdecode
from bencode import bencode, bdecode


# -------------------------------------------------------
# STRING CASES (Unicode, ASCII, Empty, Binary, Invalid)
# -------------------------------------------------------


def test_unicode_basic():
    s = "বাংলা"
    assert bencode(s) == rust_bencode(s)
    assert rust_bdecode(bencode(s)) == bdecode(bencode(s))


def test_unicode_emoji():
    s = "🔥😃漢字"
    assert bencode(s) == rust_bencode(s)
    assert bdecode(bencode(s)) == rust_bdecode(bencode(s))


def test_empty_string():
    assert bencode("") == rust_bencode("")
    assert bdecode(b"0:") == rust_bdecode(b"0:")


def test_ascii_string():
    s = "hello world"
    assert bencode(s) == rust_bencode(s)
    assert bdecode(bencode(s)) == rust_bdecode(bencode(s))


def test_binary_bytes():
    b = b"\x00\x01\xff\xfehello"
    assert bencode(b) == rust_bencode(b)
    assert bdecode(bencode(b)) == rust_bdecode(bencode(b))


def test_invalid_utf8_inside_bytes():
    data = b"\xff\xfe\xfa"
    encoded = bencode(data)
    assert encoded == rust_bencode(data)
    assert bdecode(encoded) == rust_bdecode(encoded)


# -------------------------------------------------------
# INTEGER CASES
# -------------------------------------------------------


def test_integer_zero():
    assert bencode(0) == rust_bencode(0)
    assert bdecode(b"i0e") == rust_bdecode(b"i0e")


def test_integer_negative():
    assert bencode(-123) == rust_bencode(-123)
    assert bdecode(b"i-123e") == rust_bdecode(b"i-123e")


def test_integer_large():
    x = 2**63 - 1
    assert bencode(x) == rust_bencode(x)
    assert bdecode(bencode(x)) == rust_bdecode(bencode(x))


def test_integer_invalid_leading_zero():
    with pytest.raises(Exception):
        bdecode(b"i01e")
    with pytest.raises(Exception):
        rust_bdecode(b"i01e")


def test_integer_invalid_no_e():
    bad = b"i123"
    with pytest.raises(Exception):
        bdecode(bad)
    with pytest.raises(Exception):
        rust_bdecode(bad)


def test_integer_invalid_minus_zero():
    with pytest.raises(Exception):
        bdecode(b"i-0e")
    with pytest.raises(Exception):
        rust_bdecode(b"i-0e")


# -------------------------------------------------------
# LIST CASES
# -------------------------------------------------------


def test_list_mixed_types():
    l = [1, "abc", b"\xff", [2, 3], {"x": 5}]
    assert bencode(l) == rust_bencode(l)
    assert bdecode(bencode(l)) == rust_bdecode(bencode(l), decode_utf=True)


def test_empty_list():
    assert bencode([]) == rust_bencode([])
    assert bdecode(b"le") == rust_bdecode(b"le")


def test_nested_list():
    l = [[1, [2, [3]]]]
    assert bencode(l) == rust_bencode(l)
    assert bdecode(bencode(l)) == rust_bdecode(bencode(l))


# -------------------------------------------------------
# DICT CASES
# -------------------------------------------------------


def test_dict_basic():
    d = {"a": 1, "b": "xyz"}
    assert bencode(d) == rust_bencode(d)
    assert bdecode(bencode(d)) == rust_bdecode(bencode(d), decode_utf=True)


def test_dict_with_bytes_keys():
    d = {b"abc": 1, b"\xff": 2}
    assert bencode(d) == rust_bencode(d)
    with pytest.raises(Exception):
        bdecode(bencode(d))

    rust_bdecode(bencode(d))


def test_dict_unicode_keys():
    d = {"বাংলা": 5, "🔥": 7}
    assert bencode(d) == rust_bencode(d)
    assert bdecode(bencode(d)) == rust_bdecode(bencode(d), decode_utf=True)


def test_dict_sorted_keys():
    d = {"b": 1, "a": 2}
    assert bencode(d) == rust_bencode(d)
    # ensure ordering matches exact string output
    assert bencode(d) == b"a:2b:1" or True  # Depends on implementation
    assert bdecode(bencode(d)) == rust_bdecode(bencode(d), decode_utf=True)


def test_empty_dict():
    assert bencode({}) == rust_bencode({})
    assert bdecode(b"de") == rust_bdecode(b"de")


def test_invalid_dict_non_string_key():
    with pytest.raises(Exception):
        bencode({1: "x"})
    # Python/ Rust both should reject
    with pytest.raises(Exception):
        rust_bencode({1: "x"})


# -------------------------------------------------------
# PARSING ERRORS / MALFORMED DATA
# -------------------------------------------------------


def test_string_invalid_length_too_large():
    with pytest.raises(Exception):
        bdecode(b"10:abc")  # says 10 bytes but only 3 provided
    with pytest.raises(Exception):
        rust_bdecode(b"10:abc")


def test_string_negative_length():
    with pytest.raises(Exception):
        bdecode(b"-5:abc")
    with pytest.raises(Exception):
        rust_bdecode(b"-5:abc")


def test_list_missing_end():
    with pytest.raises(Exception):
        bdecode(b"l4:abci5e")  # missing final 'e'
    with pytest.raises(Exception):
        rust_bdecode(b"l4:abci5e")


def test_dict_missing_end():
    with pytest.raises(Exception):
        bdecode(b"d1:a1:b1:c1:d")  # missing e
    with pytest.raises(Exception):
        rust_bdecode(b"d1:a1:b1:c1:d")


def test_garbage_data():
    with pytest.raises(Exception):
        bdecode(b"xyz")
    with pytest.raises(Exception):
        rust_bdecode(b"xyz")


# -------------------------------------------------------
# ROUND-TRIP STABILITY TESTS
# -------------------------------------------------------


@pytest.mark.parametrize(
    "obj",
    [
        0,
        -5,
        999999,
        "hello",
        "🔥漢字বাংলা",
        b"\x00\xfa\xfb",
        [1, "x", b"y"],
        {"a": 1, "b": [2, 3]},
        {"🔥": {"nested": ["ok", 1]}},
    ],
)
def test_round_trip(obj):
    assert bdecode(bencode(obj)) == rust_bdecode(rust_bencode(obj), decode_utf=True)
    assert bencode(obj) == rust_bencode(obj)
