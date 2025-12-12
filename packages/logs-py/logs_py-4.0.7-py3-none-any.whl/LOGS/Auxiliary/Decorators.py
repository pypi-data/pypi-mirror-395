import types
from typing import Any, Callable, List, Type, TypeVar, Union, cast

TClass = TypeVar("TClass", bound=Callable[..., Any])


class InitConstructor:
    def _set_new_attribute(self, name, value):
        # Never overwrites an existing attribute.  Returns True if the
        # attribute already exists.
        if name in self.__dict__:
            return True
        setattr(self, name, value)
        return False

    def _new_constructor(self):
        print("New Constructor")

    def __call__(self, classInput: TClass) -> TClass:
        print(classInput.__class__)
        c = cast(Type, classInput)

        print(c.__init__.__code__.co_varnames)
        print(c.__init__.__defaults__)
        print(c.__init__.__code__)

        constructor = types.FunctionType(self._new_constructor.__code__, {})

        return classInput


class Endpoint:
    def __init__(self, path: Union[List[str], str]) -> None:
        self.path = [path] if isinstance(path, str) else path

    def __call__(self, classInput: TClass) -> TClass:
        from LOGS.Entity.ConnectedEntity import ConnectedEntity
        from LOGS.Entity.EntityConnector import EntityConnector

        if not isinstance(classInput, type) or not issubclass(
            classInput, (ConnectedEntity, EntityConnector)
        ):
            raise Exception(
                "%s decorator expect %a or %a type. (got type %a)"
                % (
                    Endpoint.__name__,
                    ConnectedEntity.__name__,
                    EntityConnector.__name__,
                    classInput.__name__,
                )
            )

        classInput._endpoint = self.path

        return cast(TClass, classInput)


class UiEndpoint:
    def __init__(self, path: Union[List[str], str]) -> None:
        self.path = [path] if isinstance(path, str) else path

    def __call__(self, classInput: TClass) -> TClass:
        from LOGS.Entity.ConnectedEntity import ConnectedEntity

        if not isinstance(classInput, type) or not issubclass(
            classInput, (ConnectedEntity)
        ):
            raise Exception(
                "%s decorator expect %a  type. (got type %a)"
                % (Endpoint.__name__, ConnectedEntity.__name__, classInput.__name__)
            )

        classInput._uiEndpoint = self.path

        return cast(TClass, classInput)


class FullModel:
    def __init__(self, fullEntity: Any) -> None:
        self.fullEntity = fullEntity

    def __call__(self, classInput: TClass) -> TClass:
        if hasattr(classInput, "_fullEntityType"):
            setattr(classInput, "_fullEntityType", self.fullEntity)
        if hasattr(self.fullEntity, "_endpoint") and hasattr(classInput, "_endpoint"):
            setattr(classInput, "_endpoint", getattr(self.fullEntity, "_endpoint"))

        return classInput


# --- Example for typed function decorator ---
# TFun = TypeVar("TFun", bound=Callable[..., Any])

# class FunctionDecorator:
#     def __init__(self, path: Union[List[str], str]) -> None:
#         self.path = [path] if isinstance(path, str) else path

#     def __call__(self, func: TFun) -> TFun:
#         path = self.path

#         @wraps(func)
#         def wrapper(*args, **kwargs) -> Any:
#             # if isclass(classInput) and issubclass(classInput, ConnectedContent):
#             #     cast(ConnectedContent, classInput)._endpoint = path
#             if hasattr(func, "_endpoint"):
#                 setattr(func, "_endpoint", path)
#             return func(*args, **kwargs)

#         return cast(TFun, wrapper)
