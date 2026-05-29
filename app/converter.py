import io
import os
import sys
import threading
import queue
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

from markitdown import MarkItDown


class Status(Enum):
    PENDING = "pending"
    CONVERTING = "converting"
    DONE = "done"
    ERROR = "error"


@dataclass
class ConversionResult:
    file_path: str
    status: Status = Status.PENDING
    markdown: str = ""
    title: str = ""
    error: str = ""


def _is_url(source: str) -> bool:
    try:
        parsed = urlparse(source)
        return parsed.scheme in ("http", "https")
    except Exception:
        return False


@contextmanager
def _quiet_convert():
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        yield
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class ConverterEngine:
    def __init__(self):
        self._md = MarkItDown(enable_plugins=False)

    def convert_file(self, file_path: str) -> ConversionResult:
        result = ConversionResult(file_path=file_path, status=Status.CONVERTING)
        try:
            with _quiet_convert():
                doc = self._md.convert(file_path)
            result.markdown = doc.markdown
            if _is_url(file_path):
                result.title = doc.title or file_path
            else:
                result.title = doc.title or Path(file_path).stem
            if not result.markdown or not result.markdown.strip():
                result.error = "No content could be extracted from this source."
                result.status = Status.ERROR
            else:
                result.status = Status.DONE
        except Exception as e:
            result.error = str(e)
            result.status = Status.ERROR
        return result

    def convert_async(
        self, file_path: str, result_queue: queue.Queue
    ) -> None:
        def _worker():
            result = self.convert_file(file_path)
            result_queue.put(result)

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()
