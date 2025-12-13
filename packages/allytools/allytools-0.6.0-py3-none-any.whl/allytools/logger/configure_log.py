from __future__ import annotations
from pathlib import Path
import logging
from datetime import datetime
from allytools.logger import LoggerSetup

def configure_file_logger(
    file: str,
    *,
    level: int = logging.DEBUG,
    console: bool = False,
    logs_subdir: str = "logs",
    include_time: bool = False,
) -> logging.Logger:
    script_path = Path(file).resolve()
    script_stem = script_path.stem
    log_dir = script_path.parent / logs_subdir
    log_dir.mkdir(exist_ok=True)
    if include_time:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        timestamp = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"{script_stem}_{timestamp}.log"
    logger = LoggerSetup.configure(
        name=script_stem,
        level=level,
        log_file=str(log_file),
        console=console)
    return logger
