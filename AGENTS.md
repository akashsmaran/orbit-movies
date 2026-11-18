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
- Use natural transparent edges. Do not add black/white outlines or artificial cutout shadows.
- Add faint, aligned context from the SAME original scene plus a soft angled background light. Keep the text panel, top controls and footer dark. The approved defaults are context 32%, light 14%, angle 64°.
- Native foreground masks, manual masks, cropping, resampling, and blur are permitted. Do not synthesize faces, bodies, or missing scene content.
- Do not claim that repository edits have synced to the projector until that behavior is verified.

- Preserve the rotating wheel and visible Spin button. Up navigates to the top buttons and must not immediately spin. Do not replace the wheel with a static gallery or thumbnail strip without explicit design approval.
- Keep the background dark. Use small previous/next arrow labels; no large stationary side images.
- `description` and `details` hold factual film text. Verify names and facts from title pages; keep the synopsis short.

- Center the selected cutout horizontally and anchor its bottom above the footer controls. Keep rotation and explicit Spin-button activation intact.

- Top-row controls: Up focuses Spin; Left/Right selects Spin or Refresh; OK activates; Down returns to the wheel. Down from the wheel opens tabs.

## Muse: adding or updating a title

1. Verify the requested title, provider link and factual metadata. Add or update its stable entry in `movies.json`; preserve other entries and ordering.
2. Find a good real scene with a useful room/environment and the requested people. Record the exact source page and image URLs in `artwork/SOURCES.md`. Never use generated images. Keep source images and same-size grayscale foreground masks under `sources/<id>/scene.jpg` and `mask.png` (white selects the people, black the background). Use a foreground segmentation tool or carefully prepared manual mask. Inspect hair, hands, furniture edges and faces; do not substitute a rectangular crop if a usable mask is unavailable.
3. Add a recipe to `sources/recipes.json`, following the existing entries. Defaults are approved; adjust the light angle to fit the actual source direction when needed. Do not change the wheel, UI or layout.
4. With Python 3.9+ and Pillow installed, run `python3 scripts/prepare_all.py`. This deterministically builds paired natural-edge cutouts and aligned dark scene/light plates, updates `artwork` and `background`, and validates the catalog. Content-derived filenames prevent stale projector caches. Re-running unchanged recipes produces the same paths.
5. Inspect the pair together on a 1920×1080 dark canvas: background fills the screen; cutout fits inside 800×650, centered at x=960, bottom y=935. No outlines, duplicated people, stretched poses or hard rectangular scene edges. Ensure text at x=110..520 remains dark and readable. Cutout lighting itself stays faithful to the source; the beam is behind it.
6. Run `python3 scripts/validate_catalog.py`; commit sources, recipe, generated assets, provenance and catalog together; push to `main`. No APK rebuild is needed for catalog entries.
7. Tell the user to press Refresh from GitHub or restart Orbit. Do not claim live deployment without checking the projector. Do not add polling or agent/API calls on the projector.

The preparation code runs on the agent's computer, not on the projector. Mask creation and source selection still require visual judgment; the composition, naming and catalog updates are automated.
