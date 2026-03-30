---
name: "reference-extractor"
description: "Extracts references from PDF documents by reading the end sections. Invoke when user needs to find and collect references from research papers."
---

# Reference Extractor Skill

This skill extracts references from PDF research papers by reading the end sections where references are typically located.

## Key Features

1. **PDF Processing**: Reads PDF files and extracts text content
2. **Reference Detection**: Automatically identifies reference sections at the end of documents
3. **Reference Parsing**: Extracts and formats references in a structured manner
4. **Batch Processing**: Can handle multiple PDF files at once
5. **Encoding Handling**: Handles different text encodings to avoid extraction errors

## When to Use

- When user needs to collect references from research papers
- When analyzing the citation network of academic papers
- When building a literature review based on existing papers
- When verifying the accuracy of citations in a document

## Workflow

1. **Input**: PDF files containing research papers
2. **Processing**: Read the PDF file and extract text content with proper encoding handling
3. **Reference Detection**: Identify the reference section using multiple methods:
   - Method 1: Look for "REFERENCES" or "BIBLIOGRAPHY" section headers
   - Method 2: Check the last pages of the document where references are typically located
   - Method 3: Search for numbered reference patterns (e.g., [1], [2], etc.)
4. **Extraction**: Extract all references from the identified section, handling multi-line references
5. **Output**: Return the extracted references in a structured format, organized by source document

## Technical Implementation

The skill uses Python with the `pypdf` library to extract text from PDF files, then processes the text using a multi-step approach to identify and extract references. It includes:

- **Encoding Handling**: Properly handles UTF-8 encoding to avoid extraction errors with special characters
- **Multi-Method Detection**: Uses multiple techniques to find reference sections in different document formats
- **Batch Processing**: Capable of processing multiple PDF files in a folder
- **Structured Output**: Organizes references by source document for easy navigation

## Example Usage

### Extract references from a single PDF:
```
python parse_pdf.py "path/to/paper.pdf" | tail -n 300
```

### Extract references from all PDFs in a folder:
```
python extract_all_references.py
```

### Output Format

The extracted references are organized by source document, with each section containing:
- Document filename
- Complete reference list with numbered citations
- Full bibliographic information for each reference

Each reference typically includes:
- Author names
- Publication titles
- Journal/conference information
- Publication year
- DOI or other identifiers

## Advanced Features

- **Robust Detection**: Uses multiple methods to find reference sections in different document structures
- **Encoding Support**: Handles UTF-8 encoding to preserve special characters in references
- **Batch Processing**: Processes multiple PDF files in one operation
- **Structured Output**: Organizes references by source document for easy review
- **Error Handling**: Gracefully handles documents with non-standard reference formats

## Requirements

- Python 3.x
- `pypdf` library (`pip install pypdf`)
- Access to the PDF files to be processed

## Limitations

- May not work correctly with PDFs that have non-standard reference section formatting
- May require adjustment of the number of lines to extract based on the length of the reference section
- Encoding issues may affect extraction of special characters in some PDFs
