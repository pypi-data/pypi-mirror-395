#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for stream base classes.

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

from exonware.xwsystem.io.stream.base import ACodecIO, APagedCodecIO


@pytest.mark.xwsystem_unit
@pytest.mark.xwsystem_io
class TestStreamBase:
    """Test stream base classes."""
    
    def test_acodec_io_base(self):
        """Test ACodecIO base class exists."""
        # Base class is abstract, just verify it exists
        assert ACodecIO is not None
    
    def test_apaged_codec_io_base(self):
        """Test APagedCodecIO base class exists."""
        # Base class is abstract, just verify it exists
        assert APagedCodecIO is not None

