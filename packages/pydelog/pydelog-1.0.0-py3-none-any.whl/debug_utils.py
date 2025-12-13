import time
from enum import Enum, auto


class LogLevel(Enum):
    INFO = auto()
    ERROR = auto()
    DEBUG = auto()
    FATAL = auto()
    CRITICAL = auto()
    WARNING = auto()
    TRACE = auto()
    VERBOSE = auto()
    SYSTEM = auto()
    ALERT = auto()


class DebugUtils:
    ENABLE_LOGS = True
    ENABLE_COLOR = True

    COLORS = {
        LogLevel.INFO:     "\033[94m",
        LogLevel.ERROR:    "\033[91m",
        LogLevel.DEBUG:    "\033[92m",
        LogLevel.FATAL:    "\033[95m",
        LogLevel.CRITICAL: "\033[31m",
        LogLevel.WARNING:  "\033[93m",
        LogLevel.TRACE:    "\033[96m",
        LogLevel.VERBOSE:  "\033[90m",
        LogLevel.SYSTEM:   "\033[97m",
        LogLevel.ALERT:    "\033[35m",
        "END":             "\033[0m"
    }

    @staticmethod
    def _log(level: LogLevel, message: str):
        if not DebugUtils.ENABLE_LOGS:
            return

        color = DebugUtils.COLORS.get(level, "")
        end = DebugUtils.COLORS["END"] if DebugUtils.ENABLE_COLOR else ""
        print(f"{color}[{level.name}] {message}{end}")

    @staticmethod
    def timer(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            DebugUtils._log(
                LogLevel.DEBUG,
                f"{func.__name__} executed in {(end - start):.6f}s"
            )
            return result
        return wrapper

    @staticmethod
    def log_i(msg): DebugUtils._log(LogLevel.INFO, msg)
    @staticmethod
    def log_e(msg): DebugUtils._log(LogLevel.ERROR, msg)
    @staticmethod
    def log_d(msg): DebugUtils._log(LogLevel.DEBUG, msg)
    @staticmethod
    def log_f(msg): DebugUtils._log(LogLevel.FATAL, msg)
    @staticmethod
    def log_c(msg): DebugUtils._log(LogLevel.CRITICAL, msg)
    @staticmethod
    def log_w(msg): DebugUtils._log(LogLevel.WARNING, msg)
    @staticmethod
    def log_t(msg): DebugUtils._log(LogLevel.TRACE, msg)
    @staticmethod
    def log_v(msg): DebugUtils._log(LogLevel.VERBOSE, msg)
    @staticmethod
    def log_s(msg): DebugUtils._log(LogLevel.SYSTEM, msg)
    @staticmethod
    def log_a(msg): DebugUtils._log(LogLevel.ALERT, msg)
