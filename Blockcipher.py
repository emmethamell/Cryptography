import random

# Example substitution box, 0x0 to 0xE etc.
S_BOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 
         0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

# Inverse sub box for decryption
INV_S_BOX = [S_BOX.index(x) for x in range(16)]

# Permutation Box (bitwise, bit 0 moves to 1, 1 to 5 etc..)
# Defines how bits are rearranged each round
PERMUTATION = [1, 5, 2, 0, 3, 7, 4, 6]

# Example key schedule (derive round keys)
# 0xFF = 255 (11111111), acts as mask bitwise & will extract lowest 8 bits
def generate_round_keys(master_key, rounds=4):
    """Generates round keys from the master key."""
    round_keys = [(master_key >> (i * 8)) & 0xFF for i in range(rounds)]
    return round_keys

# Substitution Step (Nibble substitution using S-Box)
def substitute(block, sbox):
    """Substitutes nibbles using the given S-Box."""
    high_nibble = sbox[(block >> 4) & 0xF]
    low_nibble = sbox[block & 0xF]
    return (high_nibble << 4) | low_nibble

# Permutation Step (Bitwise rearrangement)
def permute(block):
    """Rearranges bits based on PERMUTATION table."""
    permuted_block = 0
    for i, bit_pos in enumerate(PERMUTATION):
        if block & (1 << bit_pos):
            permuted_block |= (1 << i)
    return permuted_block

# Block Cipher Encryption
def encrypt_block(plaintext, key):
    """Encrypts an 8-bit plaintext block using a block cipher structure."""
    round_keys = generate_round_keys(key)
    
    state = plaintext
    for i in range(3):  # 3 Rounds
        state ^= round_keys[i]  # AddRoundKey (XOR with round key)
        state = substitute(state, S_BOX)  # S-Box Substitution
        state = permute(state)  # Permutation Layer
    
    # Final round (No permutation)
    state ^= round_keys[3]
    state = substitute(state, S_BOX)
    state ^= round_keys[0]  # Final AddRoundKey
    
    return state

# Block Cipher Decryption
def decrypt_block(ciphertext, key):
    """Decrypts an 8-bit ciphertext block using the inverse of encryption steps."""
    round_keys = generate_round_keys(key)
    
    state = ciphertext
    state ^= round_keys[0]  # Reverse final AddRoundKey
    state = substitute(state, INV_S_BOX)  # Reverse S-Box
    
    for i in range(3, 0, -1):  # 3 Rounds (Reverse Order)
        state ^= round_keys[i]
        state = permute(state)  # Reverse Permutation
        state = substitute(state, INV_S_BOX)  # Reverse S-Box
    
    state ^= round_keys[0]  # Final AddRoundKey
    
    return state

# Example Usage
if __name__ == "__main__":
    master_key = random.randint(0, 255)  # Random 8-bit key
    plaintext = random.randint(0, 255)  # Random 8-bit message

    ciphertext = encrypt_block(plaintext, master_key)
    decrypted = decrypt_block(ciphertext, master_key)

    print(f"Master Key: {bin(master_key)[2:].zfill(8)}")
    print(f"Plaintext:  {bin(plaintext)[2:].zfill(8)}")
    print(f"Ciphertext: {bin(ciphertext)[2:].zfill(8)}")
    print(f"Decrypted:  {bin(decrypted)[2:].zfill(8)}")
    print("Decryption successful" if decrypted == plaintext else "Decryption failed.")
