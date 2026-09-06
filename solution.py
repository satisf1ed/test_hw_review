import re
from copy import deepcopy


def _integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("integer out of range")
    return value


def _name(value):
    if type(value) is not str or re.fullmatch(r"[A-Za-z0-9_.:-]{1,64}", value) is None:
        raise ValueError("invalid identifier")
    return value


def _event(value):
    if type(value) is not dict:
        raise ValueError("event must be a dictionary")
    kind = value.get("kind")
    if kind == "post":
        if set(value) != {"id", "kind", "account", "effective", "amount"}:
            raise ValueError("invalid post fields")
        _name(value["account"])
        _integer(value["effective"], 0, 10**9)
        if _integer(value["amount"], -(10**12), 10**12) == 0:
            raise ValueError("zero amount")
    elif kind == "retract":
        if set(value) != {"id", "kind", "target"}:
            raise ValueError("invalid retract fields")
        _name(value["target"])
    else:
        raise ValueError("invalid event kind")
    _name(value.get("id"))
    return dict(value)


class Ledger:
    def __init__(self):
        self._revision = 0
        self._entries = {}
        self._retracted = {}
        self._journal = []

    @property
    def revision(self):
        return self._revision

    def apply(self, events):
        if type(events) is not list:
            raise ValueError("batch must be a list")
        entries = self._entries.copy()
        retracted = self._retracted.copy()
        pending = []
        revision = self._revision + 1
        for raw in events:
            event = _event(raw)
            identifier = event["id"]
            if identifier in entries:
                if entries[identifier][1] != event:
                    raise ValueError("conflicting retry")
                continue
            if event["kind"] == "retract":
                target = event["target"]
                if target not in entries or entries[target][1]["kind"] != "post":
                    raise ValueError("target must precede retract")
                if target in retracted:
                    raise ValueError("target already retracted")
                retracted[target] = revision
            entries[identifier] = (revision, event)
            pending.append({"revision": revision, "event": event})
        if pending:
            self._entries = entries
            self._retracted = retracted
            self._journal.extend(pending)
            self._revision = revision
        return self._revision

    def _knowledge(self, known_at):
        if known_at is None:
            return self._revision
        return _integer(known_at, 0, self._revision)

    def _visible(self, known_at):
        for revision, event in self._entries.values():
            if event["kind"] == "post" and revision <= known_at:
                withdrawn = self._retracted.get(event["id"])
                if withdrawn is None or withdrawn > known_at:
                    yield event

    def balance(self, account, at, known_at=None):
        _name(account)
        _integer(at, 0, 10**9)
        known_at = self._knowledge(known_at)
        return sum(event["amount"] for event in self._visible(known_at)
                   if event["account"] == account and event["effective"] <= at)

    def window(self, start, end, width, known_at=None):
        _integer(start, 0, 10**9)
        _integer(end, start, 10**9)
        _integer(width, 1, 10**9)
        known_at = self._knowledge(known_at)
        events = [event for event in self._visible(known_at) if start <= event["effective"] < end]
        accounts = sorted({event["account"] for event in events})
        aggregates = {}
        for event in events:
            key = ((event["effective"] - start) // width, event["account"])
            amount, count = aggregates.get(key, (0, 0))
            aggregates[key] = (amount + event["amount"], count + 1)
        result = []
        for index, left in enumerate(range(start, end, width)):
            for account in accounts:
                amount, count = aggregates.get((index, account), (0, 0))
                result.append({"start": left, "end": min(end, left + width),
                               "account": account, "amount": amount, "count": count})
        return result

    def checkpoint(self):
        return deepcopy({"version": 1, "revision": self._revision, "events": self._journal})

    @classmethod
    def restore(cls, snapshot):
        if type(snapshot) is not dict or set(snapshot) != {"version", "revision", "events"}:
            raise ValueError("invalid snapshot fields")
        _integer(snapshot["version"], 1, 1)
        revision = snapshot["revision"]
        if type(revision) is not int or revision < 0:
            raise ValueError("invalid snapshot revision")
        rows = snapshot["events"]
        if type(rows) is not list:
            raise ValueError("invalid journal")
        ledger = cls()
        group = []
        current = 0
        seen = set()
        for row in rows:
            if type(row) is not dict or set(row) != {"revision", "event"}:
                raise ValueError("invalid journal row")
            number = _integer(row["revision"], 1, revision)
            if number != current:
                if number != current + 1:
                    raise ValueError("non-contiguous revision")
                if group:
                    ledger.apply(group)
                group = []
                current = number
            event = _event(row["event"])
            if event["id"] in seen:
                raise ValueError("duplicate journal identifier")
            seen.add(event["id"])
            group.append(event)
        if group:
            ledger.apply(group)
        if ledger.revision != revision:
            raise ValueError("snapshot revision mismatch")
        return ledger
