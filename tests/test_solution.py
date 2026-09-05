"""Trusted instructor tests for reviewflow-synthetic-courses-v1, HW 2."""
import unittest
import solution


class Requirements(unittest.TestCase):
    def test_first_page_and_purity(self):
        items = ["c", "a", "b"]
        result = solution.paginate(items, 1, 2)
        self.assertEqual(result, ["c", "a"])
        result.append("x")
        self.assertEqual(items, ["c", "a", "b"])

    def test_empty_and_past_end(self):
        self.assertEqual(solution.paginate([], 1, 5), [])
        self.assertEqual(solution.paginate([1, 2], 9, 1), [])

    def test_second_page(self):
        self.assertEqual(solution.paginate([5, 4, 3, 2, 1], 2, 2), [3, 2])

    def test_invalid_page(self):
        for page in [0, -1, True]:
            with self.subTest(page=page), self.assertRaises(ValueError):
                solution.paginate([1, 2], page, 2)

    def test_invalid_page_size(self):
        for size in [0, 51, True]:
            with self.subTest(size=size), self.assertRaises(ValueError):
                solution.paginate([1, 2], 1, size)


if __name__ == "__main__":
    unittest.main()
