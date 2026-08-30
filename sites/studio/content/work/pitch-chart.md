---
title: "Pitch Chart"
description: "Charts every pitch, and recalls a batter's history from the dugout."
weight: 5
---

## What it does

A coach standing in the dugout wants one thing before calling the next pitch:
what has this hitter done before? That history is usually spread across
seasons, age groups, and team changes, in a stack of paper scorebooks, which
means in practice it is unavailable.

Pitch Chart records every pitch of a game and keeps a batter's history attached
to the batter rather than to the season — so a hitter who has changed teams
twice still brings his record with him. It is built offline-first, because the
places youth baseball is played reliably have no signal.

## Where it stands

**In development, and early.** The data model, the game setup flow, and live
pitch entry are in. It is not on the Play Store and there is nothing to install
yet.

## How it is built

Flutter and Dart, with drift over SQLite for local storage. Android first.
