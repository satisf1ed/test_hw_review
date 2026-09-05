# HW 4: TTL cache snapshot semantics

Implement visible_entries(entries, now). Input maps keys to (value, expires_at) pairs using numeric timestamps or None for no expiry. Return a new key-to-value dict containing entries whose expiry is strictly greater than now or None. Preserve falsy values and input data. Expiry exactly at now is already expired.

Use Python 3 standard library only. Edit solution.py; do not change the trusted tests. Run python -m unittest discover -s tests -v in the offline sandbox. Add a short SUBMISSION.md describing the implementation and limitations. The base contains a passing reference implementation for this explicitly synthetic course.

## Rubric (10 points; reviewer decides)

- Correct cache boundary and permanent entries (4): 4: all core requirements hold; 2: main path works with gaps; 0: core behavior absent or incorrect.
- Preserve falsy values and input snapshot (4): 4: boundary and invalid-input requirements hold; 2: some cases handled; 0: no reliable handling. Cite concrete cases.
- Readable implementation and evidence (2): 2: concise, reproducible explanation with limitations; 1: partial explanation; 0: absent or misleading. Test counts are evidence, not a grade.

Submission deadline (simulated): 2026-08-28T18:00:00Z
Review deadline (simulated): 2026-08-31T18:00:00.000Z

## Synthetic course

reviewflow-synthetic-courses-v1. All identities and submission dates are simulations, not real students.
Submit solutions/hw_4/<slug> into hw_4, never main.
