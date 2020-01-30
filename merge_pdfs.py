#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileMerger
import sys

# This script will merge two or more pdf files and give the resulting file a new name - subject#_visit#_SRTmerged.pdf
# If not merging SRT files, change the last line of the script (line 19)
# Usage: py .\merge_pdfs.py <pdffile1.pdf> <pdffile2.pdf>

path=''

pdfs = sys.argv[1:]

merger = PdfFileMerger()

for pdf in pdfs:
	merger.append(pdf)

newfilename = pdfs[1][2:12]

merger.write(newfilename+"SRTmerged.pdf")
