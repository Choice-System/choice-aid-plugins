# choice aid｜面接FB共有スキル（v1.3／全CA共通シート・ChatGPT／Claude両対応）

### できること
Gemini議事録/逐語録・Indeedレジュメ・手打ちメモを入力すると、**毎回同じ8項目で面接官を評価**し、良い点・改善点・次回質問のFB、**44項目の求職者プロファイル**、職歴、求人照合、追加質問、育成アクション、質問ナレッジを作ります。Google Sheetsが接続され編集できれば、**全CAが同じ元スプレッドシート**の14タブへ追記し、書いた範囲を読み戻して確認します。

履歴書・職務経歴書の作成は別スキル `choice-aid-application-documents` で行います（v1.3でこのスキルから分けました）。

### 共有・導入
1. このZIPをメンバーに共有します（実在求職者の資料は**同梱していません**）。
2. 導入手順は `references/env-claude.md`／`references/env-chatgpt.md`。スキルが使えないChatGPT環境では `prompts/team-paste-prompt.md` を新しい会話の最初に貼り、`SKILL.md` と `references/` を添付します。
3. **全CAの登録先は1つだけ**：`https://docs.google.com/spreadsheets/d/1dIJ5reidWBJqUL76bwY77kHvoKPfJWXTwj940-aYJFg/edit`。スキルを配っただけでは権限は付きません。管理者が各CAに編集権限を付けてください。CA名で複製したシートへの登録は禁止です（CAの区別は各タブの `CA`／`面接官`／`対象CA` 列）。
4. 毎回は `references/input-template.md` の文章に3資料を添えて依頼します。
5. 複数のCAが同時に登録すると衝突することがあります。続けて登録するときは、前の人の登録確認が終わってから依頼してください。

### 使い方（1回の依頼）
> 次の人の面接FBをお願いします。Geminiメモ・Indeedレジュメ・手打ちメモを添付します。choice aid面接FBスキルで評価して、シートへ追加してください。

### 運用ルール
- 全CAが1つの同じ元シートを使い、他CAの行は上書きしない。
- 正規の採点は**統一評価Ver.1.0**。基準を変えるときは `references/scoring-rubric.md` とシートの採点マスターを**両方**直す。
- 求職者の属性や人格に点をつけず、面接官の行動を根拠に採点する。採用結果とCA面接品質は別に管理する。
- Geminiの要約の誤りを本人確認済みの事実にしない。住所・電話・メール等をナレッジに残さない。

### パッケージ内のファイル
- `SKILL.md` — 手順の本体（守ること・Step 1〜6・最後のチェック）
- `references/scoring-rubric.md` — 8項目・配点・判定、判断が割れやすい所の読み方（毎回読む）
- `references/output-format.md` — 画面に出すFBの型（毎回読む）
- `references/sheet-registration.md` — 14タブ、読む範囲、追記行、数式、同時書き込み、書けないとき（毎回読む）
- `references/id-rules.md` — ID形式と採番（毎回読む）
- `references/sheet-columns.json` — 14タブの見出しの控え（シートを読めないときだけ）
- `references/env-chatgpt.md`／`references/env-claude.md` — 導入・接続
- `references/input-template.md` — メンバー用の依頼文
- `prompts/team-paste-prompt.md` — スキル未対応環境の代わり
- `scripts/extract_candidate_management.py` — 管理表がXLSXのとき対象者の行だけを取り出す
- `config.example.yaml` — 対象シートの設定例

### 1面接で登録する件数（資料しだい）
ログ1、面接評価1、統一評価1、詳細FB8、候補者プロファイル1（44列）、求人提案1、成果連携1、職歴は件数分、追加質問は必要数、育成カルテ2〜3、アクション3〜4、改善ナレッジ2〜3、質問ナレッジ2〜3。求人マッチングは実際に応募・紹介した企業だけ。

### ChatGPTとClaudeの両方で使う
- 中身は同じで、配布ZIPだけ `_chatgpt` と `_claude` に分かれています。
- 直すときは元ソース1か所だけを直し、PJフォルダの build_skill_packages.py（スキル外）で両方のZIPを作り直します。

### バージョン
v1.3.0：軽量化。応募書類の作成を別スキルへ分離。採点・FBを先に終えてからシートを読む順番に変更。管理表は対象者の行だけ、FBシートは見出し・ID列だけを読む形に限定。追記行・数式列の扱いを明記。重複していた記述を1か所に集約（品質確認はSKILL.mdのチェックリストに統合）。採点基準の判断が割れやすい所に読み方を追加（基準は同じ）。
v1.2.0：ID規則v1.0を追加。1面接で必ずそろえる行を明記。ChatGPT版／Claude版を同じ元ソースから作る形に変更。テスト環境への登録指定に対応。
v1.1.0：全CAで同じ元シートに追記する運用を正式採用。
v1.0.0：2026-10-16時点の14タブ見出し・統一評価Ver.1.0を基準として作成。
