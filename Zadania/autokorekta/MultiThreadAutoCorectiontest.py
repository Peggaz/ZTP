import random
import unittest
import requests
import Zadania
import MultiThreadAutoCorection as q


class MultiThreadAutoCorectionTest(unittest.TestCase):
    def testBigFirstChar(self):
        self.assertEqual("Ala", q.BigFirstChar("ala"))
        self.assertEqual("Ala.", q.BigFirstChar("ala."))
        self.assertEqual("Ala", q.BigFirstChar("Ala"))
        self.assertEqual("Ala.", q.BigFirstChar("Ala."))
    def testkorekta(self):
        self.assertEqual("Koty to fajne zwierzęta ", q.MainTextCorection("Koty to fajne zfieszęta", "../../teksty/test.txt"))
        self.assertEqual("Śmiech to zdrowie. Ptaki mają pierze. Huśtawka nie tylko dla dzieci. Robić złośliwości. ", q.MainTextCorection("Smiehc to zdrowie. Ptaki mają pieże. Chóśtawka nie ytlko lda zdieic. Robic zlośliwosci.",
                                                                                                                               "../../teksty/test.txt"))

if __name__ == '__main__':
    unittest.main()