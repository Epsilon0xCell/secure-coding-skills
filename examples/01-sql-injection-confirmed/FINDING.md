# Pass 1: finding

```
ID: F1
Class: injection (SQL)
Location: app.py, the query built in search_items()
Claim: The q request parameter reaches the SQL query as text, so a caller
  can change the query's structure.
Flow: request.args["q"] -> concatenated into the query string -> DB.execute()
Preconditions: Any unauthenticated caller can reach /search.
Evidence: The change adds the concatenation. The existing endpoint in the
  same file (get_item) passes its value as a bound parameter, so the safe
  pattern was available and not used.
Confidence: high
```
