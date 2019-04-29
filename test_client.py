def test_read_file_as_b64():
    from client import read_file_as_b64
    a = bytes([1, 2, 3, 4])
    b64_string = read_file_as_b64(a)
    expected = 'AQIDBA=='
    assert b64_string == expected
