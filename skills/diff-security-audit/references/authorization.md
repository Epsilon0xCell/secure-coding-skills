# Authorization

The code checks who the caller is and then lets them touch something that is not theirs, or never checks at all.

## Where to look in a diff

- New routes, handlers, or GraphQL resolvers that fetch an object by an ID from the request and return or mutate it, with an authentication check but no ownership or tenancy check. Authentication is not authorization.
- Checks applied to the wrong object: the caller's right to the parent is verified, then a child object from the request is used unchecked.
- Ordering bugs: the action runs, then the check runs; the check runs on a stale copy; the check is skipped on an error path or an early return.
- Role and privilege fields accepted from the request body (mass assignment): `is_admin`, `role`, `tenant_id`, price, or status set directly from input.
- Background jobs, webhooks, and internal endpoints that assume the caller is trusted because the route is obscure or the network is private.
- Identifier types that invite enumeration (sequential IDs) combined with any of the above. Enumeration alone is not the finding; enumeration plus a missing check is.

## The two questions

1. For every object the handler touches, is there a check that binds this caller to this object, on the server, in the code path that actually runs?
2. If the check lives in middleware or a decorator, does it know which object to check? Middleware can verify a login and a role; it usually cannot verify ownership of the row in the handler.

## False-positive traps

- The check is in the data layer: the query itself is scoped by tenant or owner (`WHERE owner_id = current_user`), which is the strongest form of the control. Read the query before claiming the check is missing.
- The object is genuinely public, or the caller is an admin by design on an admin surface.
- The ID in the request is a lookup key the server then re-resolves against the caller's own objects (a cart, a session, an upload ticket).

## What good looks like

Server-side ownership or tenancy checks at the point of access, queries scoped to the caller by construction, and request bodies that name fields the server accepts rather than objects it binds wholesale.
