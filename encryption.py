
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidTag


# File format information
MAGIC = b"AES256G1"
SALT_SIZE = 16
NONCE_SIZE = 12


def derive_key(password, salt):
    """Derive a 256-bit encryption key from a password."""

    if not password:
        raise ValueError("Password cannot be empty.")

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1
    )

    return kdf.derive(password.encode("utf-8"))


def encrypt_file(input_path, output_path, password):
    """Encrypt a file using AES-256-GCM."""

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError("The input file was not found.")

    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output files must be different.")

    # Read the original file
    data = input_path.read_bytes()

    # Generate random salt and nonce
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    # Derive the AES-256 key
    key = derive_key(password, salt)

    # Encrypt the file
    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, data, None)

    # Save file header, salt, nonce and ciphertext
    encrypted_data = MAGIC + salt + nonce + ciphertext

    output_path.write_bytes(encrypted_data)

    return output_path


def decrypt_file(input_path, output_path, password):
    """Decrypt an AES-256-GCM encrypted file."""

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError("The encrypted file was not found.")

    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output files must be different.")

    encrypted_data = input_path.read_bytes()

    # Check the file format
    minimum_size = len(MAGIC) + SALT_SIZE + NONCE_SIZE + 16

    if len(encrypted_data) < minimum_size:
        raise ValueError("Invalid or incomplete encrypted file.")

    if not encrypted_data.startswith(MAGIC):
        raise ValueError("Invalid AES encrypted file format.")

    # Extract salt, nonce and ciphertext
    offset = len(MAGIC)

    salt = encrypted_data[offset:offset + SALT_SIZE]
    offset += SALT_SIZE

    nonce = encrypted_data[offset:offset + NONCE_SIZE]
    offset += NONCE_SIZE

    ciphertext = encrypted_data[offset:]

    # Derive the same key
    key = derive_key(password, salt)

    # Decrypt and verify data integrity
    aes = AESGCM(key)

    try:
        plaintext = aes.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise ValueError(
            "Decryption failed: incorrect password "
            "or the encrypted file was modified."
        )

    # Save recovered file only after successful verification
    output_path.write_bytes(plaintext)

    return output_path
