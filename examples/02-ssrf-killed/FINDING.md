# Pass 1: finding

```
ID: F1
Class: SSRF
Location: preview.js, the /api/preview route added by this change
Claim: The url field of the request body is passed straight to fetch(),
  so any caller can make the server request internal addresses,
  including cloud metadata endpoints.
Flow: req.body.url -> fetch() -> response body returned to the caller
Preconditions: Any caller who can reach /api/preview.
Evidence: The new route performs no validation of the URL at all; the
  handler trusts the body completely.
Confidence: high
```

Note what the first pass read: the diff, and the new file. Note what it did not read: the middleware registered for the route in the application setup, in a file the change did not touch.
