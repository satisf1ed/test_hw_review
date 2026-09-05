# HW 3: Idempotent payment-event aggregation

Implement balance(events) for dictionaries with id (nonempty string) and amount (integer cents, not bool). Sum positive charges and negative refunds. Ignore repeated ids with the same amount. Conflicting repeated ids or invalid amounts raise ValueError. Do not mutate events; an empty stream totals zero.

Use Python 3 standard library only. Edit solution.py; do not change the trusted tests. Run python -m unittest discover -s tests -v in the offline sandbox. Add a short SUBMISSION.md describing the implementation and limitations. The base contains a passing reference implementation for this explicitly synthetic course.

## Rubric (10 points; reviewer decides)

- Signed cents and idempotent replay (4): 4: all core requirements hold; 2: main path works with gaps; 0: core behavior absent or incorrect.
- Detect conflicting events and invalid amounts (4): 4: boundary and invalid-input requirements hold; 2: some cases handled; 0: no reliable handling. Cite concrete cases.
- Readable implementation and evidence (2): 2: concise, reproducible explanation with limitations; 1: partial explanation; 0: absent or misleading. Test counts are evidence, not a grade.

Submission deadline (simulated): 2026-08-21T18:00:00Z
Review deadline (simulated): 2026-08-24T18:00:00.000Z

## Synthetic course

reviewflow-synthetic-courses-v1. All identities and submission dates are simulations, not real students.
Submit solutions/hw_3/<slug> into hw_3, never main.
