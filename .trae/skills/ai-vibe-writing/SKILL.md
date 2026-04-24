---
name: "ai-vibe-writing"
description: "AI写作助手，管理写作全流程：规范制定→大纲生成→写作→检阅→迭代。Invoke when user needs writing assistance, style matching, or multi-agent writing workflow."
---

# AI Vibe Writing Skill

This is the main AI writing assistant skill that orchestrates the entire writing workflow.

## Key Features

1. **Workflow Coordination**: Manages the complete writing loop from spec definition to final review
2. **Style Matching**: Uses your personal writing style from `.ai_context/style_profile.md`
3. **Error Avoidance**: Checks `.ai_context/error_log.md` to avoid repeating mistakes
4. **Long-Term Memory**: Leverages hard/soft memory for domain knowledge
5. **Multi-Agent System**: Coordinates outline manager, content writer, and review agents
6. **Progress Tracking**: Checks chapter-specific `进度.md` to maintain consistency with previous content and chapter objectives

## When to Use

- When user asks for writing assistance
- When creating academic papers, technical blogs, or essays
- When style matching is required
- When a full multi-agent writing workflow is needed

## Workflow Steps

1. **Spec Definition**: Create/validate `document_spec.md` as single source of truth
2. **Outline**: Generate outline with clear `definition_of_done` (DoD)
3. **Analyze & Recall**: Read style profile, error log, and memory
4. **Check Progress**: Read chapter-specific `进度.md` to understand:
   - **目录安排**: Check `目录.md` for chapter structure and writing outline
   - **本章研究目标**: Core innovation points and technical roadmap
   - **各节完成情况**: For each section:
     - Core content and key points
     - Key data and parameters (ensure consistency)
     - Logical framework and writing structure
     - Writing tips and important notes
   - **写作注意事项**: 
     - Abbreviation standards and usage
     - Data consistency checks (baud rate, distance, dispersion coefficient, target BER, etc.)
     - Chapter logic connections and transitions
   - **待解决问题**: Pending issues and tasks to address
5. **Draft**: Content writer generates content under constraints
6. **Audit**: Review against spec, detect AI tone, verify evidence
7. **Iterate**: Rewrite if audit fails, update memory with feedback

## Required Files

- `.traerules` - System configuration
- `.ai_context/style_profile.md` - Writing style
- `.ai_context/error_log.md` - Error avoidance rules
- `.ai_context/custom_specs.md` - Global configuration
- `.ai_context/memory/hard_memory.json` - Hard facts
- `.ai_context/memory/soft_memory.json` - Soft preferences
- `论文章节/第X章/进度.md` - Chapter progress and context (created per chapter)
  - **Format**: Follows standard structure with 目录安排, 本章研究目标, 各节完成情况, 写作注意事项, 待解决问题
  - **Update frequency**: Update after completing each section
  - **Key focus**: Maintain data consistency, logical flow, and chapter coherence
