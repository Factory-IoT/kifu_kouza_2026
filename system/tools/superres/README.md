# 画像の超解像（Real-ESRGAN、Docker・CPUのみ）

講義スライドの写真が小さいときに、2倍に拡大する。AIが細部を補うため、実物と細部が異なる場合がある。
製品や施設の写真は、可能なら元データを使い、超解像は代替として使う。

```powershell
# 初回のみ：イメージを作る（PyTorch・Real-ESRGAN・学習済みモデルを取得する）
docker build -t kifu-superres system/tools/superres

# 入力フォルダの画像を2倍にして出力フォルダへ（フォルダは絶対パスでマウントする）
docker run --rm -v "<作業フォルダ>:/work" kifu-superres /work/in /work/out 2
```

- モデル：RealESRGAN_x4plus（Real-ESRGAN v0.1.0、BSD-3-Clause）。
- 8枚（約1000px以下）で約6分（CPU）。
- 出力は `system/web/public/assets/sr-*` として使い、`assets-manifest.json` に記録する。
- Docker Desktop が「sock ... The file cannot be accessed」で起動しない場合は、`%LOCALAPPDATA%\Docker\run` と `%LOCALAPPDATA%\docker-secrets-engine` を改名してから再起動する。
