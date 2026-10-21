---
title: "Interstate Tracker"
description: "Tracks which stretches of the Interstate Highway System you have driven."
weight: 1
---

## What it does

Interstate Tracker answers a question that is surprisingly hard to answer for
yourself: which parts of the Interstate Highway System have I actually driven?

An Android app records the drive — start and stop it by hand, or import a GPX
file afterwards — and matches the trace against real interstate geometry on the
phone. The sync API keeps what it found, and the web app renders it back as a
personal completion map of the country, rolled up per route and per state, with
achievements that unlock as coverage grows.

The phone is a client of that backend rather than a device-only app. It still
matches locally, which is what lets a finished drive summarize with no network
and no round trip, but the facts it derives are pushed to the server, and the
server decides what they add up to. Privacy is delivered through control and
data rights — a full export endpoint and an account-delete endpoint — rather
than through the app being unable to open a socket.

## Where it stands

The public site, the sync API, and the web app are **live**. Accounts,
magic-link sign-in, server-evaluated achievements, and the backup-and-restore
drill are all in place, and the whole thing has been road-tested on real
drives.

The **Android app is not publicly released**. The build on Play internal
testing is still the earlier local-only version; the sync build has not shipped
to Play, pending the Play Console data-safety paperwork.

- [interstatetracker.com](https://interstatetracker.com) — the public site
- [app.interstatetracker.com](https://app.interstatetracker.com) — the web app

## How it is built

Kotlin and Jetpack Compose on Android. Kotlin and Ktor for the sync API, over
PostgreSQL with PostGIS for the geometry. Svelte for the web app. A Python
pipeline prepares the highway network data. Zola builds the marketing site. It
all runs in Docker Compose on a single VPS.
