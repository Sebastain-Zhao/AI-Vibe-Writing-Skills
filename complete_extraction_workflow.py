#!/usr/bin/env python3
"""
完整的文献提取工作流程：
1. 读取文献文件夹并更新 reference_library.json
2. 提取参考文献
3. 提取引用上下文
"""
import os
import subprocess
import sys

def run_script(script_name, description):
    """运行指定的脚本"""
    print(f"\n{'='*60}")
    print(f"步骤: {description}")
    print(f"{'='*60}")
    
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"错误: 找不到脚本 {script_path}")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(__file__))
        if result.returncode == 0:
            print(f"✓ {description} 完成")
            return True
        else:
            print(f"✗ {description} 失败，返回码: {result.returncode}")
            return False
    except Exception as e:
        print(f"✗ {description} 执行出错: {e}")
        return False

def main():
    print("="*60)
    print("开始完整的文献提取工作流程")
    print("="*60)
    
    # 步骤 1: 更新 reference_library.json
    success1 = run_script("process_literature.py", "更新 reference_library.json")
    
    # 步骤 2: 提取参考文献
    success2 = run_script("extract_and_save_references.py", "提取参考文献")
    
    # 步骤 3: 提取引用上下文
    success3 = run_script("extract_citation_contexts.py", "提取引用上下文")
    
    # 总结
    print("\n" + "="*60)
    print("工作流程完成")
    print("="*60)
    print(f"更新 reference_library.json: {'✓ 成功' if success1 else '✗ 失败'}")
    print(f"提取参考文献: {'✓ 成功' if success2 else '✗ 失败'}")
    print(f"提取引用上下文: {'✓ 成功' if success3 else '✗ 失败'}")
    
    if success1 and success2 and success3:
        print("\n✓ 所有步骤成功完成！")
        return 0
    else:
        print("\n✗ 部分步骤失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
