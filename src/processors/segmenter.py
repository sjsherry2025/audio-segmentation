# src/processors/segmenter.py

from pathlib import Path
from typing import List, Tuple
import torch
from silero_vad import get_speech_timestamps

from ..config.settings import VADConfig, SegmenterConfig
from src.utils.audio_utils import extract_segment, save_segment, split_long_segments, filter_by_duration
from .normalizer import AudioNormalizer
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AudioSegmenter:
    # 音频切分器

    def __init__(self, vad_config: VADConfig, segmenter_config: SegmenterConfig, normalizer: AudioNormalizer):
        self.vad_config = vad_config
        self.segmenter_config = segmenter_config
        self.normalizer = normalizer

    def detect_speech_segments(self, audio: torch.Tensor, sr: int, model) -> List[dict]:
        # 检测语音片段
        timestamps = get_speech_timestamps(
            audio,
            model,
            threshold=self.vad_config.threshold,
            sampling_rate=sr,
            min_speech_duration_ms=self.vad_config.min_speech_duration_ms,
            min_silence_duration_ms=self.vad_config.min_silence_duration_ms,
            speech_pad_ms=self.vad_config.speech_pad_ms,
            return_seconds=False
        )
        return timestamps

    def extract_and_process_segment(self, audio: torch.Tensor, start: int, end: int, sr: int) -> Tuple[torch.Tensor, dict]:
        # 提取并处理单个片段
        return extract_segment(audio, start, end, sr,
            normalizer=self.normalizer,
            clipping_threshold=self.normalizer.config.clipping_threshold
        )

    def apply_duration_limit(self, timestamps: List[dict], audio: torch.Tensor, sr: int, model, enabled_double_split: bool ) -> List[dict]:
        # 应用时长限制：
        # 1. 过长的片段 → 递归用 VAD 继续切分
        # 2. 过短的片段 → 丢弃
        if not timestamps:
            return []

        min_dur = self.segmenter_config.min_second
        max_dur = self.segmenter_config.max_second

        # 准备 VAD 配置
        vad_config = {
            "threshold": self.vad_config.threshold,
            "min_speech_duration_ms": self.vad_config.min_speech_duration_ms,
            "min_silence_duration_ms": self.vad_config.min_silence_duration_ms,
            "speech_pad_ms": self.vad_config.speech_pad_ms,
        }
        # 1. 拆分过长的片段
        split_result = split_long_segments(timestamps, audio, sr, model, vad_config, max_dur, enabled_double_split )
        # 2. 丢弃过短的片段
        final_result = filter_by_duration(split_result, sr, min_dur, max_dur)
        # 3. 返回
        return final_result

    def save_segment(self, segment: torch.Tensor, output_path: Path, sr: int):
        # 保存片段
        save_segment(segment, output_path, sr)