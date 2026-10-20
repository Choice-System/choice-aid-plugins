"""公開前チェック：このリポジトリに、外に出してはいけないものが入っていないか調べる。

使い方: py -3 scripts/check_public.py --denylist <禁止語の一覧ファイル>
    禁止語の一覧（実名など）はこのリポジトリに入れず、手元にだけ置く。
    git のフック（.githooks/）からは `git config choiceaid.denylist` の場所を使う。
1件でも見つかれば終了コード1で止まる（コミット・プッシュも止まる）。
"""
import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

# 置いてよいファイルの種類。表計算・PDF・文書・画像などは求職者情報が入りうるので置かない
ALLOWED_EXT = {".md", ".json", ".py", ".yaml", ".yml", ".svg", ".txt", ".gitignore", ""}
MAX_BYTES = 300_000

# スキルが書き込み・参照する本番シートのIDだけは公開してよい（共有が社内に限られているため。2026-10-21判断）
ALLOWED_DRIVE_IDS = {
    "1dIJ5reidWBJqUL76bwY77kHvoKPfJWXTwj940-aYJFg",  # 中途人材紹介_AI面談FB
    "1AkIYX56cig3FxCetRC5YzHBONXTBZQ6gbQF_pW5W8o8",  # 求職者管理表（読み取りのみ）
}

PATTERNS = [
    ("メールアドレス", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("電話番号", re.compile(r"(?<!\d)0\d{1,4}-\d{1,4}-\d{3,4}(?!\d)|(?<!\d)0[789]0\d{8}(?!\d)")),
    ("郵便番号", re.compile(r"〒\s?\d{3}-?\d{4}")),
    ("生年月日", re.compile(r"(19|20)\d{2}年\d{1,2}月\d{1,2}日生")),
    ("人名＋敬称", re.compile(r"[一-龥々]{1,4}(さん|様|氏)")),
    ("APIキー・トークン", re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,}|xox[bp]-[A-Za-z0-9-]{10,})")),
]
DRIVE_ID = re.compile(r"(?<![A-Za-z0-9_-])1[A-Za-z0-9_-]{32,}(?![A-Za-z0-9_-])")
# 「お客さん」「皆さん」のように人名でない敬称つきの語
HONORIFIC_OK = {"皆さん", "お客さん", "お客様", "皆様", "各位様", "求職者様", "担当者様"}


def targets():
    for p in sorted(REPO.rglob("*")):
        if p.is_file() and ".git" not in p.relative_to(REPO).parts and "__pycache__" not in p.parts:
            yield p


def load_denylist(path):
    if not path:
        sys.exit("禁止語の一覧の場所が指定されていません（--denylist）。指定がないまま公開すると実名を見落とすため止めます。")
    f = pathlib.Path(path)
    if not f.is_file():
        sys.exit(f"禁止語の一覧が見つかりません: {f}")
    return [w.strip() for w in f.read_text(encoding="utf-8").splitlines() if w.strip() and not w.lstrip().startswith("#")]


def check_manifests(problems):
    market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    for entry in market["plugins"]:
        pj = REPO / entry["source"] / ".claude-plugin" / "plugin.json"
        if not pj.is_file():
            problems.append(f"marketplace.json: {entry['name']} の plugin.json がない（{pj.relative_to(REPO)}）")
            continue
        meta = json.loads(pj.read_text(encoding="utf-8"))
        if meta.get("name") != entry["name"]:
            problems.append(f"marketplace.json と plugin.json の name が違う: {entry['name']} / {meta.get('name')}")
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(meta.get("version", ""))) or meta["version"] == "0.0.0":
            problems.append(f"{pj.relative_to(REPO)}: version が未設定（ビルドで入れる）")
        for skill in (REPO / entry["source"] / "skills").glob("*/SKILL.md"):
            head = skill.read_text(encoding="utf-8").split("---")[1]
            if f"name: {skill.parent.name}" not in head:
                problems.append(f"{skill.relative_to(REPO)}: name がフォルダ名と違う")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--denylist")
    args = ap.parse_args()
    deny = load_denylist(args.denylist)
    problems = []

    for p in targets():
        rel = p.relative_to(REPO).as_posix()
        if any(ord(c) > 127 for c in rel):
            problems.append(f"{rel}: ファイル名に英数字以外がある（Claudeの登録エラーの原因）")
        if p.suffix.lower() not in ALLOWED_EXT and p.name != ".gitignore":
            problems.append(f"{rel}: 置いてはいけない種類のファイル（{p.suffix}）。求職者の資料などが紛れていないか確認")
            continue
        if p.stat().st_size > MAX_BYTES:
            problems.append(f"{rel}: ファイルが大きすぎる（{p.stat().st_size:,}バイト）")
        if rel in {"scripts/check_public.py"}:
            continue  # このファイル自体はパターンを書いているので対象外
        text = p.read_text(encoding="utf-8", errors="replace")
        for n, line in enumerate(text.splitlines(), 1):
            for w in deny:
                if w in line:
                    problems.append(f"{rel}:{n}: 禁止語「{w}」")
            for label, pat in PATTERNS:
                for m in pat.finditer(line):
                    if label == "人名＋敬称" and m.group(0) in HONORIFIC_OK:
                        continue
                    problems.append(f"{rel}:{n}: {label}「{m.group(0)}」")
            for m in DRIVE_ID.finditer(line):
                if m.group(0) not in ALLOWED_DRIVE_IDS:
                    problems.append(f"{rel}:{n}: 許可していないGoogleドライブのID「{m.group(0)[:10]}…」")

    check_manifests(problems)
    if problems:
        print("公開前チェック：NG（公開・コミットを止めます）")
        for x in problems:
            print("  - " + x)
        sys.exit(1)
    print(f"公開前チェック：OK（{sum(1 for _ in targets())}ファイル）")


if __name__ == "__main__":
    main()
