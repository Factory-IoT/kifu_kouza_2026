"""Crop lecture images from the first-half PowerPoint deck (Windows + PowerPoint required).

Usage: python system/tools/extract-pptx-assets.py "<path to pptx>"
Slides are exported to PNG by PowerPoint, then body regions are cropped (fractions of the slide)
into system/web/public/assets/pptx-*.png and recorded in assets-manifest.json.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / 'system/web/public'
SOURCE_NOTE = 'みのる化成 技術開発部の講義用スライド（前半）から切り出した画像'

# output name: (slide number, (left, top, right, bottom) as fractions of the slide)
CROPS = {
    'pptx-group.png': (3, (0.0, 0.09, 0.985, 0.955)),
    'pptx-map.png': (4, (0.455, 0.50, 0.975, 0.945)),
    'pptx-auto-parts.png': (5, (0.0, 0.09, 0.985, 0.955)),
    'pptx-blow-products.png': (6, (0.0, 0.09, 0.985, 0.955)),
    'pptx-naphtha.png': (8, (0.0, 0.14, 0.56, 0.93)),
    'pptx-brush.png': (18, (0.06, 0.355, 0.94, 0.56)),
}


def export_slides(pptx: Path, out_dir: Path) -> None:
    script = (
        "$ppt = New-Object -ComObject PowerPoint.Application;"
        "try { $p = $ppt.Presentations.Open('%s', $true, $false, $false);"
        "$p.Export('%s', 'PNG', 2400, 1800); $p.Close() } finally { $ppt.Quit() }"
    ) % (str(pptx).replace("'", "''"), str(out_dir).replace("'", "''"))
    subprocess.run(['powershell', '-NoProfile', '-Command', script], check=True)


def erase_header_rule(image: Image.Image) -> None:
    # The green header rule at the top of each slide cuts through pictures that overlap it; paint it out.
    w, h = image.size
    pixels = image.load()
    for y in range(round(h * 0.105), round(h * 0.128)):
        for x in range(w):
            r, g, b = pixels[x, y]
            if g > r + 30 and g > b + 30 and g > 120:
                pixels[x, y] = (255, 255, 255)


def main() -> None:
    pptx = Path(sys.argv[1])
    if not pptx.is_file():
        raise SystemExit('pptx not found: ' + str(pptx))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        export_slides(pptx, tmp_dir)
        manifest_path = PUBLIC / 'assets-manifest.json'
        manifest = [m for m in json.loads(manifest_path.read_text(encoding='utf-8'))
                    if not m['file'].startswith('assets/pptx-')]
        for name, (number, box) in CROPS.items():
            candidates = list(tmp_dir.glob('*%d.PNG' % number)) + list(tmp_dir.glob('*%d.png' % number))
            source = next(c for c in candidates if c.stem.lstrip('スライドSlide') == str(number))
            image = Image.open(source).convert('RGB')
            w, h = image.size
            erase_header_rule(image)
            crop = image.crop((round(box[0] * w), round(box[1] * h), round(box[2] * w), round(box[3] * h)))
            if crop.width > 1600:
                crop = crop.resize((1600, round(crop.height * 1600 / crop.width)), Image.LANCZOS)
            crop.save(PUBLIC / 'assets' / name, optimize=True)
            manifest.append({
                'file': 'assets/' + name,
                'source_repository_path': 'スライド%d（%s）' % (number, pptx.name),
                'source_site': 'https://www.minorukasei.co.jp/',
                'source_note': SOURCE_NOTE,
                'permission': '2026-10-13 ユーザーが本講義用に前半スライドの内容の利用を指示',
                'copied_on': '2026-10-13',
            })
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Cropped %d images.' % len(CROPS))


if __name__ == '__main__':
    main()
