#!/usr/bin/env python3
"""
解析参考文献文件，提取所有参考文献条目
"""
import re

def parse_references_file(file_path):
    """解析参考文献文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    references_by_pdf = {}
    current_pdf = None
    current_references = []
    current_ref = []
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # 检测新的PDF文件
        pdf_match = re.match(r'^=== \[(\d+)\](.+?)\.pdf ===$', line)
        if pdf_match:
            if current_pdf and current_references:
                references_by_pdf[current_pdf] = current_references
            
            current_pdf = pdf_match.group(2).strip()
            current_references = []
            current_ref = []
            continue
        
        # 检测新的参考文献条目
        ref_match = re.match(r'^\[(\d+)\]\s*(.+)$', line)
        if ref_match:
            if current_ref:
                current_references.append(' '.join(current_ref))
            
            ref_num = ref_match.group(1)
            ref_content = ref_match.group(2)
            current_ref = [ref_content]
        elif current_ref and line:
            # 继续当前参考文献
            current_ref.append(line)
    
    # 添加最后一个PDF的参考文献
    if current_pdf and current_references:
        if current_ref:
            current_references.append(' '.join(current_ref))
        references_by_pdf[current_pdf] = current_references
    
    return references_by_pdf

if __name__ == "__main__":
    file_path = r'd:\AAAAAAAA\AI-Vibe-Writing-Skills-main\所有参考文献.txt'
    refs = parse_references_file(file_path)
    
    total_refs = 0
    for pdf_name, ref_list in refs.items():
        print(f"\n=== {pdf_name} ===")
        print(f"共 {len(ref_list)} 篇参考文献")
        total_refs += len(ref_list)
        for i, ref in enumerate(ref_list[:3], 1):
            print(f"  [{i}] {ref[:100]}...")
    
    print(f"\n总计: {total_refs} 篇参考文献")
