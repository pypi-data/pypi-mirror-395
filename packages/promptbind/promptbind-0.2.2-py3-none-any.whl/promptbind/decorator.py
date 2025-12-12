from collections.abc import Callable
from typing import Any
from functools import wraps
import inspect

from .container import PromptEntry
from .bank import register_and_check, get_prompt_entry
from .util import set_prompt_key, get_effective_prompt_key, set_is_promptbind_decorator


def has_self_or_cls(impl: Callable[..., Any]) -> bool:
    """
    Check if the first parameter of the function is 'self' or 'cls',
    indicating that it is likely a method of a class.
    """
    qualname: str = impl.__qualname__
    first_param: str | None = None
    code_varnames = impl.__code__.co_varnames
    if code_varnames:
        first_param = code_varnames[0]
    return qualname.count(".") >= 1 and first_param in ("self", "cls")


def dispatch_prompt_entry(func: Callable[..., Any]) -> PromptEntry:
    """
    Retrieve the PromptEntry associated with the given function at runtime,
    so that we could use __prompt_key_patch__ if it is set.

    Args:
        func (Callable): The function to retrieve the PromptEntry for.

    Returns:
        PromptEntry: The associated PromptEntry.
    """
    src_path: str = func.__code__.co_filename
    prompt_key: str | None = get_effective_prompt_key(func)
    assert prompt_key is not None, "Prompt key is not set for the function"
    return get_prompt_entry(src_path, prompt_key)


def _exposed_signature(impl: Callable[..., Any]) -> inspect.Signature:
    """
    Build a public-facing signature that hides the injected prompt parameter.

    The original implementation expects the PromptEntry as the first argument
    (after `self/cls` for methods). External callers should not see it.
    """
    sig = inspect.signature(impl)
    params = list(sig.parameters.values())
    if not params:
        return sig

    # For methods, drop the parameter after `self`/`cls`; otherwise drop the first.
    drop_index = 1 if has_self_or_cls(impl) and len(params) >= 2 else 0
    params.pop(drop_index)
    return sig.replace(parameters=params)


def with_prompt(key: str | None = None) -> Callable[..., Callable[..., Any]]:
    def decorator(impl: Callable[..., Any]) -> Callable[..., Any]:
        src_path: str = impl.__code__.co_filename
        qualname: str = impl.__qualname__
        register_key = key or qualname

        # Register and check the prompt key existence
        register_and_check(src_path, register_key)
        set_prompt_key(impl, register_key)
        # Wrap the implementation based on whether it's a method or a function
        if has_self_or_cls(impl):
            @wraps(impl)
            def wrapper_class(self_or_cls: Any, *args: Any, **kwargs: Any) -> Any:
                prompt = dispatch_prompt_entry(impl)
                return impl(self_or_cls, prompt, *args, **kwargs)

            set_is_promptbind_decorator(wrapper_class)
            wrapper_class.__signature__ = _exposed_signature(impl)
            return wrapper_class
        else:
            @wraps(impl)
            def wrapper_func(*args: Any, **kwargs: Any) -> Any:
                prompt = dispatch_prompt_entry(impl)
                return impl(prompt, *args, **kwargs)

            set_is_promptbind_decorator(wrapper_func)
            wrapper_func.__signature__ = _exposed_signature(impl)
            return wrapper_func

    return decorator


__all__ = ["with_prompt"]
