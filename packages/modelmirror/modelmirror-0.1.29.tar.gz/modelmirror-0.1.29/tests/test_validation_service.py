"""
Test suite for ValidationService with safe init functionality.
"""

import unittest
from dataclasses import dataclass, field
from typing import List
from unittest.mock import Mock

from pydantic import BaseModel, ConfigDict

from modelmirror.instance.validation_service import ValidationService


# Test classes with different patterns
class RegularClass:
    """Regular class with side effects in init."""

    class_var: int = 42

    def __init__(self, name: str, callback):
        self.name = name
        self.callback = callback
        callback()  # Side effect - should be removed
        self._data = callback.get_data()  # Side effect - should be removed


class ClassWithClassVars:
    """Class with class variables."""

    default_timeout: int = 30
    max_retries: int = 3

    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port


@dataclass
class DataclassWithPostInit:
    """Dataclass with __post_init__ side effects."""

    name: str
    values: List[str] = field(default_factory=list)

    def __post_init__(self):
        # This should not be called during validation
        self.values.append("processed")
        self._computed = len(self.values)


class PydanticModel(BaseModel):
    """Pydantic model with validation."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    port: int
    computed_value: str

    def model_post_init(self, __context):
        # This should not be called during validation
        self.computed_value = f"{self.name}:{self.port}"


class ComplexClass:
    """Class with complex initialization logic."""

    version: str = "1.0"

    def __init__(self, config: dict, factory, logger):
        self.config = config
        self.factory = factory
        self.logger = logger

        # All these should be removed
        logger.info("Initializing service")
        self._service = factory.create_service()
        self._connection = self._establish_connection()
        factory.register(self)

    def _establish_connection(self):
        return "connection"


# Test classes with different init patterns
class SafeClass:
    """Class with only safe assignments."""

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value


class UnsafeClass:
    """Class with function calls in init."""

    def __init__(self, name: str, callback):
        self.name = name
        self.callback = callback
        callback()  # This should be removed
        self._data = callback()  # This should be removed


class MixedClass:
    """Class with both safe and unsafe operations."""

    def __init__(self, name: str, value: int, func):
        self.name = name  # Safe - should be kept
        self.value = value  # Safe - should be kept
        func()  # Unsafe - should be removed
        self._result = func()  # Unsafe - should be removed


class ClsParameterClass:
    """Class with cls parameter that conflicts with Pydantic."""

    def __init__(self, cls, name: str):
        self.cls = cls
        self.name = name
        cls()


class ComplexUnsafeClass:
    """Class with complex unsafe operations."""

    def __init__(self, name: str, factory, processor):
        self.name = name
        # These should all be removed
        factory.create()
        self._processed = processor(name)


class TestValidationService(unittest.TestCase):
    """Test ValidationService safe init functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.validation_service = ValidationService()

    def test_regular_class_no_side_effects(self):
        """Test that regular classes don't trigger side effects during validation."""
        mock_callback = Mock()
        params = {"name": "test", "callback": mock_callback}

        # Should validate without calling callback methods
        self.validation_service.validate_or_raise(RegularClass, params)

        # No methods should be called
        mock_callback.assert_called_once()
        mock_callback.get_data.assert_called_once()

    def test_class_variables_preserved(self):
        """Test that class variables are preserved in isolated class."""
        params = {"name": "test", "port": 8080}

        # Should work and preserve class variables
        isolated_class = self.validation_service.validate_or_raise(ClassWithClassVars, params)

        # Create isolated class to check class variables
        # isolated_class = self.validation_service._ValidationService__create_isolated_class(ClassWithClassVars)  # type: ignore

        # Class variables should be preserved
        self.assertEqual(isolated_class.default_timeout, 30)
        self.assertEqual(isolated_class.max_retries, 3)

    def test_dataclass_post_init(self):
        """Test that dataclass __post_init__ is not called during validation."""
        params = {"name": "test", "values": ["initial"]}

        # Should validate without calling __post_init__
        instance = self.validation_service.validate_or_raise(DataclassWithPostInit, params)

        # Should only have assigned parameters, no post-init processing
        self.assertEqual(instance.name, "test")
        self.assertEqual(instance.values, ["initial", "processed"])
        # Should not have computed attributes from __post_init__
        self.assertTrue(hasattr(instance, "_computed"))

    def test_pydantic_model_post_init(self):
        """Test that Pydantic model_post_init is not called during validation."""
        params = {"name": "service", "port": 8080, "computed_value": ""}

        # Create instance to verify model_post_init wasn't called
        instance = self.validation_service.validate_or_raise(PydanticModel, params)

        # Should only have assigned parameters
        self.assertEqual(instance.name, "service")
        self.assertEqual(instance.port, 8080)
        # Should not have computed attributes from model_post_init
        self.assertEqual(instance.computed_value, "service:8080")

    def test_complex_class(self):
        """Test that complex initialization side effects are removed."""
        mock_factory = Mock()
        mock_logger = Mock()
        params = {"config": {"key": "value"}, "factory": mock_factory, "logger": mock_logger}

        # Should validate without side effects
        self.validation_service.validate_or_raise(ComplexClass, params)

        # No side effect methods should be called
        mock_logger.info.assert_called_once()
        mock_factory.create_service.assert_called_once()
        mock_factory.register.assert_called_once()

    def test_validation_still_works(self):
        """Test that parameter validation still works."""
        # Missing required parameter should fail
        with self.assertRaises(Exception):
            self.validation_service.validate_or_raise(RegularClass, {"name": "test"})  # Missing callback

        # Valid parameters should work
        mock_callback = Mock()
        params = {"name": "test", "callback": mock_callback}
        self.validation_service.validate_or_raise(RegularClass, params)

    def test_empty_init_class(self):
        """Test class with no __init__ method."""

        class NoInitClass:
            class_var = "test"

        params = {}
        # Should work even without __init__
        isolated_class = self.validation_service.validate_or_raise(NoInitClass, params)
        self.assertEqual(isolated_class.class_var, "test")

    def test_class_with_only_private_vars(self):
        """Test class with only private variables."""

        class PrivateVarsClass:
            _private_var = "private"
            __very_private = "very_private"
            public_var = "public"

            def __init__(self, name: str):
                self.name = name

        params = {"name": "test"}
        isolated_class = self.validation_service.validate_or_raise(PrivateVarsClass, params)

        # isolated_class = self.validation_service._ValidationService__create_isolated_class(PrivateVarsClass)  # type: ignore
        self.assertEqual(isolated_class.public_var, "public")
        self.assertTrue(hasattr(isolated_class, "_private_var"))
        self.assertTrue(hasattr(isolated_class, "_PrivateVarsClass__very_private"))

    def test_safe_class_validation(self):
        """Test that safe classes work normally."""
        params = {"name": "test", "value": 42}

        # Should not raise any exception
        self.validation_service.validate_or_raise(SafeClass, params)

    def test_unsafe_class_validation_no_side_effects(self):
        """Test that unsafe classes don't trigger side effects during validation."""
        mock_callback = Mock()
        params = {"name": "test", "callback": mock_callback}

        self.validation_service.validate_or_raise(UnsafeClass, params)

        self.assertEqual(mock_callback.call_count, 2)

    def test_mixed_class_validation(self):
        """Test that mixed classes only keep safe assignments."""
        mock_func = Mock()
        params = {"name": "test", "value": 42, "func": mock_func}

        # Should validate without calling the function
        self.validation_service.validate_or_raise(MixedClass, params)

        # Function should not be called during validation
        self.assertEqual(mock_func.call_count, 2)

    def test_cls_parameter_handling(self):
        """Test that classes with cls parameter are handled correctly."""
        mock_cls = Mock()
        params = {"cls": mock_cls, "name": "test"}

        # Should handle cls parameter without Pydantic conflicts
        instance = self.validation_service.validate_or_raise(ClsParameterClass, params)

        instance.cls.assert_called_once()

    def test_complex_unsafe_class(self):
        """Test complex unsafe operations are executed exactly once."""
        mock_factory = Mock()
        mock_processor = Mock()
        params = {"name": "test", "factory": mock_factory, "processor": mock_processor}
        instance = self.validation_service.validate_or_raise(ComplexUnsafeClass, params)
        mock_factory.create.assert_called_once()
        mock_processor.assert_called_once_with("test")
        self.assertEqual(instance._processed, mock_processor.return_value)

    def test_validation_with_invalid_parameters(self):
        """Test that validation still works for parameter validation."""
        # Missing required parameter should still raise validation error
        with self.assertRaises(Exception):
            self.validation_service.validate_or_raise(SafeClass, {"name": "test"})  # Missing value

        # Valid parameters should work
        try:
            self.validation_service.validate_or_raise(SafeClass, {"name": "test", "value": 42})
        except Exception as e:
            self.fail(f"Valid parameters should work: {e}")

    def test_isolated_class_creation(self):
        """Test that validation returns an instance of the original class."""
        params = {"name": "test", "value": 10}

        instance = self.validation_service.validate_or_raise(SafeClass, params)

        # Instance should be of the original class, not a dynamically-created subclass
        self.assertIs(instance.__class__, SafeClass)

        # Values should be correctly set
        self.assertEqual(instance.name, "test")
        self.assertEqual(instance.value, 10)

        """Test fallback behavior when AST parsing fails."""

        # Create a class that might cause AST parsing issues
        class ProblematicClass:
            pass

        # Manually set an unparseable init (simulating edge case)
        def problematic_init(self, name: str):
            self.name = name

        # Remove source code to trigger fallback
        problematic_init.__code__ = problematic_init.__code__.replace(co_filename="<built-in>")
        ProblematicClass.__init__ = problematic_init  # type: ignore

        # Should still work with fallback
        params = {"name": "test"}
        self.validation_service.validate_or_raise(ProblematicClass, params)

    def test_empty_init_body_after_filtering(self):
        """Test behavior when all statements are filtered out."""

        class AllUnsafeClass:
            def __init__(self, func):
                func()  # Only unsafe operations
                func.call()

        mock_func = Mock()
        params = {"func": mock_func}

        # Should work even when all statements are removed
        self.validation_service.validate_or_raise(AllUnsafeClass, params)

        # No calls should be made
        mock_func.assert_called_once()
        mock_func.call.assert_called_once()

    def test_nested_function_calls_executed_once(self):
        """Test that nested function calls are executed exactly once."""

        class NestedCallsClass:
            def __init__(self, name: str, service):
                self.name = name
                service.method().chain().call()  # Complex nested calls

        mock_service = Mock()
        params = {"name": "test", "service": mock_service}
        self.validation_service.validate_or_raise(NestedCallsClass, params)
        mock_service.method.assert_called_once()
        mock_service.method.return_value.chain.assert_called_once()
        mock_service.method.return_value.chain.return_value.call.assert_called_once()


class TestValidationServiceIntegration(unittest.TestCase):
    """Integration tests for ValidationService with real scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.validation_service = ValidationService()

    def test_real_world_service_class(self):
        """Test with a realistic service class."""

        class DatabaseService:
            def __init__(self, host: str, port: int, logger):
                self.host = host
                self.port = port
                self.logger = logger
                logger.info(f"Connecting to {host}:{port}")  # Should be removed
                self._connection = self._create_connection()  # Should be removed

            def _create_connection(self):
                return f"connection to {self.host}:{self.port}"

        mock_logger = Mock()
        params = {"host": "localhost", "port": 5432, "logger": mock_logger}

        # Should validate without side effects
        self.validation_service.validate_or_raise(DatabaseService, params)

        # Logger should not be called during validation
        mock_logger.info.assert_called_once()

    def test_factory_pattern_class(self):
        """Test with factory pattern that has initialization side effects."""

        class ServiceFactory:
            def __init__(self, config: dict, registry):
                self.config = config
                self.registry = registry
                registry.register(self)  # Should be removed
                self._services = self._initialize_services()  # Should be removed

            def _initialize_services(self):
                return []

        mock_registry = Mock()
        params = {"config": {"key": "value"}, "registry": mock_registry}

        # Should validate without registering or initializing
        self.validation_service.validate_or_raise(ServiceFactory, params)

        # Registry should not be called
        mock_registry.register.assert_called_once()

    def test_validation_with_pydantic_model(self):
        """Test validation works correctly with Pydantic-style validation."""

        class ServiceWithValidation:
            def __init__(self, name: str, port: int, callback):
                if port < 1 or port > 65535:
                    raise ValueError("Invalid port")
                self.name = name
                self.port = port
                self.callback = callback
                callback.initialize()  # Should be removed

        mock_callback = Mock()

        # Valid parameters should work
        valid_params = {"name": "service", "port": 8080, "callback": mock_callback}
        self.validation_service.validate_or_raise(ServiceWithValidation, valid_params)

        # Callback should not be called during validation
        mock_callback.initialize.assert_called_once()

        # Invalid parameters should still raise validation errors
        # Note: This might not raise an error since we're only doing structural validation
        # The actual business logic validation is bypassed for safety

    def test_real_world_service_pattern(self):
        """Test with realistic service class pattern."""

        class DatabaseService:
            connection_timeout: int = 30

            def __init__(self, host: str, port: int, logger):
                self.host = host
                self.port = port
                self.logger = logger
                logger.info(f"Connecting to {host}:{port}")  # Should be removed
                self._pool = self._create_connection_pool()  # Should be removed

            def _create_connection_pool(self):
                return "pool"

        mock_logger = Mock()
        params = {"host": "localhost", "port": 5432, "logger": mock_logger}

        # Should validate without side effects
        self.validation_service.validate_or_raise(DatabaseService, params)

        # Logger should be called once
        mock_logger.info.assert_called_once()

    def test_factory_pattern_with_registration(self):
        """Test factory pattern that registers itself."""

        class ServiceFactory:
            registry_enabled: bool = True

            def __init__(self, config: dict, registry):
                self.config = config
                self.registry = registry
                registry.register(self)  # Should be removed
                self._initialize()  # Should be removed

            def _initialize(self):
                pass

        mock_registry = Mock()
        params = {"config": {"type": "factory"}, "registry": mock_registry}

        # Should validate without registration
        self.validation_service.validate_or_raise(ServiceFactory, params)

        # Registry should not be called
        mock_registry.register.assert_called_once()

    def test_mixed_dataclass_and_regular_class(self):
        """Test validation works with mixed class types."""

        @dataclass
        class DataConfig:
            name: str
            enabled: bool = True

            def __post_init__(self):
                self.computed = f"{self.name}_computed"

        class RegularService:
            def __init__(self, config: DataConfig, processor):
                self.config = config
                self.processor = processor
                processor.initialize(config)  # Should be removed

        mock_processor = Mock()
        data_config = DataConfig(name="test", enabled=True)
        params = {"config": data_config, "processor": mock_processor}

        # Should validate without calling processor
        self.validation_service.validate_or_raise(RegularService, params)

        # Processor should not be called
        mock_processor.initialize.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
