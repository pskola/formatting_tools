# -*- coding: utf-8 -*-

#extract third float from ROI report file
#Usage: python ./ROI_report_mean.py <filename>

import glob, os

for file in glob.glob("*.txt"):
	with open(file, "r+") as f:
		data = f.read()
		f.seek(0)
		tex=data.split("\n")
		te=[line.split(" ") for line in tex]
		vals=[te[i][5] for i in range(len(te)-1)]
		f.write(file[:-4]+"\n")
		for t in vals:
			f.write(t)
			f.write("\n")
		f.truncate()

