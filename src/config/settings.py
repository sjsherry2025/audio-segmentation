from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

@dataclass
class VADConfig:
    # VAD 参数配置
    # 语音检测敏感度
    threshold: float = 0.5
    # 最小静音间隔
    min_silence_duration_ms: int = 500
    # 最小语音片段时长
    min_speech_duration_ms: int = 500
    # speech_pad_ms
    speech_pad_ms: int = 200

    def to_dict(self):
        return {
            "threshold": self.threshold,
            "min_silence_duration_ms": self.min_silence_duration_ms,
            "min_speech_duration_ms": self.min_speech_duration_ms,
            "speech_pad_ms": self.speech_pad_ms,
        }


@dataclass
class NormalizeConfig:
    # 音量归一化配置
    enabled: bool = True
    # rms 基于平均响度调整 peak 基于最大峰值调整
    method: str = "rms"  # 'peak', 'rms'
    # Root Mean Square（均方根），代表音频的平均响度
    target_rms: float = 0.15
    # 目标峰值 音频的最大振幅上限
    target_peak: float = 0.95
    # 削波的检测阈值
    clipping_threshold : float = 0.99

    def __post_init__(self):
        assert self.method in ["peak", "rms"], f"Unknown method: {self.method}"
        assert 0 < self.target_rms < 1, "target_rms must be between 0 and 1"
        assert 0 < self.target_peak <= 1, "target_peak must be between 0 and 1"
        assert 0 < self.clipping_threshold  <= 1, "clipping_threshold must be between 0 and 1"

@dataclass
class SegmenterConfig:
    # 分割音频配置
    min_second: int = 3
    # 目标峰值 音频的最大振幅上限
    max_second: int = 8
    # 启用多级分割（当音频大于当前长度时，继续分割直到符合要求）
    enabled_double_split: bool = False

    def to_dict(self):
        return {
            "min_second": self.min_second,
            "max_second": self.max_second,
        }

@dataclass
class SettingConfig:
    # 应用主配置
    input_dir: Path = Path("./input")
    output_dir: Path = Path("./output")
    supported_formats: Tuple[str, ...] = (".wav", ".mp3")
    vad: VADConfig = field(default_factory=VADConfig)
    normalize: NormalizeConfig = field(default_factory=NormalizeConfig)
    segmenter: SegmenterConfig = field(default_factory=SegmenterConfig)

    def __post_init__(self):
        self.input_dir = Path(self.input_dir)
        self.output_dir = Path(self.output_dir)