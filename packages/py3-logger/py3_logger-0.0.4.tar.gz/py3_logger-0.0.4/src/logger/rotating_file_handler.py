import os
from logging import handlers
from typing import Any, Final


class RotatingFileHandler(handlers.RotatingFileHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._zero_padding: Final[int] = len(str(self.backupCount)) if self.backupCount > 0 else 0

    def doRollover(self) -> None:
        if self.stream:
            self.stream.close()
            self.stream = None  # noqa

        if self.backupCount > 0:
            oldest = self._format_backup_filename(self.backupCount)
            if os.path.exists(oldest):
                os.remove(oldest)

            for i in range(self.backupCount - 1, 0, -1):
                sfn = self._format_backup_filename(i)
                dfn = self._format_backup_filename(i + 1)
                if os.path.exists(sfn):
                    os.rename(sfn, dfn)

            dfn = self._format_backup_filename(1)
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)

        self.mode = "w"
        self.stream = self._open()

    def _format_backup_filename(self, index: int) -> str:
        root, ext = os.path.splitext(self.baseFilename)
        padded = str(index).zfill(self._zero_padding)
        return f"{root}.{padded}{ext}"


__all__ = ["RotatingFileHandler"]
