# Rules

親ルール（`projects_management`）に追加する、このリポジトリ独自のルール。親ルールと矛盾する内容は定義しない。

## 講義資料のルール

- 講義画面・セリフには、固有のプロジェクト名を使わない。詳細な画像出典は `system/web/public/assets-manifest.json` に保持する。
- 保存済みのUI画像・設計画像は、実物の写真やリアルタイムの稼働状況と区別して注記する。
- 実装済みの機能と、活用の可能性・考え方は区別して述べる。未確認の数値や性能は述べない。
- スライド・セリフ・時間配分の正本は `system/web/public/slides.js` とし、変更後は `node system/tools/export-script.cjs` でダウンロード用台本を再生成する。
- 講義レジュメ `lectures/10_minoru_kasei/resume.md` を変更したら、`resume.html` も再生成して揃える。
- 画像は、2026-10-12 にユーザーが本講義への利用を許可した素材に限る。出典は `assets-manifest.json` に記録する。