"""Toy modular-inversion verification routines."""


def inv_mod(x, p):
    """Return x^{-1} mod p."""
    if x % p == 0:
        raise ValueError("zero has no inverse modulo p")
    return pow(x, -1, p)


def check_modinv_pair(x, y, p):
    """Check whether y is an inverse of x modulo p."""
    return (x * y) % p == 1


def verify_modinv_outputs(p, pairs):
    """Verify an iterable of (x, y) modular-inversion pairs."""
    return all(check_modinv_pair(x, y, p) for x, y in pairs)
