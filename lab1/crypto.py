#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Adorjani Biborka
SUNet: abim1985

Replace this with a description of the program.
"""
import utils
import string

ALPHABET = sorted(set(string.ascii_uppercase))
k = 3

# Caesar Cipher

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    if len(plaintext) == 0:
        return plaintext
    return ''.join([ALPHABET[(ALPHABET.index(symbol) + k) % len(ALPHABET)] if symbol in ALPHABET else symbol for symbol in plaintext.upper()])


def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    if len(ciphertext) == 0:
        return ciphertext
    return ''.join([ALPHABET[(ALPHABET.index(symbol) - k) % len(ALPHABET)] if symbol in ALPHABET else symbol for symbol in ciphertext.upper()])


# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if not plaintext.isalpha() or not keyword.isalpha():
        return "The given text or keyword contains non alphabetic character."
    if len(plaintext) == 0 or len(key) == 0:
        return plaintext
    plaintext = plaintext.upper()
    key = ''.join([keyword] * ((len(plaintext) // len(keyword) + 1))) 
    return ''.join([ALPHABET[(ord(plaintext[i]) + ord(key[i])) % len(ALPHABET)] for i in range(len(plaintext))])

def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if not ciphertext.isalpha() or not keyword.isalpha():
        return "The given text or keyword contains non alphabetic character."
    if len(ciphertext) == 0 or len(key) == 0:
        return ciphertext
    ciphertext = ciphertext.upper()
    key = ''.join([keyword] * ((len(ciphertext) // len(keyword) + 1))) 
    return ''.join([ALPHABET[(ord(ciphertext[i]) - ord(key[i])) % len(ALPHABET)] for i in range(len(ciphertext))])


# Scytale Cipher

def encrypt_scytale(plaintext, circumference):
    return ''.join(plaintext[slice(i, len(plaintext), circumference)] for i in range(circumference))

def decrypt_scytale(ciphertext, circumference):
    new_circum = len(ciphertext) // circumference
    return ''.join(ciphertext[slice(i, len(ciphertext), new_circum)] for i in range(new_circum))


# Railfence Cipher

def encrypt_railfence(plaintext, num_rails):
    encrypted_text = ''
    for i in range(1, num_rails-1):
        row1 = [plaintext[i] for i in range(i, len(plaintext), num_rails*2-2)]
        row2 = [plaintext[i] for i in range(num_rails*2-(2+i), len(plaintext), num_rails*2-2)]
        if row1 != row2:
            merged = [0 for i in range(len(row1) + len(row2))] 
            merged[0:len(merged):2] = row1
            merged[1:len(merged):2] = row2
            encrypted_text += ''.join(merged) 
    encrypted_text = ''.join(plaintext[i] for i in range(0, len(plaintext), num_rails*2-2)) + encrypted_text + ''.join(plaintext[i] for i in range(num_rails-1, len(plaintext), num_rails*2-2))     
    return encrypted_text


def decrypt_railfence(ciphertext, num_rails):
    l = len(ciphertext)
    x = 1
    while num_rails + (num_rails-1)*x <= l:
        x += 1
    y = num_rails + (num_rails-1)*x - l

    rows = [[] for i in range(num_rails)]
    for i in range(num_rails):
        r = 1 if (y < num_rails) else 0
        if i == 0 or i == num_rails-1:
            slice_size = (x+1)//2 + r
        else:
            slice_size = x+r
        rows[i] = ciphertext[slice(0, slice_size)]
        ciphertext = ciphertext[slice_size:len(ciphertext)]
        y += 1

    decrypted_text = ['' for i in range(l)]
    decrypted_text[0:l:num_rails*2-2] = list(rows[0])
    decrypted_text[num_rails-1:l:num_rails*2-2] = list(rows[num_rails-1])
    for i in range(1,num_rails-1):
        decrypted_text[i:l:num_rails*2-2] = list(rows[i])[slice(0,len(rows[i]),2)]
        decrypted_text[num_rails*2-(2+i):l:num_rails*2-2] = list(rows[i])[slice(1,len(rows[i]),2)]
        
    return ''.join(decrypted_text)


# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here

