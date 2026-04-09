# src/utils/asr_utils.py
import gc
from pathlib import Path
from opencc import OpenCC
from src.utils.progress_utils import progressBar
from src.config.errors import CaseError, NotEnableError, AsrError
from src.config.settings import FasterWhisperConfig
from faster_whisper import WhisperModel
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
cc = OpenCC('t2s')

def get_model_path(config: FasterWhisperConfig) -> str:
    # 获取模型路径
    local_model_path = Path(f"./models/faster-whisper-{config.model}")
    if local_model_path.exists():
        return str(local_model_path)

    return config.model

def load_asr_model(config: FasterWhisperConfig):
    # 加载 ASR 模型
    if not config.enabled:
        # raise NotEnableError("未启用音频识别功能")
        return None

    return WhisperModel(
        model_size_or_path=get_model_path(config),
        device=config.device,
        compute_type=config.compute_type,
        cpu_threads=config.cpu_threads if config.device == "cpu" else 0,
        num_workers=1,
    )


def transcribe_audio(model:WhisperModel, config: FasterWhisperConfig, audio_path: Path):
    # 识别音频
    if model is None:
        model = load_asr_model(config)

    try:
        segments, info = model.transcribe(
            str(audio_path),
            language=config.language,
            task=config.task,
            vad_filter=True,
            initial_prompt=config.initial_prompt
        )
    except Exception as e:
        raise AsrError(f"音频识别错误, {e}")
    # 收集识别结果
    text = cc.convert((" ".join([seg.text for seg in segments])))
    # 保存识别结果
    if config.enables_auto_save:
        output_dir = config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = audio_path.parent / f"{audio_path.stem}.txt"
        output_path.write_text(text, encoding="utf-8")
    return text.strip()

def batch_transcribe(model:WhisperModel, config: FasterWhisperConfig, audio_paths: list):
    # 批量识别
    results = {}
    if config.enables_auto_save:
        logger.info(f"音频识别结果将保存至： {config.output_dir}")

    with progressBar(len(audio_paths)) as progress:
        for index, audio_path in enumerate(audio_paths):
            text = transcribe_audio(model, config, audio_path)
            progress()
            progress.text(f" #{index + 1} ")
            print(f"文本识别： {text}")
            results[audio_path.stem] = text
    # 返回最终结果
    return results