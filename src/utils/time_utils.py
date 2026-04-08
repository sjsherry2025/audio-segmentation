# src/utils/file_utils.py

from datetime import datetime, timezone, timedelta
import time

def get_time() -> str:
    # 获取当前时间字符串
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_timestamp() -> int:
    # 获取当前时间戳（秒）
    return int(time.time())


def get_timestamp_ms() -> int:
    # 获取当前时间戳（毫秒）
    return int(time.time() * 1000)


def get_time_with_timezone(timezone_offset: int = 8) -> str:
    # 获取带时区的时间字符串
    tz = timezone(timedelta(hours=timezone_offset))
    dt = datetime.now(tz)
    return dt.strftime("%Y-%m-%d %H:%M:%S %z")


def get_utc_time() -> str:
    # 获取 UTC 时间
    dt = datetime.now(timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")