#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for filesystem base classes.

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

from exonware.xwsystem.io.filesystem.base import AFileSystem


@pytest.mark.xwsystem_unit
@pytest.mark.xwsystem_io
class TestAFileSystem:
    """Test AFileSystem base class."""
    
    def test_afilesystem_base(self):
        """Test AFileSystem base class exists."""
        # Base class is abstract, just verify it exists
        assert AFileSystem is not None

