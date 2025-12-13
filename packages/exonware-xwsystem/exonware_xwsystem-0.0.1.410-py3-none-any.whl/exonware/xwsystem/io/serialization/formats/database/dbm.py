"""
Company: eXonware.com
Author: Eng. Muhammad AlShehri
Email: connect@exonware.com
Version: 0.0.1.410
Generation Date: November 2, 2025

DBM serialization - Unix database manager.

Following I→A pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- Concrete: DbmSerializer
"""

import dbm
from typing import Any, Optional, Union
from pathlib import Path

from ...base import ASerialization
from ....contracts import EncodeOptions, DecodeOptions
from ....defs import CodecCapability
from ....errors import SerializationError


class DbmSerializer(ASerialization):
    """DBM serializer - follows the I→A pattern."""
    
    @property
    def codec_id(self) -> str:
        return "dbm"
    
    @property
    def media_types(self) -> list[str]:
        return ["application/x-dbm"]
    
    @property
    def file_extensions(self) -> list[str]:
        return [".dbm", ".db"]
    
    @property
    def format_name(self) -> str:
        return "DBM"
    
    @property
    def mime_type(self) -> str:
        return "application/x-dbm"
    
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
        return ["dbm", "DBM"]
    
    def encode(self, value: Any, *, options: Optional[EncodeOptions] = None) -> Union[bytes, str]:
        """DBM encode requires file path - use save_file() instead."""
        raise NotImplementedError("DBM requires file-based operations - use save_file()")
    
    def decode(self, repr: Union[bytes, str], *, options: Optional[DecodeOptions] = None) -> Any:
        """DBM decode requires file path - use load_file() instead."""
        raise NotImplementedError("DBM requires file-based operations - use load_file()")

