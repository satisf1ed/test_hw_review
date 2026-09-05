# HW 2: Stable pagination for a listing feed

Implement paginate(items, page, page_size). Pages are 1-indexed; return a new list in original order without mutating items. Both numeric arguments must be ints, not bool; page >= 1 and 1 <= page_size <= 50, otherwise ValueError. Empty and out-of-range pages return [].

Use Python 3 standard library only. Edit solution.py; do not change the trusted tests. Run python -m unittest discover -s tests -v in the offline sandbox. Add a short SUBMISSION.md describing the implementation and limitations. The base contains a passing reference implementation for this explicitly synthetic course.

## Rubric (10 points; reviewer decides)

- Stable 1-indexed slicing without mutation (4): 4: all core requirements hold; 2: main path works with gaps; 0: core behavior absent or incorrect.
- Validate bounds and cap response size (4): 4: boundary and invalid-input requirements hold; 2: some cases handled; 0: no reliable handling. Cite concrete cases.
- Readable implementation and evidence (2): 2: concise, reproducible explanation with limitations; 1: partial explanation; 0: absent or misleading. Test counts are evidence, not a grade.

Submission deadline (simulated): 2026-08-14T18:00:00Z
Review deadline (simulated): 2026-08-17T18:00:00.000Z

## Synthetic course

reviewflow-synthetic-courses-v1. All identities and submission dates are simulations, not real students.
Submit solutions/hw_2/<slug> into hw_2, never main.
