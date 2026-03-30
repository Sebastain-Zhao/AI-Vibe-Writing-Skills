#!/usr/bin/env python3
"""
Process all PDF files in the literature folder and store them in reference_library.json
"""
import os
import json
import re
import sys

# Add the scripts directory to the path
script_dir = os.path.join(os.path.dirname(__file__), '.ai_context', 'scripts')
sys.path.append(script_dir)

from parse_pdf import extract_text_from_pdf

LITERATURE_FOLDER = os.path.join(os.path.dirname(__file__), '文献')
REFERENCE_LIBRARY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'reference_library.json')
HARD_MEMORY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'hard_memory.json')
SOFT_MEMORY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'soft_memory.json')

def load_json(file_path):
    """Load JSON file"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(data, file_path):
    """Save JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_metadata_from_filename(filename):
    """Extract metadata from filename"""
    # Extract citation number and title
    match = re.match(r'\[(\d+)\](.+?)\.pdf', filename)
    if match:
        citation_number = match.group(1)
        title = match.group(2).strip()
        # Replace underscores with spaces
        title = title.replace('_', ' ')
        return {
            'citation_number': citation_number,
            'title': title
        }
    return {
        'title': os.path.splitext(filename)[0]
    }

def extract_key_information(text):
    """Extract key information from PDF text"""
    lines = text.split('\n')
    
    # Find abstract
    abstract_start = -1
    abstract_end = -1
    for i, line in enumerate(lines):
        if re.search(r'\babstract\b', line, re.IGNORECASE):
            abstract_start = i + 1
        elif abstract_start != -1 and (re.search(r'\bintroduction\b|\brelated work\b', line, re.IGNORECASE) or i > abstract_start + 50):
            abstract_end = i
            break
    
    abstract = ''
    if abstract_start != -1 and abstract_end != -1:
        abstract = ' '.join(lines[abstract_start:abstract_end]).strip()
    
    # Extract key terms (simplified)
    key_terms = []
    # Look for keywords section
    for i, line in enumerate(lines):
        if re.search(r'\bkeywords?\b', line, re.IGNORECASE):
            keywords_line = ' '.join(lines[i:i+5])
            terms = re.findall(r'\b\w+\b', keywords_line.lower())
            # Filter common words
            common_words = set(['and', 'or', 'the', 'of', 'in', 'for', 'with', 'on', 'by', 'at'])
            key_terms = [term for term in terms if term not in common_words and len(term) > 3][:10]
            break
    
    return {
        'abstract': abstract,
        'key_terms': key_terms
    }

def process_pdf_file(pdf_path):
    """Process a single PDF file"""
    print(f"Processing: {os.path.basename(pdf_path)}")
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Extract metadata from filename
    metadata = extract_metadata_from_filename(os.path.basename(pdf_path))
    
    # Extract key information from text
    key_info = extract_key_information(text)
    
    # Create source entry
    source = {
        'id': f"paper_{metadata.get('citation_number', 'unknown')}",
        'title': metadata['title'],
        'file_path': pdf_path,
        'abstract': key_info['abstract'],
        'key_terms': key_info['key_terms'],
        'domain': 'Optical Communication',  # Based on file names
        'year': 2024,  # Default year, can be extracted from text later
        'extracted_text': text[:5000]  # Store first 5000 chars to keep file size manageable
    }
    
    return source

def main():
    """Main function"""
    # Load existing data
    reference_library = load_json(REFERENCE_LIBRARY)
    hard_memory = load_json(HARD_MEMORY)
    soft_memory = load_json(SOFT_MEMORY)
    
    # Initialize if empty
    if 'sources' not in reference_library:
        reference_library['sources'] = []
    if 'index' not in reference_library:
        reference_library['index'] = {
            'by_domain': {},
            'by_tag': {},
            'by_year': {}
        }
    
    # Process all PDF files in the literature folder
    pdf_files = [f for f in os.listdir(LITERATURE_FOLDER) if f.lower().endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files in {LITERATURE_FOLDER}")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(LITERATURE_FOLDER, pdf_file)
        source = process_pdf_file(pdf_path)
        
        # Add to reference library
        reference_library['sources'].append(source)
        
        # Update index
        domain = source['domain']
        if domain not in reference_library['index']['by_domain']:
            reference_library['index']['by_domain'][domain] = []
        reference_library['index']['by_domain'][domain].append(source['id'])
        
        year = source['year']
        if year not in reference_library['index']['by_year']:
            reference_library['index']['by_year'][year] = []
        reference_library['index']['by_year'][year].append(source['id'])
        
        # Add key terms to tags index
        for term in source['key_terms']:
            if term not in reference_library['index']['by_tag']:
                reference_library['index']['by_tag'][term] = []
            reference_library['index']['by_tag'][term].append(source['id'])
        
        # Update hard memory with domain knowledge
        if 'Optical Communication' not in hard_memory:
            hard_memory['Optical Communication'] = {
                'terminology': set(),
                'facts': []
            }
        
        # Add key terms to terminology
        for term in source['key_terms']:
            hard_memory['Optical Communication']['terminology'].add(term)
        
        # Add abstract as a fact
        if source['abstract']:
            hard_memory['Optical Communication']['facts'].append({
                'source': source['id'],
                'content': source['abstract']
            })
    
    # Convert sets to lists for JSON serialization
    if 'Optical Communication' in hard_memory:
        hard_memory['Optical Communication']['terminology'] = list(hard_memory['Optical Communication']['terminology'])
    
    # Update soft memory with preferences
    if 'writing_style' not in soft_memory:
        soft_memory['writing_style'] = {}
    soft_memory['writing_style']['preferred_domains'] = ['Optical Communication']
    
    # Save updated data
    save_json(reference_library, REFERENCE_LIBRARY)
    save_json(hard_memory, HARD_MEMORY)
    save_json(soft_memory, SOFT_MEMORY)
    
    print(f"\nProcessing complete!")
    print(f"Added {len(pdf_files)} sources to reference_library.json")
    print(f"Updated hard_memory.json with domain knowledge")
    print(f"Updated soft_memory.json with preferences")

if __name__ == "__main__":
    main()
