"""
AI Vibe Writing Tool — Gradio 可视化写作助手
支持：写作助手、语法检查、AI 味检测、风格提取
"""

import os
import re
import json
import textwrap

import gradio as gr

# ─────────────────────────── 路径常量 ────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CTX_DIR  = os.path.join(BASE_DIR, ".ai_context")

def _read(path: str, fallback: str = "") -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return fallback

def _load_json(path: str, fallback=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return fallback if fallback is not None else {}

# ─────────────────────────── LLM 调用 ────────────────────────────
def _call_llm(system_prompt: str, user_message: str, api_key: str,
              model: str = "gpt-4o-mini", base_url: str = "") -> str:
    """调用 OpenAI 兼容接口；若未提供 API Key 则返回构造好的提示词供手动使用。"""
    if not api_key.strip():
        return (
            "⚠️ **未检测到 API Key，已切换为「提示词模式」**\n\n"
            "请将下方内容复制到您偏好的 AI 对话界面（如 ChatGPT、Claude）中使用：\n\n"
            "---\n\n"
            f"**【系统提示】**\n{system_prompt}\n\n"
            f"**【用户输入】**\n{user_message}\n\n"
            "---"
        )
    try:
        from openai import OpenAI  # type: ignore
        kwargs = {"api_key": api_key}
        if base_url.strip():
            kwargs["base_url"] = base_url.strip()
        client = OpenAI(**kwargs)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message},
            ],
        )
        return resp.choices[0].message.content or ""
    except Exception as exc:
        return f"❌ API 调用失败：{exc}"

# ═══════════════════════════════════════════════════════════════════
# 模块一：写作助手
# ═══════════════════════════════════════════════════════════════════
def _build_writer_system() -> str:
    """读取所有上下文文件，拼装写作助手的系统提示词。"""
    style   = _read(os.path.join(CTX_DIR, "style_profile.md"))
    errors  = _read(os.path.join(CTX_DIR, "error_log.md"))
    hard    = _load_json(os.path.join(CTX_DIR, "memory", "hard_memory.json"))
    soft    = _load_json(os.path.join(CTX_DIR, "memory", "soft_memory.json"))
    prompt  = _read(os.path.join(CTX_DIR, "prompts", "2_writer.md"))

    hard_str = json.dumps(hard, ensure_ascii=False, indent=2)
    soft_str = json.dumps(soft, ensure_ascii=False, indent=2)

    system = textwrap.dedent(f"""\
        {prompt}

        ## Style Profile (style_profile.md)
        {style or '（未配置）'}

        ## Error Log (error_log.md)
        {errors or '（未配置）'}

        ## Hard Memory
        ```json
        {hard_str}
        ```

        ## Soft Memory
        ```json
        {soft_str}
        ```
    """)
    return system


def run_writer(topic: str, mode: str, extra: str,
               api_key: str, model: str, base_url: str) -> str:
    if not topic.strip():
        return "⚠️ 请先填写写作主题或内容。"

    mode_map = {
        "直接起草 Direct Draft":       "直接按照风格和禁忌清单起草内容。",
        "结构化起草 Structured Draft":  "先列大纲，再逐节起草。",
        "参考驱动 Reference-Driven":    "优先引用记忆库中的证据与参考文献，再起草。",
        "段落扩写 Expand":              "将用户提供的要点或粗稿扩写为完整段落。",
        "精简缩写 Condense":            "将用户提供的内容压缩，保留核心论点。",
    }
    mode_instruction = mode_map.get(mode, "直接起草。")
    user_msg = (
        f"写作模式：{mode_instruction}\n\n"
        f"写作主题 / 内容：\n{topic}"
        + (f"\n\n补充说明：\n{extra}" if extra.strip() else "")
    )

    system = _build_writer_system()
    return _call_llm(system, user_msg, api_key, model, base_url)


# ═══════════════════════════════════════════════════════════════════
# 模块二：语法检查
# ═══════════════════════════════════════════════════════════════════
_GRAMMAR_PROMPT = _read(os.path.join(CTX_DIR, "prompts", "4_grammar_checker.md"))
if not _GRAMMAR_PROMPT:
    _GRAMMAR_PROMPT = (
        "You are a bilingual (English / Chinese) grammar and style checker. "
        "Identify grammar errors, typos, and AI-style clichés. "
        "Return a Markdown table: Location | Original | Correction | Reason. "
        "If no issues, say ✅ No errors found."
    )

def run_grammar_check(text: str, api_key: str, model: str, base_url: str) -> str:
    if not text.strip():
        return "⚠️ 请先输入需要检查的文本。"
    return _call_llm(_GRAMMAR_PROMPT, text, api_key, model, base_url)


# ═══════════════════════════════════════════════════════════════════
# 模块三：AI 味检测（本地规则，无需 API Key）
# ═══════════════════════════════════════════════════════════════════

# 英文高频词（来自 paper_ai_detector.py + error_log + custom_specs）
_AI_WORDS_EN = [
    r"\bdelve(?:s|d)?\b", r"\btapestry\b", r"\blandscape\b",
    r"\bunderscore(?:s|d)?\b", r"\bcrucial\b", r"\bparadigm shift\b",
    r"\bnuanced\b", r"\btestament\b", r"\bnavigate?(?:s|d|ing)?\b",
    r"\brobust\b", r"\bdemystify\b", r"\bpivotal\b", r"\bintricate\b",
    r"\bseamless(?:ly)?\b", r"\bcornerstone\b", r"\bparamount\b",
    r"\bsynergy\b", r"\bvital\b", r"\bunprecedented\b",
    r"\bshed light on\b", r"\bmultifaceted\b", r"\bfosters?\b",
    r"\brevolutionar(?:y|ies)\b", r"\bgame.changer?\b",
    r"\bin summary\b", r"\bto summarize\b", r"\bfurthermore\b",
    r"\bmoreover\b", r"\badditionally\b", r"\bin conclusion\b",
    r"\bleverage(?:s|d|ing)?\b", r"\becosystem\b",
    r"\borthogonal\b",
]

# 中文高频词（来自 paper_ai_detector.py + error_log）
_AI_WORDS_CN = [
    r"毋庸置疑", r"不可否认的是", r"值得注意的是", r"综上所述",
    r"在.{0,10}背景下", r"旨在", r"深入探讨", r"凸显了",
    r"赋能", r"重塑", r"彰显", r"鲁棒", r"显著的",
    r"前所未有的", r"错综复杂的", r"全面的", r"画卷",
    r"织锦", r"里程碑", r"双刃剑", r"基石",
    r"范式转变", r"协同效应",
]

# 机械过渡词
_MECHANICAL_TRANSITIONS = re.compile(
    r"\b(furthermore|moreover|additionally|in conclusion|in summary|"
    r"to summarize|firstly|secondly|thirdly|lastly|in addition|"
    r"on the other hand)\b",
    re.IGNORECASE,
)

# 绝对化断言
_ABSOLUTE_CLAIMS = re.compile(
    r"\b(this proves? that|it is (clear|evident|obvious) that|"
    r"undoubtedly|without (a )?doubt)\b",
    re.IGNORECASE,
)

# 僵尸名词（-tion/-ment/-ance 高密度）
def _nominalization_density(text: str) -> float:
    words = re.findall(r"\b\w+\b", text)
    if not words:
        return 0.0
    heavy = sum(1 for w in words
                if re.search(r"(tion|ment|ance|ence|ity|ism)\b", w, re.I))
    return round(heavy / len(words), 4)


def run_ai_detector(text: str) -> str:
    if not text.strip():
        return "⚠️ 请先输入需要检测的文本。"

    found_en: list[str] = []
    for pattern in _AI_WORDS_EN:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        found_en.extend(m.lower() for m in matches)

    found_cn: list[str] = []
    for pattern in _AI_WORDS_CN:
        matches = re.findall(pattern, text)
        found_cn.extend(matches)

    mech = _MECHANICAL_TRANSITIONS.findall(text)
    abs_claims = _ABSOLUTE_CLAIMS.findall(text)
    nomi_density = _nominalization_density(text)

    # 评分
    score = 0
    score += min(len(found_en) * 5, 30)
    score += min(len(found_cn) * 5, 20)
    score += min(len(mech) * 8, 24)
    score += min(len(abs_claims) * 10, 20)
    score += min(int(nomi_density * 200), 6)
    score = min(score, 100)

    if score >= 60:
        verdict = "🚨 **AI 味极高**——建议大幅修改，参考 Don'ts 清单逐项替换。"
    elif score >= 35:
        verdict = "🤔 **存在 AI 润色痕迹**——有几处典型 AI 套话，建议针对性替换。"
    else:
        verdict = "✅ **整体较为自然**——未发现显著 AI 味指标。"

    lines = [
        f"## 🤖 AI 味检测报告",
        f"",
        f"**综合评分：{score} / 100**　{verdict}",
        f"",
        f"---",
        f"",
    ]

    if found_en:
        lines += [
            "### 🔴 英文高频词（AI Buzzwords）",
            f"发现 **{len(found_en)}** 个：`{'`, `'.join(sorted(set(found_en)))}`",
            "",
        ]
    if found_cn:
        lines += [
            "### 🔴 中文高频词（AI 套话）",
            f"发现 **{len(found_cn)}** 个：{'、'.join(sorted(set(found_cn)))}",
            "",
        ]
    if mech:
        unique_mech = sorted(set(m.lower() for m in mech))
        lines += [
            "### 🟠 机械过渡词",
            f"发现 **{len(mech)}** 处：`{'`, `'.join(unique_mech)}`",
            "> 建议：复用上段关键词自然承接，避免段首使用机械过渡。",
            "",
        ]
    if abs_claims:
        lines += [
            "### 🟠 绝对化断言",
            f"发现 **{len(abs_claims)}** 处",
            "> 建议：改用 *These findings suggest...* 或 *The data indicates...* 等学术性 hedging。",
            "",
        ]
    lines += [
        "### 📊 僵尸名词密度",
        f"{nomi_density:.1%}"
        + ("  ⚠️ 较高，建议将 -tion/-ment/-ance 名词还原为主动动词。"
           if nomi_density > 0.06 else "  ✅ 正常"),
        "",
    ]

    if not any([found_en, found_cn, mech, abs_claims]) and nomi_density <= 0.06:
        lines += ["", "✅ **未发现任何典型 AI 标志词汇或句式问题。**"]

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# 模块四：风格提取
# ═══════════════════════════════════════════════════════════════════
_STYLE_PROMPT = _read(os.path.join(CTX_DIR, "prompts", "1_style_extractor.md"))
if not _STYLE_PROMPT:
    _STYLE_PROMPT = (
        "You are a professional stylometrics expert. "
        "Analyze the provided writing samples and extract a Style DNA in Markdown, "
        "covering: Tone, Sentence Pattern, Do's list, and Don'ts list."
    )

def run_style_extractor(samples: str, api_key: str, model: str, base_url: str) -> str:
    if not samples.strip():
        return "⚠️ 请粘贴您过去撰写的文章样本（建议 3 段以上）。"

    user_msg = (
        "以下是我的写作样本，请深入分析并提取我的写作风格指纹（Style DNA），"
        "输出内容可直接写入 `style_profile.md`：\n\n"
        + samples
    )
    return _call_llm(_STYLE_PROMPT, user_msg, api_key, model, base_url)


# ═══════════════════════════════════════════════════════════════════
# Gradio 界面
# ═══════════════════════════════════════════════════════════════════
def _api_settings_row():
    with gr.Accordion("⚙️ API 设置（可折叠）", open=False):
        with gr.Row():
            api_key = gr.Textbox(
                label="API Key",
                placeholder="sk-...（留空则进入「提示词模式」）",
                type="password",
                scale=3,
            )
            model = gr.Textbox(
                label="模型",
                value="gpt-4o-mini",
                placeholder="gpt-4o-mini / gpt-4o / ...",
                scale=1,
            )
            base_url = gr.Textbox(
                label="Base URL（可选，用于第三方兼容接口）",
                placeholder="https://api.openai.com/v1",
                scale=2,
            )
    return api_key, model, base_url


with gr.Blocks(title="AI Vibe Writing Tool") as app:
    gr.Markdown(
        """
# ✍️ AI Vibe Writing Tool
**风格迁移 · 语法检查 · AI 味检测 · 风格提取**

> 配置文件位于 `.ai_context/` 目录，可自定义 `style_profile.md`、`error_log.md` 与 `memory/` 以贴合您的写作偏好。
        """
    )

    # ── Tab 1: 写作助手 ──────────────────────────────────────────
    with gr.Tab("✍️ 写作助手"):
        gr.Markdown("根据您的风格档案、错题本与长期记忆，生成个性化内容。")
        with gr.Row():
            with gr.Column(scale=2):
                topic_input = gr.Textbox(
                    label="写作主题 / 粗稿 / 要点",
                    placeholder="输入您的写作主题、粗稿或要点……",
                    lines=6,
                )
                write_mode = gr.Dropdown(
                    label="写作模式",
                    choices=[
                        "直接起草 Direct Draft",
                        "结构化起草 Structured Draft",
                        "参考驱动 Reference-Driven",
                        "段落扩写 Expand",
                        "精简缩写 Condense",
                    ],
                    value="直接起草 Direct Draft",
                )
                extra_input = gr.Textbox(
                    label="补充说明（可选）",
                    placeholder="例如：目标读者为领域专家；字数约 300 字；需引用数据……",
                    lines=2,
                )
                writer_api, writer_model, writer_base = _api_settings_row()
                write_btn = gr.Button("🚀 开始写作", variant="primary")
            with gr.Column(scale=3):
                writer_output = gr.Markdown(label="输出结果")

        write_btn.click(
            fn=run_writer,
            inputs=[topic_input, write_mode, extra_input,
                    writer_api, writer_model, writer_base],
            outputs=writer_output,
        )

    # ── Tab 2: 语法检查 ──────────────────────────────────────────
    with gr.Tab("🔍 语法检查"):
        gr.Markdown("中英文双语语法、拼写与 AI 风格洁癖项检查。")
        with gr.Row():
            with gr.Column(scale=2):
                grammar_input = gr.Textbox(
                    label="待检查文本",
                    placeholder="粘贴需要检查的文章段落……",
                    lines=10,
                )
                g_api, g_model, g_base = _api_settings_row()
                grammar_btn = gr.Button("🔍 开始检查", variant="primary")
            with gr.Column(scale=3):
                grammar_output = gr.Markdown(label="检查报告")

        grammar_btn.click(
            fn=run_grammar_check,
            inputs=[grammar_input, g_api, g_model, g_base],
            outputs=grammar_output,
        )

    # ── Tab 3: AI 味检测 ────────────────────────────────────────
    with gr.Tab("🤖 AI 味检测"):
        gr.Markdown(
            "**本地规则引擎，无需 API Key。**  \n"
            "扫描英文高频词、中文 AI 套话、机械过渡词、绝对化断言与僵尸名词密度。"
        )
        with gr.Row():
            with gr.Column(scale=2):
                detect_input = gr.Textbox(
                    label="待检测文本",
                    placeholder="粘贴需要检测的文章段落……",
                    lines=10,
                )
                detect_btn = gr.Button("🤖 开始检测", variant="primary")
            with gr.Column(scale=3):
                detect_output = gr.Markdown(label="检测报告")

        detect_btn.click(
            fn=run_ai_detector,
            inputs=[detect_input],
            outputs=detect_output,
        )

    # ── Tab 4: 风格提取 ──────────────────────────────────────────
    with gr.Tab("🎭 风格提取"):
        gr.Markdown(
            "上传您的历史写作样本，提取专属风格 DNA，"
            "输出内容可直接写入 `.ai_context/style_profile.md`。"
        )
        with gr.Row():
            with gr.Column(scale=2):
                style_input = gr.Textbox(
                    label="写作样本（建议粘贴 3 段以上）",
                    placeholder="粘贴您过往的写作样本……",
                    lines=12,
                )
                s_api, s_model, s_base = _api_settings_row()
                style_btn = gr.Button("🎭 提取风格", variant="primary")
            with gr.Column(scale=3):
                style_output = gr.Markdown(label="风格 DNA 报告")

        style_btn.click(
            fn=run_style_extractor,
            inputs=[style_input, s_api, s_model, s_base],
            outputs=style_output,
        )

    gr.Markdown(
        """
---
> 💡 **提示词模式**：不填写 API Key 时，工具会将完整提示词输出，供您复制到任意 AI 对话界面使用。  
> 📁 配置文件：`.ai_context/style_profile.md` · `.ai_context/error_log.md` · `.ai_context/memory/`
        """
    )


if __name__ == "__main__":
    print("正在启动 AI Vibe Writing Tool…")
    app.launch(server_name="127.0.0.1", server_port=7861, inbrowser=True)
