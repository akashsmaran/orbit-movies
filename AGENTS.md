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
- Before committing, parse both JSON files, check unique IDs, and verify every local artwork path exists.
- Do not claim that repository edits have synced to the projector until that behavior is verified.
