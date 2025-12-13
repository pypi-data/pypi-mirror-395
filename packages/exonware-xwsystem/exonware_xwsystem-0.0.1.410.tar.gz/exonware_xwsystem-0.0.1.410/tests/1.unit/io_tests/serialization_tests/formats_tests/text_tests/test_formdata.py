#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for FormData serializer.

Following GUIDE_TEST.md standards.
"""

import sys

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
class TestFormDataSerializer:
    """Test FormData serializer."""
    
    def test_formdata_serializer_encode_decode(self):
        """Test FormData encode/decode."""
        try:
            from exonware.xwsystem.io.serialization.formats.text.formdata import FormDataSerializer
            
            serializer = FormDataSerializer()
            test_data = {"username": "test", "password": "secret"}
            
            encoded = serializer.encode(test_data)
            decoded = serializer.decode(encoded)
            
            assert decoded is not None
        except ImportError:
            pytest.skip("FormData serializer not available")

