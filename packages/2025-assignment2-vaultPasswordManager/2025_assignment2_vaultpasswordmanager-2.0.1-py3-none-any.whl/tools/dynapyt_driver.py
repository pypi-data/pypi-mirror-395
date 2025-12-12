import sys
import os

# Add src to path so we can import lib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.Encryption import Encryption

def run():
    print("Starting DynaPyt Driver")
    key = b"supersecretkey"
    enc = Encryption(key)
    salt = enc.gen_salt()
    print(f"Generated salt: {salt}")
    digest = enc.digest_key()
    print(f"Digested key: {digest}")
    enc.set_salt()

    ### Another example
    message = b"Encrypt This!!"
    print(f"Original message: {message}")
    ciphertext = enc.encrypt(message)
    print(f"Encrypted message (base64): {ciphertext}")
    plaintext = enc.decrypt(ciphertext)
    print(f"Decrypted message: {plaintext}")
    enc.set_salt(salt)
    secret2 = b"Secret with salt"
    ciphertext2 = enc.encrypt(secret2)
    print(f"Encrypted with salt (base64): {ciphertext2}")
    enc.set_salt(salt)
    plaintext2 = enc.decrypt(ciphertext2)
    print(f"Decrypted with salt: {plaintext2}")
    print("Finished DynaPyt Driver")

if __name__ == "__main__":
    run()
