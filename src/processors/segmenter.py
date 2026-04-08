from pathlib import Path
from typing import List, Tuple
import torch
import torchaudio
from silero_vad import get_speech_timestamps

from ..config.settings import VADConfig
from src.utils.audio_utils import analyze_audio, ensure_channels
from .normalizer import AudioNormalizer
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AudioSegmenter:
    # 音频切分器

    def __init__(self, vad_config: VADConfig, normalizer: AudioNormalizer):
        self.vad_config = vad_config
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

    def extract_segment(self, audio: torch.Tensor, start: int, end: int, sr: int) -> Tuple[torch.Tensor, dict]:
        # 提取并处理单个片段
        clipping_threshold = self.normalizer.config.clipping_threshold
        segment = audio[start:end]
        original_stats = analyze_audio(segment, sr,clipping_threshold)
        # 音量归一化
        segment = self.normalizer.normalize(segment)
        normalized_stats = analyze_audio(segment, sr,clipping_threshold)

        return segment, {
            "duration_sec": (end - start) / sr,
            "original_rms": original_stats["rms"],
            "normalized_rms": normalized_stats["rms"]
        }

    def save_segment(self, segment: torch.Tensor, output_path: Path, sr: int):
        # 保存片段
        segment = ensure_channels(segment)
        torchaudio.save(str(output_path), segment.cpu(), sr)