# Real-scene sticker sources

The active v4 artwork is made from real movie/show frames. No image generation,
face replacement, invented bodies, or generative fill was used. Original pixels
are retained through ordinary cropping/resampling and an alpha mask. A narrow
black outline and shadow provide the sticker edge. Background JPEGs are
blurred versions of the same original frames. Source imagery belongs to its
respective rights holders.

## Anand (2004, Telugu)

- Moment: Roopa and Anand seated with their coffee cups.
- Source page: https://www.bigtvlive.com/movies/anad-movie-fame-hero-raja-turns-as-poster-misses-rs-2-cr-offer.html
- Source image: https://images.bigtvlive.com/2025/06/Your-paragraph-text-47-2.jpg
- Sticker: `anand-2004-v4-sticker.png`.
- Background: `anand-2004-v3-background.jpg`.
- Watch: https://www.youtube.com/watch?v=FB504Bec9uU

## Baththa (2026)

- Moment: Vijay Sethupathi and the schoolboy seated together in the restroom.
- Source page: https://www.zoomtventertainment.com/south/vijay-sethupathi-baththa-box-office-opening-day-collection-article-156262228
- Source image: https://images.zoomnews.com/photo/msid-156262227.jpg?height=720&thumbsize=767753&width=1280
- Sticker: `baththa-2026-v4-sticker.png`.
- Background: `baththa-2026-v3-background.jpg`.
- Watch: https://www.netflix.com/title/83064751

## The Big Bang Theory

- Moment: Leonard laughing beside Sheldon on their couch.
- Source page: https://www.cheatsheet.com/news/the-big-bang-theory-the-pilot-episode-opened-much-different-conversation.html/
- Source image: https://www.cheatsheet.com/wp-content/uploads/2021/07/The-Big-Bang-Theory-3.jpg?h=800&quality=89&strip=all&w=1200
- Sticker: `the-big-bang-theory-v4-sticker.png`.
- Background: `the-big-bang-theory-v3-background.jpg`.
- Watch: https://www.hulu.com/series/9bde5aeb-5297-4290-b173-19a4d59cc11d

The previous generated v2 images have been removed from the current repository.
The v1 original title images are retained as historical source references and
are not used by the active catalog. Availability and playback still depend on
the user's streaming subscriptions and region.

Preparation uses macOS Vision foreground masks plus deterministic Pillow image
operations. These masks select pixels from the source; they do not generate new
people or scene content. The source preparation scripts are in the local Android
project's `tools/` directory.

The v4 files use the same real-source masks and RGB imagery as v3, with only
the outline changed to black. Earlier outline variants are not active.
