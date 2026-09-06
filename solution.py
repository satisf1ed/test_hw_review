from copy import deepcopy


class Ledger:
    def __init__(self):
        self._revision = 0
        self._events = []

    @property
    def revision(self):
        return self._revision

    def apply(self, events):
        if not isinstance(events, list):
            raise ValueError("expected a list")
        ids = {row["event"]["id"] for row in self._events}
        changed = False
        for event in events:
            if not isinstance(event, dict) or not event.get("id"):
                raise ValueError("event id is required")
            if event["id"] in ids:
                continue
            kind = event.get("kind")
            if kind == "post":
                if not isinstance(event.get("account"), str):
                    raise ValueError("account is required")
                if not isinstance(event.get("amount"), int) or not isinstance(event.get("effective"), int):
                    raise ValueError("posting requires integer values")
            elif kind == "retract":
                if not isinstance(event.get("target"), str):
                    raise ValueError("target is required")
            else:
                raise ValueError("unknown operation")
            if not changed:
                self._revision += 1
                changed = True
            self._events.append({"revision": self._revision, "event": dict(event)})
            ids.add(event["id"])
        return self._revision

    def _active(self):
        removed = {row["event"]["target"] for row in self._events if row["event"]["kind"] == "retract"}
        return [row["event"] for row in self._events
                if row["event"]["kind"] == "post" and row["event"]["id"] not in removed]

    def balance(self, account, at, known_at=None):
        return sum(event["amount"] for event in self._active()
                   if event["account"] == account and event["effective"] <= at)

    def window(self, start, end, width, known_at=None):
        if not 0 <= start <= end <= 10**9 or not 1 <= width <= 10**9:
            raise ValueError("invalid interval")
        result = []
        for left in range(start, end, width):
            right = min(left + width, end)
            buckets = {}
            for event in self._active():
                if left <= event["effective"] < right:
                    bucket = buckets.setdefault(event["account"], [0, 0])
                    bucket[0] += event["amount"]
                    bucket[1] += 1
            for account in sorted(buckets):
                amount, count = buckets[account]
                result.append({"start": left, "end": right, "account": account,
                               "amount": amount, "count": count})
        return result

    def checkpoint(self):
        return deepcopy({"version": 1, "revision": self._revision, "events": self._events})

    @classmethod
    def restore(cls, snapshot):
        if not isinstance(snapshot, dict) or snapshot.get("version") != 1:
            raise ValueError("unsupported format")
        ledger = cls()
        ledger._revision = snapshot["revision"]
        ledger._events = deepcopy(snapshot["events"])
        return ledger
