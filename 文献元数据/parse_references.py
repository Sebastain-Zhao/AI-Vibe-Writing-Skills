#!/usr/bin/env python3
"""
直接从PDF文件中解析参考文献，不使用中间的.txt文件
"""
import re
import os
import sys

# Add the scripts directory to the path
script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.ai_context', 'scripts')
sys.path.append(script_dir)

from parse_pdf import extract_text_from_pdf

def extract_references_from_pdf(pdf_path):
    """从单个PDF文件中提取参考文献部分"""
    text = extract_text_from_pdf(pdf_path)
    
    lines = text.split('\n')
    
    reference_start = -1
    
    # Method 1: Look for REFERENCES or BIBLIOGRAPHY section
    for i, line in enumerate(lines):
        line_upper = line.upper()
        if 'REFERENCES' in line_upper or 'BIBLIOGRAPHY' in line_upper:
            reference_start = i
            break
    
    # Method 2: If not found, look for the last page which often contains references
    if reference_start == -1:
        last_lines = lines[-500:]
        for i, line in enumerate(last_lines):
            if line.strip().startswith('[') and ']' in line:
                reference_start = len(lines) - 500 + i
                break
    
    references = []
    if reference_start != -1:
        collecting = False
        for line in lines[reference_start:]:
            if not collecting and (line.strip().startswith('[') and ']' in line):
                collecting = True
            
            if collecting:
                references.append(line)
                
                if len(line.strip()) > 0 and not line.strip().startswith('[') and not any(char.isdigit() for char in line.strip()):
                    if len(line.strip()) < 30 and line.strip().isupper():
                        break
    
    if not references:
        for i, line in enumerate(lines):
            if line.strip().startswith('[') and ']' in line:
                references = lines[i:i+100]
                break
    
    return references

def parse_references_from_lines(lines):
    """从参考文献行中解析出单个参考文献条目"""
    current_references = []
    current_ref = []
    
    for line in lines:
        line = line.strip()
        
        ref_match = re.match(r'^\[(\d+)\]\s*(.+)$', line)
        if ref_match:
            if current_ref:
                current_references.append(' '.join(current_ref))
            
            ref_num = ref_match.group(1)
            ref_content = ref_match.group(2)
            current_ref = [ref_content]
        elif current_ref and line:
            current_ref.append(line)
    
    if current_ref:
        current_references.append(' '.join(current_ref))
    
    return current_references

def parse_references_from_pdf_folder(folder_path):
    """从文件夹中的所有PDF文件解析参考文献"""
    references_by_pdf = {}
    
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        
        references_lines = extract_references_from_pdf(pdf_path)
        references = parse_references_from_lines(references_lines)
        
        pdf_name = os.path.splitext(pdf_file)[0]
        references_by_pdf[pdf_name] = references
    
    return references_by_pdf

def parse_references_from_pdf(pdf_path):
    """从单个PDF文件解析参考文献"""
    references_lines = extract_references_from_pdf(pdf_path)
    references = parse_references_from_lines(references_lines)
    return references

if __name__ == "__main__":
    folder_path = r'd:\AAAAAAAA\AI-Vibe-Writing-Skills-main\文献'
    refs = parse_references_from_pdf_folder(folder_path)
    
    total_refs = 0
    for pdf_name, ref_list in refs.items():
        print(f"\n=== {pdf_name} ===")
        print(f"共 {len(ref_list)} 篇参考文献")
        total_refs += len(ref_list)
        for i, ref in enumerate(ref_list[:3], 1):
            print(f"  [{i}] {ref[:100]}...")
    
    print(f"\n总计: {total_refs} 篇参考文献")
