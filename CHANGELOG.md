# Changelog

## v0.1.0, 2026-11-12

First release.

- `diff-security-audit` skill: diff-scoped pre-PR security audit across injection, SSRF, authorization, secrets, and unsafe deserialization, with a reference file per class and a findings format built to be attacked.
- `adversarial-disproof` skill: the second pass. Four attacks per finding (guard hunt, independent retrace, precondition break, strongest counter-argument) and four verdicts: confirmed, downgraded, killed, unexamined.
- Three worked examples with code, finding, and disproof attempt: a confirmed SQL injection, an SSRF killed by a middleware guard the first pass missed, and a confirmed IDOR restated at its true size.
- `install.sh` installer for the SKILL.md layout.
