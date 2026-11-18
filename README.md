# Orbit Movies

A movie favorites catalog for the Orbit launcher on an Android TV projector.
Muse or another agent maintains this repository; the planned launcher integration
will read `movies.json` and display movie cutouts in the Orbit wheel.

**Status:** catalog repository initialized. Automatic projector syncing is not
implemented yet. The catalog starts empty; add real favorites and artwork.

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

## Planned projector sync

The launcher will poll the configured branch over HTTPS, use conditional
requests, and keep a validated local catalog plus cached artwork for offline
use. GitHub updates will become visible after a successful refresh, not through
an immediate push notification.

This repository is private. Device authentication still needs to be implemented;
never place a GitHub token in this repository, image URLs, or a compiled APK.

## Files

- `movies.json`: favorites list.
- `movies.schema.json`: version 1 catalog contract.
- `artwork/`: movie cutouts.
- `AGENTS.md`: editing instructions for Muse and other agents.
