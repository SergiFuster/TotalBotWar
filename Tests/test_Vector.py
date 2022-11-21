import math
import unittest

from Utilities.Vector import Vector


class TestVector(unittest.TestCase):
    def test_magnitude(self):
        v = Vector([1, 2, 3])
        actual = v.magnitude()
        expected = math.sqrt(1*1+2*2+3*3)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
