# choice aid 応募書類スキル 導入と担当者運用

Claude Chat、Claude Cowork、Claude Code向けの**履歴書・職務経歴書専用**スキルです。候補者のデータは入っていません。履歴書の元書式、職務経歴書の元書式、写真抽出・管理表抽出・書類入力スクリプト、開始指示文が入っています。

## 1 入れ方（各担当者が1回）

1. Claudeの 設定 → カスタマイズ → **プラグイン** → **＋追加** → **マーケットプレイスを追加** → **リポジトリから追加** に `Choice-System/choice-aid-skills` を入れて同期する（面接FBスキルを入れた人は済んでいる）。
2. 一覧の **Choice aid application documents** の **追加** を押す。スイッチが青になれば完了。
3. Team／Enterpriseの場合は、管理者が組織にまとめて配ることもできる。

## 2 担当者ごとの使い方

1. スキルが有効か確認する。Claude ChatまたはCoworkでは、`prompts/start-prompt.md` の文章を新しい会話に貼る。
2. 求職者のIndeed等のレジュメPDF、Gemini面接メモ・逐語録、CA手打ちメモ、管理表の該当行を添付する。Driveに接続できるなら管理表の指定ファイルIDの現在版を読む。求人票がある場合は加える。
3. 候補者名、担当CA、作成日を指示文へ入力する。書類を受け取ったら写真・氏名・メール・電話・年月を確認する。
4. 写真入りXLSXとDOCXがチャットに出る。それぞれファイルの右の「∨」→「Google Driveで開く」を押すと、Googleスプレッドシート／Googleドキュメントとして自分のDriveに作られる。写真と印刷表示を確認する。
5. 本人確認後、作成CAと別担当者のダブルチェックを済ませてから企業提出する。

## 3 Claude Code

claude.aiアカウントにアップロード・有効化したスキルがClaude Codeへ同期される設定なら、`/skills` で表示を確認して `/choice-aid-application-documents` を呼び出す。同期しない環境ではZIPを展開して、スキルフォルダをプロジェクトの `.claude/skills/choice-aid-application-documents/` または個人の `~/.claude/skills/choice-aid-application-documents/` に配置する。`SKILL.md` と `assets/`、`scripts/`、`references/` を同じフォルダに保つ。候補者ファイルと出力先はこのスキルフォルダ外に置く。

## 4 Claude Cowork

ClaudeのCustomizeで有効にしたスキルを使う。Coworkはローカルの `~/.claude/skills/` を自動では読み込まないため、Claude Codeの個人フォルダへ置くだけではCoworkに共有されない。開始指示文と資料をCoworkタスクに渡し、候補者ごとに作業する。

## 5 受け入れ条件

- 履歴書は元テンプレートの記入欄を維持したGoogleスプレッドシート。職務経歴書は元テンプレートに沿ったGoogleドキュメント。
- 元レジュメの本人写真が履歴書に表示され、印刷時にも残る。見つからないときは未添付と明記する。
- 管理表から対象者だけを抽出し、提案企業・選考日を職歴に混ぜない。
- 氏名、ふりがな、メール、電話、生年月日、学歴、入退社年月を一次資料に照合する。
- 本人確認と別担当者チェックが終わるまでは「確認用ドラフト」。

## 6 必要な環境

Python実行時は `openpyxl`、`python-docx`、`Pillow` と Popplerの `pdfimages` が必要です。Claude Chatでコード実行やDrive書き込みが使えない場合は、スキルの判断基準とテンプレートを使ってXLSX/DOCXを作り、ネイティブ変換は担当者が実施します。Google Driveへの接続は各担当者の権限に従います。
