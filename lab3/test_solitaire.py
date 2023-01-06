import unittest
from solitaire import *

seed = [12, 26, 20, 37, 31, 38, 24, 4, 54, 28, 48, 42, 53, 23, 27, 40, 3, 39, 13, 45, 30, 43, 8, 36, 32, 52, 47, 29, 1, 14, 46, 22, 9, 10, 16, 7, 44, 21, 35, 6, 18, 33, 5, 19, 34, 2, 49, 41, 15, 25, 51, 11, 17, 50]
seed2 = [5, 19, 34, 2, 49, 41, 15, 25, 51, 11, 17, 50, 54, 42, 23, 53, 12, 26, 20, 37, 31, 38, 24, 4, 48, 27, 40, 3, 39, 13, 45, 30, 43, 8, 36, 32, 52, 47, 29, 1, 14, 46, 22, 9, 10, 16, 7, 44, 21, 35, 6, 18, 33, 28]

class TestSolitaireMethods(unittest.TestCase):
    def test_solitaire_new_seed(self):
        new_seed, _ = solitaire(seed)
        expected = [5, 19, 34, 2, 49, 41, 15, 25, 51, 11, 17, 50, 54, 42, 23, 53, 12, 26, 20, 37, 31, 38, 24, 4, 48, 27, 40, 3, 39, 13, 45, 30, 43, 8, 36, 32, 52, 47, 29, 1, 14, 46, 22, 9, 10, 16, 7, 44, 21, 35, 6, 18, 33, 28]
        self.assertEqual(new_seed, expected)
        
    def test_solitaire_key(self):
        _, key = solitaire(seed)
        self.assertEqual(key, 41)

    def test_solitaire_key2(self):
        _, key = solitaire(seed2)
        self.assertEqual(key, 14)

    def test_key_generation(self):
        n = 1 # one byte
        [result] = generate_key_with_solitaire(n, seed)
        self.assertEqual(result, (41*14) % 256)

if __name__ == '__main__':
    unittest.main()