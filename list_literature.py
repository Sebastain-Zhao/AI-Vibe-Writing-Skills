#!/usr/bin/env python3
"""
List all files in the literature folder and save to a text file
"""
import os

LITERATURE_FOLDER = os.path.join(os.path.dirname(__file__), '文献')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '文献列表.txt')

def main():
    print(f"Listing files in: {LITERATURE_FOLDER}")
    
    # Get all files in the literature folder
    files = os.listdir(LITERATURE_FOLDER)
    
    # Filter for PDF files
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files:")
    for file in pdf_files:
        print(f"  - {file}")
    
    # Save to output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for file in pdf_files:
            f.write(file + '\n')
    
    print(f"\nSaved to: {OUTPUT_FILE}")
    print(f"Total files: {len(pdf_files)}")

if __name__ == "__main__":
    main()
