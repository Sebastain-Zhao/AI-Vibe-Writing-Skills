import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r'd:\AAAAAAAA\AI-Vibe-Writing-Skills-main\文献\中国激光v1.pdf')
full_text = ""
for i, page in enumerate(doc):
    text = page.get_text()
    full_text += text

print(full_text)
