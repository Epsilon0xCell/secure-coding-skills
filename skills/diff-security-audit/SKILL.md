---
name: diff-security-audit
description: Audit a code diff for security defects before it becomes a pull request. Use when asked to security-review changes, check a branch or patch before opening a PR, or self-review code an agent has just written. Covers injection, SSRF, broken authorization, secrets, and unsafe deserialization. Produces findings with traced data flows, ready for the adversarial-disproof pass.
---

# Diff Security Audit

You are auditing a diff, not a codebase. The diff is the scope. Your job is to find the places where the change lets attacker-controlled input reach something it should not reach, and to prove each one with a data flow you can point at. A finding without a traced flow is a guess, and guesses do not ship.

Run this before the pull request opens. Run the adversarial-disproof skill after this one, on this skill's output, before anything is reported to a human.

## Step 1: Get the diff and read it whole

1. Identify the base. If the user names a branch or PR, diff against its base. Otherwise diff the working branch against the repository's default branch: `git diff <base>...HEAD`. Include staged and unstaged work if the user asks about uncommitted changes: `git diff HEAD`.
2. Read every changed hunk. Do not sample. A three-line change to an authorization helper outweighs a thousand lines of new tests.
3. Note what the diff does in one sentence. If you cannot, read it again. The audit findings hang off that sentence.

## Step 2: Map the changed attack surface

From the diff alone, list:

- **New or changed inputs.** Request parameters, headers, bodies, file uploads, CLI arguments, environment reads, queue messages, webhook payloads, anything deserialized.
- **New or changed sinks.** Database queries, shell commands, template renders, outbound HTTP requests, file paths, HTML output, eval-like constructs, object construction from serialized data.
- **New or changed trust decisions.** Authentication checks, authorization checks, allowlists, signature verification, rate limits, tenancy filters.
- **New or changed secrets handling.** Keys, tokens, passwords, connection strings, logging of any of the above.

Any line that touches two lists at once (an input and a sink, an input and a trust decision) gets audited first.

## Step 3: Audit by class

Work the five classes in this order. The reference file for each class has the concrete patterns and the false-positive traps. Read the reference when a hunk smells like the class; do not load all five by default.

1. **Injection** (`references/injection.md`). Attacker text becomes part of a query, command, template, or expression.
2. **SSRF** (`references/ssrf.md`). Attacker text decides where the server makes a request.
3. **Authorization** (`references/authorization.md`). A check is missing, ordered wrong, applied to the wrong object, or trusts an identifier the caller supplied.
4. **Secrets** (`references/secrets.md`). Credentials enter code, config, logs, error messages, or the diff itself.
5. **Unsafe deserialization** (`references/deserialization.md`). Bytes an attacker can influence are turned into live objects, code, or types.

## Step 4: State each finding so it can be attacked

Every finding leaves this skill in exactly this shape:

```
ID: F1
Class: injection (SQL)
Location: app/search.py, the query built in search_items()
Claim: The q request parameter reaches the SQL query as text, so a caller
  can change the query's structure.
Flow: request.args["q"] -> query string built by concatenation -> cursor.execute()
Preconditions: Any unauthenticated caller can reach /search.
Evidence: The diff adds the concatenation; the old code passed q as a
  bound parameter.
Confidence: high
```

Rules for findings:

- **The flow names real code.** File, function, and the path the data takes. If you cannot trace it end to end inside the diff and the code it touches, the finding is not ready; either trace it or drop it to a note.
- **Preconditions are part of the finding.** Who can reach the input, authenticated or not, and what they control. A defect only an admin can trigger, on an admin-only surface, is a different finding from the same defect on a public route.
- **Evidence cites the diff.** Say what the change introduced or removed. Pre-existing defects outside the diff are out of scope unless the diff makes them reachable; note those in one line at the end, separately.
- **Confidence is honest.** High means you traced the flow and saw no guard. Medium means a guard might exist outside the code you read. Low means pattern match only. Low-confidence findings go in a separate "worth a look" list, never in the findings list.

## Step 5: Close out

End the audit with:

1. The findings list (step 4 format), highest impact first.
2. The "worth a look" list, clearly marked as untraced.
3. One line naming what you did not cover: files you could not read, classes you skipped and why, tests you could not run.
4. A hand-off line: "Ready for the adversarial-disproof pass" with the finding IDs.

Then stop. Do not soften findings, do not add fixes beyond a one-line direction per finding, and do not report to the user yet if the disproof pass is part of the workflow. The disproof pass exists because this pass, like every first pass, will contain at least one finding that does not survive scrutiny. Find out which one before a human reads it.
