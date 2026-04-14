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

def clean_unicode(text):
    """Clean invalid Unicode characters from text"""
    if isinstance(text, str):
        return text.encode('utf-8', errors='ignore').decode('utf-8')
    return text

def clean_data(obj):
    """Recursively clean all strings in a data structure"""
    if isinstance(obj, dict):
        return {k: clean_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_data(item) for item in obj]
    elif isinstance(obj, str):
        return clean_unicode(obj)
    else:
        return obj

def save_json(data, file_path):
    """Save JSON file with Unicode cleaning"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    cleaned_data = clean_data(data)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

def extract_metadata_from_filename(filename):
    """Extract metadata from filename"""
    # Extract title without numbers
    match = re.match(r'\[\d+\](.+?)\.pdf', filename)
    if match:
        title = match.group(1).strip()
    else:
        title = os.path.splitext(filename)[0]
    # Replace underscores with spaces
    title = title.replace('_', ' ')
    # Get clean filename without extension for ID
    clean_filename = os.path.splitext(filename)[0]
    return {
        'title': title,
        'clean_filename': clean_filename
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
        'id': metadata['clean_filename'],
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
    
    # Remove duplicates from existing data
    existing_ids = set()
    unique_sources = []
    for source in reference_library['sources']:
        if source['id'] not in existing_ids:
            existing_ids.add(source['id'])
            unique_sources.append(source)
    reference_library['sources'] = unique_sources
    
    # Clean up index
    reference_library['index'] = {
        'by_domain': {},
        'by_tag': {},
        'by_year': {}
    }
    for source in reference_library['sources']:
        domain = source['domain']
        if domain not in reference_library['index']['by_domain']:
            reference_library['index']['by_domain'][domain] = []
        reference_library['index']['by_domain'][domain].append(source['id'])
        
        year = source['year']
        if year not in reference_library['index']['by_year']:
            reference_library['index']['by_year'][year] = []
        reference_library['index']['by_year'][year].append(source['id'])
        
        for term in source['key_terms']:
            if term not in reference_library['index']['by_tag']:
                reference_library['index']['by_tag'][term] = []
            reference_library['index']['by_tag'][term].append(source['id'])
    
    # Process all PDF files in the literature folder
    pdf_files = [f for f in os.listdir(LITERATURE_FOLDER) if f.lower().endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files in {LITERATURE_FOLDER}")
    
    added_count = 0
    # Create a map of existing sources by ID for easy lookup
    existing_sources_map = {source['id']: source for source in reference_library['sources']}
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(LITERATURE_FOLDER, pdf_file)
        source = process_pdf_file(pdf_path)
        
        # Check if already exists
        if source['id'] in existing_ids:
            print(f"  Already exists, updating: {source['title']}")
            # Preserve existing references and citation_contexts
            existing_source = existing_sources_map.get(source['id'], {})
            if 'references' in existing_source:
                source['references'] = existing_source['references']
            if 'citation_contexts' in existing_source:
                source['citation_contexts'] = existing_source['citation_contexts']
            # Replace the old source with the new one
            for i, s in enumerate(reference_library['sources']):
                if s['id'] == source['id']:
                    reference_library['sources'][i] = source
                    break
            continue
        
        # Add to reference library
        reference_library['sources'].append(source)
        existing_ids.add(source['id'])
        added_count += 1
        
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
    
    # Rebuild hard memory from scratch
    hard_memory = load_json(HARD_MEMORY)
    if 'Optical Communication' not in hard_memory:
        hard_memory['Optical Communication'] = {
            'terminology': [],
            'facts': []
        }
    
    # Collect unique terminology and facts
    terminology_set = set()
    facts_dict = {}
    for source in reference_library['sources']:
        for term in source['key_terms']:
            terminology_set.add(term)
        if source['abstract']:
            facts_dict[source['id']] = {
                'source': source['id'],
                'content': source['abstract']
            }
    
    hard_memory['Optical Communication']['terminology'] = list(terminology_set)
    hard_memory['Optical Communication']['facts'] = list(facts_dict.values())
    
    # Update soft memory with preferences
    if 'writing_style' not in soft_memory:
        soft_memory['writing_style'] = {}
    soft_memory['writing_style']['preferred_domains'] = ['Optical Communication']
    
    # Save updated data
    save_json(reference_library, REFERENCE_LIBRARY)
    save_json(hard_memory, HARD_MEMORY)
    save_json(soft_memory, SOFT_MEMORY)
    
    print(f"\nProcessing complete!")
    print(f"Added {added_count} new sources to reference_library.json")
    print(f"Total sources: {len(reference_library['sources'])}")
    print(f"Updated hard_memory.json with domain knowledge")
    print(f"Updated soft_memory.json with preferences")

if __name__ == "__main__":
    main()
