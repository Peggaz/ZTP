import random
import unittest
import requests
from rozmowa import new_dic


#paragraf kodeksu pracy

class RozmowaDicTest(unittest.TestCase):
    def test_all(self):
        test = new_dic()
        test.set(1, 2)
        test.set(2, 3)
        self.assertEqual(test.get(1), [1, 2])
        test.set(1, 88)
        self.assertEqual(test.get(1), [1, 88])
        test.remove(1)
        self.assertEqual(test.get(1), None)

    def test_secound(self):
        test = new_dic()
        test.set(1, 2)
        test.set(2, 3)
        self.assertEqual(test.get(1), [1, 2])
        test.set(1, 88)
        self.assertEqual(test.get(1), [1, 88])
        test.remove(1)
        self.assertEqual(test.get(1), None)

if __name__ == '__main__':
    unittest.main()