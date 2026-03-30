# 文献元数据文件夹

本文件夹包含从文献中提取和整理的元数据信息。

## 文件说明

### 1. 文献元数据.md
第一篇PDF的前10篇参考文献搜索结果，包含：
- 论文标题、作者、年份
- 摘要信息
- 可用链接
- 研究领域

### 2. 文献元数据.json
第一篇PDF文献元数据的JSON格式版本，便于程序处理。

### 3. 第二篇PDF期刊论文列表.md
第二篇PDF的期刊论文整理（排除会议论文），包含：
- 23篇期刊论文详细信息
- 期刊名称、卷期、页码、日期
- 搜索平台指南
- 期刊分布统计

### 4. parse_references.py
参考文献解析脚本（临时文件）

## 来源PDF

### 第一篇PDF
- **标题**: Convolutional Neural Network based Nonlinear Classifier.pdf
- **参考文献数**: 13篇
- **搜索范围**: 前10篇

### 第二篇PDF
- **标题**: End-to-End_Learning_for_100G-PON_Based_on_Noise_Adaptation_Network.pdf
- **总参考文献数**: 34篇
- **排除会议论文**: 11篇
- **保留期刊论文**: 23篇

## 主要期刊分布

| 期刊 | 数量 |
|------|------|
| Journal of Lightwave Technology (JLT) | 9篇 |
| Journal of Optical Communications and Networking (JOCN) | 3篇 |
| 其他期刊 | 11篇 |

## 搜索平台指南

| 平台 | 网址 | 可搜索期刊 |
|------|------|-----------|
| IEEE Xplore | https://ieeexplore.ieee.org | JLT、IEEE系列期刊 |
| Optica Publishing Group | https://opg.optica.org | JOCN、Optics Letters、Optics Express |
| ScienceDirect | https://www.sciencedirect.com | Neural Networks等 |
| MDPI | https://www.mdpi.com | Micromachines |

---

*生成时间: 2026-03-30*
