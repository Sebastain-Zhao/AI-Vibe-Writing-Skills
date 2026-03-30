---
name: "style-extractor"
description: "Extracts writing style DNA from text samples and generates style_profile.md. Invoke when user provides writing samples to analyze and capture their personal style."
---

# Style Extractor Skill

This skill analyzes writing samples to extract the user's unique "style DNA" and generates a `style_profile.md`.

## Key Features

1. **Sentence Structure Analysis**: Measures average sentence length, preference for short/long sentences, use of specific structures
2. **Vocabulary & Tone Analysis**: Assesses academic rigor, identifies signature words, determines emotional tone
3. **Micro-Habits Analysis**: Captures title formatting, citation style, punctuation preferences
4. **Do's & Don'ts Generation**: Creates clear guidelines for what to emulate and what to avoid

## When to Use

- When user provides writing samples (academic papers, blogs, essays)
- When initializing or updating the personal writing style
- Before starting a new writing project to match existing style

## Analysis Dimensions

### Sentence Structure
- Average sentence length
- Preference for short vs long sentences
- Use of inversion, emphasis, or specific conjunctions
- Active vs passive voice ratio

### Vocabulary & Tone
- Academic rigor score (1-10)
- Signature words (unique verbs/adjectives)
- Emotional tone (objective, humorous, critical, etc.)

### Micro-Habits
- Title formatting preferences
- Citation and example style
- Punctuation usage (dashes, semicolons, etc.)

## Output

Generates content directly for `.ai_context/style_profile.md` including:
- Core Style DNA (Tone, Sentence Pattern)
- Do's (what to keep)
- Don'ts (what to avoid)
