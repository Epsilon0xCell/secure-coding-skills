# Pass 2: disproof attempt

```
F1 (authorization, invoices.py)
Verdict: CONFIRMED, and restated more precisely than the audit put it.
Closest attack: Attack 1 (find the guard), aimed at the gap the audit
  itself flagged. db.get_invoice() runs
  "SELECT * FROM invoices WHERE id = ?" with no owner column in the
  WHERE clause, and send_file() is called on the row it returns. The
  check does not live in the data layer either. Attack 3 fails to shrink
  the preconditions: accounts are self-serve, so "any logged-in user"
  means anyone who signs up, and sequential IDs make every invoice in
  the system reachable one integer at a time.
Restated claim: An unauthenticated visitor gets nothing (the 401 is
  real). An authenticated user gets every customer's invoices, which
  carry names, addresses, and amounts. That is the finding at its true
  size: cross-customer data exposure, gated only by a free account.
Fix direction: Scope the fetch by owner, as list_invoices() already
  does: fetch the invoice where id = ? AND owner_id = current user, and
  let the 404 stand for both missing and not-yours, so the response does
  not confirm which IDs exist.
```

The medium confidence was the honest part of the first pass: it named the one place a guard could be hiding. The second pass went and looked, and the finding came out the other side both stronger and more precisely stated.
