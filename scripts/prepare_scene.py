#!/usr/bin/env python3
"""Build an aligned natural cutout and dark scene/light plate. Requires Pillow.

Only source pixels are used. A same-size grayscale mask selects the people.
The background is baked once here; the projector just draws cached bitmaps.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SIZE = (960, 540)
RESAMPLE = getattr(Image, 'Resampling', Image)
TRANSFORM = getattr(Image, 'Transform', Image)

def prepare(source_path, mask_path, context=32, light=14, angle=64):
    source = Image.open(source_path).convert('RGB')
    mask = Image.open(mask_path).convert('L')
    if mask.size != source.size:
        raise ValueError('Mask and source dimensions must match')
    mask = mask.point(lambda v: 0 if v < 8 else 255 if v > 247 else v)
    bbox = mask.point(lambda v: 255 if v > 16 else 0).getbbox()
    if not bbox:
        raise ValueError('Empty subject mask')
    subject = source.convert('RGBA'); subject.putalpha(mask)
    subject = subject.crop(bbox)
    resize = min(1, 1180 / max(subject.size))
    if resize < 1:
        subject = subject.resize(tuple(round(v * resize) for v in subject.size), RESAMPLE.LANCZOS)
    cutout = Image.new('RGBA', (subject.width + 32, subject.height + 32))
    cutout.alpha_composite(subject, (16, 12))  # Natural alpha edge, no outline or shadow.
    scale = min(400 / cutout.width, 325 / cutout.height)
    x = 480 - cutout.width * scale / 2
    y = 467.5 - cutout.height * scale
    source_scale = scale * resize
    sx = x + 16 * scale - bbox[0] * source_scale
    sy = y + 12 * scale - bbox[1] * source_scale
    scene = source.transform(SIZE, TRANSFORM.AFFINE,
        (1/source_scale, 0, -sx/source_scale, 0, 1/source_scale, -sy/source_scale),
        RESAMPLE.BICUBIC).convert('RGBA')
    # Each source has different dimensions: feather its own bounds as well as
    # the screen bounds so shorter photos cannot leave a visible rectangle.
    sw, sh = source.width * source_scale, source.height * source_scale
    photo_alpha = Image.new('L', SIZE)
    photo_alpha.putdata([round(context * 2.55 * max(0,min(1,(px-sx)/36,(sx+sw-px)/36))
                             * max(0,min(1,(py-sy)/36,(sy+sh-py)/36)))
                         for py in range(540) for px in range(960)])
    scene.putalpha(photo_alpha)
    # Warm soft beam behind the unchanged foreground, angled toward its center.
    ox, oy = 480 + math.sin(math.radians(angle)) * 410, -45
    dx, dy = 480-ox, 340-oy
    length = math.hypot(dx, dy); nx, ny = -dy/length, dx/length
    cone = Image.new('L', SIZE)
    ImageDraw.Draw(cone).polygon([(ox+nx*20,oy+ny*20),(480+nx*265,500+ny*265),
                                (480-nx*265,500-ny*265),(ox-nx*20,oy-ny*20)], fill=255)
    cone = cone.filter(ImageFilter.GaussianBlur(25))
    beam_alpha = Image.new('L', SIZE)
    beam_alpha.putdata([round(cone.getpixel((px,py)) * light/100 * .8 * max(0,1-py/500))
                        for py in range(540) for px in range(960)])
    beam = Image.new('RGBA', SIZE, (238,211,156)); beam.putalpha(beam_alpha)
    scene = Image.alpha_composite(scene, beam)
    def fade(v, start, full, end_full, end):
        return max(0,min(1,(v-start)/(full-start),(end-v)/(end-end_full)))
    alpha = scene.getchannel('A')
    horizontal = [fade(px,250,335.2,853.5,960) for px in range(960)]
    vertical = [fade(py,66,119.56,412.08,478) for py in range(540)]
    alpha.putdata([round(alpha.getpixel((px,py))*horizontal[px]*vertical[py])
                   for py in range(540) for px in range(960)])
    scene.putalpha(alpha)
    background = Image.new('RGBA', SIZE, (8,11,16,255))
    background.alpha_composite(scene)
    return cutout, background.convert('RGB')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True, help='Existing movies.json entry ID')
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--mask', required=True, type=Path)
    parser.add_argument('--context', type=int, default=32, choices=range(0,56), metavar='0..55')
    parser.add_argument('--light', type=int, default=14, choices=range(0,46), metavar='0..45')
    parser.add_argument('--angle', type=int, default=64, choices=range(-65,66), metavar='-65..65')
    args = parser.parse_args()
    catalog_path = ROOT/'movies.json'
    catalog = json.loads(catalog_path.read_text())
    movie = next((m for m in catalog['movies'] if m['id'] == args.id), None)
    if movie is None:
        raise ValueError('Add the factual catalog entry first, then prepare its artwork')
    cutout, background = prepare(args.source, args.mask, args.context, args.light, args.angle)
    # Content-derived immutable names avoid old projector cache entries.
    digest = hashlib.sha256(cutout.tobytes()+background.tobytes()).hexdigest()[:12]
    for field, image, suffix in [('artwork',cutout,'cutout.png'),('background',background,'scene.jpg')]:
        relative = f'artwork/{args.id}-{digest}-{suffix}'
        destination = ROOT/relative
        destination.parent.mkdir(exist_ok=True)
        image.save(destination, **({'quality':90,'optimize':True} if field=='background' else {'optimize':True}))
        if destination.stat().st_size > 4*1024*1024:
            raise ValueError('Image exceeds 4 MiB')
        movie[field] = relative
        print(relative)
    catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False)+'\n')

if __name__ == '__main__':
    main()
