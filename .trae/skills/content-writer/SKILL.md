---
name: "content-writer"
description: "Generates content matching personal style, avoids errors, uses long-term memory. Invoke when drafting or revising text with style constraints and memory alignment."
---

# Content Writer Skill

This skill generates high-quality content that matches the user's personal writing style while avoiding known errors.

## Key Features

1. **Style Matching**: Strictly follows `style_profile.md` for tone, sentence structure, and word choice
2. **Error Avoidance**: Checks `error_log.md` and self-audits to prevent repeating mistakes
3. **Long-Term Memory**: Uses `hard_memory.json` and `soft_memory.json` for domain consistency
4. **Evidence Integration**: Retrieves and embeds relevant evidence from `reference_library.json`
5. **AI Tone Detection**: Identifies and removes AI-sounding words (like "delve", "tapestry", "utilize")

## When to Use

- When drafting new content (papers, blogs, essays)
- When revising existing text to match personal style
- When evidence-based writing is required
- When avoiding AI tone is important

## Workflow

1. **Recall**: Review error log and list top 3 relevant "don'ts"
2. **Retrieve**: Pull relevant hard/soft memory for the domain
3. **Mimic**: Internalize style profile to set tone baseline
4. **Evidence**: Select evidence from reference library meeting requirements
5. **Context Budget**: Trim irrelevant context based on custom specs
6. **Draft**: Generate content and embed evidence where needed
7. **Audit**: Self-correct for AI words and error log violations
8. **Evidence Check**: Verify evidence coverage and citation count

## Required Context Files

- `.ai_context/style_profile.md` - Writing style guidelines
- `.ai_context/error_log.md` - Mistakes to avoid
- `.ai_context/memory/hard_memory.json` - Hard facts & terms
- `.ai_context/memory/soft_memory.json` - Preferences & habits
- `.ai_context/custom_specs.md` - Global requirements
- `.ai_context/memory/reference_library.json` - Evidence database
