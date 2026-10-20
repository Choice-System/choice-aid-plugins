#!/usr/bin/env python3
"""Extract one candidate's rows from the linked management workbook.

Usage: python extract_candidate_management.py management.xlsx '求職者名' [担当CA]
Prints a compact JSON fact supplement with source sheet and row numbers.
Use only when the management file is an XLSX that cannot be read as a sheet;
the workbook must be downloaded fresh from the Drive file ID written in SKILL.md (Step 4).
"""
import json
import sys
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook

SHEETS = {
    '案件管理': ('求職者名', '担当CA', '初回面談日', '年齢', '現住所',
             '興味のある職種', '興味のある業界', '備考', '離脱日',
             '離脱フェーズ', '離脱理由', '離脱理由詳細', '再アプローチ可否'),
    '選考管理': ('求職者名', '提案企業・求人', '選考ステータス', '提案日',
             '応募承諾日', '推薦日', '書類結果日', '面接日', '面接フェーズ',
             '選考結果', '内定日', '承諾日', '入社予定日', '入社日',
             '次回アクション', '対応期限', '備考'),
}

def normalized(value):
    return ''.join(str(value or '').split())

def scalar(value):
    if isinstance(value, (date, datetime)): return value.isoformat()
    return value

def rows(sheet, fields, name):
    iterator=sheet.values
    header=next(iterator)
    indexes={str(value): i for i, value in enumerate(header) if value is not None}
    missing=set(fields)-set(indexes)
    if missing: raise ValueError(f'{sheet.title}: missing headers {sorted(missing)}')
    for row_number, row in enumerate(iterator, 2):
        def cell(field):
            index=indexes[field]
            return row[index] if index<len(row) else None
        if normalized(cell('求職者名')) != normalized(name): continue
        result={field:scalar(cell(field)) for field in fields
                if cell(field) not in ('', None)}
        result['source']={'sheet':sheet.title,'row':row_number}
        yield result

def extract(path, name, ca=None):
    wb=load_workbook(path,read_only=True,data_only=True)
    try:
        all_candidates=list(rows(wb['案件管理'],SHEETS['案件管理'],name))
        candidates=all_candidates
        if ca: candidates=[row for row in candidates if normalized(row.get('担当CA'))==normalized(ca)]
        if len(candidates)>1:
            raise ValueError('Multiple candidate rows match; disambiguate by CA or inspect source rows.')
        if not candidates:
            return {'candidate':name,'found':False,'source':'management workbook',
                    'message':'No matching candidate row; do not infer data from another person.'}
        # The selection tab has no CA or stable person ID; a namesake is ambiguous.
        selection=(list(rows(wb['選考管理'],SHEETS['選考管理'],name))
                   if len(all_candidates)==1 else [])
        return {'candidate':name,'found':True,'management':candidates[0],
                'selections':selection,
                'note':('Selection rows omitted due to duplicate names.' if len(all_candidates)>1
                        else 'Management notes are unverified CA notes; selection dates are not employment dates.')}
    finally:
        wb.close()

def main():
    if len(sys.argv) not in (3,4): raise SystemExit(__doc__)
    print(json.dumps(extract(Path(sys.argv[1]),sys.argv[2],
                             sys.argv[3] if len(sys.argv)==4 else None),
                     ensure_ascii=False,default=str))

if __name__=='__main__': main()
