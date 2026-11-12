# SSRF (server-side request forgery)

Attacker text decides where the server makes a request, so the server's network position becomes the attacker's.

## Where to look in a diff

- New outbound HTTP calls whose URL, host, or path segments come from request data, stored user content, webhook configuration, or import and preview features (URL unfurlers, avatar fetchers, feed importers, PDF and screenshot services).
- Redirect handling: a client that follows redirects turns an allowed public URL into an internal one.
- URL parsers used as the defense. Parser differences between the checker and the HTTP client are a classic bypass source: credentials in the URL, unusual schemes, `@` in the authority, decimal or octal IP forms, DNS names that resolve to private addresses.
- DNS rebinding exposure: a hostname validated once and resolved again at request time can change answers in between.

## The two questions

1. Can the caller influence the destination beyond choosing among server-defined targets? Choosing a path on a fixed host is a smaller problem than choosing the host.
2. After all validation, can the request still land on a private, loopback, link-local, or cloud-metadata address (169.254.169.254 and friends), directly, by redirect, or by DNS?

## False-positive traps

- The URL is validated against an allowlist of hosts AND the resolved IP is checked AND redirects are off or revalidated. Look for all three before killing a concern; find which one is missing before raising it.
- The fetch runs in a sandbox or egress-restricted worker with no route to internal services. Deployment context decides severity; state it in the preconditions either way.
- The destination is user-configured by an administrator in a self-hosted tool, where the admin is the trust boundary. That is a design decision to note, not a vulnerability to file.

## What good looks like

Host allowlists plus resolved-IP checks against private ranges, redirects disabled or revalidated per hop, metadata endpoints blocked by default, and short timeouts with response-size limits.
