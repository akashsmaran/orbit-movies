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
- Automatic sync runs only when Orbit starts. The visible Refresh from GitHub button also syncs on explicit user action. Returning from another app, switching tabs, and browsing do not sync.
- Artwork must be cut from real movie/show scenes, using original people and poses. Do not use AI-generated or illustrated characters. Seated or cropped scenes are welcome; do not force standing bodies.
- Use a transparent PNG with a subtle sticker outline. The active design uses a plain dark background; do not add scene backdrops.
- Native foreground masks, manual masks, cropping, resampling, outlines, and blur are permitted. Do not synthesize faces, bodies, or missing scene content.
- Do not claim that repository edits have synced to the projector until that behavior is verified.

- Preserve the rotating wheel and Up-to-spin interaction. Do not replace it with a static gallery or thumbnail strip without explicit design approval.
- Keep the background dark. Use small previous/next arrow labels; no large stationary side images.
- `description` and `details` hold factual film text. Verify names and facts from title pages; keep the synopsis short.
