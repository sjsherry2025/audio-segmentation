# src/utils/file_utils.py

from pathlib import Path
from typing import List, Tuple

def get_audio_files(input_dir: Path, supported_formats: Tuple[str, ...]) -> List[Path]:
    # 递归获取所有音频文件
    audio_files = []
    for ext in supported_formats:
        # 使用 **/* 递归匹配所有子文件夹
        audio_files.extend(input_dir.glob(f"**/*{ext}"))
        audio_files.extend(input_dir.glob(f"**/*{ext.upper()}"))
    return audio_files


def get_unique_files(audio_files: List[Path]) -> List[Path]:
    # 文件去重
    unique = {}
    for f in audio_files:
        unique[f.name.lower()] = f
    return sorted(unique.values())