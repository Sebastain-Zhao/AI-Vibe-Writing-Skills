#!/usr/bin/env python3
"""
Extract writing style from literature in reference_library.json
"""
import json
import os
import re
from collections import Counter
import string

REFERENCE_LIBRARY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'reference_library.json')
STYLE_PROFILE = os.path.join(os.path.dirname(__file__), '.ai_context', 'style_profile.md')

def load_json(file_path):
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_sentence_structure(texts):
    """Analyze sentence structure"""
    all_sentences = []
    for text in texts:
        sentences = re.split(r'[.!?]+', text)
        all_sentences.extend([s.strip() for s in sentences if s.strip()])
    
    if not all_sentences:
        return {}
    
    sentence_lengths = [len(s.split()) for s in all_sentences]
    avg_length = sum(sentence_lengths) / len(sentence_lengths)
    
    short_sentences = sum(1 for l in sentence_lengths if l < 15)
    medium_sentences = sum(1 for l in sentence_lengths if 15 <= l <= 30)
    long_sentences = sum(1 for l in sentence_lengths if l > 30)
    
    total = len(sentence_lengths)
    
    passive_count = 0
    active_count = 0
    passive_patterns = [
        r'\b(is|are|was|were|been|being)\s+\w+ed\b',
        r'\b(has|have|had)\s+been\s+\w+ed\b'
    ]
    
    for sentence in all_sentences:
        for pattern in passive_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                passive_count += 1
                break
        else:
            if re.search(r'\b\w+s\b.*\b\w+\b', sentence):
                active_count += 1
    
    transition_words = []
    transition_patterns = [
        r'\b(Therefore|Thus|Hence|Consequently|Moreover|Furthermore|Additionally|However|Nevertheless|Notably|Interestingly|Conversely|Similarly|In contrast|In conclusion|In summary)\b'
    ]
    
    for sentence in all_sentences:
        for pattern in transition_patterns:
            matches = re.findall(pattern, sentence, re.IGNORECASE)
            transition_words.extend(matches)
    
    transition_freq = Counter(transition_words).most_common(10)
    
    return {
        'avg_sentence_length': round(avg_length, 1),
        'short_sentence_ratio': round(short_sentences / total * 100, 1),
        'medium_sentence_ratio': round(medium_sentences / total * 100, 1),
        'long_sentence_ratio': round(long_sentences / total * 100, 1),
        'passive_voice_count': passive_count,
        'active_voice_count': active_count,
        'common_transitions': transition_freq
    }

def analyze_vocabulary_tone(texts):
    """Analyze vocabulary and tone"""
    all_text = ' '.join(texts)
    words = re.findall(r'\b[a-zA-Z]+\b', all_text.lower())
    
    word_freq = Counter(words)
    
    academic_words = []
    academic_pattern = r'\b(optimization|performance|demonstration|experimental|significantly|respectively|indicate|achieve|propose|investigate|analyze|implement|demonstrate|evaluate|enhance|improve|utilize|employ|introduce|present|suggest)\b'
    
    for match in re.finditer(academic_pattern, all_text, re.IGNORECASE):
        academic_words.append(match.group(0).lower())
    
    academic_freq = Counter(academic_words).most_common(15)
    
    ai_taste_words = []
    ai_pattern = r'\b(delve|tapestry|testament|multifaceted|fosters|leverage|ecosystem|orthogonal|paramount|crucial|revolutionary|vital|utilize|employ)\b'
    
    for match in re.finditer(ai_pattern, all_text, re.IGNORECASE):
        ai_taste_words.append(match.group(0).lower())
    
    ai_freq = Counter(ai_taste_words).most_common(10)
    
    hedging_words = []
    hedging_pattern = r'\b(suggest|indicate|demonstrate|show|reveal|imply|may|might|could|would|appear|seem|likely|potential|possibly)\b'
    
    for match in re.finditer(hedging_pattern, all_text, re.IGNORECASE):
        hedging_words.append(match.group(0).lower())
    
    hedging_freq = Counter(hedging_words).most_common(10)
    
    return {
        'total_words': len(words),
        'unique_words': len(set(words)),
        'academic_words': academic_freq,
        'ai_taste_words': ai_freq,
        'hedging_words': hedging_freq
    }

def analyze_micro_habits(texts):
    """Analyze micro-habits"""
    all_text = ' '.join(texts)
    
    citation_patterns = re.findall(r'\[\d+\]', all_text)
    citation_count = len(citation_patterns)
    
    semicolon_count = all_text.count(';')
    dash_count = all_text.count('—') + all_text.count('-')
    colon_count = all_text.count(':')
    
    first_person_plural = len(re.findall(r'\bwe\b', all_text, re.IGNORECASE))
    first_person_singular = len(re.findall(r'\bI\b', all_text))
    passive_voice = len(re.findall(r'\b(is|are|was|were|been|being)\s+\w+ed\b', all_text, re.IGNORECASE))
    
    return {
        'citation_count': citation_count,
        'semicolon_count': semicolon_count,
        'dash_count': dash_count,
        'colon_count': colon_count,
        'first_person_plural': first_person_plural,
        'first_person_singular': first_person_singular,
        'passive_voice_instances': passive_voice
    }

def generate_style_profile(sentence_stats, vocab_stats, micro_stats):
    """Generate style profile markdown"""
    
    tone = "学术严谨、客观中立"
    if vocab_stats['hedging_words']:
        tone += "，使用hedging表达（如suggest, indicate, demonstrate等）"
    
    sentence_pattern = f"平均句长{sentence_stats['avg_sentence_length']}词，"
    if sentence_stats['short_sentence_ratio'] > sentence_stats['long_sentence_ratio']:
        sentence_pattern += "偏好短句有力，"
    elif sentence_stats['long_sentence_ratio'] > sentence_stats['short_sentence_ratio']:
        sentence_pattern += "偏好长句展开复杂论述，"
    else:
        sentence_pattern += "长短句结合，节奏均衡，"
    
    if sentence_stats['passive_voice_count'] > sentence_stats['active_voice_count']:
        sentence_pattern += "被动语态使用较多"
    else:
        sentence_pattern += "主动语态为主"
    
    dos = []
    dos.append("使用第一人称复数 \"We proposed...\" 或 \"We demonstrate...\"")
    dos.append("使用学术性hedging表达：These findings suggest / The data indicates / The results demonstrate")
    dos.append("注入具体性：数字、方法约束与变量范围（如 0.8 dB, 31.4 dB）")
    dos.append("变换句式节奏：关键结论用短句强调，复杂论述用长句展开")
    dos.append("使用具体的技术术语而非泛泛而谈")
    
    if vocab_stats['academic_words']:
        top_academic = [word for word, count in vocab_stats['academic_words'][:5]]
        dos.append(f"常用学术动词：{', '.join(top_academic)}")
    
    donts = []
    donts.append("段首机械过渡词：Furthermore / Moreover / Additionally / In conclusion")
    donts.append("夸张形容词与副词：paramount / crucial / revolutionary / vital")
    donts.append("绝对化结论：This proves that...")
    donts.append("僵尸名词泛滥（-tion/-ment/-ance 名词化，例：perform an evaluation of）")
    donts.append("领域外隐喻/行话：orthogonal / leverage / ecosystem 等非本域用语")
    donts.append("高频 AI 味词：delve / tapestry / testament / multifaceted / fosters / in summary / to summarize")
    
    if vocab_stats['ai_taste_words']:
        ai_words = [word for word, count in vocab_stats['ai_taste_words']]
        if ai_words:
            donts.append(f"避免使用AI味词汇：{', '.join(ai_words[:5])}")
    
    profile = f"""## Core Style DNA
- **Tone**: {tone}
- **Sentence Pattern**: {sentence_pattern}

## Do's (我要的风格)
"""
    for do in dos:
        profile += f"- {do}\n"
    
    profile += "\n## Don'ts (我不要的风格)\n"
    for dont in donts:
        profile += f"- {dont}\n"
    
    return profile

def main():
    """Main function"""
    print("Loading reference library...")
    reference_library = load_json(REFERENCE_LIBRARY)
    
    texts = []
    for source in reference_library['sources']:
        if 'extracted_text' in source:
            texts.append(source['extracted_text'])
    
    print(f"Analyzing {len(texts)} documents...")
    
    print("Analyzing sentence structure...")
    sentence_stats = analyze_sentence_structure(texts)
    
    print("Analyzing vocabulary and tone...")
    vocab_stats = analyze_vocabulary_tone(texts)
    
    print("Analyzing micro-habits...")
    micro_stats = analyze_micro_habits(texts)
    
    print("Generating style profile...")
    profile = generate_style_profile(sentence_stats, vocab_stats, micro_stats)
    
    with open(STYLE_PROFILE, 'w', encoding='utf-8') as f:
        f.write(profile)
    
    print(f"\nStyle profile saved to {STYLE_PROFILE}")
    print("\n=== Style Profile ===")
    print(profile)
    
    print("\n=== Statistics ===")
    print(f"Sentence Structure: {sentence_stats}")
    print(f"\nTop Academic Words: {vocab_stats['academic_words'][:10]}")
    print(f"\nAI-taste Words Found: {vocab_stats['ai_taste_words']}")
    print(f"\nMicro-habits: {micro_stats}")

if __name__ == "__main__":
    main()
