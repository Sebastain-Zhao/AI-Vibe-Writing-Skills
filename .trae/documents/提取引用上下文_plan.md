# 提取引用上下文 - The Implementation Plan (Decomposed and Prioritized Task List)

## [x] Task 1: 分析文献中引用的格式
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 研究文献中引用标记的格式（如 [1], [2], 等）
  - 理解如何定位引用标记周围的上下文句子
  - 确定需要提取多少上下文（引用前后的句子）
- **Success Criteria**:
  - 能够识别文献中的引用标记
  - 能够提取引用标记周围的上下文
- **Test Requirements**:
  - `programmatic` TR-1.1: 能够在示例文献中找到至少 5 个引用标记
  - `human-judgement` TR-1.2: 提取的上下文应该包含完整的句子，清晰展示引用的使用场景
- **Notes**: 引用通常出现在正文段落中，需要区分参考文献列表中的编号

## [x] Task 2: 实现引用上下文提取函数
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 创建函数来识别文献中的引用标记
  - 创建函数来提取引用标记周围的上下文句子
  - 将提取的上下文与参考文献编号关联
- **Success Criteria**:
  - 函数能够正确提取引用上下文
  - 每个引用编号都有对应的上下文
- **Test Requirements**:
  - `programmatic` TR-2.1: 函数返回的引用上下文数量与参考文献数量匹配
  - `programmatic` TR-2.2: 每个引用上下文都包含引用标记 [n]
  - `human-judgement` TR-2.3: 上下文句子完整且语义清晰

## [x] Task 3: 更新数据结构以保存引用上下文
- **Priority**: P0
- **Depends On**: Task 2
- **Description**: 
  - 修改 reference_library.json 的数据结构
  - 将引用上下文保存到每篇文献的 entry 中
  - 确保与现有 references 字段兼容
- **Success Criteria**:
  - reference_library.json 中有新的字段保存引用上下文
  - 数据结构清晰且可扩展
- **Test Requirements**:
  - `programmatic` TR-3.1: reference_library.json 可以正常加载和保存
  - `programmatic` TR-3.2: 新字段包含引用编号和对应的上下文
  - `human-judgement` TR-3.3: 数据结构设计合理，易于后续使用

## [x] Task 4: 集成到现有工作流
- **Priority**: P1
- **Depends On**: Task 3
- **Description**: 
  - 更新 extract_and_save_references.py 以包含引用上下文提取
  - 更新 process_literature.py（如需要）
  - 更新 reference-extractor skill 文档
- **Success Criteria**:
  - 运行现有脚本时能够自动提取引用上下文
  - 功能集成平滑，不破坏现有功能
- **Test Requirements**:
  - `programmatic` TR-4.1: 运行 extract_and_save_references.py 可以成功提取并保存引用上下文
  - `human-judgement` TR-4.2: 文档更新清晰，说明新功能的使用方法

## [x] Task 5: 测试和验证
- **Priority**: P1
- **Depends On**: Task 4
- **Description**: 
  - 在现有文献上测试完整流程
  - 验证提取的引用上下文质量
  - 检查边界情况（如一个引用多次出现、引用在句首/句尾等）
- **Success Criteria**:
  - 所有功能正常工作
  - 提取的引用上下文质量良好
- **Test Requirements**:
  - `programmatic` TR-5.1: 完整流程运行无错误
  - `programmatic` TR-5.2: 能够处理多次出现的同一引用
  - `human-judgement` TR-5.3: 提取的上下文能够帮助理解文献的引用关系
