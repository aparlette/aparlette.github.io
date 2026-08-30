import { resolveRedirect } from "./redirect.js";

export default {
  /**
   * Every hostname this Worker is routed to is a mirror or a retired name, so
   * an unknown host means a route was bound without a matching table entry.
   * Say so plainly rather than redirecting somewhere arbitrary.
   */
  fetch(request) {
    const destination = resolveRedirect(request.url);

    if (!destination) {
      return new Response("No redirect is configured for this hostname.\n", {
        status: 404,
        headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }

    return new Response(null, {
      status: 301,
      headers: {
        location: destination,
        "cache-control": "public, max-age=3600",
      },
    });
  },
};
