from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Generate a random 16-byte key
key = os.urandom(16)

# Create AES cipher in ECB mode (not recommended for real use, CBC is better)
cipher = AES.new(key, AES.MODE_ECB)

# Encrypt a message
plaintext = b"hello world 1234"  # 16-byte message
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

# Decrypt the message
decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

print("Ciphertext:", ciphertext.hex())
print("Decrypted:", decrypted.decode())
