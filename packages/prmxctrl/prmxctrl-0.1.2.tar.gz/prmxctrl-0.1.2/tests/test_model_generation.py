"""
Tests for model generation functionality.

Tests the ModelGenerator class to ensure it creates proper Pydantic models
with correct field types, constraints, and validation.
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generator.generators.model_generator import ModelGenerator
from generator.parse_schema import Endpoint, Method, Parameter, Response


class TestModelGenerator:
    """Test ModelGenerator functionality."""

    def test_generate_request_model_simple(self):
        """Test generation of simple request model."""
        generator = ModelGenerator()
        endpoint = Endpoint(path="/test", text="test", leaf=True, methods={}, children=[])

        method = Method(
            method="POST",
            name="create",
            description="Create test",
            parameters=[
                Parameter(name="name", type="string", description="Name field", optional=False),
                Parameter(
                    name="count",
                    type="integer",
                    description="Count field",
                    optional=True,
                    minimum=0,
                ),
            ],
            returns=Response(type="object"),
            protected=False,
        )

        model = generator._generate_request_model(endpoint, "POST", method)
        assert model is not None
        assert model.name == "TestPOSTRequest"
        assert len(model.fields) == 2

        # Check name field
        name_field = model.fields[0]
        assert name_field.name == "name"
        assert name_field.type_annotation == "str"

        # Check count field
        count_field = model.fields[1]
        assert count_field.name == "count"
        assert (
            count_field.type_annotation == "int | str | None"
        )  # Permissive union for Proxmox API compatibility
        assert "ge" in count_field.field_kwargs
        assert count_field.field_kwargs["ge"] == 0

    def test_generate_response_model_simple(self):
        """Test generation of simple response model."""
        generator = ModelGenerator()
        endpoint = Endpoint(path="/test", text="test", leaf=True, methods={}, children=[])

        method = Method(
            method="GET",
            name="get",
            description="Get test",
            parameters=[],
            returns=Response(type="object"),
            protected=False,
        )

        model = generator._generate_response_model(endpoint, "GET", method)
        assert model is not None
        assert model.name == "TestGETResponse"
        assert len(model.fields) == 1

        data_field = model.fields[0]
        assert data_field.name == "data"
        assert data_field.type_annotation == "dict[str, Any]"

    def test_generate_response_model_array(self):
        """Test generation of array response model."""
        generator = ModelGenerator()
        endpoint = Endpoint(path="/test", text="test", leaf=True, methods={}, children=[])

        method = Method(
            method="GET",
            name="list",
            description="List tests",
            parameters=[],
            returns=Response(type="array", items={"type": "string"}),
            protected=False,
        )

        model = generator._generate_response_model(endpoint, "GET", method)
        assert model is not None
        assert model.name == "TestGETResponse"

        data_field = model.fields[0]
        assert data_field.name == "data"
        assert data_field.type_annotation == "list[str]"

    def test_field_name_sanitization(self):
        """Test field name sanitization."""
        generator = ModelGenerator()

        # Test various invalid characters
        assert generator._sanitize_field_name("valid_name") == "valid_name"
        assert generator._sanitize_field_name("invalid-name") == "invalid_name"
        assert generator._sanitize_field_name("invalid.name") == "invalid_name"
        assert generator._sanitize_field_name("123invalid") == "field_123invalid"
        assert generator._sanitize_field_name("class") == "class_"  # Python keyword

    def test_model_name_generation(self):
        """Test model name generation."""
        generator = ModelGenerator()
        endpoint = Endpoint(path="/access/users", text="users", leaf=True, methods={}, children=[])

        # Test unique naming
        name1 = generator._generate_base_model_name(endpoint, "GET", "Request")
        name2 = generator._generate_base_model_name(endpoint, "POST", "Request")

        assert name1 != name2
        assert "Users" in name1
        assert "Request" in name1

    def test_enum_literal_generation(self):
        """Test enum values are converted to Literal types."""
        from generator.generators.type_mapper import TypeMapper

        mapper = TypeMapper()

        # Small enum should become Literal
        param_spec = {"type": "string", "enum": ["option1", "option2", "option3"]}

        type_annotation, field_kwargs = mapper.map_parameter_type(param_spec)
        assert "Literal[" in type_annotation
        assert '"option1"' in type_annotation
        assert '"option2"' in type_annotation
        assert '"option3"' in type_annotation

    def test_large_enum_handling(self):
        """Test large enums are handled as str type."""
        from generator.generators.type_mapper import TypeMapper

        mapper = TypeMapper()

        # Large enum should remain as str
        large_enum = [f"option{i}" for i in range(15)]
        param_spec = {"type": "string", "enum": large_enum}

        type_annotation, field_kwargs = mapper.map_parameter_type(param_spec)
        assert type_annotation == "str"
        # Large enums are not added to field_kwargs (Pydantic limitation)
        assert "enum" not in field_kwargs

    def test_constraint_mapping(self):
        """Test various constraint mappings."""
        from generator.generators.type_mapper import TypeMapper

        mapper = TypeMapper()

        # Integer with constraints
        param_spec = {
            "type": "integer",
            "minimum": 1,
            "maximum": 100,
        }

        type_annotation, field_kwargs = mapper.map_parameter_type(param_spec)
        assert type_annotation == "int | str"  # Permissive union for Proxmox API compatibility
        assert field_kwargs["ge"] == 1
        assert field_kwargs["le"] == 100

        # String with constraints
        param_spec = {
            "type": "string",
            "minLength": 5,
            "maxLength": 50,
            "pattern": r"^[a-z]+$",
        }

        type_annotation, field_kwargs = mapper.map_parameter_type(param_spec)
        assert type_annotation == "str"
        assert field_kwargs["min_length"] == 5
        assert field_kwargs["max_length"] == 50
        # Pattern validation is disabled due to regex compilation issues
        assert "pattern" not in field_kwargs

    def test_proxmox_format_mapping(self):
        """Test Proxmox custom format mappings."""
        from generator.generators.type_mapper import TypeMapper

        mapper = TypeMapper()

        # Test various Proxmox formats
        formats_to_test = {
            "pve-node": "ProxmoxNode",
            "pve-vmid": "ProxmoxVMID",
            "pve-storage-id": "str",
            "ipv4": "str",
            "mac-addr": "str",
        }

        for format_name, expected_type in formats_to_test.items():
            param_spec = {"type": "string", "format": format_name}
            type_annotation, field_kwargs = mapper.map_parameter_type(param_spec)
            assert type_annotation == expected_type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
