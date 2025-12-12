import inspect
from typing import Any, Type

from pydantic import validate_call


class ValidationService:
    def validate_or_raise(self, cls: type, params: dict[str, Any]) -> None:
        try:
            isolated_class = self.__create_isolated_class(cls)
            isolated_class(**params)
        except Exception as e:
            raise e

    def __create_isolated_class(self, original_class: Type) -> Type:
        """Create an isolated copy of the class with validation."""
        class_name = f"Isolated{original_class.__name__}"

        # Create isolated class with validation
        class IsolatedClass(original_class):
            pass

        IsolatedClass.__name__ = class_name
        IsolatedClass.__qualname__ = class_name

        init_method = original_class.__init__
        if init_method:
            validated_init = self.__create_validated_init(init_method)
            setattr(IsolatedClass, "__init__", validated_init)

        return IsolatedClass

    def __create_validated_init(self, init_method):
        """Create a validated init method, handling cls parameter conflicts."""
        sig = inspect.signature(init_method)

        # Check if 'cls' parameter exists (excluding 'self')
        has_cls_param = "cls" in [p.name for p in sig.parameters.values() if p.name != "self"]

        if has_cls_param:
            # Skip validation for methods with cls parameter to avoid Pydantic conflicts
            return init_method
        else:
            # No cls parameter, use validation
            return validate_call(config={"arbitrary_types_allowed": True, "extra": "forbid"})(init_method)
