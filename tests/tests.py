import unittest
import random
from hashlib import sha1
from batteryhorse.encoder import encode_data, decode_data


class TestEncoding(unittest.TestCase):
    def test_encodes(self):
        self.assertEqual(encode_data(b'test'), "Appertain backrest ablative")
        self.assertEqual(encode_data(b't'), "Adsorb")

        sentence = 'Birdnest bluetongue cheliferous yet aristotelic. Bethink bafflement afoot lest artesian. Digitalize alocasia cherubic nor absolved'
        self.assertEqual(encode_data(sha1(b'test').digest()), sentence)
    
    def test_decodes(self):
        sentence = 'Birdnest bluetongue cheliferous yet aristotelic. Bethink bafflement afoot lest artesian. Digitalize alocasia cherubic nor absolved'
        self.assertEqual(decode_data(sentence, 20), sha1(b'test').digest())

    def test_known_matches(self):
        expected_result = b'a'
        self.assertEqual(decode_data(encode_data(expected_result), len(expected_result)), expected_result)
    
    def test_random_matches(self):
        for _ in range(500):
            expected_result = sha1(str(random.randint(0, 2 ** 64)).encode('ascii')).digest()
            self.assertEqual(decode_data(encode_data(expected_result), len(expected_result)), expected_result, "Failed with bytes: %s" % expected_result)
