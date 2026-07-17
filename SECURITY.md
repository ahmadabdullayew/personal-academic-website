# Security Policy

## Reporting

Report suspected vulnerabilities privately to the website owner, Ahmad
Abdullayev. Do not include credentials, private records or exploit details in a
public issue.

## Foundation security rules

1. No secret may enter Git, browser bundles, logs, generated public assets or
   examples.
2. Production credentials come from IAM task roles and managed secret storage.
3. Public output reads only approved public snapshots.
4. Uploads use separate quarantine, private and public-derivative storage
   boundaries.
5. Queue handlers are idempotent and reject obsolete revision events.
6. Applicable security, privacy, accessibility and recoverability failures block
   release.

The detailed threat model and incident-response procedure remain separate later
milestones; their absence does not weaken these foundation constraints.
