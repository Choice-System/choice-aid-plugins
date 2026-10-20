# 入力と確認

## JSONの主要項目

`slug`, `name`, `as_of`, `furigana`, `birth_and_age`, `address_furigana`, `address`, `phone`, `email`, `nearest_station`, `hobbies`, `resume_rows`, `qualifications`, `summary`, `jobs`, `skills`, `self_pr`, `photo_path`。

- `resume_rows` は `[年, 月, 内容]` を古い順に並べる。学歴と職歴の見出し、最後の「以上」も必要な行として入力する。
- `qualifications` は `[年, 月, 名称]`。資格なし・年月不明を推測で埋めない。
- `jobs` は `{company, period, role, duties}` の配列。雇用形態や退職理由が不明なときは本文に勝手に追加しない。
- `photo_path` はPDFから抽出して本人と確認した画像の絶対パス。未取得なら省略する。
- 作業用JSONには個人情報が入るため、候補者別の作業領域に置き、スキルのZIPには含めない。

## 写真

```bash
python scripts/extract_resume_photo.py レジュメ.pdf 本人写真.jpg
```

本人写真を目視確認してからJSONの `photo_path` に指定する。画像が複数または埋め込み写真が見つからないときはPDFを目視して切り出すか、写真を未添付として報告する。写真を生成・修整して別人の顔にしない。

## 管理表

指定のDriveファイルが読み取れる場合は、現在版をXLSXとして一時取得する。

```bash
python scripts/extract_candidate_management.py 管理表.xlsx '求職者名' '担当CA'
```

`found:false` は該当行なしを意味する。`案件管理` の年齢、市区町村、希望条件、CA備考は照合用。`選考管理` は応募先別の選考進捗。面接日・推薦日・入社予定日は職歴の入退社年月ではない。`今日対応` は重複表示、KPIは集計なので読まない。

## 書類作成

```bash
python scripts/build_application_sources.py candidate.json output_dir
```

必要なPythonライブラリ：`openpyxl`, `python-docx`, `Pillow`。写真抽出に `pdfimages`（Poppler）が必要。コードを使えないClaude Chatでは、テンプレート・元資料を添付して同じ入力項目と検証条件を指示し、Google形式に変換できなければXLSX/DOCXを受け取ってDriveで変換する。

## 確認

- 原本の見出し、罫線、結合セル、配置が保たれている。
- 写真が本人のものとして履歴書に表示され、印刷時も欠落しない。
- 氏名、ふりがな、メール、電話、生年月日、学校名、入退社年月を一次資料と照合した。
- 企業別版では求人との接点が事実だけで説明されている。
- 未確認事項を別リストにし、応募先へ送る前に作成CAと別担当者が確認する。
