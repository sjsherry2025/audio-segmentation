# src/utils/file_utils.py

from pathlib import Path
from typing import List, Tuple

def get_file_count(input_dir: Path, supported_formats: Tuple[str, ...]) -> int:
    # 递归获取所有音频文件的数量
    audio_files = []
    for ext in supported_formats:
        audio_files.extend(input_dir.glob(f"**/*{ext}"))
        audio_files.extend(input_dir.glob(f"**/*{ext.upper()}"))
    return len(audio_files)

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

def rename_folder(old_path: Path, new_name: str) -> Path:
    # 修改文件夹名称
    new_path = old_path.parent / new_name
    old_path.rename(new_path)
    return new_path

def rename_file(old_path: Path, new_name: str) -> Path:
    # 修改文件名称
    new_path = old_path.parent / f"{new_name}{old_path.suffix}"
    old_path.rename(new_path)
    return new_path