# ChatGPTで使うとき（導入・接続）

毎回の手順は `SKILL.md`、シートの読み書きは `sheet-registration.md` だけを見る。このファイルは導入時と接続に困ったときに読む。

## 準備（初回だけ）
1. ChatGPTの会社契約アカウント（入力が学習に使われない設定）で使う。個人の無料アカウントには求職者情報を入れない。
2. スキルの登録：配布された `choice-aid-interview-fb_chatgpt_vNN.zip` をスキル画面から登録する。スキルが使えない環境では `prompts/team-paste-prompt.md` を新しい会話の最初に貼り、`SKILL.md` と `references/` を添付する。
3. Googleの接続：Google Drive（読み取り）と、書き込みに使える Google Sheets の接続を有効にする。接続するGoogleアカウントに「中途人材紹介_AI面談FB」の**編集権限**と、求職者管理表の閲覧権限があることを確かめる。
4. 履歴書・職務経歴書の作成は別スキル `choice-aid-application-documents` で行う。

## 1人ごとの実行
1. 候補者ごとに新しい会話を開く（前の候補者の情報を混ぜない）。
2. `references/input-template.md` の依頼文を貼り、3点セット（Geminiメモ・Indeedレジュメ・手打ちメモ）を添付する。

## 接続ごとの注意
- 「まとめ読み」は複数範囲を1回で読む方法を使い、タブ全体を読まない。
- Sheetsへの書き込みができない接続しかない場合は `sheet-registration.md`「書き込めないとき」に従う。
