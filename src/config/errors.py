# src/exception/errors.py

from dataclasses import dataclass, field
from typing import Optional, Any

@dataclass
class BasesError(Exception):
    def __init__(self, message: Optional[str] = None):
        self.message = message or self.default_message
        super().__init__(self.message)

    @property
    def default_message(self) -> str:
        return "发生错误"

class AudioError(BasesError):
    @property
    def default_message(self) -> str:
        return "音频处理失败"


class FileError(BasesError):
    @property
    def default_message(self) -> str:
        return "文件操作失败"

class CaseError(BasesError):
    @property
    def default_message(self) -> str:
        return "异常的条件分支"