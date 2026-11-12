# Pass 2: disproof attempt

```
F1 (SQL injection, app.py)
Verdict: CONFIRMED
Closest attack: Guard hunt (Attack 1). Small Flask apps often sanitize in
  a before_request hook or a shared helper, so I read the whole file and
  the route registration looking for one.
Why it survives: There is no hook, no helper, and no escaping anywhere on
  the path. q passes from request.args into the query string untouched.
  The counter-argument ("the database layer parameterizes") fails inside
  search_items() itself: the query is one plain string by the time
  execute() sees it, and sqlite3 cannot bind what has already been
  concatenated. Attack 3 also fails to shrink it: /search has no login
  decorator, so the precondition stands as written.
Fix direction: Pass q as a bound parameter, as get_item() already does,
  and treat the LIKE wildcards in the value as data, not pattern, if
  literal substring search is what was intended.
```

The finding that survives the second pass is worth more than the finding that entered it, because the strongest argument against it is now on the record, with the reason it fails.
