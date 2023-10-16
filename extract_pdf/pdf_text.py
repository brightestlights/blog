## Convert: lease.pdf (page 0) -> lease.txt
from PyPDF2 import PdfReader
reader = PdfReader('lease.pdf')
with open('lease.txt', 'w') as f:
    f.write(reader.pages[0].extract_text())
