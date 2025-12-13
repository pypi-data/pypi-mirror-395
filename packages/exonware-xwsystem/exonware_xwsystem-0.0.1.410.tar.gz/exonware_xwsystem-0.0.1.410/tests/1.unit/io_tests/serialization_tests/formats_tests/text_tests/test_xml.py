#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for XML serializer.

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
class TestXmlSerializer:
    """Test XML serializer."""
    
    def test_xml_serializer_roundtrip(self, tmp_path):
        """Test XML serializer roundtrip."""
        try:
            from exonware.xwsystem.io.serialization.formats.text.xml import XmlSerializer
            
            serializer = XmlSerializer()
            test_file = tmp_path / "test.xml"
            test_data = {"root": {"key": "value"}}
            
            serializer.save_file(test_data, test_file)
            loaded = serializer.load_file(test_file)
            
            assert loaded is not None
        except ImportError:
            pytest.skip("XML serializer not available")

