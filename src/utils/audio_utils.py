import torch
import torchaudio
from pathlib import Path
from typing import Dict, Any
from typing import List, Tuple
from silero_vad import get_speech_timestamps
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def get_audio_duration(audio: torch.Tensor, sr: int) -> float:
    # 获取音频时长（秒） =  采样点数 / 采样率
    return len(audio) / sr

def analyze_audio(audio: torch.Tensor, sr: int,
                  clipping_threshold: float) -> Dict[str, Any]:
    # 分析音频特征  Returns: 包含峰值、RMS、时长的字典
    max_val = torch.abs(audio).max().item()
    rms = torch.sqrt(torch.mean(audio ** 2)).item()
    duration = get_audio_duration(audio, sr)
    return {
        "peak": max_val,
        "rms": rms,
        "duration": duration,
        "is_clipping": max_val > clipping_threshold
    }

def ensure_channels(audio: torch.Tensor) -> torch.Tensor:
    # 确保音频格式为 [channels, samples]
    if audio.dim() == 1:
        return audio.unsqueeze(0)  # [1, samples]
    return audio


def extract_segment( audio: torch.Tensor, start: int, end: int, sr: int,
                     normalizer=None, clipping_threshold: float = 0.99 ) -> Tuple[torch.Tensor, dict]:
    # 提取并处理单个片段
    segment = audio[start:end]
    original_stats = analyze_audio(segment, sr, clipping_threshold)
    # 音量归一化
    if normalizer:
        segment = normalizer.normalize(segment)
    normalized_stats = analyze_audio(segment, sr, clipping_threshold)

    return segment, {
        "duration_sec": (end - start) / sr,
        "original_rms": original_stats["rms"],
        "normalized_rms": normalized_stats["rms"]
    }

def save_segment(segment: torch.Tensor, output_path: Path, sr: int):
    # 保存音频片段
    segment = ensure_channels(segment)
    torchaudio.save(str(output_path), segment.cpu(), sr)

def filter_by_duration(timestamps: List[Dict], sr: int, min_duration: float, max_duration: float) -> List[Dict]:
    # 丢弃时长不在范围内的片段
    return [
        ts for ts in timestamps
        if min_duration <= (ts['end'] - ts['start']) / sr <= max_duration
    ]


def split_long_segments(timestamps: List[Dict], audio: torch.Tensor, sr: int, vad_model,vad_config: dict,
                        max_duration: float , enabled_double_split: bool , factor: float ) -> List[Dict]:
    # 拆分过长的片段
    result = []

    for ts in timestamps:
        start = ts['start']
        end = ts['end']
        duration = (end - start) / sr

        logger.debug(f"片段: {start / sr:.2f}s - {end / sr:.2f}s (时长: {(end - start) / sr:.2f}s)")

        if duration <= max_duration:
            result.append(ts)
        elif not enabled_double_split:
            result.append(ts)
            logger.info(f"未启用用多级分割, 已跳过该片段")
        else:
            segment_audio = audio[start:end]
            logger.debug(f"过长片段，降级切分中")

            # 递归调用 VAD 检测
            next_config = {
                "threshold": round(vad_config["threshold"] * factor, 2),
                "min_speech_duration_ms": int(vad_config["min_speech_duration_ms"] * factor),
                "min_silence_duration_ms": int(vad_config["min_silence_duration_ms"] * factor),
                "speech_pad_ms": int(vad_config["speech_pad_ms"] * factor)
            }
            # 避免过深分割
            if next_config["threshold"] <= 0.20:
                result.append(ts)
                continue

            sub_timestamps = get_speech_timestamps(
                segment_audio,
                vad_model,
                threshold=next_config["threshold"],
                sampling_rate=sr,
                min_speech_duration_ms=next_config["min_speech_duration_ms"],
                min_silence_duration_ms=next_config["min_silence_duration_ms"],
                speech_pad_ms=next_config["speech_pad_ms"],
                return_seconds=False
            )

            # 调整子片段的偏移量
            for sub_ts in sub_timestamps:
                sub_ts['start'] += start
                sub_ts['end'] += start
                # 调试
                logger.debug(f"切分过长片段: "
                             f"{sub_ts['start'] / sr:.2f}s - {sub_ts['end'] / sr:.2f}s" 
                             f"(时长: {(sub_ts['end'] - sub_ts['start']) / sr:.2f}s)")

            # 递归处理子片段（可能还有更长的）
            # sub_result = split_long_segments(
            #     sub_timestamps, audio, sr, vad_model, vad_config, max_duration
            # )
            # result.extend(sub_result)
            for sub_ts in sub_timestamps:
                sub_duration = (sub_ts['end'] - sub_ts['start']) / sr
                if sub_duration > max_duration:
                    # 还过长，继续递归
                    sub_result = split_long_segments([sub_ts], audio, sr, vad_model, next_config,
                                                     max_duration, enabled_double_split, factor
                    )
                    result.extend(sub_result)
                else:
                    result.append(sub_ts)
    return result

