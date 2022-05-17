import unittest

from Zadania.Library.clp3 import CLP
from Zadania.Library.library import CLP_ON


class Clp3Test(unittest.TestCase):

    zolc_list = ['zolc', 'żolc', 'żólc', 'żółc', 'żółć', 'żólć', 'żołc', 'żołć', 'żolć', 'źolc', 'źólc', 'źółc', 'źółć', 'źólć', 'źołc', 'źołć', 'źolć', 'zólc', 'zółc', 'zółć', 'zólć', 'zołc', 'zołć', 'zolć']

    def testNewRec(self):
        if CLP_ON:
            obj = CLP()
            self.assertEqual(obj.newRec('krol'),
                             [
                                 obj.rec('krol'),
                                 obj.rec('król'),
                                 obj.rec('kroł'),
                                 obj.rec('krół')
                             ])  # add assertion here
            compare_list = []
            for it in self.zolc_list:
                compare_list.append(obj.rec(it))
            self.assertEqual(obj.newRec('zolc'), compare_list)  # add assertion here
    def testAllWords(self):
        obj = CLP()
        self.assertEqual(obj.allWords('zolc'), self.zolc_list)



if __name__ == '__main__':
    unittest.main()
