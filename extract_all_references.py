#!/usr/bin/env python3
"""
Extract references from all PDF files in the literature folder
"""
import os
import sys

# Add the scripts directory to the path
script_dir = os.path.join(os.path.dirname(__file__), '.ai_context', 'scripts')
sys.path.append(script_dir)

from parse_pdf import extract_text_from_pdf

LITERATURE_FOLDER = os.path.join(os.path.dirname(__file__), '文献')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '所有参考文献.txt')

def extract_references_from_pdf(pdf_path):
    """Extract references from a single PDF file"""
    print(f"Processing: {os.path.basename(pdf_path)}")
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Split text into lines
    lines = text.split('\n')
    
    # Find reference section using multiple methods
    reference_start = -1
    
    # Method 1: Look for REFERENCES or BIBLIOGRAPHY section
    for i, line in enumerate(lines):
        line_upper = line.upper()
        if 'REFERENCES' in line_upper or 'BIBLIOGRAPHY' in line_upper:
            reference_start = i
            break
    
    # Method 2: If not found, look for the last page which often contains references
    if reference_start == -1:
        # Take the last 500 lines (assuming references are at the end)
        last_lines = lines[-500:]
        for i, line in enumerate(last_lines):
            # Look for numbered references
            if line.strip().startswith('[') and ']' in line:
                # Found references, start from here
                reference_start = len(lines) - 500 + i
                break
    
    # Extract references
    references = []
    if reference_start != -1:
        # Start from the reference section and collect until the end
        collecting = False
        for line in lines[reference_start:]:
            # Start collecting when we find the first reference
            if not collecting and (line.strip().startswith('[') and ']' in line):
                collecting = True
            
            if collecting:
                references.append(line)
                
                # Stop if we encounter a new section (not a reference)
                if len(line.strip()) > 0 and not line.strip().startswith('[') and not any(char.isdigit() for char in line.strip()):
                    # Check if this is likely a new section
                    if len(line.strip()) < 30 and line.strip().isupper():
                        break
    
    # If still no references found, try to find any line with [number]
    if not references:
        for i, line in enumerate(lines):
            if line.strip().startswith('[') and ']' in line:
                # Found a reference, collect from here
                references = lines[i:i+100]  # Collect next 100 lines
                break
    
    return references

def main():
    print(f"Extracting references from PDF files in: {LITERATURE_FOLDER}")
    
    # Get all PDF files in the literature folder
    pdf_files = [f for f in os.listdir(LITERATURE_FOLDER) if f.lower().endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Extract references from each PDF
    all_references = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(LITERATURE_FOLDER, pdf_file)
        references = extract_references_from_pdf(pdf_path)
        
        if references:
            all_references.append(f"\n=== {pdf_file} ===")
            all_references.extend(references[:200])  # Limit to first 200 lines to avoid excessive output
        else:
            all_references.append(f"\n=== {pdf_file} ===")
            all_references.append("No references found")
    
    # Save all references to output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_references))
    
    print(f"\nExtraction complete!")
    print(f"Saved all references to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
