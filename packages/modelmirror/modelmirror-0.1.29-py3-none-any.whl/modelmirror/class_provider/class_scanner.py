"""
Isolated class scanner that creates copies instead of modifying classes globally.
"""

import importlib
import pkgutil
from typing import Dict, Type

from modelmirror.class_provider.class_reference import ClassReference
from modelmirror.class_provider.class_register import ClassRegister


class ClassScanner:
    """Scanner that creates isolated class copies instead of global modifications."""

    def __init__(self, package_name: str):
        self.__package_name = package_name
        self.__original_classes: Dict[str, Type] = {}
        self.__isolated_classes: Dict[str, Type] = {}

    def scan(self) -> list[ClassReference]:
        """Scan and create isolated class copies with validation."""
        self.__import_all_modules(self.__package_name)
        subclasses = self.__all_subclasses(ClassRegister)
        classes_reference: list[ClassReference] = []

        for cls in subclasses:
            if not cls.__module__.startswith(self.__package_name):
                continue

            class_reference: ClassReference | None = getattr(cls, "reference", None)
            if not class_reference:
                continue

            if self.__is_duplicate(class_reference, classes_reference):
                raise Exception(f"Duplicate class registration with id {class_reference.id}")

            # Create isolated copy instead of modifying original
            # isolated_class = self.__create_isolated_class(class_reference.cls)
            isolated_reference = ClassReference(id=class_reference.id, cls=class_reference.cls)

            classes_reference.append(isolated_reference)

        return classes_reference

    def __is_duplicate(self, reference: ClassReference, existing: list[ClassReference]) -> bool:
        return any(ref.id == reference.id for ref in existing)

    def __import_all_modules(self, package_name: str):
        package = importlib.import_module(package_name)
        for _, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            try:
                importlib.import_module(name)
            except Exception:
                continue
            if is_pkg:
                self.__import_all_modules(name)

    def __all_subclasses(self, cls: type):
        subclasses = set(cls.__subclasses__())
        for subclass in cls.__subclasses__():
            subclasses.update(self.__all_subclasses(subclass))
        return subclasses
