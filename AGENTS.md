# AGENTS

このリポジトリで作業する AI エージェントは、作業開始前に必ず
`projects_management` の親仕様と親ルールを確認すること。

確認順序:

1. `projects_management` の管理サイトを開き、「継承ガイド」を確認する
2. `projects_management/rules/rule-inheritance-standard.md` を読む
3. `projects_management/rules/project-registry-standard.md` を読む
4. このリポジトリ固有の `rules/` と `doc/specifications/project-rule-inheritance.md` を読む

管理サイトが見られない場合のみ、下記のリポジトリ文書を正本として読むこと。

親仕様:

- `projects_management/doc/specifications/repository-specification.md`

親ルール:

- `projects_management/rules/deploy-standard.md`
- `projects_management/rules/web-portal-standard.md`
- `projects_management/rules/project-registry-standard.md`
- `projects_management/rules/rule-inheritance-standard.md`

作業時の原則:

- このリポジトリでは、親ルールを前提とした追加ルールだけを `rules/` に置く
- 親ルール本文をこのリポジトリへコピーして改変しない
- 親ルールと矛盾する独自ルールを定義しない
- このリポジトリ固有の例外や追加制約は `doc/specifications/project-rule-inheritance.md` と `rules/` に記録する

## タスク管理

このリポジトリは `TASKS.md` をリポジトリルートに置き、自身のタスクを管理する。

- 記法・運用は `projects_management/doc/specifications/task-file-standard.md` に準拠する (スキーマ: `htm-tasks-v1`)
- ひな型: `projects_management/doc/specifications/tasks-template.md`
- 上位ポータル (http://192.168.1.64:3030) が自動収集する

AI エージェントは作業中、以下を厳守すること。

- 新規タスクを発見・想起したら `TASKS.md` の `## 進行中` セクションに追記する
- 作業着手時に該当タスクを `[ ]` → `[/]` (in_progress) に変更する
- 完了時に `[x]` (done) に変更する。任意で `## 完了` セクションへ移動
- ブロック発生時は `[!]` (blocked) にし、サブバレットで理由を書く
- 取り下げ時は `[-]` (dropped)、本文は `~~取り消し線~~` で残す
- `TASKS.md` を変更したら frontmatter の `updated_at` を当日に更新する
- これらの更新は可能な限りコミット単位で行う
