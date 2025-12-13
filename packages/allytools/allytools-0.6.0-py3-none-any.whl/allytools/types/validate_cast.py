from typing import Any, Type, TypeVar, overload
import importlib

T = TypeVar("T")

@overload
def validate_cast(obj: Any, target: Type[T]) -> T: ...
@overload
def validate_cast(obj: Any, target: str) -> T: ...

def validate_cast(obj: Any, target: Type[T] | str) -> T:
    # resolve target type (supports "pkg.mod:Name" or "pkg.mod.Name")
    if isinstance(target, str):
        mod_path, sep, name = target.partition(":")
        if not sep:
            mod_path, _, name = target.rpartition(".")
        if not mod_path or not name:
            raise TypeError(f"Invalid target string {target!r}")
        mod = importlib.import_module(mod_path)
        typ: Type[T] = getattr(mod, name)
    else:
        typ = target

    # runtime check (works for classes and @runtime_checkable Protocols)
    try:
        ok = isinstance(obj, typ)  # type: ignore[arg-type]
    except TypeError:
        ok = True  # non-runtime-checkable Protocol → skip strict check

    if not ok:
        raise TypeError(f"{type(obj).__name__} is not instance of {getattr(typ, '__name__', typ)!r}")

    return obj