import sys
import os
import tempfile

# Add project root to path so we can import src as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib.Encryption import Encryption
from src.lib.Config import Config
from src.models.Secret import SecretModel
from src.models.Category import CategoryModel
from src.models.User import UserModel
from src.modules.carry import global_scope

def run():
    # Example usage of Encryption class
    print("Starting DynaPyt Driver")
    key = b"supersecretkey"
    enc = Encryption(key)

    global_scope['enc'] = enc
    salt = enc.gen_salt()
    print(f"Generated salt: {salt}")
    digest = enc.digest_key()
    print(f"Digested key: {digest}")
    enc.set_salt()

    # Encrypt and decrypt a message
    message = b"Encrypt This!!"
    print(f"Original message: {message}")
    ciphertext = enc.encrypt(message)
    print(f"Encrypted message (base64): {ciphertext}")
    plaintext = enc.decrypt(ciphertext)
    print(f"Decrypted message: {plaintext}")

    # Encrypt and decrypt with a specific salt
    enc.set_salt(salt)
    secret2 = b"Secret with salt"
    ciphertext2 = enc.encrypt(secret2)
    print(f"Encrypted with salt (base64): {ciphertext2}")
    enc.set_salt(salt)
    plaintext2 = enc.decrypt(ciphertext2)
    print(f"Decrypted with salt: {plaintext2}")

    # Example usage of Config class
    print("\n--- Config Example ---")
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        config_path = tmp.name

    try:
        conf = Config(config_path)
        conf.set_default_config_file()
        print(f"Config loaded from: {config_path}")
        print(f"Config version: {conf.version}")
        print(f"Config salt: {conf.salt}")

        global_scope['conf'] = conf
        print("\n--- SecretModel Example ---")
        secret = SecretModel("MySecret", "http://example.com", "user", "password123", "my notes")
        print(f"Created Secret: {secret.name}")
        print(f"Secret Login: {secret.login}")
        print(f"Secret Password (decrypted): {secret.password}")
        print(f"Secret Notes (decrypted): {secret.notes}")
        print(f"Internal Encrypted Password: {secret._password}")

    finally:
        if os.path.exists(config_path):
            os.remove(config_path)

    # Example usage of CategoryModel
    print("\n--- CategoryModel Example ---")
    category = CategoryModel(name="Work", active=1)
    print(f"Category: {category}")

    # Example usage of UserModel
    print("\n--- UserModel Example ---")
    user = UserModel(key="setting_key", value="setting_value")
    print(f"User Setting: {user}")

    print("Finished DynaPyt Driver")

if __name__ == "__main__":
    run()
