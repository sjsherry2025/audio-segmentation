import torch
from typing import Dict, Any

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