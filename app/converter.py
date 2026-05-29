import threading
import queue
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

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


class ConverterEngine:
    def __init__(self):
        self._md = MarkItDown(enable_plugins=False)

    def convert_file(self, file_path: str) -> ConversionResult:
        result = ConversionResult(file_path=file_path, status=Status.CONVERTING)
        try:
            doc = self._md.convert(file_path)
            result.markdown = doc.markdown
            result.title = doc.title or Path(file_path).stem
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
