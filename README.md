# AI Vibe 写作工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 一款基于 Gradio 的可视化 AI 写作助手，整合风格迁移、语法检查、AI 味检测与风格提取四大核心功能，帮助你高效生产高质量、去"AI 味"的原创内容。

---

## 目录

- [项目简介](#项目简介)
- [功能模块](#功能模块)
- [快速开始](#快速开始)
- [目录结构](#目录结构)
- [配置说明](#配置说明)
- [辅助工具](#辅助工具)
- [开源协议](#开源协议)

---

## 项目简介

本项目的核心是 **`ai_writing_tool.py`**，一个基于 [Gradio](https://gradio.app) 构建的本地 Web 写作助手。它将 `.ai_context/` 目录下所有的提示词模板、风格档案、错题本与长期记忆统一整合为一个可交互界面，让你无需手动拼接提示词，即可在浏览器中完成写作全流程。

**设计理念**：跳出"AI 替代创作"的误区，把重复性的脏活（素材整理、格式规范、基础校对）交给 AI，把精力留给创意构思、内容深度打磨与风格个性化。

---

## 功能模块

### ✍️ 写作助手

根据你的风格档案（`style_profile.md`）、错题本（`error_log.md`）以及硬性/柔性长期记忆，自动构建完整的系统提示词，调用 LLM 生成个性化内容。

支持五种写作模式：

| 模式 | 说明 |
|------|------|
| 直接起草 | 按风格与禁忌清单直接生成 |
| 结构化起草 | 先输出大纲，再逐节展开 |
| 参考驱动 | 优先引用记忆库中的证据与参考文献 |
| 段落扩写 | 将要点或粗稿扩写为完整段落 |
| 精简缩写 | 压缩内容，保留核心论点 |

### 🔍 语法检查

调用 `.ai_context/prompts/4_grammar_checker.md` 中的专业提示词，对文本进行中英双语语法、拼写与 AI 风格洁癖项检查，输出结构化 Markdown 报告表格。

### 🤖 AI 味检测（本地规则引擎，无需 API Key）

完全离线运行，对文本进行五维扫描并给出 0–100 综合评分：

| 维度 | 内容 |
|------|------|
| 英文高频词 | delve / tapestry / robust / cornerstone 等 30+ 个典型 AI 词 |
| 中文 AI 套话 | 值得注意的是 / 赋能 / 前所未有的 / 里程碑 等 20+ 条 |
| 机械过渡词 | Furthermore / Moreover / Additionally / 综上所述 等 |
| 绝对化断言 | "This proves that..." 等结论夸大表述 |
| 僵尸名词密度 | -tion / -ment / -ance 名词化过度堆砌 |

评分结果：
- **0–34**：✅ 整体较为自然
- **35–59**：🤔 存在 AI 润色痕迹
- **60–100**：🚨 AI 味极高，建议大幅修改

### 🎭 风格提取

粘贴你过往的写作样本（建议 3 段以上），调用 `.ai_context/prompts/1_style_extractor.md` 提示词，提取专属风格 DNA，输出内容可直接写入 `.ai_context/style_profile.md`，供写作助手长期复用。

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 内容：
```
gradio>=4.0.0
openai>=1.0.0
```

### 2. 启动工具

```bash
python ai_writing_tool.py
```

启动后浏览器会自动打开 `http://127.0.0.1:7861`。

### 3. 填写 API Key（可选）

在界面的「⚙️ API 设置」折叠栏中填入你的 API Key（支持 OpenAI 及任何兼容接口）。

**提示词模式**：若不填 API Key，工具会将完整的系统提示词与用户输入一并输出，你可以直接复制到 ChatGPT、Claude 等任意 AI 对话界面使用。

---

## 目录结构

```
AI-Vibe-Writing-Skills/
├── ai_writing_tool.py          # 主程序：Gradio 可视化写作助手
├── requirements.txt            # 主程序依赖
│
├── .ai_context/                # AI 上下文配置目录
│   ├── style_profile.md        # 写作风格档案（Do's / Don'ts）
│   ├── error_log.md            # 错题本（历史纠错规则）
│   ├── custom_specs.md         # 自定义规范（受众、模式、限额等）
│   ├── document_spec_template.md  # 规范驱动写作模板
│   ├── outline_template.md     # 大纲模板（含 DoD 校验）
│   ├── pdf_ingestion_template.md  # PDF 入库模板
│   ├── reference_learning.md   # 参考文献学习说明
│   ├── memory/
│   │   ├── hard_memory.json    # 硬性记忆（术语、数据、单位）
│   │   ├── soft_memory.json    # 柔性记忆（偏好、语气、表达习惯）
│   │   └── reference_library.json  # 参考文献库
│   ├── prompts/                # 各智能体提示词
│   │   ├── 1_style_extractor.md
│   │   ├── 2_writer.md
│   │   ├── 3_error_logger.md
│   │   ├── 4_grammar_checker.md
│   │   ├── 5_long_term_memory.md
│   │   ├── 6_outline_manager_agent.md
│   │   ├── 7_content_writer_agent.md
│   │   ├── 8_content_review_agent.md
│   │   ├── 9_workflow_coordinator.md
│   │   └── 10_pdf_reader_agent.md
│   └── scripts/
│       └── parse_pdf.py        # PDF 文字提取脚本
│
├── Local_AI_Style_Check/       # 离线 LaTeX 论文 AI 检测工具
│   ├── paper_ai_detector.py
│   ├── requirements.txt
│   └── README.md
│
├── mineru_gui.py               # MinerU 高精度 PDF 解析可视化界面
├── run_magic_pdf.py            # MinerU 命令行调用脚本
├── create_pdf.py               # PDF 生成工具
├── magic-pdf.json              # MinerU 配置文件
├── configs/                    # 模型推理配置
├── SKILLS.md                   # 写作技艺总览（提示词索引）
└── FREE_AI_DETECTION_APIS.md   # 免费 AI 检测 API 汇总
```

---

## 配置说明

所有个性化配置均位于 `.ai_context/` 目录，修改后重启工具即可生效。

| 文件 | 作用 | 修改频率 |
|------|------|----------|
| `style_profile.md` | 定义你的写作风格 DNA（语调、句式、Do's / Don'ts） | 定期更新 |
| `error_log.md` | 记录历史纠错规则，写作时自动回避 | 每次纠错后追加 |
| `custom_specs.md` | 配置目标受众、写作模式、字数限额、证据要求等 | 按项目调整 |
| `memory/hard_memory.json` | 存储精确术语、单位、关键数据 | 按领域录入 |
| `memory/soft_memory.json` | 存储语气偏好、表达习惯 | 按领域录入 |
| `memory/reference_library.json` | 存储已入库的参考文献摘要 | 阅读文献后更新 |

---

## 辅助工具

### 离线 LaTeX 论文 AI 检测（`Local_AI_Style_Check/`）

基于本地 GPT-2 模型计算文本困惑度（PPL），结合高频词正则扫描，对 `.tex` 文件进行批量 AI 味检测。适合论文提交前的本地隐私检查。

```bash
cd Local_AI_Style_Check
pip install -r requirements.txt
python paper_ai_detector.py
```

### MinerU 高精度 PDF 解析（`mineru_gui.py`）

提供 Gradio 可视化界面，调用 MinerU（magic-pdf）对学术 PDF 进行深度版面分析，保留公式、表格与图片布局，输出结构化 Markdown。

```bash
python mineru_gui.py
```

---

## 开源协议

本项目采用 [MIT License](LICENSE) 开源。
