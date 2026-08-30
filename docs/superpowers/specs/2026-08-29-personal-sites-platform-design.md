# Personal sites platform — design

**Date:** 2026-08-29
**Status:** built on branch `multi-site` 2026-08-29; DNS cutover outstanding
**Scope:** the `parlette.net` family of personal sites, their shared build system, and
Cloudflare Workers hosting.

## Problem

Andrew maintains (or plans) a set of personal sites plus several software products and
two sites run for other people. Today `andrew.parlette.net` is a single Hugo + Blowfish
repo deployed to GitHub Pages; the other personal sites do not exist yet. The goal
recorded on 2026-08-28 is *one cheap, simple, flexible hosting and build system* for the
personal sites, without each new site meaning a new toolchain, a new theme fork, and a
new deploy story.

## Decisions

### 1. One monorepo, several Hugo sites

All personal sites live in this repository under `sites/<name>/`. Each is a complete,
independently buildable Hugo site with its own `config/`, `content/`, and `go.mod`.

The alternative — a repo per site — was rejected because the shared layer (brand, cross-
site nav, deploy config, CI) would have to be published and version-bumped to be
consumed, which is heavy friction for three small sites maintained by one person.

### 2. Shared code is a local Hugo module

`shared/` is a Hugo module holding what every site needs: brand CSS tokens, the
cross-site network footer, and shared partial overrides. Each site imports it:

```toml
# sites/<name>/config/_default/module.toml
[[imports]]
  path = "github.com/nunocoracao/blowfish/v2"
[[imports]]
  path = "github.com/aparlette/parlette-sites/shared"
```

and resolves it locally with a `replace` directive in that site's `go.mod`:

```
replace github.com/aparlette/parlette-sites/shared => ../../shared
```

Hugo's layering means precedence runs **site > shared > Blowfish**, so any site can
override anything without forking the theme. This was verified working before adoption.

Note: Hugo's own `module.replacements` setting resolves relative paths inconsistently
here (it drops a path segment); the Go `replace` directive is the mechanism that works.
Do not add a `replacements` line to `module.toml`.

### 3. Hugo + Blowfish everywhere

One SSG, one theme, one set of conventions. Blowfish already carries search, dark mode,
galleries, TOC, and breadcrumbs, which is more than a hand-rolled theme would give for
the effort. Hugo requires the Go toolchain because the theme is a module — this is a
real dependency and is documented in the README.

Zola was considered (Andrew already runs `interstatetracker.com` on it, and it needs no
Go). It was rejected for the personal sites because it would mean rebuilding Blowfish's
feature set by hand and rewriting the existing `andrew.parlette.net` content's shortcodes
for no user-visible gain.

### 4. Cloudflare Workers static assets, one Worker per site

Each site deploys as an **assets-only Worker** — a `wrangler.jsonc` with an `assets`
block and no script. This is Cloudflare's current static-hosting path (it supersedes
Pages for new projects), keeps every site on one account and one CLI, and costs nothing
at this traffic.

### 5. Mirror and legacy hostnames are redirects, not sites

A single `workers/redirects` Worker owns every hostname that should not serve its own
content, and 301s it to the canonical URL, preserving path and query:

| Hostname | Redirects to |
|---|---|
| `parlette.net` (apex) | `https://www.parlette.net/` |
| `andrewparlette.com`, `www.andrewparlette.com` | `https://andrew.parlette.net/` |
| `parlettestudios.com`, `www.parlettestudios.com` | `https://studio.parlette.net/` |
| `baseball.parlette.net` | `https://andrew.parlette.net/baseball/` |

`baseball.parlette.net` is deliberately a redirect rather than a fourth site. The
baseball content is the bulk of `andrew.parlette.net` and splitting it would fragment
the site's best material to serve a hostname nobody has asked for yet. The redirect
reserves the name; promoting it to a real site later is a `sites/baseball/` directory
and one line removed from the redirect map.

### 6. What is out of scope

These keep their own stacks and repos, and are only *linked to* from the personal sites:

- **Interstate Tracker** — Zola site + Svelte web app + API on a VPS (`/projects/local/interstate`)
- **NogLog** — Next.js monorepo + Capacitor mobile app (`/projects/local/NogLog`)
- **Elkridge 13U / Elkridge Berry** — Next.js + Supabase + Resend on Vercel, run for
  other people, needs a server runtime (`/projects/local/elkridge-baseball`)

A static Hugo site cannot host the signup forms, auth, and APIs these need. Folding them
in would mean giving every personal site a server runtime to serve three of them.

## The sites

### `andrew.parlette.net` — personal

The existing site, moved to `sites/andrew/` with history preserved. Baseball coaching
(philosophy, record, player profiles, resources), blog, apps, photo gallery, about,
contact. This is the site with real ported WordPress content.

### `www.parlette.net` — family / landing

A deliberately small hub: who Andrew is in one paragraph, and signposts to the other
sites in the family. **It does not invent family biography.** Content beyond the hub
(family news, kids, photos) needs input from Andrew and is marked TODO rather than
written speculatively.

### `studio.parlette.net` — Parlette Studios

The software-and-photography brand. A project index with a page per public project,
written from each repo's own README so nothing is overstated, plus a photography
section. New software projects start here as a sub-page and graduate to their own
domain when they earn one (as Interstate Tracker did).

Project pages state status honestly — "in development" is not "available".

## Build and deploy

```
scripts/dev.sh <site>      # hugo server for one site
scripts/build.sh [site]    # build one site, or all of them
scripts/deploy.sh <site>   # wrangler deploy (build first)
```

CI is one GitHub Actions workflow with a matrix over the sites. A path filter means a
change under `sites/studio/` deploys only studio; a change under `shared/` deploys all
of them.

Deploy needs a `CLOUDFLARE_API_TOKEN` repository secret. The old GitHub Pages workflow
is removed in the same change — two deploy paths to two hosts is how a site ends up
stale on one of them.

## Repository layout

```
shared/                     shared Hugo module (brand, cross-site nav)
sites/
  andrew/                   andrew.parlette.net
  www/                      www.parlette.net
  studio/                   studio.parlette.net
workers/
  redirects/                mirror + legacy hostname redirects
scripts/                    dev / build / deploy helpers
docs/superpowers/specs/     this document
.github/workflows/deploy.yml
```

## Risks and open questions

- **DNS is not done here.** Every hostname above needs a Cloudflare DNS record and a
  Workers custom-domain binding. The code is ready; the cutover is a manual step.
- **`andrewparlette.com` and `parlettestudios.com` may not be registered yet.** The
  redirect map is harmless if they aren't — the routes simply never fire.
- **Family site content** is blocked on Andrew, by design.
- **Go is a hard build dependency.** It was missing from this machine and was installed
  to `~/.local/go` during this work.
