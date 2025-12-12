import os
from ..lib.Encryption import Encryption

def test_encryption_decryption_performance(benchmark):
    """
    Benchmarks the performance of a full encryption and decryption cycle.
    """
    key = os.urandom(32)  # Generate a random 256-bit key
    secret = b"this is a top secret message for performance testing"
    encryption = Encryption(key)

    def f():
        encrypted = encryption.encrypt(secret)
        decrypted = encryption.decrypt(encrypted)
        assert decrypted == secret

    benchmark(f)
