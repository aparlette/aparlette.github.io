import { test } from "node:test";
import assert from "node:assert/strict";
import { resolveRedirect, REDIRECTS } from "../src/redirect.js";

test("apex parlette.net goes to www", () => {
  assert.equal(resolveRedirect("https://parlette.net/"), "https://www.parlette.net/");
});

test("mirror domain keeps the path", () => {
  assert.equal(
    resolveRedirect("https://andrewparlette.com/baseball/coaching-record/"),
    "https://andrew.parlette.net/baseball/coaching-record/",
  );
});

test("mirror domain keeps the query string", () => {
  assert.equal(
    resolveRedirect("https://parlettestudios.com/work/?sort=recent"),
    "https://studio.parlette.net/work/?sort=recent",
  );
});

test("a prefixed host mounts the root at the prefix, without a doubled slash", () => {
  assert.equal(
    resolveRedirect("https://baseball.parlette.net/"),
    "https://andrew.parlette.net/baseball/",
  );
});

test("a prefixed host mounts deep paths under the prefix", () => {
  assert.equal(
    resolveRedirect("https://baseball.parlette.net/coaching-record/"),
    "https://andrew.parlette.net/baseball/coaching-record/",
  );
});

test("hostname matching is case-insensitive", () => {
  assert.equal(resolveRedirect("https://AndrewParlette.com/"), "https://andrew.parlette.net/");
});

test("an unrouted hostname resolves to nothing", () => {
  assert.equal(resolveRedirect("https://example.com/"), null);
});

test("every destination is a host this repo actually publishes", () => {
  const published = new Set([
    "www.parlette.net",
    "andrew.parlette.net",
    "studio.parlette.net",
  ]);
  for (const [from, entry] of Object.entries(REDIRECTS)) {
    assert.ok(published.has(entry.host), `${from} points at unpublished host ${entry.host}`);
    assert.ok(!REDIRECTS[entry.host], `${from} points at ${entry.host}, which itself redirects`);
  }
});
