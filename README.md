<div align="center">

# 🎵 音频智能切割工具

## 基于 Silero VAD 的语音活动检测与智能分割

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.12+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## 📖 项目简介

本项目是一个基于 **Silero VAD (Voice Activity Detection)** 技术的专业音频预处理工具。它能将任意时长的原始音频文件（如录音、讲座、访谈）自动切割成 **3-10 秒**、语句完整的短音频片段。切割后的音频非常适合用于训练 **TTS（文本转语音）模型**，如 **Index-TTS、GPT-SoVITS、Fish-Speech** 等。

---

## ✨ 功能特点

- 🎯 **智能语音检测**：基于 Silero VAD 高精度识别语音片段
- ⏱️ **时长可控**：自动将切割片段控制在 3-10 秒范围内
- 📝 **语句完整性**：优先在静音间隙切割，保证语句语义完整
- 📁 **批量处理**：支持单/多文件/多层级下的文件批量处理
- 🔊 **音量统一归一化**：内置RMS/峰值归一化，确保输出音频响度一致

---

## 🖼️ 界面预览

<div align="center">
  <img width="100%" alt="image" src="https://github.com/user-attachments/assets/f42c7e5c-50fa-4dfa-a5aa-68435296e649" />
</div>

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本 |
|------|------|
| Python | >= 3.10 |
| PyTorch | >= 1.12.0 |
| Silero VAD | >= 0.1.0 |
| SoundFile | >= 0.10.0 |
| Librosa | >= 0.9.0 |

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/sjsherry2025/audio-segmentation.git
cd audio-segmentation

# 2. 创建虚拟环境（推荐）
conda create -n audio-segmentation python=3.10
conda activate audio-segmentation

# 3. 安装依赖
pip install -r requirements.txt
