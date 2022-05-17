import unittest

from Zadania.AEI.konkordancja import Answer


class TestAnswer(unittest.TestCase):
    def testStr(self):
        obj = Answer(12, 11, "ala ma kota")
        self.assertEqual("tekst nr: 12 zdanie nr: 11 ala ma kota\n", str(obj))
        obj = Answer(12, -1, "ala ma kota")
        self.assertEqual("tekst nr: 12 ala ma kota\n", str(obj))
        obj = Answer(zdanie="ala ma kota", nr_tekst=12)
        self.assertEqual("tekst nr: 12 ala ma kota\n", str(obj))

class TestKonkordancja(unittest.TestCase):
    

