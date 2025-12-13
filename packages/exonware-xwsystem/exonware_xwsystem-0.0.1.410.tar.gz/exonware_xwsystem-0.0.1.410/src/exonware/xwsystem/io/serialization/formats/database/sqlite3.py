"""
Company: eXonware.com
Author: Eng. Muhammad AlShehri
Email: connect@exonware.com
Version: 0.0.1.410
Generation Date: November 2, 2025

SQLite3 serialization - Embedded database storage.

Following I→A pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- Concrete: Sqlite3Serializer
"""

import sqlite3
from typing import Any, Optional, Union
from pathlib import Path

from ...base import ASerialization
from ....contracts import EncodeOptions, DecodeOptions
from ....defs import CodecCapability
from ....errors import SerializationError


class Sqlite3Serializer(ASerialization):
    """SQLite3 serializer - follows the I→A pattern."""
    
    @property
    def codec_id(self) -> str:
        return "sqlite3"
    
    @property
    def media_types(self) -> list[str]:
        return ["application/x-sqlite3", "application/vnd.sqlite3"]
    
    @property
    def file_extensions(self) -> list[str]:
        return [".db", ".sqlite", ".sqlite3"]
    
    @property
    def format_name(self) -> str:
        return "SQLite3"
    
    @property
    def mime_type(self) -> str:
        return "application/x-sqlite3"
    
    @property
    def is_binary_format(self) -> bool:
        return True
    
    @property
    def supports_streaming(self) -> bool:
        return False
    
    @property
    def capabilities(self) -> CodecCapability:
        return CodecCapability.BIDIRECTIONAL
    
    @property
    def aliases(self) -> list[str]:
        return ["sqlite3", "sqlite", "db"]
    
    def encode(self, value: Any, *, options: Optional[EncodeOptions] = None) -> Union[bytes, str]:
        """SQLite3 encode requires file path - use save_file() instead."""
        raise NotImplementedError("SQLite3 requires file-based operations - use save_file()")
    
    def decode(self, repr: Union[bytes, str], *, options: Optional[DecodeOptions] = None) -> Any:
        """SQLite3 decode requires file path - use load_file() instead."""
        raise NotImplementedError("SQLite3 requires file-based operations - use load_file()")

