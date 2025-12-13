#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for TOML serializer.

Following GUIDE_TEST.md standards.
"""

import sys
from pathlib import Path

import pytest

# Windows UTF-8 setup
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass


@pytest.mark.xwsystem_unit
@pytest.mark.xwsystem_serialization
class TestTomlSerializer:
    """Test TOML serializer."""
    
    def test_toml_serializer_roundtrip(self, tmp_path):
        """Test TOML serializer roundtrip."""
        try:
            from exonware.xwsystem.io.serialization.formats.text.toml import TomlSerializer
            
            serializer = TomlSerializer()
            test_file = tmp_path / "test.toml"
            test_data = {"key": "value", "number": 42}
            
            serializer.save_file(test_data, test_file)
            loaded = serializer.load_file(test_file)
            
            assert loaded == test_data
        except ImportError:
            pytest.skip("TOML serializer not available")
    
    def test_toml_serializer_encode_decode(self):
        """Test TOML encode/decode."""
        try:
            from exonware.xwsystem.io.serialization.formats.text.toml import TomlSerializer
            
            serializer = TomlSerializer()
            test_data = {"key": "value"}
            
            encoded = serializer.encode(test_data)
            decoded = serializer.decode(encoded)
            
            assert decoded == test_data
        except ImportError:
            pytest.skip("TOML serializer not available")

