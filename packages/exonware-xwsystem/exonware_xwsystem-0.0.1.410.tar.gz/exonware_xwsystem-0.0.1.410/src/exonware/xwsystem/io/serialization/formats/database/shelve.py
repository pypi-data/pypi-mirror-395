"""
Company: eXonware.com
Author: Eng. Muhammad AlShehri
Email: connect@exonware.com
Version: 0.0.1.410
Generation Date: November 2, 2025

Shelve serialization - Persistent dictionary storage.

Following I→A pattern:
- I: ISerialization (interface)
- A: ASerialization (abstract base)
- Concrete: ShelveSerializer
"""

import shelve
from typing import Any, Optional, Union
from pathlib import Path

from ...base import ASerialization
from ....contracts import EncodeOptions, DecodeOptions
from ....defs import CodecCapability
from ....errors import SerializationError


class ShelveSerializer(ASerialization):
    """Shelve serializer - follows the I→A pattern."""
    
    @property
    def codec_id(self) -> str:
        return "shelve"
    
    @property
    def media_types(self) -> list[str]:
        return ["application/x-shelve"]
    
    @property
    def file_extensions(self) -> list[str]:
        return [".shelve", ".db"]
    
    @property
    def format_name(self) -> str:
        return "Shelve"
    
    @property
    def mime_type(self) -> str:
        return "application/x-shelve"
    
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
        return ["shelve", "Shelve"]
    
    def encode(self, value: Any, *, options: Optional[EncodeOptions] = None) -> Union[bytes, str]:
        """Shelve encode requires file path - use save_file() instead."""
        raise NotImplementedError("Shelve requires file-based operations - use save_file()")
    
    def decode(self, repr: Union[bytes, str], *, options: Optional[DecodeOptions] = None) -> Any:
        """Shelve decode requires file path - use load_file() instead."""
        raise NotImplementedError("Shelve requires file-based operations - use load_file()")

