"""Upscale images with Real-ESRGAN (CPU). Usage: upscale.py <input_dir> <output_dir> [outscale=2]"""
import sys
from pathlib import Path

import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
outscale = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
dst.mkdir(parents=True, exist_ok=True)

model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
upsampler = RealESRGANer(scale=4, model_path='/models/RealESRGAN_x4plus.pth', model=model,
                         tile=256, tile_pad=10, pre_pad=0, half=False)

for path in sorted(p for p in src.iterdir() if p.suffix.lower() in ('.jpg', '.jpeg', '.png')):
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        print('skip', path.name)
        continue
    output, _ = upsampler.enhance(image, outscale=outscale)
    target = dst / path.name
    if target.suffix.lower() == '.png':
        cv2.imwrite(str(target), output)
    else:
        cv2.imwrite(str(target), output, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(path.name, image.shape[1], 'x', image.shape[0], '->', output.shape[1], 'x', output.shape[0])
