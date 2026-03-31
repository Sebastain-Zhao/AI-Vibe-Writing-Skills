#!/usr/bin/env python3
"""
提取文献中引用的上下文并保存到 reference_library.json
"""
import os
import sys
import json
import re

# Add the scripts directory to the path
script_dir = os.path.join(os.path.dirname(__file__), '.ai_context', 'scripts')
sys.path.append(script_dir)

from parse_pdf import extract_text_from_pdf

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

def find_citation_contexts(text, num_refs):
    """
    找到文献中所有引用的上下文
    """
    # 首先找到参考文献部分的位置，避免从参考文献列表中提取
    ref_section_start = -1
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_upper = line.upper()
        if 'REFERENCES' in line_upper or 'BIBLIOGRAPHY' in line_upper:
            ref_section_start = i
            break
    
    # 只在参考文献部分之前搜索引用
    if ref_section_start != -1:
        search_text = '\n'.join(lines[:ref_section_start])
    else:
        search_text = text
    
    citation_contexts = {}
    
    # 先将文本按句子分割
    # 使用正则表达式匹配句子结束符（.!?）
    # 但要注意避免缩写中的句号
    sentences = []
    current_sentence = []
    
    # 简单的句子分割方法
    i = 0
    n = len(search_text)
    while i < n:
        current_sentence.append(search_text[i])
        # 检查是否是句子结束符
        if search_text[i] in ['.', '!', '?']:
            # 简单的结束判断
            sentences.append(''.join(current_sentence))
            current_sentence = []
        i += 1
    
    if current_sentence:
        sentences.append(''.join(current_sentence))
    
    # 现在搜索每个句子中的引用
    for ref_num in range(1, num_refs + 1):
        pattern = rf'\[{ref_num}\]'
        contexts = []
        for sentence in sentences:
            if re.search(pattern, sentence):
                clean_sentence = sentence.strip()
                # 清理开头的纯数字（如页码）
                clean_sentence = re.sub(r'^\d+\s*', '', clean_sentence)
                # 清理换行符
                clean_sentence = clean_sentence.replace('\n', ' ')
                # 清理多余的空格
                clean_sentence = re.sub(r'\s+', ' ', clean_sentence)
                if clean_sentence:
                    contexts.append(clean_sentence)
        
        if contexts:
            citation_contexts[str(ref_num)] = contexts
    
    return citation_contexts

def main():
    print("开始提取引用上下文...")
    
    reference_library = load_json(REFERENCE_LIBRARY)
    
    if 'sources' not in reference_library:
        print("没有找到 sources")
        return
    
    total_citations = 0
    for source in reference_library['sources']:
        pdf_path = source['file_path']
        print(f"\n处理: {source['title']}")
        
        try:
            # 从 PDF 提取文本
            text = extract_text_from_pdf(pdf_path)
            
            # 获取参考文献数量
            num_refs = len(source.get('references', []))
            
            if num_refs == 0:
                print("  没有找到参考文献，跳过")
                continue
            
            # 提取引用上下文
            citation_contexts = find_citation_contexts(text, num_refs)
            
            # 保存到 source
            source['citation_contexts'] = citation_contexts
            
            citation_count = sum(len(contexts) for contexts in citation_contexts.values())
            total_citations += citation_count
            print(f"  找到 {len(citation_contexts)} 个引用的上下文，共 {citation_count} 次引用")
            
            # 显示前几个引用的上下文
            for ref_num in list(citation_contexts.keys())[:3]:
                contexts = citation_contexts[ref_num]
                print(f"    [{ref_num}] 出现 {len(contexts)} 次")
                if contexts:
                    print(f"      示例: {contexts[0][:100]}...")
                    
        except Exception as e:
            print(f"  错误: {e}")
            import traceback
            traceback.print_exc()
    
    # 保存更新后的数据
    save_json(reference_library, REFERENCE_LIBRARY)
    
    print(f"\n完成！总共找到 {total_citations} 次引用")
    print(f"已保存到: {REFERENCE_LIBRARY}")

if __name__ == "__main__":
    main()
