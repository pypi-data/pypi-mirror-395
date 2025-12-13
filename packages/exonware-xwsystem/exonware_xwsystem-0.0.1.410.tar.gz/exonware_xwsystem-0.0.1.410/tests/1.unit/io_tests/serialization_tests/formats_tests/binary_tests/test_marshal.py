#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Marshal serializer.

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
class TestMarshalSerializer:
    """Test Marshal serializer."""
    
    def test_marshal_serializer_roundtrip(self, tmp_path):
        """Test Marshal serializer roundtrip."""
        try:
            from exonware.xwsystem.io.serialization.formats.binary.marshal import MarshalSerializer
            
            serializer = MarshalSerializer()
            test_file = tmp_path / "test.marshal"
            test_data = {"key": "value", "number": 42}
            
            serializer.save_file(test_data, test_file)
            loaded = serializer.load_file(test_file)
            
            assert loaded == test_data
        except ImportError:
            pytest.skip("Marshal serializer not available")

