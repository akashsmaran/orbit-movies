# Orbit Movies

A movie favorites catalog for the Orbit launcher on an Android TV projector.
Muse or another agent maintains this repository; the launcher integration
reads `movies.json` and display movie cutouts in the Orbit wheel.

**Status:** the Android implementation is built and tested on the projector.
The catalog starts empty; add real favorites and artwork.

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
verified title link, omit `url`; the planned fallback opens the streaming app
and does not promise to open that movie. Availability depends on region,
subscription, and installed app support. Multiple links allow provider choice.

## Projector sync

The launcher polls the configured branch over HTTPS, use conditional
requests, and keep a validated local catalog plus cached artwork for offline
use. GitHub updates will become visible after a successful refresh, not through
an immediate push notification.

This repository is public so the projector can read it without credentials.
Never place a GitHub token, account data, or private information here.

Catalog endpoint:
`https://raw.githubusercontent.com/akashsmaran/orbit-movies/main/movies.json`

The launcher checks about once per minute while active, and when entering Orbit
or returning to the launcher. GitHub caching may delay a new commit. Press the
remote’s Menu button in Orbit to request a refresh. Artwork at the same path is
rechecked after five minutes while visible; use a new filename for immediate
artwork replacement. Keep images under 4 MiB and the catalog under 1 MiB.
Invalid updates preserve the last working catalog.

## Validate before committing

Run `python3 scripts/validate_catalog.py` (Python 3.9+). This checks the catalog
contract, unique IDs, local artwork files, size limits, and link schemes.

## Projector controls

- Left/right: browse movies.
- Up: spin to choose a movie.
- OK: open the title link or choose a service.
- Down: select a launcher tab.
- Menu: refresh the movie catalog.

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
