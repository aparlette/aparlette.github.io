---
title: "NogLog"
description: "Logs eggnog tastings — brands, reviews, ratings, and recipes."
weight: 4
---

## What it does

NogLog is a logbook for eggnog. Browse the brands, record a tasting, write the
review, keep your favorites, and share a homemade recipe. It is a small,
cheerful, genuinely seasonal product, and it takes the logging part seriously
even though the subject is eggnog.

## Where it stands

**In development.** The web app and the Android build both exist, and recent
work has been production hardening rather than new features — rate limiting,
security headers, a CORS allowlist, refresh-token rotation, and account
lockout.

It has not launched. There is no public URL to send you to yet.

## How it is built

A monorepo: Next.js and React for the web app, Capacitor wrapping a Vite build
for Android, and a shared component package so both surfaces render the same
things. PostgreSQL with Prisma behind it, NextAuth for sign-in on the web and
tokens on mobile, Cloudflare R2 for images, and Resend for transactional email.
