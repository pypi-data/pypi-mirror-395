# src/pypurge/modules/logging.py

import json
import logging
import sys
from datetime import datetime as _dt, timezone
from pathlib import Path
from typing import Optional


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": _dt.fromtimestamp(record.created, timezone.utc).isoformat() + "Z",
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(
    log_format: str,
    log_file: Optional[Path],
    level: int = logging.INFO,
    rotate: bool = True,
) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    # clear existing handlers
    while root.handlers:
        root.handlers.pop()

    if log_format == "json":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    if log_file:
        try:
            if rotate:
                from logging.handlers import RotatingFileHandler

                fh = RotatingFileHandler(
                    str(log_file),
                    maxBytes=5 * 1024 * 1024,
                    backupCount=5,
                    encoding="utf-8",
                )
            else:
                fh = logging.FileHandler(str(log_file), encoding="utf-8")
            fh.setFormatter(
                JsonFormatter()
                if log_format == "json"
                else logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
            )
            root.addHandler(fh)
        except Exception:
            # best-effort: add a simple file handler
            try:
                fh = logging.FileHandler(str(log_file), encoding="utf-8")
                fh.setFormatter(
                    JsonFormatter()
                    if log_format == "json"
                    else logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
                )
                root.addHandler(fh)
            except Exception:
                logging.getLogger(__name__).warning(
                    "Failed to open log file: %s", log_file
                )
