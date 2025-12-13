"""
Unit tests for JSON serializer

Tests XWJsonSerializer implementation.
Following GUIDELINES_TEST.md structure and eXonware testing standards.

Company: eXonware.com
Author: Eng. Muhammad AlShehri
Email: connect@exonware.com
"""

import pytest
from exonware.xwsystem.io.serialization.formats.text.json import XWJsonSerializer
from exonware.xwsystem.io.serialization.base import ASerialization


@pytest.mark.xsystem_unit
class TestJsonSerializer:
    """Test XWJsonSerializer implementation."""
    
    def test_json_serializer_can_be_instantiated(self):
        """Test that XWJsonSerializer can be created."""
        serializer = XWJsonSerializer()
        assert serializer is not None
    
    def test_json_serializer_extends_aserialization(self):
        """Test XWJsonSerializer extends ASerialization."""
        assert issubclass(XWJsonSerializer, ASerialization)
    
    def test_json_serializer_has_encode_decode(self):
        """Test XWJsonSerializer has codec methods."""
        serializer = XWJsonSerializer()
        assert hasattr(serializer, 'encode')
        assert hasattr(serializer, 'decode')
        assert callable(serializer.encode)
        assert callable(serializer.decode)


@pytest.mark.xsystem_unit
class TestJsonSerializerBackwardCompatibility:
    """Test JSON serializer backward compatibility."""
    
    def test_jsonserializer_alias_exists(self):
        """Test JsonSerializer alias exists for backward compatibility."""
        from exonware.xwsystem.io.serialization import JsonSerializer
        assert JsonSerializer is XWJsonSerializer

