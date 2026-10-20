# choice-aid-skills

choice aid の業務で使う Claude 用スキル集です（プラグインのマーケットプレイス形式）。

## 入っているもの

| プラグイン | できること |
|---|---|
| `choice-aid-interview-fb` | 面接・CA面談の資料（Gemini議事録・逐語録、Indeedレジュメ、手打ちメモ）から、統一評価（8項目100点）の採点、面接官へのFB、求職者プロファイルを作り、全CA共通の「中途人材紹介_AI面談FB」シートへ追記する |
| `choice-aid-application-documents` | 同じ資料と求職者管理表から、会社指定の書式で履歴書（Googleスプレッドシート）と職務経歴書（Googleドキュメント）の確認用ドラフトを作る |

## 入れ方（1回だけ）

Claude（ブラウザ・デスクトップアプリ）で:

1. 設定 → カスタマイズ → **プラグイン** → **＋追加** → **マーケットプレイスを追加** → **リポジトリから追加**
2. URL欄にこのリポジトリの `owner/repo` を入れて追加する
3. 一覧に出たプラグイン（`choice-aid-interview-fb`、`choice-aid-application-documents`）をそれぞれ「追加」する
4. 「自動で同期」をオンにしておくと、更新が自動で届く

Claude Code では `/plugin marketplace add <owner/repo>` → `/plugin install choice-aid-interview-fb@choice-aid-skills`。

使うには、Claude の設定 → 機能 →「クラウドでのコード実行とファイル作成」がオンであること、Google Drive・Google Sheets のコネクタがつながっていること、対象シートへの編集権限があることが必要です。

## 注意

- このリポジトリは公開されています。求職者の資料・実名・連絡先・社内の未公開情報は入れないでください。
- スキルは求職者の情報をシートから読み書きしますが、その情報自体はこのリポジトリには入りません。
- スキルの中のシートIDは、社内に共有を限ったシートのものです。IDを知っていても、共有されていない人は開けません。

## 更新する人へ

- スキルの正本はこのリポジトリの外にあり、ビルドでここへ反映します。ここを直接書き換えないでください。
- 反映のたびに `plugins/*/.claude-plugin/plugin.json` の `version` が上がります。version が変わらないと利用者に更新が届きません。
- 利用者への更新は、main への push をきっかけに Claude GitHub App 経由で同期されます（組織 Choice-System でこのリポジトリへのアクセスを許可済み）。
- コミット・プッシュの前に公開前チェック（`scripts/check_public.py`）が自動で動きます。初回だけ次を設定してください:
  - `git config core.hooksPath .githooks`
  - `git config choiceaid.denylist <禁止語の一覧ファイルの場所>`（一覧は手元にだけ置き、このリポジトリには入れない）
