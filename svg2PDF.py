from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import os

path = ''
os.chdir(path)

for filename in os.listdir(path):
    drawing = svg2rlg(filename)
    renderPDF.drawToFile(drawing, filename + ".pdf")
	
#convert svg to PDF