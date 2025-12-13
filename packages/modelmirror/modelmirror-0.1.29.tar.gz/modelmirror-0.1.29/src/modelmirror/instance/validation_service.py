from typing import Any, Type, TypeVar

from pydantic import validate_call

T = TypeVar("T")


class ValidationService:
    def validate_or_raise(self, cls: Type[T], params: dict[str, Any]) -> T:
        """
        Validate parameters against the __init__ signature of `cls` and
        return an instance of the ORIGINAL class (not a subclass).
        """
        instance = cls.__new__(cls)  # type: ignore[call-arg]
        validated_init = self.__create_validated_init(cls.__init__)
        validated_init(instance, **params)

        return instance

    def __create_validated_init(self, init_method):
        try:
            return validate_call(
                config={
                    "arbitrary_types_allowed": True,
                    "extra": "forbid",
                }
            )(init_method)
        except Exception:
            return init_method
