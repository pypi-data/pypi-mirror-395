
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))
import unittest
from l0n0lc.jit import 即时编译


class TestJitFunction(unittest.TestCase):
    def test_basic_function(self):
        @即时编译()
        def add(a: int, b: int) -> int:
            return a + b

        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(10, -5), 5)

    def test_type_handling(self):
        @即时编译()
        def multiply(a: int, b: int) -> int:
            return a * b

        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(2, 2), 4)

    def test_edge_cases(self):
        @即时编译()
        def decrement(x: int) -> int:
            return x - 1


        self.assertEqual(decrement(0), -1)
        self.assertEqual(decrement(-10), -11)


if __name__ == '__main__':
    unittest.main()
