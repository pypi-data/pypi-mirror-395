import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import unittest
from l0n0lc import jit
class Point:
    x: int
    y: int
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def area(self) -> int:
        return self.x * self.y

@jit()
def test_point_area(x: int, y: int) -> int:
    p = Point(x, y)
    return p.area()

class TestClassJit(unittest.TestCase):
    def test_basic_class(self):
        self.assertEqual(test_point_area(10, 20), 200)

if __name__ == '__main__':
    unittest.main()
