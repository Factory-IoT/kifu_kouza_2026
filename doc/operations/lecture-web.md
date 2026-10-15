# 寄付講座スライドWebアプリ

公開先: http://192.168.1.64:3110/

管理ページ: http://192.168.1.64:3110/admin.html
全ページのセリフをUTF-8テキストでダウンロード可能。セリフのみと進行メモ付きの2種類。
台本の正本はスライドと共通の`slides.js`で、変更後は`node system/tools/export-script.cjs`を実行してダウンロードファイルを再生成し、公開先へ転送する。

## 講義

2026年11月16日 16:00〜17:30。全69ページ、90分の目安。
導入・前半45分（坪井）、後半40分（山下）、締め・質疑5分（坪井）。

スライドを開き「講師ウィンドウを開く」を押す。投影用ウィンドウはプロジェクターへ、
セリフを表示する講師ウィンドウは手元の画面へ移動する。
同じブラウザ・同じサイト内の2ウィンドウで同期する。

- 戻る・送るボタン、左右キーでページ送り（スライド画面はホイールも可。講師画面のホイールはセリフのスクロール専用）
- 投影画面のFで全画面、Escで操作バー復帰
- 講師画面はセリフ・進行メモ・現在/次ページ・時間・ページ選択を表示
- セリフはホイールでスクロール、文字サイズは＋/−
- 経過タイマーは講師画面から開始・一時停止・リセットできる
- URLの`#ページ番号`で再開。自動送りはしない
- スクリプトは下書き。目安時間には写真説明・問いかけ・講師の実例紹介を含む

## 正本・出典

- 講義骨子: `lectures/10_minoru_kasei/resume.md`
- スライド・セリフ・時間: `system/web/public/slides.js`
- 画像出典: `system/web/public/assets-manifest.json`
- 素材準備: `python system/tools/prepare-assets.py`
- UI保存画像はリアルタイムデータではない。基板の設計画像は実物写真と区別
- 公式サイト: みのる化成、みのる産業、みのるグループ（2026-10-12確認）
- 画像利用: 2026-10-12にユーザーが本講義への利用を許可

## 配備

DB-S01、ユーザー`minoru`、専用ポート3110、コンテナ`kifu-kouza-2026-web`。
既存サービスとは独立。公開ディレクトリのみ読み取り専用でマウントする。
親ルールは`projects_management/rules/deploy-standard.md`を参照。
サーバーでGit操作はせず、開発PCから転送する。rsyncが使えない場合のみscpで代替する。

```powershell
# 親ルール（deploy-standard.md）に従い rsync（cwRsync）で転送する。--chmod は必須（Windowsから転送すると権限がなくなり、nginxが403を返す）
foreach ($sub in 'web','infra') {
  & "C:\cwrsync\bin\rsync.exe" -av --chmod=D755,F644 --exclude=".git/" --exclude="node_modules/" `
    -e "C:\cwrsync\bin\ssh.exe -i C:\Users\yamashita_y00031\.ssh\id_ed25519 -o StrictHostKeyChecking=no -o UserKnownHostsFile=C:\cwrsync\etc\known_hosts" `
    "/cygdrive/d/github/Factory-IoT/kifu_kouza_2026/system/$sub/" `
    "minoru@192.168.1.64:~/kifu_kouza_2026/system/$sub/"
}
ssh minoru@192.168.1.64 "cd /home/minoru/kifu_kouza_2026/system/infra && docker compose up -d"
```

公開後は `/`, `/presenter.html`, `/guide.html`, `/metadata.json` と画像の取得を確認。
サーバー側でアプリを編集せず、ローカルを変更して再転送する。

## 検証

`system/tools/verify-web.cjs`は全ページの画像読込・文字のはみ出しと、
2ウィンドウ間の双方向ページ同期、左右キー、ホイール、タイマー、境界ページを確認する。
開発環境のPlaywrightとEdgeを利用。環境によりPlaywrightの場所を変更する。

```powershell
python -m http.server 8310 --bind 127.0.0.1 --directory system/web/public
node system/tools/verify-web.cjs
```

公開環境の検証は`LECTURE_URL`に公開URLを指定して実行。
スクリーンショットはOSの一時フォルダーへ保存し、公開ディレクトリには置かない。

## レジストリ

本体と操作ガイドをpm-webサービスレジストリへ登録。ページ数など説明が変わったら、system/tools/register-service.pyをDB-S01で実行して更新する（レジストリキーはpm-webコンテナの環境変数から読み、出力しない）。
入口情報は `/metadata.json`。秘密値は公開ファイルに入れない。
