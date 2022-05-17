import unittest


#paragraf kodeksu pracy
from Zadania.Library import EasyThread as q
from cwiczenia.rozmowa import new_dic


class EasyThreadTest(unittest.TestCase):
    def test_all(self):
        test = q.EasyThread()
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