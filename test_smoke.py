import unittest

from solution import Ledger


class LedgerSmoke(unittest.TestCase):
    def test_initial_state(self):
        ledger = Ledger()
        self.assertEqual(ledger.revision, 0)
        self.assertEqual(ledger.balance("cash", 0), 0)
        self.assertEqual(ledger.apply([]), 0)

    def test_post_and_retry(self):
        ledger = Ledger()
        event = {"id": "p1", "kind": "post", "account": "cash", "effective": 4, "amount": 9}
        self.assertEqual(ledger.apply([event]), 1)
        self.assertEqual(ledger.apply([dict(event)]), 1)
        self.assertEqual(ledger.balance("cash", 4), 9)

    def test_window(self):
        ledger = Ledger()
        ledger.apply([{"id": "p1", "kind": "post", "account": "cash", "effective": 4, "amount": 9}])
        self.assertEqual(ledger.window(0, 10, 10), [
            {"start": 0, "end": 10, "account": "cash", "amount": 9, "count": 1}
        ])

    def test_restore_and_retract(self):
        ledger = Ledger()
        ledger.apply([{"id": "p1", "kind": "post", "account": "cash", "effective": 4, "amount": 9}])
        other = Ledger.restore(ledger.checkpoint())
        other.apply([{"id": "r1", "kind": "retract", "target": "p1"}])
        self.assertEqual(other.balance("cash", 10), 0)
        self.assertEqual(ledger.balance("cash", 10), 9)


if __name__ == "__main__":
    unittest.main()
