#!/usr/bin/env python3
"""Extract one embedded headshot from a candidate's PDF resume.

Usage: python extract_resume_photo.py resume.pdf output.jpg
Requires Poppler pdfimages and Pillow. If zero or multiple plausible photos
are found, stop for visual inspection instead of choosing another image.
"""
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

from PIL import Image

def extract(source, output):
    with tempfile.TemporaryDirectory(prefix='candidate_photo_') as tmp:
        base=Path(tmp)/'image'
        subprocess.run(['pdfimages','-j',str(source),str(base)],check=True,
                       capture_output=True)
        matches=[]
        for path in base.parent.glob('image-*'):
            try:
                with Image.open(path) as image:
                    width,height=image.size
                    if 120<=width<=800 and 160<=height<=1100 and .64<=width/height<=.85:
                        matches.append(path)
            except (OSError, ZeroDivisionError):
                continue
        if len(matches)!=1:
            raise ValueError(f'{len(matches)} plausible photos; inspect the source PDF visually.')
        if matches[0].suffix.lower() in ('.jpg','.jpeg'):
            shutil.copyfile(matches[0],output)
        else:
            with Image.open(matches[0]) as image:
                image.convert('RGB').save(output,quality=95)
    return output

def main():
    if len(sys.argv)!=3: raise SystemExit(__doc__)
    print(extract(Path(sys.argv[1]),Path(sys.argv[2])))

if __name__=='__main__':main()
