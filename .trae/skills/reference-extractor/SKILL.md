---
name: "reference-extractor"
description: "Extracts references from PDF documents and from papers in reference_library.json. Also extracts citation contexts showing where references are cited in the text. Invoke when user needs to find and collect references from research papers, read references from existing literature in reference_library, or extract citation contexts. Also works in pipeline with pdf-reader skill: first read literature with pdf-reader, then extract references and citation contexts with this skill."
---

# Reference Extractor Skill

This skill extracts references from PDF research papers by reading the end sections where references are typically located. It can also extract references from papers already stored in reference_library.json, and extract citation contexts showing where each reference is cited in the text.

## Complete Workflow Pipeline

This skill works best in conjunction with the `pdf-reader` skill:

1. **First**: Use `pdf-reader` skill to read PDF literature and store in `reference_library.json`
2. **Then**: Use this `reference-extractor` skill to extract references and citation contexts from the stored literature

## Key Features

1. **PDF Processing**: Reads PDF files and extracts text content
2. **Reference Detection**: Automatically identifies reference sections at the end of documents
3. **Reference Parsing**: Extracts and formats references in a structured manner
4. **Batch Processing**: Can handle multiple PDF files at once
5. **Encoding Handling**: Handles different text encodings to avoid extraction errors
6. **Reference Library Integration**: Reads references from papers already in reference_library.json and saves them back
7. **Citation Context Extraction**: Extracts the surrounding sentences where each reference is cited in the text
8. **Multi-occurrence Handling**: Captures all occurrences of a reference when cited multiple times

## When to Use

- When user needs to collect references from research papers
- When analyzing the citation network of academic papers
- When building a literature review based on existing papers
- When verifying the accuracy of citations in a document
- **When user says "读取reference_library下文献的参考文献" or similar phrases** - extract references from papers in reference_library.json
- **When user says "读取reference_library下文献的引用上下文" or "保留引用的那一句话" or similar phrases** - extract citation contexts showing where references are cited
- **When user says "进行提取操作" or similar phrases** - execute the complete extraction workflow
- **When user says "完整提取" or "完整工作流" or similar phrases** - run complete_extraction_workflow.py for the full pipeline

## Workflow

### Complete Workflow (Recommended)
First read literature with pdf-reader, then extract references and citation contexts:

1. **Step 1**: Use pdf-reader skill to read PDF literature and store in reference_library.json
2. **Step 2**: Extract references from papers in reference_library.json
3. **Step 3**: Extract citation contexts from papers in reference_library.json
4. **Step 4**: All data is saved in reference_library.json

### Scenario 1: Extract from PDF files directly
1. **Input**: PDF files containing research papers
2. **Processing**: Read the PDF file and extract text content with proper encoding handling
3. **Reference Detection**: Identify the reference section using multiple methods:
   - Method 1: Look for "REFERENCES" or "BIBLIOGRAPHY" section headers
   - Method 2: Check the last pages of the document where references are typically located
   - Method 3: Search for numbered reference patterns (e.g., [1], [2], etc.)
4. **Extraction**: Extract all references from the identified section, handling multi-line references
5. **Output**: Return the extracted references in a structured format, organized by source document

### Scenario 2: Extract references from reference_library.json
1. **Input**: Load reference_library.json
2. **Processing**: For each paper in the library, read its PDF file and extract references
3. **Extraction**: Use the same reference detection methods as Scenario 1
4. **Storage**: Save the extracted references back to each paper's entry in reference_library.json under the "references" field
5. **Output**: Display summary of extracted references

### Scenario 3: Extract citation contexts from reference_library.json
1. **Input**: Load reference_library.json
2. **Processing**: For each paper in the library, read its PDF file and search for citation markers [1], [2], etc.
3. **Context Extraction**: 
   - Skip the reference section to avoid extracting from the bibliography
   - For each citation marker found in the main text, extract the surrounding sentences (from previous period to next period)
   - Handle multiple occurrences of the same citation
   - Clean up the sentences (remove page numbers, replace newlines with spaces, normalize whitespace)
4. **Storage**: Save the extracted citation contexts back to each paper's entry in reference_library.json under the "citation_contexts" field
5. **Output**: Display summary of extracted citation contexts and occurrences

## Technical Implementation

The skill uses Python with the `pypdf` library to extract text from PDF files, then processes the text using a multi-step approach to identify and extract references and citation contexts. It includes:

- **Encoding Handling**: Properly handles UTF-8 encoding to avoid extraction errors with special characters
- **Multi-Method Detection**: Uses multiple techniques to find reference sections in different document formats
- **Batch Processing**: Capable of processing multiple PDF files in a folder
- **Structured Output**: Organizes references by source document for easy navigation
- **Reference Library Integration**: Seamlessly works with reference_library.json for reading and saving references
- **Citation Context Extraction**: Smartly identifies citation markers [n] in the main text and extracts surrounding sentences
- **Reference Section Skipping**: Automatically skips the reference section to avoid extracting from the bibliography
- **Multi-occurrence Support**: Captures and stores all occurrences when a reference is cited multiple times

## Example Usage

### Complete Pipeline (Recommended):
Run the complete workflow in one step:
```
python complete_extraction_workflow.py
```

This will:
1. Update reference_library.json from the literature folder
2. Extract references from all papers
3. Extract citation contexts from all papers

### Step-by-Step Pipeline:
If you prefer to run each step individually:

#### Step 1: Update reference_library.json
```
python process_literature.py
```

#### Step 2: Extract references from papers in reference_library.json:
```
python extract_and_save_references.py
```

#### Step 3: Extract citation contexts from papers in reference_library.json:
```
python extract_citation_contexts.py
```

### Extract references from all PDFs in a folder:
```
python extract_all_references.py
```

### Extract references from a single PDF:
```
python parse_pdf.py "path/to/paper.pdf" | tail -n 300
```

### Output Format

#### References
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

#### Citation Contexts
The extracted citation contexts are stored in reference_library.json under the "citation_contexts" field, organized as:
- Key: reference number (as string, e.g., "1", "2")
- Value: list of context strings where the reference is cited
- Each context contains the full sentence(s) around the citation marker [n]

Example structure in reference_library.json:
```json
{
  "citation_contexts": {
    "1": [
      "Nowadays, 50G-PON has been standardized by ITU-T and IEEE [1], [2], [3]."
    ],
    "11": [
      "The main challenges for high-speed IM/DD PON system are bandwidth limitation, channel impairments and low receiver sensitivity, which means that it is hard to meet the performance requirement such as an optical power budget of at least 29 dB [11], [12]."
    ],
    "14": [
      "In recent years, as the in-depth research of machine learning technique in optical communication systems, end-to-end learning has earned a lot of attention and is regarded as a promising way to improve the overall system performance [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25].",
      "Some studies directly use theoretical formulas or known numerical models of real physical channel to construct differentiable channel [14], [15], [16], [17], [18]."
    ]
  }
}
```

## Advanced Features

- **Robust Detection**: Uses multiple methods to find reference sections in different document structures
- **Encoding Support**: Handles UTF-8 encoding to preserve special characters in references
- **Batch Processing**: Processes multiple PDF files in one operation
- **Structured Output**: Organizes references by source document for easy review
- **Error Handling**: Gracefully handles documents with non-standard reference formats
- **Reference Library Sync**: Automatically saves extracted references back to reference_library.json
- **Smart Context Extraction**: Intelligently extracts complete sentences around citation markers
- **Bibliography Skipping**: Automatically skips the reference section when extracting citation contexts
- **Multi-occurrence Capture**: Captures all instances when a reference is cited multiple times

## Requirements

- Python 3.x
- `pypdf` library (`pip install pypdf`)
- Access to the PDF files to be processed
- reference_library.json for library integration

## Limitations

- May not work correctly with PDFs that have non-standard reference section formatting
- May require adjustment of the number of lines to extract based on the length of the reference section
- Encoding issues may affect extraction of special characters in some PDFs
- Citation context extraction relies on proper sentence boundary detection
