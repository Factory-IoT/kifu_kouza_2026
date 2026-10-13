# プロジェクトルール継承

`projects_management` を親ルール管理リポジトリとして参照し、そのルールを前提に運用する。

## 親ルール参照先

- 親リポジトリ: `projects_management`
- 親仕様: `doc/specifications/repository-specification.md`
- 親ルール:
  - `rules/deploy-standard.md`
  - `rules/web-portal-standard.md`
  - `rules/project-registry-standard.md`
  - `rules/rule-inheritance-standard.md`

## 継承確認記録

| 項目 | 内容 |
|------|------|
| 初回継承日 | 2026-10-13 |
| 最終確認日 | 2026-10-13 |
| 確認者 | 山下 |
| 例外の有無 | なし |

## 親ルールとの対応

- デプロイ標準: DB-S01 へ rsync で転送する（`doc/operations/lecture-web.md`）。サーバー上では git を使わず、`docker compose down -v` は実行しない。
- 外部プロジェクト登録標準: `project_key` は `kifu-kouza-2026`。入口情報は `system/web/public/metadata.json`。サービスは `kifu-kouza-2026`（webui）と `kifu-kouza-2026-mgmt`（management）の2系統でレジストリに登録し、登録内容は `system/tools/register-service.py` で更新する。
- Web ポータル標準: ポート 3110 は `rules/web-portal-standard.md` の割当表に登録済み。

## このプロジェクトの追加ルール

`rules/README.md` を参照。

## 例外事項

- なし