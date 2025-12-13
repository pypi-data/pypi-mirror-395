from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


@dataclass(frozen=True)
class DataSource:
    """
    Represents a logical data source.

    For now it supports local file paths and simple HTTP/HTTPS URLs.
    We can later extend this to S3/Blob/etc. without touching adapters.
    """
    uri: str
    format_hint: Optional[str] = None

    def is_local_file(self) -> bool:
        return Path(self.uri).exists()

    def suffix(self) -> str:
        """
        Return the lowercase file extension (without dot) from the URI path.
        Example: 'data/file.CSV' -> 'csv'
        """
        path = urlparse(self.uri).path
        suffix = Path(path).suffix
        return suffix.lstrip(".").lower()
