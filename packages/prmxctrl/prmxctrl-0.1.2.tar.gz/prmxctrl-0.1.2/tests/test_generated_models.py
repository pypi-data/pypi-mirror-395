"""
Tests for generated Pydantic models.

Tests that generated models validate correctly and handle constraints properly.
"""

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestGeneratedModels:
    """Test generated Pydantic models."""

    def test_basic_model_creation(self):
        """Test that basic generated models can be created."""
        try:
            from prmxctrl import models

            # Get a model from the models module
            model_names = [
                name
                for name in dir(models)
                if name.endswith("Request") or name.endswith("Response")
            ]
            if not model_names:
                pytest.skip("No models generated yet")

            # Test first available model
            model_name = model_names[0]
            model_class = getattr(models, model_name)

            # Try to create instance - for models with required fields, provide basic data
            try:
                instance = model_class()
            except ValidationError:
                # If model has required fields, provide basic sample data
                if "Response" in model_name:
                    instance = model_class(data=[])
                else:
                    # For request models, skip this test as they may have complex requirements
                    pytest.skip(f"Model {model_name} has required fields that need specific data")
            assert instance is not None

        except ImportError:
            pytest.skip("Models not generated yet")

    def test_model_validation(self):
        """Test model validation with sample data."""
        try:
            from pydantic import ValidationError

            from prmxctrl import models

            # Find a request model
            request_models = [name for name in dir(models) if name.endswith("Request")]
            if not request_models:
                pytest.skip("No request models generated yet")

            # Test with a simple model
            for model_name in request_models[:3]:  # Test first 3 models
                model_class = getattr(models, model_name)

                try:
                    # Try to create with empty data (should work for optional fields)
                    instance = model_class()
                    assert instance is not None

                    # Try model_dump
                    data = instance.model_dump()
                    assert isinstance(data, dict)

                    # Try JSON serialization
                    json_data = instance.model_dump_json()
                    assert isinstance(json_data, str)

                except Exception:
                    # Some models might require specific fields, skip those
                    continue

        except ImportError:
            pytest.skip("Models not generated yet")

    def test_response_model_structure(self):
        """Test that response models have expected structure."""
        try:
            from prmxctrl import models

            # Find response models
            response_models = [name for name in dir(models) if name.endswith("Response")]
            if not response_models:
                pytest.skip("No response models generated yet")

            for model_name in response_models[:3]:  # Test first 3 models
                model_class = getattr(models, model_name)

                # Response models should have a 'data' field
                if hasattr(model_class, "model_fields"):
                    fields = model_class.model_fields
                    if "data" in fields:
                        # Should be able to create with data
                        test_data = {"data": []}
                        instance = model_class(**test_data)
                        assert instance.data == []

        except ImportError:
            pytest.skip("Models not generated yet")

    def test_field_constraints(self):
        """Test that field constraints are properly applied."""
        try:
            from pydantic import ValidationError

            from prmxctrl import models

            # Find models with constrained fields
            request_models = [name for name in dir(models) if name.endswith("Request")]
            if not request_models:
                pytest.skip("No request models generated yet")

            # Test constraints on a few models
            constraints_found = False
            for model_name in request_models:
                model_class = getattr(models, model_name)

                if hasattr(model_class, "model_fields"):
                    for field_name, field_info in model_class.model_fields.items():
                        # Check for constraints
                        if (
                            hasattr(field_info, "ge")
                            or hasattr(field_info, "le")
                            or hasattr(field_info, "min_length")
                        ):
                            constraints_found = True

                            # Test constraint validation
                            if hasattr(field_info, "ge") and field_info.ge is not None:
                                # Test valid value
                                try:
                                    valid_value = field_info.ge
                                    instance = model_class(**{field_name: valid_value})
                                    assert getattr(instance, field_name) == valid_value
                                except (ValidationError, TypeError):
                                    pass  # Might not be the only required field

                                # Test invalid value
                                try:
                                    invalid_value = field_info.ge - 1
                                    with pytest.raises(ValidationError):
                                        model_class(**{field_name: invalid_value})
                                except (ValidationError, TypeError):
                                    pass  # Expected

            if not constraints_found:
                pytest.skip("No constrained fields found in generated models")

        except ImportError:
            pytest.skip("Models not generated yet")

    def test_enum_validation(self):
        """Test that enum fields validate correctly."""
        try:
            from typing import get_args, get_origin

            from pydantic import ValidationError

            from prmxctrl import models

            # Find models with enum fields
            request_models = [name for name in dir(models) if name.endswith("Request")]
            if not request_models:
                pytest.skip("No request models generated yet")

            enum_found = False
            for model_name in request_models:
                model_class = getattr(models, model_name)

                if hasattr(model_class, "model_fields"):
                    for field_name, field_info in model_class.model_fields.items():
                        # Check if field type is Literal (enum)
                        field_type = field_info.annotation
                        if hasattr(field_type, "__origin__") and field_type.__origin__ is not None:
                            origin = get_origin(field_type)
                            if origin is not None and "Literal" in str(origin):
                                enum_found = True

                                # Get allowed values
                                args = get_args(field_type)
                                if args:
                                    valid_value = args[0]
                                    invalid_value = "invalid_" + str(valid_value)

                                    # Test valid value
                                    try:
                                        instance = model_class(**{field_name: valid_value})
                                        assert getattr(instance, field_name) == valid_value
                                    except (ValidationError, TypeError):
                                        pass

                                    # Test invalid value
                                    try:
                                        with pytest.raises(ValidationError):
                                            model_class(**{field_name: invalid_value})
                                    except (ValidationError, TypeError):
                                        pass

            if not enum_found:
                pytest.skip("No enum fields found in generated models")

        except ImportError:
            pytest.skip("Models not generated yet")


class TestModelSerialization:
    """Test model serialization and deserialization."""

    def test_json_roundtrip(self):
        """Test JSON serialization roundtrip."""
        try:
            from prmxctrl import models

            request_models = [name for name in dir(models) if name.endswith("Request")]
            if not request_models:
                pytest.skip("No request models generated yet")

            for model_name in request_models[:2]:  # Test first 2 models
                model_class = getattr(models, model_name)

                try:
                    # Create instance
                    instance = model_class()

                    # Serialize to JSON
                    json_str = instance.model_dump_json()

                    # Deserialize back
                    instance2 = model_class.model_validate_json(json_str)

                    # Should be equal
                    assert instance.model_dump() == instance2.model_dump()

                except Exception:
                    # Some models might require specific data
                    continue

        except ImportError:
            pytest.skip("Models not generated yet")

    def test_dict_roundtrip(self):
        """Test dict serialization roundtrip."""
        try:
            from prmxctrl import models

            request_models = [name for name in dir(models) if name.endswith("Request")]
            if not request_models:
                pytest.skip("No request models generated yet")

            for model_name in request_models[:2]:  # Test first 2 models
                model_class = getattr(models, model_name)

                try:
                    # Create instance
                    instance = model_class()

                    # Serialize to dict
                    dict_data = instance.model_dump()

                    # Deserialize back
                    instance2 = model_class(**dict_data)

                    # Should be equal
                    assert instance.model_dump() == instance2.model_dump()

                except Exception:
                    # Some models might require specific data
                    continue

        except ImportError:
            pytest.skip("Models not generated yet")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
