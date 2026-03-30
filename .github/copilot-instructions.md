# AI Vibe Writing Skill — GitHub Copilot Instructions

This repository is an **AI Writing Assistant** with Style Transfer, Error Memory, and Multi-Agent writing capabilities. When generating or editing any text, you **MUST** follow the workflow below.

---

## Workflow (Mandatory)

1. **Analyze**
   - Read `.ai_context/style_profile.md` to match the user's tone and style.
   - Read `.ai_context/custom_specs.md` for topic, audience, and constraints.

2. **Recall**
   - Read `.ai_context/error_log.md` for past mistakes to avoid.
   - Read `.ai_context/memory/hard_memory.json` and `.ai_context/memory/soft_memory.json` for domain-specific facts and preferences.
   - Read `.ai_context/memory/reference_library.json` when evidence or citations are required.
   - Internally list the top 3 relevant "Don'ts" before generating any text.

3. **Plan**
   - For complex tasks (full article, thesis section, report), propose an outline first using `.ai_context/outline_template.md`. Include a `definition_of_done` for each section.
   - For Spec-Driven writing, create or load `.ai_context/document_spec.md` using the template `.ai_context/document_spec_template.md`. Do NOT proceed to drafting until the spec is confirmed.

4. **Draft**
   - Generate content in strict adherence to the style profile and error log.
   - Avoid all "AI-sounding" words (e.g., delve, tapestry, robust, cornerstone, utilize, furthermore, moreover, additionally, 值得注意的是, 赋能, 前所未有的).
   - For large revisions, output a `<Revision_Plan>` first and wait for user approval before rewriting.

5. **Audit**
   - Self-check against `error_log.md` and `style_profile.md`.
   - Verify no prohibited words or mechanical transitions slipped through.
   - If violations are found, rewrite the affected passages before responding.

6. **Iterate**
   - If the user corrects output, update `.ai_context/error_log.md` with a new negative-constraint rule.
   - If feedback contains durable facts or preferences, update the relevant domain entry in `hard_memory.json` or `soft_memory.json`.

---

## Available Prompt Modules

| Module | File | When to Use |
|--------|------|-------------|
| Style Extractor | `.ai_context/prompts/1_style_extractor.md` | Analyzing writing samples to extract style DNA |
| Writer | `.ai_context/prompts/2_writer.md` | Default logic for all writing tasks |
| Error Logger | `.ai_context/prompts/3_error_logger.md` | Processing user corrections into negative constraints |
| Grammar Checker | `.ai_context/prompts/4_grammar_checker.md` | Identifying grammar, spelling, and punctuation issues |
| Long-Term Memory | `.ai_context/prompts/5_long_term_memory.md` | Storing and recalling domain-specific hard/soft memory |
| Outline Manager Agent | `.ai_context/prompts/6_outline_manager_agent.md` | Creating, validating, and storing outlines |
| Content Writer Agent | `.ai_context/prompts/7_content_writer_agent.md` | Drafting and revising content under outline constraints |
| Content Review Agent | `.ai_context/prompts/8_content_review_agent.md` | AI tone detection and external check integration |
| Workflow Coordinator | `.ai_context/prompts/9_workflow_coordinator.md` | Orchestrating the full outline → draft → review loop |
| PDF Reader Agent | `.ai_context/prompts/10_pdf_reader_agent.md` | Reading local/online PDFs and extracting evidence |

---

## Multi-Agent Writing Loop

When running the full multi-agent skill (see `.agents/workflows/ai_vibe_writing.md`):

1. Use **Outline Manager Agent** to load or create an outline; save it to `hard_memory.json` under key `latest_outline`.
2. Use **Content Writer Agent** to draft content section by section under outline and memory constraints.
3. Use **Outline Manager Agent** to validate output against the `definition_of_done` per section.
4. Iterate up to the configured maximum revision rounds.
5. Use **Content Review Agent** to check AI tone, evidence coverage, and spec compliance.
6. If the review fails any `definition_of_done`, request a rewrite and re-run the review.

---

## Key File References

| Purpose | Path |
|---------|------|
| Writing style profile | `.ai_context/style_profile.md` |
| Error / negative-constraint log | `.ai_context/error_log.md` |
| Custom specs (audience, mode, limits) | `.ai_context/custom_specs.md` |
| Document spec template | `.ai_context/document_spec_template.md` |
| Outline template (with DoD) | `.ai_context/outline_template.md` |
| Hard memory (facts, terms, units) | `.ai_context/memory/hard_memory.json` |
| Soft memory (tone, preferences) | `.ai_context/memory/soft_memory.json` |
| Reference library | `.ai_context/memory/reference_library.json` |

---

## Critical Rule

> **Every time you generate text in this repository, you MUST read `.ai_context/style_profile.md` to match the user's tone, `.ai_context/error_log.md` to avoid past mistakes, and the memory files to align with long-term facts and preferences. If the user corrects you, update the error log and the relevant memory.**
