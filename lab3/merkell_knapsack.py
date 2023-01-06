import random
import math
import utils

def generate_superincreasing(n):
    seed = random.randint(2, 10)
    w = [seed]
    for _ in range(1, n):
        total = sum(w)
        w.append(random.randint(total + 1, 2 * total))
    return w

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem

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
    w = generate_superincreasing(n)
    total = sum(w)
    q = random.randint(total + 1, 2 * total)
    r = random.randint(2, q-1)
    while math.gcd(r, q) != 1:
        r = random.randint(2, q-1)
    return (w, q, r)

def create_public_key(private_key):
    """Creates a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    w, q, r = private_key
    n = len(w)
    return [(r * w[i]) % q for i in range(0, n)]

def bytechunk_to_bits(chunk):
    bits = [utils.byte_to_bits(chunk[i]) for i in range(0, len(chunk))]
    return [value for b in bits for value in b]

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
    i = 0
    message = bytechunk_to_bits(message) # convert to bits
    message_size = len(message)
    chunk_size = len(public_key)    # n is the chunk size
    cipher_text = []
    while i < message_size:
        chunk = message[i:min(i+chunk_size, message_size)]
        cipher_text.append(sum([chunk[i] * public_key[i] for i in range(0, chunk_size)]))
        i += chunk_size
    return cipher_text

def solve_subset_sum(c_, w):
    a = [0 for _ in range(len(w))]
    k = len(w)-1
    while c_ != 0:
        if w[k] > c_:
            k -= 1
        elif w[k] <= c_:
            a[k] = 1
            c_ -= w[k]
    return a

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
    w, q, r = private_key
    s = utils.modinv(r, q)
    c_ = [] 
    bytez = []
    for c in message:
        c_ = (c * s) % q
        a = solve_subset_sum(c_, w)
        bytez.append(utils.bits_to_byte(a))

    return bytez