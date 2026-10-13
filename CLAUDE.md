# CLAUDE

このリポジトリの親ルール正本は `projects_management` にある。

作業開始前に必ず次を確認すること。

確認順序:

1. `projects_management` の管理サイトを開き、「継承ガイド」を確認する
2. `projects_management/rules/rule-inheritance-standard.md` を読む
3. `projects_management/rules/project-registry-standard.md` を読む
4. このリポジトリ固有の `rules/` と `doc/specifications/project-rule-inheritance.md` を読む

管理サイトが見られない場合のみ、下記のリポジトリ文書を正本として読むこと。

- `projects_management/doc/specifications/repository-specification.md`
- `projects_management/rules/deploy-standard.md`
- `projects_management/rules/web-portal-standard.md`
- `projects_management/rules/project-registry-standard.md`
- `projects_management/rules/rule-inheritance-standard.md`

AI エージェントは以下を守ること。

- まず親仕様と親ルールを読む
- このリポジトリ固有の追加ルールだけを `rules/` に置く
- 親ルールと矛盾する独自ルールを作らない
- 例外事項がある場合は `doc/specifications/project-rule-inheritance.md` に記録する

## タスク管理

このリポジトリは `TASKS.md` をリポジトリルートに置き、自身のタスクを管理する。

- 記法・運用は `projects_management/doc/specifications/task-file-standard.md` に準拠する (スキーマ: `htm-tasks-v1`)
- ひな型: `projects_management/doc/specifications/tasks-template.md`
- 上位ポータル (http://192.168.1.64:3030) が自動収集する

作業中は次を厳守:

- 新規タスクを発見・想起したら `TASKS.md` の `## 進行中` セクションに追記する
- 作業着手時に該当タスクを `[ ]` → `[/]` (in_progress) に変更する
- 完了時に `[x]` (done) に変更する。任意で `## 完了` セクションへ移動
- ブロック発生時は `[!]` (blocked) にし、サブバレットで理由を書く
- 取り下げ時は `[-]` (dropped)、本文は `~~取り消し線~~` で残す
- `TASKS.md` を変更したら frontmatter の `updated_at` を当日に更新する
- これらの更新は可能な限りコミット単位で行う
