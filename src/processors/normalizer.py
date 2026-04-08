import torch

from ..config.errors import CaseError
from ..config.settings import NormalizeConfig
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AudioNormalizer:
    # 音频音量归一化器

    def __init__(self, config: NormalizeConfig):
        self.config = config

    def normalize_peak(self, audio: torch.Tensor) -> torch.Tensor:
        # 峰值归一化
        max_val = torch.abs(audio).max()
        if max_val > 1e-6:
            audio = audio / max_val * self.config.target_peak
        return audio

    def normalize_rms(self, audio: torch.Tensor) -> torch.Tensor:
        # RMS 响度归一化
        rms = torch.sqrt(torch.mean(audio ** 2))
        if rms > 1e-6:
            audio = audio / rms * self.config.target_rms
        # 防削波
        max_val = torch.abs(audio).max()
        if max_val > 0.95:
            audio = audio / max_val * 0.95
        return audio

    def normalize(self, audio: torch.Tensor) -> torch.Tensor:
        # 统一归一化接口
        if not self.config.enabled:
            return audio
        if self.config.method == "peak":
            return self.normalize_peak(audio)
        elif self.config.method == "rms":
            return self.normalize_rms(audio)
        else:
            # return self.normalize_rms(audio)
            raise CaseError()