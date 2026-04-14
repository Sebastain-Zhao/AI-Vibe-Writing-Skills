#!/usr/bin/env python3
"""
Extract Chinese writing style from Chinese literature in reference_library.json
"""
import json
import os
import re
from collections import Counter

REFERENCE_LIBRARY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'reference_library.json')
STYLE_PROFILE = os.path.join(os.path.dirname(__file__), '.ai_context', 'style_profile.md')

def load_json(file_path):
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_chinese_text(text):
    """Check if text contains Chinese characters"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    return bool(chinese_pattern.search(text))

def analyze_chinese_sentence_structure(texts):
    """Analyze Chinese sentence structure"""
    all_sentences = []
    for text in texts:
        sentences = re.split(r'[。！？；\n]+', text)
        all_sentences.extend([s.strip() for s in sentences if s.strip() and is_chinese_text(s)])
    
    if not all_sentences:
        return {}
    
    sentence_lengths = [len(s) for s in all_sentences]
    avg_length = sum(sentence_lengths) / len(sentence_lengths)
    
    short_sentences = sum(1 for l in sentence_lengths if l < 15)
    medium_sentences = sum(1 for l in sentence_lengths if 15 <= l <= 30)
    long_sentences = sum(1 for l in sentence_lengths if l > 30)
    
    total = len(sentence_lengths)
    
    passive_count = 0
    passive_patterns = [
        r'被.*?所',
        r'由.*?所',
        r'受到.*?的影响',
        r'得到.*?的处理'
    ]
    
    for sentence in all_sentences:
        for pattern in passive_patterns:
            if re.search(pattern, sentence):
                passive_count += 1
                break
    
    first_person_plural = 0
    first_person_patterns = [
        r'我们提出',
        r'我们实现',
        r'我们设计',
        r'我们研究',
        r'我们分析',
        r'我们演示',
        r'本文提出',
        r'本文实现',
        r'本文设计'
    ]
    
    for sentence in all_sentences:
        for pattern in first_person_patterns:
            if re.search(pattern, sentence):
                first_person_plural += 1
                break
    
    return {
        'avg_sentence_length': round(avg_length, 1),
        'short_sentence_ratio': round(short_sentences / total * 100, 1),
        'medium_sentence_ratio': round(medium_sentences / total * 100, 1),
        'long_sentence_ratio': round(long_sentences / total * 100, 1),
        'passive_voice_count': passive_count,
        'first_person_usage': first_person_plural,
        'total_sentences': total
    }

def analyze_chinese_vocabulary(texts):
    """Analyze Chinese vocabulary and expressions"""
    all_text = ' '.join(texts)
    
    hedging_patterns = [
        (r'结果表明', '结果表明'),
        (r'实验显示', '实验显示'),
        (r'数据提示', '数据提示'),
        (r'研究发现', '研究发现'),
        (r'我们认为', '我们认为'),
        (r'可以推测', '可以推测'),
        (r'可能的原因', '可能的原因'),
        (r'表明', '表明'),
        (r'显示', '显示'),
        (r'提示', '提示')
    ]
    
    hedging_freq = {}
    for pattern, name in hedging_patterns:
        count = len(re.findall(pattern, all_text))
        if count > 0:
            hedging_freq[name] = count
    
    transition_patterns = [
        (r'此外', '此外'),
        (r'另外', '另外'),
        (r'而且', '而且'),
        (r'再者', '再者'),
        (r'综上所述', '综上所述'),
        (r'因此', '因此'),
        (r'由此可见', '由此可见'),
        (r'基于上述', '基于上述')
    ]
    
    transition_freq = {}
    for pattern, name in transition_patterns:
        count = len(re.findall(pattern, all_text))
        if count > 0:
            transition_freq[name] = count
    
    ai_taste_patterns = [
        (r'深入探讨', '深入探讨'),
        (r'错综复杂', '错综复杂'),
        (r'见证', '见证'),
        (r'多维度的', '多维度的'),
        (r'助力', '助力'),
        (r'赋能', '赋能'),
        (r'底层逻辑', '底层逻辑'),
        (r'颗粒度', '颗粒度')
    ]
    
    ai_taste_freq = {}
    for pattern, name in ai_taste_patterns:
        count = len(re.findall(pattern, all_text))
        if count > 0:
            ai_taste_freq[name] = count
    
    academic_verbs = [
        (r'提出', '提出'),
        (r'实现', '实现'),
        (r'优化', '优化'),
        (r'演示', '演示'),
        (r'验证', '验证'),
        (r'分析', '分析'),
        (r'研究', '研究'),
        (r'设计', '设计'),
        (r'构建', '构建'),
        (r'提高', '提高'),
        (r'改善', '改善'),
        (r'降低', '降低')
    ]
    
    academic_freq = {}
    for pattern, name in academic_verbs:
        count = len(re.findall(pattern, all_text))
        if count > 0:
            academic_freq[name] = count
    
    return {
        'hedging_expressions': hedging_freq,
        'transition_words': transition_freq,
        'ai_taste_words': ai_taste_freq,
        'academic_verbs': academic_freq
    }

def analyze_chinese_technical_writing(texts):
    """Analyze Chinese technical writing patterns"""
    all_text = ' '.join(texts)
    
    number_patterns = re.findall(r'\d+\.?\d*\s*(?:dB|GHz|km|nm|Gb/s|Mb/s|THz)', all_text)
    
    formula_patterns = re.findall(r'如式\(\d+\)所示|根据式\(\d+\)|由式\(\d+\)可得', all_text)
    
    figure_patterns = re.findall(r'如图\d+所示|如表\d+所列|从图\d+可以看出', all_text)
    
    return {
        'number_with_units': len(number_patterns),
        'formula_references': len(formula_patterns),
        'figure_references': len(figure_patterns)
    }

def generate_chinese_style_profile(sentence_stats, vocab_stats, tech_stats):
    """Generate Chinese style profile"""
    
    profile = """## Core Style DNA (中文文献分析)
- **Tone**: 学术严谨、客观中立，使用hedging表达
- **Sentence Pattern**: """
    
    profile += f"平均句长{sentence_stats['avg_sentence_length']}字，"
    
    if sentence_stats['short_sentence_ratio'] > 50:
        profile += "偏好短句有力，"
    elif sentence_stats['long_sentence_ratio'] > 30:
        profile += "偏好长句展开，"
    else:
        profile += "长短句结合，节奏均衡，"
    
    profile += f"主动语态为主（被动句仅{sentence_stats['passive_voice_count']}例）"
    profile += "\n"
    
    profile += "\n## Do's (中文写作规范)\n"
    
    profile += "- 使用第一人称复数：我们提出/实现/设计/研究...\n"
    profile += "- 使用hedging表达避免绝对化：\n"
    
    if vocab_stats['hedging_expressions']:
        sorted_hedging = sorted(vocab_stats['hedging_expressions'].items(), key=lambda x: x[1], reverse=True)
        for expr, count in sorted_hedging[:5]:
            profile += f"  - {expr}（{count}次）\n"
    
    profile += "- 注入具体数值和技术参数\n"
    profile += "- 变换句式节奏，关键结论用短句强调\n"
    profile += "- 常用学术动词：\n"
    
    if vocab_stats['academic_verbs']:
        sorted_verbs = sorted(vocab_stats['academic_verbs'].items(), key=lambda x: x[1], reverse=True)
        for verb, count in sorted_verbs[:8]:
            profile += f"  - {verb}（{count}次）\n"
    
    profile += "\n## Don'ts (中文写作禁忌)\n"
    profile += "- 避免被动句式：被...所... / 由...所...\n"
    profile += "- 避免机械过渡词：\n"
    
    if vocab_stats['transition_words']:
        sorted_trans = sorted(vocab_stats['transition_words'].items(), key=lambda x: x[1], reverse=True)
        for word, count in sorted_trans[:5]:
            profile += f"  - {word}（{count}次）- 建议减少使用\n"
    
    profile += "- 避免AI味词汇：\n"
    
    if vocab_stats['ai_taste_words']:
        for word, count in vocab_stats['ai_taste_words'].items():
            profile += f"  - {word}（{count}次）\n"
    else:
        profile += "  - 深入探讨 / 错综复杂 / 见证 / 多维度的 / 助力 / 赋能\n"
    
    profile += "- 避免翻译腔：对于...来说 / 在...方面\n"
    profile += "- 避免绝对化结论：证明了 / 毫无疑问\n"
    
    profile += "\n## 中文写作统计\n"
    profile += f"- 平均句长：{sentence_stats['avg_sentence_length']}字\n"
    profile += f"- 短句比例（<15字）：{sentence_stats['short_sentence_ratio']}%\n"
    profile += f"- 中句比例（15-30字）：{sentence_stats['medium_sentence_ratio']}%\n"
    profile += f"- 长句比例（>30字）：{sentence_stats['long_sentence_ratio']}%\n"
    profile += f"- 第一人称使用：{sentence_stats['first_person_usage']}次\n"
    profile += f"- 被动句使用：{sentence_stats['passive_voice_count']}次\n"
    profile += f"- 技术参数引用：{tech_stats['number_with_units']}次\n"
    profile += f"- 公式引用：{tech_stats['formula_references']}次\n"
    profile += f"- 图表引用：{tech_stats['figure_references']}次\n"
    
    return profile

def main():
    """Main function"""
    print("加载文献库...")
    reference_library = load_json(REFERENCE_LIBRARY)
    
    chinese_texts = []
    for source in reference_library['sources']:
        if 'extracted_text' in source:
            text = source['extracted_text']
            if is_chinese_text(text):
                chinese_texts.append(text)
                print(f"  发现中文文献: {source['title']}")
    
    if not chinese_texts:
        print("未找到中文文献！")
        return
    
    print(f"\n分析{len(chinese_texts)}篇中文文献...")
    
    print("分析句式结构...")
    sentence_stats = analyze_chinese_sentence_structure(chinese_texts)
    
    print("分析词汇表达...")
    vocab_stats = analyze_chinese_vocabulary(chinese_texts)
    
    print("分析技术写作...")
    tech_stats = analyze_chinese_technical_writing(chinese_texts)
    
    print("生成风格档案...")
    profile = generate_chinese_style_profile(sentence_stats, vocab_stats, tech_stats)
    
    with open(STYLE_PROFILE, 'w', encoding='utf-8') as f:
        f.write(profile)
    
    print(f"\n风格档案已保存到 {STYLE_PROFILE}")
    print("\n=== 中文写作风格档案 ===")
    print(profile)

if __name__ == "__main__":
    main()
