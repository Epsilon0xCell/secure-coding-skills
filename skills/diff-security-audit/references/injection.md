# Injection

Attacker text becomes part of a query, a command, a template, or an expression, and changes what it does.

## Where to look in a diff

- SQL or NoSQL queries built by string concatenation, f-strings, format calls, or query-builder fragments passed raw fragments (`.raw()`, `$where`, `sequelize.literal`, string `ORDER BY` and `LIMIT` clauses, which often cannot be bound as parameters).
- Shell commands: `os.system`, `subprocess` with `shell=True`, `exec`/`spawn` with a shell string, backticks, command strings assembled from variables.
- Template engines rendering user input as template source rather than as a variable.
- Expression languages and eval: `eval`, `exec`, `Function(...)`, dynamic imports from input, LDAP and XPath queries built by concatenation, log and header injection through unescaped newlines.

## The two questions

1. Does attacker-controlled text cross into the statement, or is it bound as a value? Bound parameters, prepared statements, and query builders used as designed are safe even when the surrounding code looks hand-built.
2. If escaping or quoting is the defense, is it the right escaping for this exact sink and encoding? Hand-rolled escaping is a finding waiting for its payload.

## False-positive traps

- The string looks concatenated but every interpolated value is an integer cast, an enum, or a server-side constant. Trace the values, not the shape.
- The command runs through an argument array (no shell), where metacharacters are inert.
- The "user input" is a fixed choice from a server-side allowlist that maps to query fragments.

## What good looks like

Bound parameters for SQL values, argument arrays for processes, identifiers chosen from allowlists, and templates that receive input as data, never as source.
