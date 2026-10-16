## What

<!-- One or two sentences on what changed, described by its effect for a user or reader. -->

## Why

<!-- The problem, decision or request behind it. Link the issue, decision record or plan item. -->

## Verification

<!-- What was run (typecheck, lint, tests, build, docs check) and what was checked by hand in the running app.
     Note anything not verified and why. List assumptions made on a delegated task. -->

## Docs

- [ ] Affected docs updated in the same commit (configuration doc and `.env.example`, architecture, decision record and index, plan status, `AGENTS.md` map, `CHANGELOG.md`), or no docs are affected because: <!-- reason -->

## Security checklist

<!-- Tick each item, or write "n/a" after it. The first pull request of a new project also copies the full
     new-project checklist: https://github.com/HafezSecure/hafez-handbook/blob/main/security/README.md -->

- [ ] No secrets, tokens, keys, IP addresses, internal hostnames, personal data or client data in the diff, the commit messages or this description
- [ ] Every new input is validated at the boundary, and every query is parameterised
- [ ] Every new route and record is authorised on the server, with a test for the denied case
- [ ] No inline script or style; the Content Security Policy is unchanged or stricter
- [ ] No new third-party origin or runtime call to an external service; fonts, scripts and media stay self-hosted
- [ ] New dependencies are needed, their licences checked, and the lockfile committed with them
- [ ] Logs and error responses expose no secrets, personal data or internals
- [ ] AI features, if touched: the model sees only what the user can see, and consequential actions need human approval
