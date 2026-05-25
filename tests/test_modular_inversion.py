import pytest

from verifier.modular_inversion import check_modinv_pair, inv_mod, verify_modinv_outputs


def test_inv_mod_small_prime():
    assert inv_mod(3, 7) == 5
    assert check_modinv_pair(3, 5, 7)


def test_inv_mod_zero_rejected():
    with pytest.raises(ValueError):
        inv_mod(0, 7)


def test_verify_modinv_outputs():
    pairs = [(x, inv_mod(x, 11)) for x in range(1, 11)]
    assert verify_modinv_outputs(11, pairs)
