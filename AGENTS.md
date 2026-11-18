# Maintaining the Orbit movie catalog

This repository contains catalog data and artwork, not the Android app source.

- Edit `movies.json` using `movies.schema.json` as the contract.
- Keep `schemaVersion` at 1 and preserve existing stable movie IDs.
- Add only movies the user requests; do not invent favorites or streaming availability.
- Store transparent PNG/WebP cutouts in `artwork/` and use relative artwork paths.
- Commit new artwork and its catalog entry together.
- Preserve movie array order unless the user requests reordering.
- Use the installed Android TV app package for each provider; verify it if unknown.
- Include title-specific links only when verified. Omit `url` for an app-only fallback.
- Do not store credentials, access tokens, signed private URLs, APKs, or personal account data.
- Run `python3 scripts/validate_catalog.py` before committing.
- Keep each image under 4 MiB. Use a new artwork filename whenever replacing an image; existing image paths are cached indefinitely.
- The repo is public. Never add private information.
- Projector sync runs only when Orbit starts. Returning from another app or switching tabs does not sync. Restart Orbit after catalog updates.
- Artwork style: tall realistic painted people on a true transparent background, full figures extending from the bottom toward the top. Avoid rectangular posters, text, frames, and clay/toy styling.
- Do not claim that repository edits have synced to the projector until that behavior is verified.
