# andrew.parlette.net

Personal site. [Hugo](https://gohugo.io) + the
[Blowfish](https://blowfish.page) theme, built and deployed to GitHub Pages by
[`.github/workflows/hugo.yaml`](.github/workflows/hugo.yaml) on every push to
`main`.

## Local development

Requires Hugo **extended** and Go (Go is needed because the theme is a Hugo
Module, not a submodule).

```bash
hugo server        # http://localhost:1313
hugo --gc --minify # production build into ./public
```

## Layout

```
config/_default/    site + theme configuration
  hugo.toml           core Hugo settings
  languages.en.toml   site title, description, author profile block
  menus.en.toml       nav bar
  params.toml         theme options (colorScheme, homepage layout, ...)
  module.toml         theme import
content/            all pages; directory structure == URL structure
assets/img/         images referenced from config (avatar, etc.)
```

## Updating the theme

```bash
hugo mod get -u github.com/nunocoracao/blowfish
```

## Status

Content is currently **placeholder**. Pages and URL paths mirror the existing
WordPress site at `andrew.parlette.net` so that links survive the eventual
cutover, but the prose still needs to be written or ported.

Not yet done:

- Real copy on every page, plus a real avatar image (`assets/img/avatar.svg` is
  a generated monogram placeholder)
- Contact form — a static site has no server, so `/contact/` currently uses a
  plain email link. A third-party endpoint (Formspree, Basin) is the
  alternative.
- Photo gallery images
- Custom domain: no `CNAME` file yet, so the site builds to
  `https://aparlette.github.io/`. Pointing `andrew.parlette.net` here needs a
  DNS `CNAME` record plus the domain set in the repo's Pages settings.
