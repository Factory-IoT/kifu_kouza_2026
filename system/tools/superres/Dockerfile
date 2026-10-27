# CPU-only Real-ESRGAN (x4plus) for upscaling lecture photos. Build and usage: see README.md.
FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# torch/torchvision come from the CPU-only index (no dependencies); everything else from PyPI.
RUN pip install --no-cache-dir filelock typing-extensions sympy networkx jinja2 requests pillow "numpy<2" \
    && pip install --no-cache-dir --no-deps torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir "numpy<2" opencv-python-headless==4.8.1.78 basicsr==1.4.2 realesrgan==0.3.0

# Official weights from the Real-ESRGAN v0.1.0 release (BSD-3-Clause), about 67 MB.
RUN mkdir -p /models \
    && curl -fL -o /models/RealESRGAN_x4plus.pth \
       https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth

COPY upscale.py /app/upscale.py
WORKDIR /work
ENTRYPOINT ["python", "/app/upscale.py"]
