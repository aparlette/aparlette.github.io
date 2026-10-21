---
title: "Grid"
description: "Makes personal AI agents on different machines behave like one team."
weight: 2
---

## What it does

Run AI agents on more than one computer, in more than one framework, and you
lose the ability to answer two basic questions: what is running, and what is
waiting on me?

Grid is the coordination layer that puts those answers in one place. One
roster, one control plane, one dashboard. It dispatches work between agents,
bridges frameworks that do not otherwise talk to each other, carries messages
out to channels like Telegram, and keeps durable state underneath so the
picture survives a restart.

## Where it stands

The federation backbone is built and tested — the control plane, dispatch,
adapters, the durable substrate, enrollment, replication, and the dashboard.
It is versioned **v0.1.0** and runs in real daily use.

Some pieces are deliberately still stubs, including semantic memory and
autonomous wake-up push, and a handful of integration points are waiting on
production validation. It is honest working software at an early version
number, not a finished product.

## How it is built

Node and TypeScript. Configuration in TOML, validated with Zod. Networking
over Tailscale. SQLite with Litestream underneath, agent-to-agent dispatch and
an MCP bridge on top, server-sent events to the dashboard, and systemd to keep
it alive. MIT licensed.
