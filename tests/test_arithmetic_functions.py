from verifier.arithmetic_functions import bits_to_int, expected_add_mod_2n, int_to_bits


def test_bits_to_int_and_int_to_bits_roundtrip():
    for value in range(8):
        bits = int_to_bits(value, 3)
        assert bits_to_int(bits) == value


def test_expected_add_mod_2n_n2():
    # a = 1, b = 2, output b = 3 mod 4.
    assert expected_add_mod_2n([1, 0, 0, 1], 2) == [1, 0, 1, 1]
    # a = 3, b = 2, output b = 1 mod 4.
    assert expected_add_mod_2n([1, 1, 0, 1], 2) == [1, 1, 1, 0]