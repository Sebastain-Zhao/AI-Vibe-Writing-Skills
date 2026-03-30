---
name: "pdf-reader"
description: "Reads local/online PDFs, extracts evidence, facts, and references, stores in reference_library.json. Invoke when user needs to ingest PDF content for writing or research."
---

# PDF Reader Skill

This skill reads and parses PDF documents to extract structured evidence, facts, and references for use in writing.

## Key Features

1. **PDF Ingestion**: Reads both local files and online URLs
2. **Evidence Extraction**: Identifies key facts, data points, and quotable content
3. **Structured Storage**: Organizes extracted content into `reference_library.json`
4. **Memory Sync**: Updates hard/soft memory with domain terminology and stable facts
5. **MinerU Integration**: Supports MinerU parser for high-quality markdown/JSON output

## When to Use

- When user provides a PDF to read and learn from
- Before starting a research paper or technical document
- When building a reference library for a specific domain
- When evidence needs to be extracted for citation

## Extraction Pipeline

1. **Acquisition**: Accept local file path or online URL
2. **Parsing**: Convert PDF to text/markdown using MinerU or built-in parser
3. **Extraction**: Identify and extract:
   - Key facts and data points
   - Terminology and domain-specific vocabulary
   - Quotable statements and conclusions
   - Citation metadata
4. **Normalization**: Clean and structure extracted content
5. **Storage**: Write to `reference_library.json`
6. **Memory Sync**: Update `hard_memory.json` with stable facts

## Output Files Updated

- `.ai_context/memory/reference_library.json` - Evidence database
- `.ai_context/memory/hard_memory.json` - Hard facts & terms
- `.ai_context/memory/soft_memory.json` - Domain preferences (if applicable)

## Integration with Writing Workflow

Extracted evidence is automatically available to the content-writer skill for citation and verification during the drafting process.
