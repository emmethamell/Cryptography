import random

def generate_random_permutation():
    """
    Generates a random permutation of the digits 0..9.
    Returns two dictionaries:
      - pi:   mapping x -> pi(x)
      - inv:  the inverse mapping pi^{-1}
    """
    digits = list(range(10))
    random.shuffle(digits)  # Shuffle in-place to create a random permutation
    
    pi = {}
    inv = {}
    for x, perm_val in enumerate(digits):
        pi[x] = perm_val    # pi(x) = perm_val
        inv[perm_val] = x   # inv[pi(x)] = x
    
    return pi, inv

def encrypt(M, pi):
    """
    Encrypts a 4-digit message string M using the permutation pi.
    (Assumes M is something like '4297' or '0123'.)
    
    Steps:
    1) Parse M as [M[1], M[2], M[3], M[4]]
    2) P[i] = (M[i] + i) mod 10
    3) C[i] = pi(P[i])
    4) Return the ciphertext C as a 4-digit string.
    """
    # Ensure M is length 4, convert to array of digits
    digits = [int(d) for d in M]
    
    # We'll store ciphertext digits here
    ciphertext_digits = []
    
    for i in range(4):
        # Note: i goes 0..3 in Python,
        # but in the scheme i goes 1..4
        # so let's define index = i+1 for the shift
        index = i + 1
        # Shift:
        P = (digits[i] + index) % 10
        # Apply permutation:
        C = pi[P]
        ciphertext_digits.append(str(C))
    
    return "".join(ciphertext_digits)

def decrypt(C, inv_pi):
    """
    Decrypts a 4-digit ciphertext C using the inverse permutation inv_pi.
    
    Steps:
    1) Parse C as [C[1], C[2], C[3], C[4]]
    2) P[i] = pi^{-1}(C[i])
    3) M[i] = (P[i] - i) mod 10
    4) Return the plaintext M as a 4-digit string.
    """
    ciphertext_digits = [int(d) for d in C]
    
    plaintext_digits = []
    
    for i in range(4):
        index = i + 1
        # First undo the permutation:
        P = inv_pi[ciphertext_digits[i]]
        # Then undo the shift:
        M = (P - index) % 10
        plaintext_digits.append(str(M))
    
    return "".join(plaintext_digits)
