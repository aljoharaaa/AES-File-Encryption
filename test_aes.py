
from pathlib import Path

from encryption import encrypt_file, decrypt_file

# Test file paths
original = Path("test_files/secret.txt")
encrypted = Path("test_files/secret.enc")
decrypted = Path("test_files/recovered.txt")

# Test password
password = "MySecurePassword123!"

print("Starting AES-256 test...")

# Step 1: Encrypt
encrypt_file(original, encrypted, password)
print("1. Encryption successful!")

# Step 2: Decrypt
decrypt_file(encrypted, decrypted, password)
print("2. Decryption successful!")

# Step 3: Compare original and recovered files
if original.read_bytes() == decrypted.read_bytes():
    print("3. SUCCESS: Files are identical!")
else:
    print("3. ERROR: Files are different!")

# Step 4: Test incorrect password
try:
    decrypt_file(encrypted, Path("test_files/wrong.txt"),
                 "WrongPassword123!")
    print("ERROR: Incorrect password was accepted!")
except ValueError:
    print("4. SUCCESS: Incorrect password rejected!")

print("All tests completed.")
