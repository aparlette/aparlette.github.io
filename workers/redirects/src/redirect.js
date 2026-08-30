/**
 * Hostnames that should not serve their own content.
 *
 * Each entry names the canonical host to send visitors to, and an optional
 * path prefix to mount them under. Paths and query strings are preserved, so
 * a deep link to a mirror domain lands on the matching page rather than the
 * home page.
 *
 * Adding a site later means deleting its line here — nothing else.
 */
export const REDIRECTS = {
  "parlette.net": { host: "www.parlette.net" },
  "andrewparlette.com": { host: "andrew.parlette.net" },
  "www.andrewparlette.com": { host: "andrew.parlette.net" },
  "parlettestudios.com": { host: "studio.parlette.net" },
  "www.parlettestudios.com": { host: "studio.parlette.net" },
  "baseball.parlette.net": { host: "andrew.parlette.net", prefix: "/baseball" },
};

/**
 * Resolve the destination for an incoming request URL.
 *
 * @param {string} requestUrl absolute URL of the incoming request
 * @param {Record<string, {host: string, prefix?: string}>} table
 * @returns {string|null} absolute destination URL, or null if the host is unknown
 */
export function resolveRedirect(requestUrl, table = REDIRECTS) {
  const url = new URL(requestUrl);
  const entry = table[url.hostname.toLowerCase()];
  if (!entry) return null;

  const prefix = entry.prefix ?? "";
  // "/" from the mirror means "the root of the target", which under a prefix
  // is the prefix itself — not the prefix with a bare slash glued on.
  const path = url.pathname === "/" ? `${prefix}/` : `${prefix}${url.pathname}`;

  return `https://${entry.host}${path}${url.search}`;
}
