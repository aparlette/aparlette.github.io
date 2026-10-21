---
title: "Memory Drop"
description: "One week, 33 families, and a graduation slideshow that needed photos."
weight: 3
---

## What it does

A graduating class needed a slideshow, which meant getting full-resolution
photos out of about 33 families' phones and into one place. The families were
not going to make accounts, and the deadline was the dinner.

Memory Drop is a single page with no login. A family opens it, enters the code
they were given, picks photos, and is done in under a minute. The files go
straight from the phone to object storage without passing through an
application server, which is what makes full-resolution uploads from a
cellular connection survivable.

## Where it stands

**Shipped in April 2026**, for the event it was built for, on a hard one-week
deadline. Every requirement was met and the live deployment was verified before
the night.

It is not linked here: the live URL is a code-gated upload endpoint belonging
to one school's families, not a public demo.

## How it is built

Cloudflare Workers with Hono for the one endpoint that matters — signing
upload requests — and Cloudflare R2 for storage, with presigned requests
generated using SigV4. The front end is vanilla HTML and ES modules: no
framework and no build step, which is a large part of why it shipped in a week.
