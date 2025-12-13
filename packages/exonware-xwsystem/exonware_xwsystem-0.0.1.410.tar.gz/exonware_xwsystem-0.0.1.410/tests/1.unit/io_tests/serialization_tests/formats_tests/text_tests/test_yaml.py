"""
Unit tests for YAML serializer

Tests XWYamlSerializer implementation.
Following GUIDELINES_TEST.md structure and eXonware testing standards.

Company: eXonware.com
Author: Eng. Muhammad AlShehri
Email: connect@exonware.com
"""

import pytest
from exonware.xwsystem.io.serialization.formats.text.yaml import XWYamlSerializer
from exonware.xwsystem.io.serialization.base import ASerialization


@pytest.mark.xsystem_unit
class TestYamlSerializer:
    """Test XWYamlSerializer implementation."""
    
    def test_yaml_serializer_can_be_instantiated(self):
        """Test that XWYamlSerializer can be created."""
        serializer = XWYamlSerializer()
        assert serializer is not None
    
    def test_yaml_serializer_extends_aserialization(self):
        """Test XWYamlSerializer extends ASerialization."""
        assert issubclass(XWYamlSerializer, ASerialization)
    
    def test_yaml_serializer_has_encode_decode(self):
        """Test XWYamlSerializer has codec methods."""
        serializer = XWYamlSerializer()
        assert hasattr(serializer, 'encode')
        assert hasattr(serializer, 'decode')


@pytest.mark.xsystem_unit
class TestYamlSerializerBackwardCompatibility:
    """Test YAML serializer backward compatibility."""
    
    def test_yamlserializer_alias_exists(self):
        """Test YamlSerializer alias exists for backward compatibility."""
        from exonware.xwsystem.io.serialization import YamlSerializer
        assert YamlSerializer is XWYamlSerializer

