import random
import unittest
import requests
import Zadania
import autokorekta as q


class autokorektaTest(unittest.TestCase):
    def testBigFirstChar(self):
        self.assertEqual("Ala", q.BigFirstChar("ala"))
        self.assertEqual("Ala.", q.BigFirstChar("ala."))
        self.assertEqual("Ala", q.BigFirstChar("Ala"))
        self.assertEqual("Ala.", q.BigFirstChar("Ala."))
    def testkorekta(self):
        self.assertEqual("Koty to fajne zwierzęta ", q.Korekta("Koty to fajne zfieszęta", "../../teksty/test.txt"))
        self.assertEqual("Śmiech to zdrowie. Ptaki mają pierze. Huśtawka nie tylko dla dzieci. Robić złośliwości. ", q.Korekta("Smiehc to zdrowie. Ptaki mają pieże. Chóśtawka nie ytlko lda zdieic. Robic zlośliwosci.",
                                                                                                                               "../../teksty/test.txt"))

if __name__ == '__main__':
    unittest.main()