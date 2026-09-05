"""Trusted instructor tests for reviewflow-synthetic-courses-v1, HW 3."""
import unittest
import solution


class Requirements(unittest.TestCase):
    def test_signed_amounts_and_purity(self):
        events = [{"id": "a", "amount": 125}, {"id": "b", "amount": -25}]
        before = [dict(event) for event in events]
        self.assertEqual(solution.balance(events), 100)
        self.assertEqual(events, before)

    def test_empty_and_invalid_id(self):
        self.assertEqual(solution.balance([]), 0)
        with self.assertRaises(ValueError):
            solution.balance([{"id": "", "amount": 1}])

    def test_replay(self):
        self.assertEqual(solution.balance([{"id": "a", "amount": 100}, {"id": "a", "amount": 100}]), 100)

    def test_conflict(self):
        with self.assertRaises(ValueError):
            solution.balance([{"id": "a", "amount": 100}, {"id": "a", "amount": 200}])

    def test_invalid_amount(self):
        for amount in [True, 1.5]:
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                solution.balance([{"id": "a", "amount": amount}])


if __name__ == "__main__":
    unittest.main()
