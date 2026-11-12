---
name: adversarial-disproof
description: Attack a list of security findings and try to prove each one wrong before any of them is reported. Use after a security audit (for example the diff-security-audit skill) produces findings, or whenever handed findings to validate. Each finding must survive a genuine attempt to disprove it, or be downgraded or killed with the reason recorded.
---

# Adversarial Disproof

The audit pass found defects. Your job is to prove it wrong.

Every finding you are handed is presumed false until it survives your best attempt to kill it. This is not a rubber stamp and it is not a rewrite. You do not improve the finding's wording, you do not add evidence the audit never gathered, and you do not lower your standard because the finding sounds plausible. Plausible and wrong is the normal state of first-pass security findings.

## For each finding, run all four attacks

### Attack 1: Find the guard

The audit claims input reaches a sink unguarded. Go and look for the guard it missed:

- Validation or sanitization upstream of the sink: middleware, decorators, request hooks, form or schema validation, a type that constrains the value.
- A framework behavior that neutralizes the input: automatic escaping, parameterized query builders used correctly, an ORM that binds values, a template engine in autoescape mode.
- An allowlist, denylist, or canonicalization step anywhere on the path, including in code the diff did not touch.
- A deployment fact the audit assumed wrongly: the route is mounted only in a test app, the feature flag is off, the value comes from server-side config and not from the caller at all.

If a guard exists and it covers the claimed flow, the finding dies or shrinks to whatever slips past the guard. Say which.

### Attack 2: Retrace the flow independently

Do not reuse the audit's reading. Starting from the sink, walk backwards to the source yourself. Check:

- Is the claimed source really attacker-controlled, or is it a constant, a server-generated value, or an internal caller's argument?
- Does the path the audit described actually exist, or does the data pass through a transformation that changes its meaning (parsed to an integer, matched against an enum, resolved to an internal object before use)?
- Is the vulnerable code reachable at all: live route, exported function with real callers, or dead code, example code, and tests?

A flow that cannot be retraced by a second reader was never a flow. Kill the finding.

### Attack 3: Break the preconditions

The finding states preconditions. Attack each one:

- Reachability: can the stated actor actually reach the input? An "unauthenticated" claim on a route behind authentication middleware fails here.
- Control: does the actor control the whole value, part of it, or only its length or timing? Partial control often caps the impact far below the claim.
- Environment: does the claim need a non-default configuration, a debug flag, or a second defect to chain? If so, the finding's impact statement must say so, and usually drops a level.

### Attack 4: Write the strongest honest counter-argument

In two or three sentences, write the case a maintainer would make for closing this finding as invalid. If you can write it and it holds against the code, kill or downgrade the finding. If you write it and it collapses on a specific line of code, that collapse is the finding's best evidence: record the line and mark the finding confirmed with more confidence than the audit gave it.

## Verdicts

Each finding leaves with exactly one verdict:

- **CONFIRMED.** At least one attack was run properly and the finding survived it; name the attack that came closest and why it failed.
- **DOWNGRADED.** The defect is real but smaller than claimed: the guard covers part of the flow, the precondition is narrower, or the impact is lower. Restate the finding at its true size, in the audit's format.
- **KILLED.** A guard exists, the flow does not exist, or the preconditions fail. Record the specific code or fact that kills it, so nobody re-files it next week.
- **UNEXAMINED.** You could not run the attacks, because code was unavailable, the environment could not be checked, or the flow leaves the repository. Unexamined is not confirmed. It goes to the human labelled as unchecked, with what is missing named.

## Output shape

```
F1 (SQL injection, app/search.py)
Verdict: CONFIRMED
Closest attack: Guard hunt. The codebase has a sanitize() helper for user
  input; it is applied to the comment form and not to /search.
Why it survives: q flows from request.args into the query string with no
  binding and no validation on the path. The counter-argument ("the ORM
  parameterizes") fails at app/search.py line 41, where the query is a
  plain string passed to execute().
```

Close with counts: how many findings entered, how many leave confirmed, downgraded, killed, unexamined. A pass that kills nothing is a pass that did not try; if everything survives, say what your strongest attack was and why the set withstood it.

## The point

A finding that reaches a human after this pass carries two things a raw audit cannot give: the strongest argument against it, and the reason that argument fails. That is what makes a report worth a maintainer's time, and it is why this skill never edits a finding to make it sound better. It only shrinks the set to the findings that are true.
