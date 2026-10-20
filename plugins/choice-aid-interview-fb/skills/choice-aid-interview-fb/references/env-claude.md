# Claudeで使うとき（導入・接続）

毎回の手順は `SKILL.md`、シートの読み書きは `sheet-registration.md` だけを見る。このファイルは導入時と接続に困ったときに読む。

## 準備（初回だけ）
1. 会社契約のClaudeアカウントで使う。
2. スキルの登録
   - **Claude（ブラウザ・デスクトップ）・おすすめ**：設定 → カスタマイズ → プラグイン → ＋追加 → マーケットプレイスを追加 → リポジトリから追加 に、配布用GitHubリポジトリの `owner/repo` を入れ、`choice-aid-interview-fb` プラグインをインストールする。自動で同期をオンにすれば、更新も自動で届く。
   - **Claude（ZIPで入れる場合）**：カスタマイズ → Skills → ＋追加 → Skills をアップロード から `choice-aid-interview-fb_claude_vNN.zip` を登録する。Team／Enterpriseなら管理者が組織に登録できる。
   - **Claude Code**：ZIPを展開し、フォルダごと `~/.claude/skills/choice-aid-interview-fb/` に置く。`/skills` に出れば完了。
3. Googleの接続：コネクタ設定で **Google Drive** と **Google Sheets** を有効にする（Driveだけでは既存シートに書けない）。接続するGoogleアカウントに「中途人材紹介_AI面談FB」の**編集権限**と、求職者管理表の閲覧権限があることを確かめる。Claude Codeでは会社指定のGoogle Sheets用MCP（Composioなど）を接続しておく。
4. 履歴書・職務経歴書も作る人は、別スキル `choice-aid-application-documents` も登録する。

## 1人ごとの実行
1. 候補者ごとに新しい会話を開く（前の候補者の情報を混ぜない）。
2. `references/input-template.md` の依頼文を貼り、3点セットを添付する（Geminiメモ／逐語録はGoogleドキュメントのリンクでもよい）。

## 接続ごとの注意
- 「まとめ読み」は、複数の範囲を1回で読む機能（batch get。Composioなら複数範囲を指定できる取得ツール）を使う。タブ全体の取得は使わない。
- 書き込みは範囲指定のまとめ書き込み（batch update）で、入力どおり解釈する方式（USER_ENTERED）にする。
- 書き込めないときの扱いは `sheet-registration.md`「書き込めないとき」。コネクタを有効にすれば同じシートに登録できることを伝える。
