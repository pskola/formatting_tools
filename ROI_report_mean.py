# -*- coding: utf-8 -*-

#extract third float from fsl's ROI report file
#Usage: python ./ROI_report_mean.py <filename>

import sys

file=open(sys.argv[1],"r")
text=file.read()
file.close()

tex=text.split("\n")
te=[line.split(" ") for line in tex]
vals=[te[i][5] for i in range(len(te)-1)]
for t in vals:
    print(t)