"""Trusted instructor tests for reviewflow-synthetic-courses-v1, HW 1."""
import unittest
import solution


class Requirements(unittest.TestCase):
    def test_canonical(self):
        self.assertEqual(solution.normalize_listing({"title": "  Desk  ", "price_cents": 150, "currency": "usd"}), {"title": "Desk", "price_cents": 150, "currency": "USD"})

    def test_defaults_and_purity(self):
        record = {"title": "Free", "price_cents": 0, "tag": "keep"}
        before = dict(record)
        self.assertEqual(solution.normalize_listing(record), {"title": "Free", "price_cents": 0, "currency": "RUB"})
        self.assertEqual(record, before)

    def test_blank_title(self):
        with self.assertRaises(ValueError):
            solution.normalize_listing({"title": "   ", "price_cents": 1})

    def test_invalid_price(self):
        for price in [-1, True, 1.5, "100", None]:
            with self.subTest(price=price), self.assertRaises(ValueError):
                solution.normalize_listing({"title": "Desk", "price_cents": price})

    def test_unsupported_currency(self):
        with self.assertRaises(ValueError):
            solution.normalize_listing({"title": "Desk", "price_cents": 1, "currency": "BTC"})


if __name__ == "__main__":
    unittest.main()
