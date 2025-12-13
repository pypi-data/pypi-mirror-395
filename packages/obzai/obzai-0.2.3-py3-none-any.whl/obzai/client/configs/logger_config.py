# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
from logging.config import dictConfig


LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] %(message)s"
SIMPLE_LOG_FORMAT = "[%(levelname)s] %(message)s"
DEFAULT_LOG_FILE = os.getenv("OBZ_LOG_FILE", os.path.join(".obz", "obz.log"))
DEFAULT_LEVEL = os.getenv("OBZ_LOG_LEVEL", "INFO")
PACKAGE_LOGGERS = ("obzai", "obzai.client", "obzai.data_inspection", "obzai.xai")


def _build_handlers(to_console: bool, to_file: bool, log_file: str) -> dict:
    handlers = {}
    if to_console:
        handlers["console"] = {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }

    if to_file:
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_file,
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 5,
            "formatter": "default",
        }

    return handlers


def _build_loggers(level: str, handler_names: list[str], include_httpx: bool, httpx_level: str) -> dict:
    loggers = {
        name: {
            "level": level,
            "handlers": handler_names,
            # If we attach handlers, do not propagate. If we do not, let host config capture logs.
            "propagate": False if handler_names else True,
        }
        for name in PACKAGE_LOGGERS
    }

    # Keep noisy HTTP client libraries quiet by default.
    http_handlers = handler_names if include_httpx else []
    loggers["httpx"] = {
        "level": httpx_level,
        "handlers": http_handlers,
        "propagate": False,
    }
    loggers["httpcore"] = {
        "level": httpx_level,
        "handlers": http_handlers,
        "propagate": False,
    }
    return loggers


def build_logging_config(
    level: str = DEFAULT_LEVEL,
    to_console: bool = True,
    to_file: bool = False,
    log_file: str = DEFAULT_LOG_FILE,
    include_httpx: bool = False,
    httpx_level: str = "WARNING",
) -> dict:
    """
    Build a dictConfig configuration for ObzAI loggers.

    The configuration is opt-in and does not modify the root logger. Host
    applications can choose to use it or supply their own logging setup.
    """
    handlers = _build_handlers(to_console=to_console, to_file=to_file, log_file=log_file)
    handler_names = list(handlers.keys())

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": LOG_FORMAT},
            "simple": {"format": SIMPLE_LOG_FORMAT},
        },
        "handlers": handlers,
        "loggers": _build_loggers(
            level=level,
            handler_names=handler_names,
            include_httpx=include_httpx,
            httpx_level=httpx_level,
        ),
    }


def setup_logging(
    level: str | None = None,
    to_console: bool = True,
    to_file: bool | None = None,
    log_file: str | None = None,
    include_httpx: bool = False,
    httpx_level: str = "WARNING",
) -> None:
    """
    Configure logging for the ObzAI package in a library-friendly way.

    Args:
        level: Log level for ObzAI loggers. Defaults to OBZ_LOG_LEVEL or INFO.
        to_console: Whether to emit logs to stdout. If False and no file is requested,
            existing handlers and propagation are left intact.
        to_file: Whether to emit logs to .obz/obz.log (defaults to OBZ_LOG_TO_FILE env flag).
        log_file: Custom log file path when to_file is True.
        include_httpx: Attach handlers to httpx/httpcore loggers. Disabled by default.
        httpx_level: Log level for httpx/httpcore.
    """
    resolved_level = level or DEFAULT_LEVEL
    resolved_to_file = to_file if to_file is not None else os.getenv("OBZ_LOG_TO_FILE", "").lower() in {"1", "true", "yes"}
    resolved_log_file = log_file or DEFAULT_LOG_FILE

    try:
        if resolved_to_file:
            os.makedirs(os.path.dirname(resolved_log_file) or ".", exist_ok=True)

        dictConfig(
            build_logging_config(
                level=resolved_level,
                to_console=to_console,
                to_file=resolved_to_file,
                log_file=resolved_log_file,
                include_httpx=include_httpx,
                httpx_level=httpx_level,
            )
        )
    except Exception as e:
        print(f"Failed to configure logging: {e}")
        logging.basicConfig(level=logging.ERROR)


def quiet_httpx(level: str = "WARNING") -> None:
    """
    Silence httpx/httpcore chatter without altering other logging settings.

    This is safe to call from host applications that want to keep their own
    logging configuration but avoid verbose HTTP client output.
    """
    for name in ("httpx", "httpcore"):
        lg = logging.getLogger(name)
        lg.setLevel(level)
        lg.propagate = False
        lg.addHandler(logging.NullHandler())
