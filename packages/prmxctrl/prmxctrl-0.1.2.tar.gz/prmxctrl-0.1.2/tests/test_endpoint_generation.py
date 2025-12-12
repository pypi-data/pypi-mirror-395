"""
Tests for endpoint generation functionality.

Tests the EndpointGenerator class to ensure it creates proper hierarchical
endpoint classes with correct method signatures and navigation.
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generator.generators.endpoint_generator import EndpointGenerator
from generator.parse_schema import Endpoint, Method, Parameter, Response


class TestEndpointGeneratorFilePaths:
    """Test file path generation for endpoints."""

    def test_top_level_endpoint(self):
        """Test file path for top-level endpoint."""
        generator = EndpointGenerator()
        endpoint = Endpoint(path="/access", text="access", leaf=False, methods={}, children=[])
        result = generator._get_file_path(endpoint)
        assert result == "access.py"

    def test_nested_endpoint(self):
        """Test file path for nested endpoint."""
        generator = EndpointGenerator()
        endpoint = Endpoint(path="/access/users", text="users", leaf=False, methods={}, children=[])
        result = generator._get_file_path(endpoint)
        assert result == "access/users.py"

    def test_parameterized_endpoint(self):
        """Test file path for parameterized endpoint."""
        generator = EndpointGenerator()
        endpoint = Endpoint(
            path="/nodes/{node}",
            text="{node}",
            leaf=False,
            methods={},
            children=[],
            path_params=["node"],
        )
        result = generator._get_file_path(endpoint)
        assert result == "nodes/node_item/_item.py"

    def test_nested_parameterized_endpoint(self):
        """Test file path for deeply nested parameterized endpoint."""
        generator = EndpointGenerator()
        endpoint = Endpoint(
            path="/nodes/{node}/qemu/{vmid}",
            text="{vmid}",
            leaf=False,
            methods={},
            children=[],
            path_params=["node", "vmid"],
        )
        result = generator._get_file_path(endpoint)
        assert result == "nodes/node_item/qemu/vmid_item/_item.py"


class TestEndpointGeneratorClassNames:
    """Test class name generation for endpoints."""

    def test_single_path_component(self):
        """Test class name for single path component."""
        generator = EndpointGenerator()
        endpoint = Endpoint(path="/access", text="access", leaf=False, methods={}, children=[])
        result = generator._generate_class_name(endpoint)
        assert "Access" in result
        assert "Endpoints" in result

    def test_multi_component_path(self):
        """Test class name for multi-component path."""
        generator = EndpointGenerator()
        endpoint = Endpoint(path="/access/users", text="users", leaf=False, methods={}, children=[])
        result = generator._generate_class_name(endpoint)
        assert "AccessUsers" in result or "Users" in result
        assert "Endpoints" in result

    def test_hyphenated_path(self):
        """Test class name for hyphenated path."""
        generator = EndpointGenerator()
        endpoint = Endpoint(path="/api-docs", text="api-docs", leaf=False, methods={}, children=[])
        result = generator._generate_class_name(endpoint)
        assert "Endpoints" in result


class TestEndpointGeneratorMethods:
    """Test method generation for endpoints."""

    def test_get_method_generation(self):
        """Test generation of GET method."""
        generator = EndpointGenerator()
        endpoint = Endpoint(path="/access", text="access", leaf=True, methods={}, children=[])
        method = Method(
            method="GET",
            name="get_access",
            description="Get access",
            parameters=[],
            returns=Response(type="object"),
            protected=False,
        )

        result = generator._generate_method(endpoint, "GET", method)
        assert result is not None
        assert result["name"] == "get"
        assert result["http_method"] == "GET"

    def test_post_method_generation(self):
        """Test generation of POST method."""
        generator = EndpointGenerator()
        endpoint = Endpoint(path="/access/users", text="users", leaf=True, methods={}, children=[])
        method = Method(
            method="POST",
            name="create_user",
            description="Create user",
            parameters=[Parameter(name="username", type="string", description="Username")],
            returns=Response(type="object"),
            protected=False,
        )

        result = generator._generate_method(endpoint, "POST", method)
        assert result is not None
        assert result["name"] == "create_user"  # Method name from method.name
        assert result["http_method"] == "POST"
        # Note: param_model would be set if model_name_map was provided

    def test_delete_method_generation(self):
        """Test generation of DELETE method."""
        generator = EndpointGenerator()
        endpoint = Endpoint(
            path="/access/users/{userid}", text="{userid}", leaf=True, methods={}, children=[]
        )
        method = Method(
            method="DELETE",
            name="delete_user",
            description="Delete user",
            parameters=[],
            returns=Response(type="null"),
            protected=False,
        )

        result = generator._generate_method(endpoint, "DELETE", method)
        assert result is not None
        assert result["name"] == "delete"
        assert result["http_method"] == "DELETE"


class TestEndpointGeneratorProperties:
    """Test property generation for child endpoints."""

    def test_child_endpoint_property(self):
        """Test generation of property for child endpoint."""
        generator = EndpointGenerator()
        current = Endpoint(path="/access", text="access", leaf=False, methods={}, children=[])
        child = Endpoint(path="/access/users", text="users", leaf=False, methods={}, children=[])

        result = generator._generate_property(current, child)
        assert result is not None
        assert result["name"] == "users"
        assert "class" in result
        assert "path" in result


class TestEndpointGeneratorCallMethod:
    """Test __call__ method generation for parameterized endpoints."""

    def test_call_method_generation(self):
        """Test generation of __call__ method for path parameter."""
        generator = EndpointGenerator()
        endpoint = Endpoint(
            path="/nodes/{node}",
            text="{node}",
            leaf=False,
            methods={},
            children=[],
            path_params=["node"],
        )

        result = generator._generate_call_method(endpoint)
        assert result is not None
        assert result["param_name"] == "node"
        assert result["param_type"] == "str"

    def test_call_method_vmid_type(self):
        """Test that vmid parameter gets int type."""
        generator = EndpointGenerator()
        endpoint = Endpoint(
            path="/nodes/{node}/qemu/{vmid}",
            text="{vmid}",
            leaf=False,
            methods={},
            children=[],
            path_params=["node", "vmid"],
        )

        result = generator._generate_call_method(endpoint)
        assert result is not None
        assert result["param_name"] == "vmid"
        assert result["param_type"] == "int"


class TestEndpointFileGeneration:
    """Test complete endpoint file generation."""

    def test_generate_simple_endpoint_file(self):
        """Test generation of simple endpoint file."""
        generator = EndpointGenerator()
        endpoint = Endpoint(
            path="/access",
            text="access",
            leaf=False,
            methods={
                "GET": Method(
                    method="GET",
                    name="get_access",
                    description="Get access",
                    parameters=[],
                    returns=Response(type="object"),
                    protected=False,
                )
            },
            children=[],
        )

        files = generator.generate_endpoints([endpoint], {})
        assert len(files) > 0

        file = files[0]
        assert file.file_path == "access/__init__.py"
        assert len(file.classes) > 0
        assert "Endpoints" in file.classes[0].name

    def test_generate_hierarchical_endpoints(self):
        """Test generation of hierarchical endpoint structure."""
        generator = EndpointGenerator()

        # Create parent endpoint with child
        users_child = Endpoint(
            path="/access/users",
            text="users",
            leaf=False,
            methods={
                "GET": Method(
                    method="GET",
                    name="list",
                    description="List users",
                    parameters=[],
                    returns=Response(type="array"),
                    protected=False,
                )
            },
            children=[],
        )

        access_parent = Endpoint(
            path="/access", text="access", leaf=False, methods={}, children=[users_child]
        )

        files = generator.generate_endpoints([access_parent], {})

        # Should generate multiple files for hierarchical structure
        assert len(files) >= 1

        # Check file paths
        file_paths = [f.file_path for f in files]
        assert "access.py" in file_paths or "access/users.py" in file_paths


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
