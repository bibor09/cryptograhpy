import unittest
import math
from merkell_knapsack import *
from utils import is_superincreasing

class TestMerkellKnapsackMethods(unittest.TestCase):
    def test_generate_superincreasing(self):
        result = generate_superincreasing(n=8)
        self.assertTrue(is_superincreasing(result))

    def test_if_q_and_r_from_private_key_are_coprimes(self):
        w, q, r = generate_private_key(n=8)
        self.assertTrue(math.gcd(q, r) == 1)

    def test_bytechunk_to_bits(self):
        bytechunk = bytearray([39, 95])
        bits = bytechunk_to_bits(bytechunk)
        self.assertEqual(''.join(map(lambda b: f'{b}', bits)), '0010011101011111')
        
    def test_encryption(self):
        # 40 (10) -> 00101000 (2), 17 (10) -> 00010001 (2)
        message = bytearray([40, 17])  
        public_key = [2472, 4120, 3434, 2131, 1380, 4132, 3681, 2134]
        cipher_text = encrypt_mh(message, public_key)
        self.assertEqual(cipher_text, [4814, 4265])

    def test_decryption(self):
        message = [4814, 4265]
        w = [3, 5, 16, 44, 120, 218, 744, 1316]
        q = 4875
        r = 824
        plain_text = decrypt_mh(message, (w, q, r))
        plain_text = [int(b) for b in plain_text]
        self.assertEqual(plain_text, [40, 17])


if __name__ == '__main__':
    unittest.main()