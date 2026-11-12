# Pass 2: disproof attempt

```
F1 (SSRF, preview.js)
Verdict: KILLED
Killed by: Attack 1 (find the guard). ssrfGuard is registered for every
  /api route and runs before this handler. It enforces an allowlist of
  two hosts over https, resolves the host and rejects private, loopback,
  and link-local answers, and the handler itself fetches with
  redirect: "manual", so an allowed host cannot bounce the request to an
  internal one either. All three controls the reference file asks for
  (allowlist, resolved-IP check, redirect handling) are present.
Recorded so it is not re-filed: The residual risk is narrower than the
  original claim and is a note, not a finding: the guard resolves DNS at
  check time and fetch() resolves again at request time, so a hostile
  authoritative server could in theory answer differently twice
  (rebinding). The two allowed hosts are first-party domains under the
  operator's control, which puts that precondition outside the stated
  threat model. If the allowlist ever opens to arbitrary hosts, this
  note becomes the first thing to re-audit.
```

The audit was right about the handler and wrong about the system. That gap, between the code in the diff and the code that actually runs, is exactly what the disproof pass is for.
