import random

# Miller-Rabin test for efficient testing if a number is prime
def miller_test(n, s, r):
    a = random.randrange(2, n-2)
    x = pow(a, s, n)

    if x == 1 or x == n-1:
        return True
        
    while r-1 > 0:
        x = (x * x) % n
        if x == n-1:
            return True
        if x == 1:
            return False
        r -= 1
        
    return False

def miller_rabin_prime_test(n, k):
    if n < 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    s = n - 1
    r = 0
    while s % 2 == 0:
        s //= 2
        r += 1
    
    # Test with k accuracy
    while k > 0:
        if miller_test(n, s, r) == False:
            return False
        k -= 1

    return True


# Generating the prime numbers
def is_prime_okay(p):
    return p % 4 == 3 and miller_rabin_prime_test((p-1) / 2, 40)

def generate_prime():
    p = random.randint(0, 2**512)
    while miller_rabin_prime_test(p, 40) == False and not is_prime_okay(p):
        p = random.randint(0, 2**1000)
    return p

# Generate the seed (first generate n)
def generate_n_for_seed_blumblum():
    p = generate_prime()
    q = generate_prime()
    while p == q:
        q = generate_prime()

    n = p * q
    return n

def generate_seed_blumblum(n):
    return random.randrange(1, n-1)

def blum_blum_shub(leng, key):
    n, seed = key
    x = [0 for _ in range(leng)]
    x[0] = pow(seed, 2, n)
    z = ['0' for _ in range(leng)]
    z[0] = f'{x[0] % 2}'

    for i in range(1, leng):
        x[i] = pow(x[i-1], 2, n)
        z[i] = f'{x[i] % 2}'
    return z
    
# Generate a key (byte stream) with 'leng' length 
# n is the product of p, q the two previously generated big primes
def generate_key_with_bbs(leng, key):
    return [int(''.join(blum_blum_shub(8, key)), 2) for _ in range(leng)]
