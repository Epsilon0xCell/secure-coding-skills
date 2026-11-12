# Secrets

Credentials end up somewhere they can be read by people or systems that should not have them. In a diff, the most common place is the diff itself.

## Where to look in a diff

- Hardcoded keys, tokens, passwords, private keys, and connection strings added in code, tests, fixtures, example configs, or comments. Test values that are real credentials are a finding; test values that are plainly fake (`sk-test-...`, `example-`) are not, and crying wolf here poisons the whole audit.
- Secrets read from config and then logged: debug logs of headers, request dumps, environment dumps, error messages and stack traces that include URLs with embedded credentials or tokens.
- Secrets sent somewhere new: a token forwarded to a third-party service, included in an outbound URL (URLs get logged by everything), or returned in an API response.
- Weakened handling: TLS verification disabled alongside a credential, a secret compared with a non-constant-time check in an auth path, a fallback default credential when configuration is missing.
- Client-side exposure: secrets compiled into shipped JavaScript, mobile bundles, or public repositories. A "public key" that can spend money or reset passwords is not public.

## The two questions

1. Is the value real, live, and committed or emitted? Reachability and liveness decide whether this is an incident or a style note.
2. Who gains read access from this change who did not have it before: log readers, CI, support tooling, end users, anyone with the repo?

## False-positive traps

- Placeholder and example values clearly marked and shaped as fake.
- Digests and public identifiers that look like secrets but are not credentials (a public key fingerprint, a key ID, a signed URL with a short expiry used as designed).
- A secret that is encrypted at rest with the key held elsewhere, in a system built for that (a vault, KMS). The finding is about exposure, not about storage existing.

## What good looks like

Secrets injected at runtime from a manager or environment, absent from the repository, redacted in logs by default, scoped to the least privilege, and rotatable without a code change. If the diff adds a real secret, the recommendation is revoke and rotate, not just delete; history keeps what the diff added.
