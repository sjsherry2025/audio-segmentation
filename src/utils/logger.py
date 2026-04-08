import logging
import sys

def setup_logger(name: str = __name__, log_file: str = "segment.log") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件 handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger