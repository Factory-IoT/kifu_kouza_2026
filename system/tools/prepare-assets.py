"""Copy the authorized source images without changing the original repositories."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / 'system/web/public'
FACTORY = ROOT.parent
COMPANY = FACTORY / 'OTEX2026/system/company-video/assets'
COUNTER = FACTORY / 'tai_cycle_counter'
images = {
    'group-agriculture.jpg': COMPANY / 'sangyo/top_agri_machine.jpg',
    'hq.jpg': COMPANY / 'hq.jpg',
    'duct.jpg': COMPANY / 'item_duct.jpg',
    'blow.jpg': COMPANY / 'tech_blow.jpg',
    'cad.jpg': COMPANY / 'work_cad.jpg',
    'fuel-tank.jpg': COMPANY / 'item_fueltank.jpg',
    'roof.jpg': COMPANY / 'item_roof.jpg',
    'heatcool.jpg': COMPANY / 'tech_heatcool_compare.jpg',
    'inspection-work.jpg': COMPANY / 'work_inspection.jpg',
    'dessertcup.jpg': COMPANY / 'item_dessertcup.jpg',
    'people-measure.jpg': COMPANY / 'people_measure.jpg',
    'scene-car.png': COMPANY / 'scene_car.png',
    'device.jpg': COUNTER / 'img/筐体正面.jpg',
    'device-inside.jpg': COUNTER / 'img/基板取付状態.jpg',
    'monitor.png': COUNTER / 'doc/manual/device_monitor/images/01_device_monitor_page.png',
    'order.png': COUNTER / 'doc/manual/device_monitor/images/02_order_progress_page.png',
    'board.png': FACTORY / 'Musa_IoT/system/devices/molding-machine-monitor/hardware/isolated-24v-input-rev2/production/isolated-24v-input-rev2-top.png',
}
origins = {
    'group-agriculture.jpg': 'https://www.minoru-sangyo.co.jp/',
    'hq.jpg': 'https://www.minorukasei.co.jp/',
    'duct.jpg': 'https://www.minorukasei.co.jp/product/',
    'blow.jpg': 'https://www.minorukasei.co.jp/technology/technology_2.php',
    'cad.jpg': 'https://www.minorukasei.co.jp/recruit/',
    'fuel-tank.jpg': 'https://www.minorukasei.co.jp/technology/technology_2.php',
    'roof.jpg': 'https://www.minorukasei.co.jp/technology/technology_2.php',
    'heatcool.jpg': 'https://www.minorukasei.co.jp/technology/technology_4.php',
    'inspection-work.jpg': 'https://www.minorukasei.co.jp/recruit/',
    'dessertcup.jpg': 'https://www.minorukasei.co.jp/product/',
    'people-measure.jpg': 'https://www.minorukasei.co.jp/',
    'scene-car.png': 'https://www.minorukasei.co.jp/',
}
(PUBLIC / 'assets').mkdir(parents=True, exist_ok=True)
CUP = FACTORY / 'stacking-cup-inspection/system/web/src/public/ai-model-report-assets/keyence-dataset-comparison'
manifest = []
for filename, source in images.items():
    if not source.is_file():
        raise FileNotFoundError(source)
    shutil.copy2(source, PUBLIC / 'assets' / filename)
    manifest.append({
        'file': 'assets/' + filename,
        'source_repository_path': source.relative_to(FACTORY).as_posix(),
        'source_site': origins.get(filename, 'https://github.com/Factory-IoT/' + source.relative_to(FACTORY).parts[0]),
        'source_note': '公式サイト由来のリポジトリ保存素材' if filename in origins else 'リポジトリに保存された写真・設計画像・UI画像',
        'permission': '2026-10-12 ユーザーが本講義用の画像利用を許可',
        'copied_on': '2026-10-12',
    })
# Three-panel comparison (stacking-cup-inspection): captured image, commercial software AI heat map, in-house model heat map.
from PIL import Image, ImageDraw, ImageFont
cup_sources = [CUP / 'kv_125827953__input.jpg', CUP / '20261002-ai-defect-1.webp', CUP / 'kv_125827953__fcn-b__heat.jpg']
for source in cup_sources:
    if not source.is_file():
        raise FileNotFoundError(source)
shot = Image.open(cup_sources[1]).convert('RGB')
panels = [
    ('撮影した画像', Image.open(cup_sources[0]).convert('RGB').crop((270, 216, 690, 720))),
    ('市販の検査ソフトのAI', shot.crop((930, 368, 1438, 830))),
    ('自作したAIモデル', Image.open(cup_sources[2]).convert('RGB').crop((270, 216, 690, 720))),
]
height, label_h, gap = 480, 70, 30
font = ImageFont.truetype(r'C:/Windows/Fonts/YuGothB.ttc', 44)
resized = [(label, im.resize((round(im.width * height / im.height), height))) for label, im in panels]
width = sum(im.width for _, im in resized) + gap * (len(resized) - 1)
sheet = Image.new('RGB', (width, label_h + height), 'white')
draw = ImageDraw.Draw(sheet)
x = 0
for label, im in resized:
    sheet.paste(im, (x, label_h))
    draw.text((x + im.width // 2, label_h // 2), label, font=font, fill=(25, 58, 48), anchor='mm')
    x += im.width + gap
sheet.save(PUBLIC / 'assets' / 'cup-inspection.png', optimize=True)
manifest.append({
    'file': 'assets/cup-inspection.png',
    'source_repository_path': 'stacking-cup-inspection/system/web/src/public/ai-model-report-assets/keyence-dataset-comparison/ (kv_125827953__input.jpg, 20261002-ai-defect-1.webp, kv_125827953__fcn-b__heat.jpg)',
    'source_site': 'https://github.com/Factory-IoT/stacking-cup-inspection',
    'source_note': '社内開発のカップ外観検査の比較画像。撮影画像、市販検査ソフトのAI画面、自作モデルのヒートマップを並べた合成',
    'permission': '2026-10-12 ユーザーが本講義用の画像利用を許可',
    'copied_on': '2026-10-12',
})
# Keep the entries created by extract-pptx-assets.py and the super-resolution step (system/tools/superres).
previous = PUBLIC / 'assets-manifest.json'
if previous.is_file():
    manifest.extend(m for m in json.loads(previous.read_text(encoding='utf-8')) if m['file'].startswith(('assets/pptx-', 'assets/sr-')))
(PUBLIC / 'assets-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Copied {len(images)} images.')
