#!/usr/bin/env python3
"""
读取 reference_library 中每篇文献的参考文献并保存
"""
import os
import sys
import json

# Add the literature metadata directory to the path
metadata_dir = os.path.join(os.path.dirname(__file__), '文献元数据')
sys.path.append(metadata_dir)

from parse_references import parse_references_from_pdf

REFERENCE_LIBRARY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'reference_library.json')

def load_json(file_path):
    """Load JSON file"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(data, file_path):
    """Save JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("开始读取文献的参考文献...")
    
    reference_library = load_json(REFERENCE_LIBRARY)
    
    if 'sources' not in reference_library:
        print("没有找到 sources")
        return
    
    total_refs = 0
    for source in reference_library['sources']:
        pdf_path = source['file_path']
        print(f"\n处理: {source['title']}")
        
        try:
            references = parse_references_from_pdf(pdf_path)
            source['references'] = references
            print(f"  找到 {len(references)} 篇参考文献")
            total_refs += len(references)
            
            # 显示前 3 篇参考文献
            for i, ref in enumerate(references[:3], 1):
                print(f"    [{i}] {ref[:80]}...")
        except Exception as e:
            print(f"  错误: {e}")
            source['references'] = []
    
    # 保存更新后的数据
    save_json(reference_library, REFERENCE_LIBRARY)
    
    print(f"\n完成！总共找到 {total_refs} 篇参考文献")
    print(f"已保存到: {REFERENCE_LIBRARY}")

if __name__ == "__main__":
    main()
