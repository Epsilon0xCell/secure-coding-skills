# Worked examples

Three findings, run through both skills in this pack. The code in each folder is small, self-contained, and written for this repository; it is not taken from any real project.

Each example has the same parts:

- The code the audit read. Example 03's code spans two files: `invoices.py`, the handlers, and `db.py`, the data layer the disproof pass checked for an ownership check.
- `FINDING.md`, the first pass, written by the diff-security-audit skill in its own format.
- `DISPROOF.md`, the second pass, written by the adversarial-disproof skill after trying to kill the finding.

Two findings survive. One does not. The one that does not is the most instructive file in this repository: the first pass was confident, the flow looked traced, and the guard was sitting in middleware the audit never opened. That is the normal failure mode of security review, human or agent, and it is why the second pass exists.

| Example | Class | First pass | Second pass |
|---|---|---|---|
| 01 | SQL injection | Reported, high confidence | CONFIRMED |
| 02 | SSRF | Reported, high confidence | KILLED |
| 03 | Broken authorization (IDOR) | Reported, medium confidence | CONFIRMED, restated more precisely |
