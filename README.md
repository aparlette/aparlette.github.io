# parlette.net

The personal sites, in one repository. Three Hugo sites share one brand layer
and one deploy path to Cloudflare Workers.

| Site | Directory | What it is |
|---|---|---|
| `www.parlette.net` | `sites/www` | The front door |
| `andrew.parlette.net` | `sites/andrew` | Personal — coaching, writing, photos |
| `studio.parlette.net` | `sites/studio` | Parlette Studios — software |

Mirror and legacy hostnames (`parlette.net`, `andrewparlette.com`,
`parlettestudios.com`, `baseball.parlette.net`) are handled by one Worker in
`workers/redirects`, not by sites of their own.

The design and the reasoning behind it are in
[`docs/superpowers/specs/2026-08-29-personal-sites-platform-design.md`](docs/superpowers/specs/2026-08-29-personal-sites-platform-design.md).

## Requirements

- **Hugo extended** 0.164 or newer
- **Go** — required, because the Blowfish theme is a Hugo Module. Without it
  Hugo cannot resolve modules and no site will build.
- **Node 20+** — for the redirect Worker's tests and for Wrangler

## Everyday commands

```bash
./scripts/dev.sh studio     # serve one site: andrew :1313, www :1314, studio :1315
./scripts/build.sh          # build all three into sites/*/public
./scripts/build.sh studio   # build one
npm test                    # redirect table tests
./scripts/deploy.sh studio  # build and deploy one site
./scripts/deploy.sh redirects
```

## Layout

```
shared/                  Shared Hugo module — the brand layer
  assets/css/            Parlette color scheme, brand CSS, the network strip
  static/fonts/          Self-hosted Archivo + IBM Plex (latin, ~120 KB)
  data/parlette.yaml     The list of sites in the network strip
  layouts/partials/      extend-head / extend-footer hooks into Blowfish
sites/<name>/            One complete Hugo site each
  config/_default/       Site config; params.toml sets [parlette] site = "<name>"
  content/               Pages; directory structure is URL structure
  wrangler.jsonc         Cloudflare Workers config (assets-only)
workers/redirects/       Mirror and legacy hostname redirects, with tests
scripts/                 dev / build / deploy
```

## How the shared layer works

`shared/` is a Hugo module that every site imports. Each site's `go.mod` has a
`replace` directive pointing at `../../shared`, so it resolves from disk with
no publishing step.

Precedence is **site > shared > Blowfish**. To override something for one site
only, put a file at the same path inside that site. To change it everywhere,
change `shared/`.

The brand layer plugs into Blowfish's own `extend-head.html` and
`extend-footer.html` hooks, so **no theme templates are forked** and theme
upgrades stay routine.

Two things to know when editing it:

- Do **not** add a `replacements` line to a site's `module.toml`. Hugo's own
  module-replacement setting mis-resolves relative paths here (it drops a path
  segment). The `replace` directive in `go.mod` is what works.
- Use `hugo.Data`, not `site.Data`. The latter is deprecated as of Hugo 0.156
  and builds warn on it.

### Adding a site

1. Copy `sites/www` as a starting point — it is the smallest one.
2. Set the module path in `go.mod`, the `baseURL`, and `[parlette] site` in
   `params.toml`.
3. Add it to `shared/data/parlette.yaml` so it appears in the network strip.
4. Add it to `SITES` in `scripts/lib.sh` and to the site loop in
   `.github/workflows/deploy.yml`.
5. Give it a `wrangler.jsonc` with its own worker name and custom domain.

## Deployment

Every push to `main` runs `.github/workflows/deploy.yml`, which works out what
changed and deploys only that. A change under `shared/` deploys all three
sites, because it can affect every rendered page.

CI needs one repository secret: **`CLOUDFLARE_API_TOKEN`**, with permission to
edit Workers.

### Still to do by hand

Deploying is code; DNS is not. Before the sites go live:

- Point each hostname at Cloudflare and bind it as a Workers custom domain.
- Comment out any `routes` entry in `workers/redirects/wrangler.jsonc` for a
  domain that is not registered yet — a route for a domain the account does
  not hold will fail the deploy.
- `andrew.parlette.net` currently serves from WordPress. Cutting it over is a
  DNS change; the content here already mirrors the old URL structure.
