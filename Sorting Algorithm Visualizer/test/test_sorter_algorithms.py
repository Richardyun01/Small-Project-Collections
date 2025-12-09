import unittest
from sorter import SORT_ALGORITHMS


class TestSorterAlgorithms(unittest.TestCase):
    def test_all_algorithms_sort_correctly(self):
        original = [5, 3, 8, 1, 4, 2, 7, 6]

        for name, algo in SORT_ALGORITHMS.items():
            with self.subTest(algorithm=name):
                arr = original[:]
                gen = algo(arr, key=lambda x: x)
                for _ in gen:
                    pass

                self.assertEqual(
                    arr,
                    sorted(original),
                    msg=f"{name} did not sort correctly",
                )


if __name__ == "__main__":
    unittest.main()
