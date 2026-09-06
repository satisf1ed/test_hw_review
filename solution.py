import re
from copy import deepcopy


def integer(value, lo, hi):
    if type(value) is not int or not lo <= value <= hi:
        raise ValueError("invalid integer")


def identifier(value):
    if type(value) is not str or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,64}", value):
        raise ValueError("invalid identifier")


def validate(event):
    if type(event) is not dict:
        raise ValueError("invalid event")
    if event.get("kind") == "post":
        if set(event) != {"id", "kind", "account", "effective", "amount"}:
            raise ValueError("invalid fields")
        identifier(event["account"])
        integer(event["effective"], 0, 10**9)
        integer(event["amount"], -(10**12), 10**12)
        if event["amount"] == 0:
            raise ValueError("empty posting")
    elif event.get("kind") == "retract":
        if set(event) != {"id", "kind", "target"}:
            raise ValueError("invalid fields")
        identifier(event["target"])
    else:
        raise ValueError("unknown kind")
    identifier(event["id"])


class Ledger:
    def __init__(self):
        self._revision = 0
        self._events = []
        self._ids = {}
        self._withdrawn = {}

    @property
    def revision(self):
        return self._revision

    def apply(self, events):
        if type(events) is not list:
            raise ValueError("invalid batch")
        started = False
        for raw in events:
            validate(raw)
            event = deepcopy(raw)
            if event["id"] in self._ids:
                if self._ids[event["id"]]["event"] != event:
                    raise ValueError("conflicting event")
                continue
            if event["kind"] == "retract":
                target = self._ids.get(event["target"])
                if not target or target["event"]["kind"] != "post":
                    raise ValueError("unknown posting")
                if event["target"] in self._withdrawn:
                    raise ValueError("already withdrawn")
            if not started:
                self._revision += 1
                started = True
            row = {"revision": self._revision, "event": event}
            self._ids[event["id"]] = row
            self._events.append(row)
            if event["kind"] == "retract":
                self._withdrawn[event["target"]] = self._revision
        return self._revision

    def _known(self, known_at):
        if known_at is not None:
            integer(known_at, 0, self._revision)
        return known_at or self._revision

    def _posts(self, known_at):
        return [row["event"] for row in self._events
                if row["revision"] <= known_at and row["event"]["kind"] == "post"
                and self._withdrawn.get(row["event"]["id"], self._revision + 1) > known_at]

    def balance(self, account, at, known_at=None):
        identifier(account)
        integer(at, 0, 10**9)
        known = self._known(known_at)
        return sum(event["amount"] for event in self._posts(known)
                   if event["account"] == account and event["effective"] <= at)

    def window(self, start, end, width, known_at=None):
        integer(start, 0, 10**9)
        integer(end, start, 10**9)
        integer(width, 1, 10**9)
        known = self._known(known_at)
        posts = [event for event in self._posts(known) if start <= event["effective"] <= end]
        accounts = sorted({event["account"] for event in posts})
        totals = {}
        for event in posts:
            key = ((event["effective"] - start) // width, event["account"])
            total = totals.setdefault(key, [0, 0])
            total[0] += event["amount"]
            total[1] += 1
        result = []
        for index, left in enumerate(range(start, end, width)):
            right = min(end, left + width)
            for account in accounts:
                amount, count = totals.get((index, account), (0, 0))
                result.append({"start": left, "end": right, "account": account,
                               "amount": amount, "count": count})
        return result

    def checkpoint(self):
        return {"version": 1, "revision": self._revision, "events": self._events}

    @classmethod
    def restore(cls, snapshot):
        if not isinstance(snapshot, dict) or snapshot.get("version") != 1:
            raise ValueError("unsupported snapshot")
        ledger = cls()
        ledger._revision = snapshot["revision"]
        ledger._events = snapshot["events"]
        for row in ledger._events:
            event = row["event"]
            ledger._ids[event["id"]] = row
            if event["kind"] == "retract":
                ledger._withdrawn[event["target"]] = row["revision"]
        return ledger
