#!/usr/bin/env python3
"""
Add user's own paper to reference library with highest priority
"""
import json
import os
from datetime import datetime

REFERENCE_LIBRARY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'reference_library.json')
HARD_MEMORY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'hard_memory.json')
SOFT_MEMORY = os.path.join(os.path.dirname(__file__), '.ai_context', 'memory', 'soft_memory.json')

def load_json(file_path):
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    """Save JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_user_paper():
    """Add user's paper with highest priority"""
    
    print("=" * 60)
    print("添加用户论文到文献库（最高优先级）")
    print("=" * 60)
    
    reference_library = load_json(REFERENCE_LIBRARY)
    hard_memory = load_json(HARD_MEMORY)
    soft_memory = load_json(SOFT_MEMORY)
    
    user_paper = {
        "id": "USER_PAPER_DP_ODB_PON",
        "title": "抗色散双偏振双二进制直接检测PON系统研究",
        "file_path": "D:\\AAAAAAAA\\AI-Vibe-Writing-Skills-main\\文献\\中国激光v1.pdf",
        "priority": "HIGHEST",
        "is_user_work": True,
        "authors": ["张兆璐", "李政轩", "罗思宇", "宋英雄"],
        "institution": "上海大学特种光纤与光接入网重点实验室",
        "journal": "中国激光",
        "year": 2024,
        "abstract": "本文提出了一种双偏振双二进制系统，能够缓解直接检测PON中的码间串扰与非线性失真。通过将复杂度转移至发射端，本方案实现了算法资源需求较低的简单直接检测接收机，并确保与现有ONU的兼容性。与PAM4相比，DP-ODB格式在高SNR下表现相当，但在低SNR场景下，尤其是高累积色散条件下对码间串扰鲁棒性显著更强。实验验证了在42.5 ps/nm累积色散处达到-23 dBm的接收灵敏度，在170 ps/nm处达到-19 dBm。此外，本文测试了对SBS的容忍度，最后得出当发射功率超过10 dBm时，分别实现了33 dB和29 dB的功率预算，证实了该方案在PON系统中的可行性。",
        "keywords": ["无源光网络", "双二进制", "偏振复用", "光纤非线性", "色散容忍度"],
        "core_contributions": [
            "提出双偏振双二进制（DP-ODB）传输架构",
            "实现40 GBaud信号传输，扩展至50 GBaud验证",
            "在42.5 ps/nm累积色散下达到-23 dBm接收灵敏度",
            "在170 ps/nm累积色散下达到-19 dBm接收灵敏度",
            "SBS容忍度从7 dBm提升至16 dBm（提升9 dB）",
            "实现33 dB和29 dB的功率预算",
            "接收机复杂度显著降低（无需Volterra均衡器）"
        ],
        "key_results": {
            "dispersion_tolerance": {
                "PAM4_limit": "127.5 ps/nm",
                "DP-ODB_limit": "170 ps/nm",
                "improvement": "提升33%"
            },
            "receiver_sensitivity": {
                "optimal_point": "-23 dBm @ 42.5 ps/nm",
                "high_dispersion": "-19 dBm @ 170 ps/nm",
                "vs_PAM4": "3 dB优势"
            },
            "SBS_threshold": {
                "PAM4": "7 dBm",
                "DP-ODB": "16 dBm",
                "improvement": "9 dB提升"
            },
            "power_budget": {
                "optimal": "33 dB",
                "high_dispersion": "29 dB",
                "standard": "超过GPON Class C+ (32 dB)"
            },
            "equalizer_complexity": {
                "PAM4": "FFE-25/DFE-1/Vol-3",
                "DP-ODB": "FFE-25/DFE-3/Vol-0",
                "advantage": "无需非线性Volterra项"
            }
        },
        "technical_innovation": [
            "双偏振架构：功率分配2:1，避免相干接收机复杂度",
            "ODB调制：抑制光载波，提高SBS阈值",
            "预编码与π相位交替：实现符号间干扰的相消作用",
            "直接检测：平方律检测实现四电平强度信号"
        ],
        "experimental_setup": {
            "transmitter": {
                "AWG": "176 mV输出",
                "amplifier": "驱动放大",
                "modulator": "25 GHz双驱动MZM，偏置在零点"
            },
            "polarization": {
                "delay": "20符号延时",
                "power_ratio": "2:1（水平:垂直）",
                "combiner": "偏振合束器"
            },
            "receiver": {
                "preamplifier": "EDFA",
                "detector": "35 GHz PIN光电二极管",
                "detection": "直接检测（平方律）"
            }
        },
        "domain": "Optical Communication",
        "subdomain": "PON / Direct Detection / Duobinary Modulation",
        "citation_priority": "HIGHEST",
        "notes": "用户本人的研究工作，大论文基础，应优先引用",
        "added_date": datetime.now().isoformat()
    }
    
    if 'user_papers' not in reference_library:
        reference_library['user_papers'] = []
    
    existing_ids = [p['id'] for p in reference_library['user_papers']]
    if user_paper['id'] not in existing_ids:
        reference_library['user_papers'].append(user_paper)
        print(f"✓ 已添加用户论文: {user_paper['title']}")
    else:
        for i, p in enumerate(reference_library['user_papers']):
            if p['id'] == user_paper['id']:
                reference_library['user_papers'][i] = user_paper
                print(f"✓ 已更新用户论文: {user_paper['title']}")
                break
    
    if 'user_research' not in hard_memory:
        hard_memory['user_research'] = {}
    
    hard_memory['user_research']['primary_paper'] = {
        "title": user_paper['title'],
        "id": user_paper['id'],
        "priority": "HIGHEST",
        "core_technology": "Dual-Polarization Optical Duobinary (DP-ODB)",
        "key_achievements": [
            "40 GBaud DP-ODB传输系统",
            "接收灵敏度: -23 dBm @ 42.5 ps/nm",
            "色散容忍度: 170 ps/nm",
            "SBS阈值提升: 9 dB",
            "功率预算: 33 dB"
        ],
        "application_scenario": "PON下行链路，100 Gbps单波长传输"
    }
    
    hard_memory['user_research']['key_parameters'] = {
        "baud_rate": "40 GBaud (扩展至50 GBaud)",
        "dispersion_tolerance": "170 ps/nm",
        "receiver_sensitivity_optimal": "-23 dBm",
        "receiver_sensitivity_high_disp": "-19 dBm",
        "SBS_threshold": "16 dBm",
        "power_budget_optimal": "33 dB",
        "power_budget_high_disp": "29 dB",
        "polarization_ratio": "2:1",
        "equalizer_config": "FFE-25/DFE-3"
    }
    
    if 'user_work' not in soft_memory:
        soft_memory['user_work'] = {}
    
    soft_memory['user_work']['primary_research'] = {
        "title": user_paper['title'],
        "priority": "HIGHEST",
        "is_basis_for_thesis": True,
        "research_focus": [
            "双偏振双二进制调制",
            "直接检测PON系统",
            "色散容忍度提升",
            "非线性效应抑制",
            "功率预算优化"
        ],
        "writing_style_preference": "基于此论文的写作风格应作为主要参考",
        "citation_instruction": "在相关主题写作中应优先引用此研究成果"
    }
    
    save_json(reference_library, REFERENCE_LIBRARY)
    save_json(hard_memory, HARD_MEMORY)
    save_json(soft_memory, SOFT_MEMORY)
    
    print("\n" + "=" * 60)
    print("✓ 用户论文已成功添加到文献库（最高优先级）")
    print("=" * 60)
    print(f"\n论文标题: {user_paper['title']}")
    print(f"作者: {', '.join(user_paper['authors'])}")
    print(f"期刊: {user_paper['journal']}")
    print(f"年份: {user_paper['year']}")
    print(f"\n核心贡献:")
    for i, contribution in enumerate(user_paper['core_contributions'], 1):
        print(f"  {i}. {contribution}")
    print(f"\n关键结果:")
    print(f"  - 色散容忍度: {user_paper['key_results']['dispersion_tolerance']['DP-ODB_limit']}")
    print(f"  - 接收灵敏度: {user_paper['key_results']['receiver_sensitivity']['optimal_point']}")
    print(f"  - SBS阈值: {user_paper['key_results']['SBS_threshold']['DP-ODB']}")
    print(f"  - 功率预算: {user_paper['key_results']['power_budget']['optimal']}")
    print(f"\n✓ 已标记为最高优先级，将在写作中优先引用")
    print("=" * 60)

if __name__ == "__main__":
    add_user_paper()
