"""Trusted instructor tests for reviewflow-synthetic-courses-v1, HW 4."""
import unittest
import solution


class Requirements(unittest.TestCase):
    def test_live_and_expired(self):
        self.assertEqual(solution.visible_entries({"old": ("x", 9), "live": ("y", 11)}, 10), {"live": "y"})

    def test_empty_and_purity(self):
        entries = {"live": ("y", 11)}
        result = solution.visible_entries(entries, 10)
        result["live"] = "changed"
        self.assertEqual(entries, {"live": ("y", 11)})
        self.assertEqual(solution.visible_entries({}, 10), {})

    def test_expiry_boundary(self):
        self.assertEqual(solution.visible_entries({"edge": ("x", 10)}, 10), {})

    def test_falsy_values(self):
        self.assertEqual(solution.visible_entries({"zero": (0, 11), "empty": ("", 11), "flag": (False, 11)}, 10), {"zero": 0, "empty": "", "flag": False})

    def test_permanent(self):
        self.assertEqual(solution.visible_entries({"forever": ("x", None)}, 10), {"forever": "x"})


if __name__ == "__main__":
    unittest.main()
