---
title: "IsoReel"
description: "Cuts tagged clips from multi-camera game footage without re-encoding."
weight: 7
---

## What it does

Film a baseball game from two or three angles and you have hours of footage and
no way to get at the twelve seconds that matter. IsoReel is the desk tool for
that: scrub the footage frame by frame, mark in and out points, tag the clip
with the player and the play type, and cut it without re-encoding, so the
export is fast and the quality is untouched.

## Where it stands

**Early development.** What exists today is the scaffold — the application
structure, dependency injection, configuration, logging, the main window shell,
and the service interfaces. The implementations behind those interfaces are not
built yet.

There is no release and nothing to install.

## How it is built

.NET 8 and WPF for Windows, in an MVVM structure. FFmpeg does the cutting as an
external process, LibVLCSharp handles playback, Serilog handles logging. MIT
licensed.
