import pymupdf
import os

doc = pymupdf.open("../data/" + os.listdir("../data")[0])
text = " ".join(page.get_text() for page in doc)

print(text)