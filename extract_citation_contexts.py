#!/usr/bin/env python3
"""
提取reference_library.json中的citation_contexts字段并整理成Markdown文件
"""
import json
import os

REFERENCE_LIBRARY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'reference_library.json')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '搜索到的文献摘要', '引用上下文整理.md')

def main():
    print("正在读取reference_library.json...")
    
    with open(REFERENCE_LIBRARY, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"找到 {len(data['sources'])} 篇文献")
    
    markdown_content = "# 文献引用上下文整理\n\n"
    markdown_content += "本文档整理了reference_library.json中所有文献的引用上下文信息。\n\n"
    markdown_content += "---\n\n"
    
    total_citations = 0
    total_contexts = 0
    
    for source in data['sources']:
        title = source['title']
        markdown_content += f"## {title}\n\n"
        markdown_content += f"- **ID**: {source['id']}\n"
        markdown_content += f"- **领域**: {source['domain']}\n"
        markdown_content += f"- **年份**: {source['year']}\n\n"
        
        if 'citation_contexts' in source and source['citation_contexts']:
            citation_contexts = source['citation_contexts']
            num_refs = len(citation_contexts)
            total_citations += num_refs
            
            markdown_content += f"### 引用上下文 ({num_refs} 篇参考文献)\n\n"
            
            # 获取参考文献列表（如果存在）
            references = source.get('references', [])
            
            # 按引用编号排序
            ref_numbers = sorted(citation_contexts.keys(), key=lambda x: int(x))
            
            for ref_num in ref_numbers:
                contexts = citation_contexts[ref_num]
                num_contexts = len(contexts)
                total_contexts += num_contexts
                
                # 显示参考文献信息（如果有）
                ref_index = int(ref_num) - 1
                if 0 <= ref_index < len(references):
                    markdown_content += f"#### [{ref_num}] {references[ref_index][:100]}...\n\n"
                else:
                    markdown_content += f"#### [{ref_num}]\n\n"
                
                markdown_content += f"**出现次数**: {num_contexts}\n\n"
                markdown_content += "**引用上下文**:\n\n"
                
                for i, ctx in enumerate(contexts, 1):
                    markdown_content += f"{i}. {ctx}\n\n"
                
                markdown_content += "---\n\n"
        else:
            markdown_content += "*暂无引用上下文信息*\n\n"
        
        markdown_content += "---\n\n"
    
    # 添加统计信息
    markdown_content = f"# 文献引用上下文整理\n\n" + \
        f"**统计信息**:\n" + \
        f"- 文献总数: {len(data['sources'])}\n" + \
        f"- 引用文献总数: {total_citations}\n" + \
        f"- 引用上下文总数: {total_contexts}\n\n" + \
        "---\n\n" + \
        markdown_content.split("---\n\n", 1)[1]
    
    print(f"正在写入Markdown文件: {OUTPUT_FILE}")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("完成！")
    print(f"- 处理文献: {len(data['sources'])} 篇")
    print(f"- 提取引用文献: {total_citations} 篇")
    print(f"- 提取引用上下文: {total_contexts} 次")

if __name__ == "__main__":
    main()
