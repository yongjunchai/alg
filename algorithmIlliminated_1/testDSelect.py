import unittest
from algorithmIlliminated_1.dSelect import *


class MyTestCase(unittest.TestCase):
    def test_rSelect(self):
        dataLen = 1024
        rounds = 100
        arr = []
        for i in range(dataLen):
            arr.append(i)
        random.shuffle(arr)
        dSelect = DSelect()
        for i in range(rounds):
            ith = random.randint(1, dataLen)
            j, index = dSelect.select(arr, 0, dataLen - 1, ith)
            self.assertTrue(j == ith - 1)
            self.assertTrue(j == arr[index])


if __name__ == '__main__':
    unittest.main()
