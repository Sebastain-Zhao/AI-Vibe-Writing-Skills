#!/usr/bin/env python3
"""
提取reference_library.json中的所有参考文献信息并整理到新文件夹
"""
import json
import os
from pathlib import Path

REFERENCE_LIBRARY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'reference_library.json')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '搜索到的文献摘要')

def main():
    print("正在读取reference_library.json...")
    
    with open(REFERENCE_LIBRARY, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"找到 {len(data['sources'])} 篇文献")
    
    # 确保输出文件夹存在
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    total_refs = 0
    
    # 为每篇文献创建独立的参考文献文件
    for source in data['sources']:
        title = source['title']
        safe_title = "".join([c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title])
        safe_title = safe_title[:100]  # 限制文件名长度
        
        if 'references' in source and source['references']:
            refs = source['references']
            num_refs = len(refs)
            total_refs += num_refs
            
            markdown_content = f"# {title}\n\n"
            markdown_content += f"- **ID**: {source['id']}\n"
            markdown_content += f"- **领域**: {source['domain']}\n"
            markdown_content += f"- **年份**: {source['year']}\n"
            markdown_content += f"- **参考文献数量**: {num_refs}\n\n"
            markdown_content += "---\n\n"
            markdown_content += "## 参考文献列表\n\n"
            
            for i, ref in enumerate(refs, 1):
                markdown_content += f"### [{i}]\n\n"
                markdown_content += f"{ref}\n\n"
                markdown_content += "---\n\n"
            
            # 保存文件
            output_file = os.path.join(OUTPUT_FOLDER, f"{safe_title}_参考文献.md")
            print(f"正在保存: {output_file}")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # 如果有引用上下文，也保存
            if 'citation_contexts' in source and source['citation_contexts']:
                citation_contexts = source['citation_contexts']
                context_content = f"# {title} - 引用上下文\n\n"
                context_content += f"- **ID**: {source['id']}\n"
                context_content += f"- **引用文献数量**: {len(citation_contexts)}\n\n"
                context_content += "---\n\n"
                
                for ref_num in sorted(citation_contexts.keys(), key=lambda x: int(x)):
                    contexts = citation_contexts[ref_num]
                    
                    # 获取对应的参考文献信息
                    ref_index = int(ref_num) - 1
                    if 0 <= ref_index < len(refs):
                        context_content += f"## [{ref_num}] {refs[ref_index][:150]}...\n\n"
                    else:
                        context_content += f"## [{ref_num}]\n\n"
                    
                    context_content += f"**出现次数**: {len(contexts)}\n\n"
                    context_content += "**引用上下文**:\n\n"
                    
                    for j, ctx in enumerate(contexts, 1):
                        context_content += f"{j}. {ctx}\n\n"
                    
                    context_content += "---\n\n"
                
                context_file = os.path.join(OUTPUT_FOLDER, f"{safe_title}_引用上下文.md")
                print(f"正在保存: {context_file}")
                
                with open(context_file, 'w', encoding='utf-8') as f:
                    f.write(context_content)
    
    # 创建总览文件
    overview_content = "# 文献参考文献总览\n\n"
    overview_content += f"**统计信息**:\n"
    overview_content += f"- 文献总数: {len(data['sources'])}\n"
    overview_content += f"- 参考文献总数: {total_refs}\n\n"
    overview_content += "---\n\n"
    
    for source in data['sources']:
        title = source['title']
        num_refs = len(source.get('references', []))
        overview_content += f"## {title}\n\n"
        overview_content += f"- **ID**: {source['id']}\n"
        overview_content += f"- **领域**: {source['domain']}\n"
        overview_content += f"- **年份**: {source['year']}\n"
        overview_content += f"- **参考文献**: {num_refs} 篇\n\n"
        overview_content += "---\n\n"
    
    overview_file = os.path.join(OUTPUT_FOLDER, "文献参考文献总览.md")
    print(f"正在保存: {overview_file}")
    
    with open(overview_file, 'w', encoding='utf-8') as f:
        f.write(overview_content)
    
    # 创建说明文件
    note_content = "# 访问限制说明\n\n"
    note_content += "由于以下原因，未能直接从IEEE Xplore或Optica网站获取完整的文献摘要：\n\n"
    note_content += "1. **IEEE Xplore访问限制**：该网站对非授权访问进行了限制\n"
    note_content += "2. **需要登录/机构权限**：IEEE Xplore需要用户登录或机构IP访问权限\n"
    note_content += "3. **Cookies/Session缺失**：自动化浏览器工具没有用户的登录会话信息\n\n"
    note_content += "## 替代方案\n\n"
    note_content += "1. **手动访问**：您可以使用自己的浏览器（已登录IEEE Xplore）直接访问：\n"
    note_content += "   - https://ieeexplore.ieee.org/abstract/document/9743347/\n\n"
    note_content += "2. **使用已有信息**：本文件夹中已包含从reference_library.json提取的所有参考文献和引用上下文信息\n\n"
    note_content += "3. **复制粘贴**：您可以将手动获取的摘要信息复制到相应的文件中\n\n"
    note_content += "---\n\n"
    note_content += "创建时间：2026-04-01\n"
    
    note_file = os.path.join(OUTPUT_FOLDER, "访问限制说明.md")
    print(f"正在保存: {note_file}")
    
    with open(note_file, 'w', encoding='utf-8') as f:
        f.write(note_content)
    
    print("\n完成！")
    print(f"- 处理文献: {len(data['sources'])} 篇")
    print(f"- 提取参考文献: {total_refs} 篇")
    print(f"- 输出文件夹: {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()
