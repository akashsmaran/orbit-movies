# Orbit Movies

A movie favorites catalog for the Orbit launcher on an Android TV projector.
Muse or another agent maintains this repository; the launcher integration
reads `movies.json` and displays movie cutouts in the Orbit wheel.

**Status:** the Android implementation is built and tested on the projector.
The first favorites are Anand (2004) on YouTube, Baththa (2026) on Netflix,
and The Big Bang Theory on Hulu. The entries now use tall, realistic painted people illustrations with transparent
backgrounds, anchored at the base of the Orbit wheel. See `artwork/SOURCES.md` for provenance.

## Add a movie

1. Put a transparent PNG or WebP in `artwork/`.
2. Add an entry to `movies.json`, following `movies.schema.json`.
3. Commit artwork and catalog together to `main`.

Entries appear in array order. Use a stable lowercase, hyphenated `id`, a title,
optional year and accent color, an artwork path relative to `movies.json`, and
one or more streaming destinations.

```json
{
  "id": "your-movie-2026",
  "title": "Your movie title",
  "year": 2026,
  "artwork": "artwork/your-movie-2026.png",
  "accent": "#C47A38",
  "links": [
    {
      "label": "Netflix",
      "packageName": "com.netflix.ninja"
    }
  ]
}
```

This is a format example, not a real movie entry. An optional `url` in a link
must be a verified title-specific HTTPS or supported app deep link. Without a
verified title link, omit `url`; the fallback opens the streaming app
and does not promise to open that movie. Availability depends on region,
subscription, and installed app support. Multiple links allow provider choice.

## Projector sync

The launcher checks GitHub **once when Orbit starts**. It loads the saved catalog
immediately, then downloads the latest catalog and any missing artwork in the
background. It does not poll, refresh on tab changes, refresh on returning from
a streaming app, or make image requests while browsing. Cached artwork is decoded
locally as needed.

To get new favorites after Muse updates the repo, restart Orbit (or the projector).
Pressing Home from a streaming app returns to the existing launcher and does not
start another sync. Missing downloads are retried at the next startup.

This repository is public so the projector can read it without credentials.
Never place a GitHub token, account data, or private information here.

Catalog endpoint:
`https://raw.githubusercontent.com/akashsmaran/orbit-movies/main/movies.json`

Each startup uses a fresh catalog URL to avoid a stale GitHub branch-file cache.
Artwork paths are immutable cache keys: **use a new filename when replacing an
image**. Existing image files are reused on later startups. Keep images under
4 MiB and the catalog under 1 MiB. Invalid catalogs preserve the last working copy.

## Validate before committing

Run `python3 scripts/validate_catalog.py` (Python 3.9+). This checks the catalog
contract, unique IDs, local artwork files, size limits, and link schemes.

## Projector controls

- Left/right: browse movies.
- Up: spin to choose a movie.
- OK: open the title link or choose a service.
- Down: select a launcher tab.
- Menu: select a launcher tab.
- Restart Orbit: check GitHub for catalog updates.

Missing streaming apps show a message. Unsupported title links fall back to
opening the streaming app, with a message to search for the movie.

## Verified installed TV packages

| Service | Android TV package |
| --- | --- |
| Netflix | `com.netflix.ninja` |
| Apple TV | `com.apple.atve.androidtv.appletv` |
| Prime Video | `com.amazon.amazonvideo.livingroom` |
| Hulu | `com.hulu.livingroomplus` |
| Sling | `com.sling` |
| YouTube | `com.google.android.youtube.tv` |

These package IDs were checked on the projector. Title links still need separate
verification; do not infer them from movie names.

## Files

- `movies.json`: favorites list.
- `movies.schema.json`: version 1 catalog contract.
- `artwork/`: movie cutouts.
- `AGENTS.md`: editing instructions for Muse and other agents.
