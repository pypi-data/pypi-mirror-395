"""
Tests for Mirror class customization features: custom parsers and placeholders.
"""

import unittest
from typing import Any

from pydantic import BaseModel, ConfigDict

from modelmirror.mirror import Mirror
from modelmirror.parser.code_link_parser import CodeLink
from modelmirror.parser.default_code_link_parser import DefaultCodeLinkParser
from tests.fixtures.test_classes import DatabaseService, SimpleService, UserService


class CustomCodeLinkParser(DefaultCodeLinkParser):
    """Custom parser that uses @ symbol for instances: service@instance"""

    def _create_code_link(self, node: dict[str, Any]) -> CodeLink:
        raw_reference: str = node.pop(self._placeholder)
        params: dict[str, Any] = {name: prop for name, prop in node.items()}
        if "@" in raw_reference:
            id, instance = raw_reference.split("@", 1)
            return CodeLink(id=id, instance=f"${instance}", params=params)
        return CodeLink(id=raw_reference, instance=None, params=params)


class VersionedCodeLinkParser(DefaultCodeLinkParser):
    """Parser that requires version: service:v1.0@instance"""

    def _is_valid(self, node: dict[str, Any]) -> bool:
        if isinstance(node[self._placeholder], str):
            if ":" not in node[self._placeholder]:
                raise ValueError("Version required: use 'id:version' or 'id:version@instance'")
            return True
        raise ValueError(f"Value of '{self._placeholder}' must be a string")

    def _create_code_link(self, node: dict[str, Any]) -> CodeLink:
        raw_reference: str = node.pop(self._placeholder)
        params: dict[str, Any] = {name: prop for name, prop in node.items()}
        if "@" in raw_reference:
            id_version, instance = raw_reference.split("@", 1)
        else:
            id_version, instance = raw_reference, None

        id_part, version = id_version.split(":", 1)
        # For testing, we ignore version and just use id
        return CodeLink(id=id_part, instance=f"${instance}" if instance else None, params=params)


class TestConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    service: SimpleService


class TestMirrorCustomization(unittest.TestCase):
    """Test suite for Mirror customization features."""

    def setUp(self):
        """Set up test fixtures."""
        self.default_mirror = Mirror("tests.fixtures")

    def test_default_parser_and_placeholder(self):
        """Test that default parser and placeholder work correctly."""
        config = self.default_mirror.reflect("tests/configs/mirror_default.json", TestConfig)
        self.assertEqual(config.service.name, "default_test")

    def test_custom_placeholder(self):
        """Test Mirror with custom placeholder."""
        mirror = Mirror("tests.fixtures", code_link_parser=DefaultCodeLinkParser("$ref"))
        config = mirror.reflect("tests/configs/mirror_custom_placeholder.json", TestConfig)
        self.assertEqual(config.service.name, "custom_placeholder")

    def test_custom_parser_with_at_symbol(self):
        """Test Mirror with custom parser using @ for instances."""
        mirror = Mirror("tests.fixtures", code_link_parser=CustomCodeLinkParser(placeholder="$mirror"))

        class CustomConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            database: DatabaseService
            user_service: UserService

        config = mirror.reflect("tests/configs/mirror_custom_parser.json", CustomConfig)
        self.assertEqual(config.database.host, "localhost")
        self.assertTrue(config.user_service.cache_enabled)
        self.assertIs(config.user_service.database, config.database)

    def test_versioned_parser(self):
        """Test Mirror with versioned parser."""
        mirror = Mirror("tests.fixtures", code_link_parser=VersionedCodeLinkParser(placeholder="$mirror"))
        config = mirror.reflect("tests/configs/mirror_versioned.json", TestConfig)
        self.assertEqual(config.service.name, "versioned_service")

    def test_versioned_parser_with_instance(self):
        """Test versioned parser with instance."""
        mirror = Mirror("tests.fixtures", code_link_parser=VersionedCodeLinkParser(placeholder="$mirror"))

        class VersionedConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            database: DatabaseService
            user_service: UserService

        config = mirror.reflect("tests/configs/mirror_versioned_instance.json", VersionedConfig)
        self.assertEqual(config.database.host, "versioned.host")
        self.assertFalse(config.user_service.cache_enabled)
        self.assertIs(config.user_service.database, config.database)

    def test_custom_placeholder_and_parser_together(self):
        """Test Mirror with both custom placeholder and parser."""
        mirror = Mirror("tests.fixtures", code_link_parser=CustomCodeLinkParser(placeholder="$create"))

        class CombinedConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            service: SimpleService
            reference_test: dict

        config = mirror.reflect("tests/configs/mirror_combined.json", CombinedConfig)
        self.assertEqual(config.service.name, "combined_test")
        self.assertIs(config.reference_test["value"], config.service)

    def test_parser_validation_error(self):
        """Test that parser validation errors are properly raised."""
        mirror = Mirror("tests.fixtures", code_link_parser=VersionedCodeLinkParser(placeholder="$mirror"))

        with self.assertRaises(ValueError) as context:
            mirror.reflect("tests/configs/mirror_validation_error.json", TestConfig)

        self.assertIn("Version required", str(context.exception))

    def test_raw_reflection_with_custom_features(self):
        """Test raw reflection works with custom parser and placeholder."""
        mirror = Mirror("tests.fixtures", code_link_parser=CustomCodeLinkParser(placeholder="$build"))

        instances = mirror.reflect_raw("tests/configs/mirror_raw_custom.json")
        service = instances.get(SimpleService)
        self.assertEqual(service.name, "raw_test")

        # Test singleton retrieval
        shared_service = instances.get(SimpleService, "$shared")
        self.assertIs(service, shared_service)


if __name__ == "__main__":
    unittest.main()
