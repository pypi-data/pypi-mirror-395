import logging
import sys
from pathlib import Path
from typing import overload  # <--- NEW

try:
    import colorama
    colorama.just_fix_windows_console()
except Exception:
    colorama = None


# ---- TRACE level + custom logger ---------------------------------
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")


class TraceLogger(logging.Logger):
    """Logger with an extra TRACE level."""
    def trace(self, message, *args, **kwargs):
        if self.isEnabledFor(TRACE_LEVEL):
            self._log(TRACE_LEVEL, message, args, **kwargs)


# Make all future loggers be TraceLogger
logging.setLoggerClass(TraceLogger)
# -------------------------------------------------------------------


class ColorFormatter(logging.Formatter):
    """ANSI-colored logging formatter for console output."""

    COLORS = {
        "TRACE": "\033[90m",   # Dark gray
        "DEBUG": "\033[36m",   # Cyan
        "INFO": "\033[32m",    # Green
        "WARNING": "\033[33m", # Yellow
        "ERROR": "\033[31m",   # Red
        "CRITICAL": "\033[41m" # White on Red background
    }
    RESET = "\033[0m"

    def format(self, record):
        level = record.levelname
        color = self.COLORS.get(level, self.RESET)
        record.levelname = f"{color}{level}{self.RESET}"
        return super().format(record)


class LoggerSetup:
    """Centralized logger configuration for scanner3d."""

    TRACE = TRACE_LEVEL

    @staticmethod
    def configure(
        name: str,
        level: int = logging.INFO,            # default level
        suppress_matplotlib: bool = True,
        log_file: str | Path | None = None,
        console: bool = True,
    ) -> TraceLogger:
        """Configure global logging with optional console and file logging."""

        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        handlers: list[logging.Handler] = []

        # Optional console (colored)
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(ColorFormatter(fmt))
            console_handler.setLevel(level)
            handlers.append(console_handler)

        # Optional file handler (no colors)
        if log_file is not None:
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(logging.Formatter(fmt))
            fh.setLevel(level)
            handlers.append(fh)

        # Configure ROOT logger.
        # Root at TRACE so TRACE records can pass through if handlers allow them.
        logging.basicConfig(level=TRACE_LEVEL, handlers=handlers, force=True)

        if suppress_matplotlib:
            logging.getLogger("matplotlib").setLevel(logging.WARNING)

        log = logging.getLogger(name)
        assert isinstance(log, TraceLogger)  # for type checkers
        log.debug("Logger initialized for %s (console=%s)", name, console)
        return log


@overload
def get_logger(name: None = ...) -> TraceLogger: ...
@overload
def get_logger(name: str) -> TraceLogger: ...

def get_logger(name: str | None = None) -> TraceLogger:
    """Typed wrapper around logging.getLogger that returns TraceLogger."""
    logger = logging.getLogger(name)
    assert isinstance(logger, TraceLogger)
    return logger
