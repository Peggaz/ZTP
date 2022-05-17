import unittest
from Zadania.autokorekta.DamerauDistance import DamerauDistance


class DamerauDistanceTest(unittest.TestCase):
    def testMain(self):
        dd = DamerauDistance()
        self.assertEqual(dd.MakeAndGetDistance('pierze', 'pieże'), 0.5)
        self.assertEqual(dd.MakeAndGetDistance('smiech', 'śmiech'), 0.2)
        self.assertEqual(dd.MakeAndGetDistance('piora', 'piórą'),0.4)
        self.assertEqual(dd.MakeAndGetDistance('piura', 'pióra'), 0.5)
        self.assertEqual(dd.MakeAndGetDistance('człowiek', 'cłzoiwek'), 1.0)
        self.assertEqual(dd.MakeAndGetDistance('zrobić', 'rzobić'), 0.5)
        self.assertEqual(dd.MakeAndGetDistance('zima', 'źima'), 0.2)
        self.assertEqual(dd.MakeAndGetDistance('prosiłem', 'prsoilem'), 0.7)
        self.assertEqual(dd.MakeAndGetDistance('ćwok', 'wciok'), 1.2)  # Godny coś pojebał
if __name__ == '__main__':
    unittest.main()