import fitz  # PyMuPDF
import os

pdf_path = r'd:\AAAAAAAA\AI-Vibe-Writing-Skills-main\文献\中国激光v1.pdf'
doc = fitz.open(pdf_path)
print(f'PDF页数: {len(doc)}')

# 读取所有页内容并保存
full_text = []
for i in range(len(doc)):
    page = doc[i]
    text = page.get_text()
    full_text.append(f'\n=== 第{i+1}页 ===\n{text}')

doc.close()

# 保存到文件
output_path = r'd:\AAAAAAAA\AI-Vibe-Writing-Skills-main\temp_pdf_content.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(full_text))

print(f'内容已保存到: {output_path}')
print(f'总字符数: {len("".join(full_text))}')
