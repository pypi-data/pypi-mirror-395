from typing import Any
from collections.abc import Callable

def flatten_nested_dict(
    nested_dict: dict[str, Any], 
    separator: str = '.', 
    prefix: str = ''
) -> dict[str, Any]:
    """
    Flattens a nested dictionary into a single-level dictionary using a specific separator.

    This function recursively traverses the dictionary. If a value is a dictionary,
    it continues to flatten it, concatenating the keys.

    Args:
        nested_dict (dict[str, Any]): The source dictionary to be flattened.
        separator (str): The delimiter used to join keys. Defaults to '_'.
        prefix (str): The prefix for the current recursion level (used internally).

    Returns:
        dict[str, Any]: A flat dictionary with concatenated keys.
    """
    # Initialize the result dictionary
    flat_dict: dict[str, Any] = {}

    # Iterate through each key-value pair in the current dictionary level
    for key, value in nested_dict.items():
        assert isinstance(key, str), "All keys must be strings"
        # Construct the new composite key
        new_key = f"{prefix}{separator}{key}" if prefix else key

        if isinstance(value, dict):
            # If the value is a dictionary, recurse deeper
            # Merge the results from the child dictionary into the main flat_dict
            flat_dict.update(flatten_nested_dict(value, separator, new_key))
        else:
            # Base case: value is not a dict, add it to the result
            flat_dict[new_key] = value

    return flat_dict


def deep_get(nested_dict: dict[str, Any], key_path: list[str]) -> Any:
    """
    Retrieve a value from a nested dictionary using a list of keys representing the path.

    Args:
        nested_dict (dict[str, Any]): The source nested dictionary.
        key_path (list[str]): A list of keys representing the path to the desired value.

    Returns:
        Any: The value found at the specified path, or None if any key is not found.
    """
    current_level = nested_dict
    for key in key_path:
        assert isinstance(current_level, dict), "Current level is not a dictionary"
        assert key in current_level, f"Key '{key}' not found in the current level"
        current_level = current_level[key]
    return current_level

PROMPT_KEY = '__prompt_key__'
PROMPT_KEY_PATCH = '__prompt_key_patch__'
PROMPT_BIND_DECORATOR = '__is_promptbind_decorator__'

def set_prompt_key(func: Callable, prompt_key: str) -> None:
    f"""
    Sets a custom attribute {PROMPT_KEY} on the given function.

    Args:
        func (Callable): The function to set the attribute on.
        prompt_key (str): The prompt key to be set as an attribute.
    """
    setattr(func, PROMPT_KEY, prompt_key)


def get_prompt_key(func: Callable) -> str | None:
    f"""
    Retrieves the custom attribute {PROMPT_KEY} from the given function.

    Args:
        func (Callable): The function to retrieve the attribute from.

    Returns:
        str | None: The prompt key if it exists, otherwise None.
    """
    return getattr(func, PROMPT_KEY, None)


def set_prompt_key_patch(func: Callable, prompt_key: str) -> None:
    f"""
    Sets a custom attribute {PROMPT_KEY_PATCH} on the given function.

    Args:
        func (Callable): The function to set the attribute on.
        prompt_key (str): The prompt key to be set as an attribute.
    """
    if (raw_func := getattr(func, "__wrapped__", None)) and getattr(func, PROMPT_BIND_DECORATOR, False):
        setattr(raw_func, PROMPT_KEY_PATCH, prompt_key)
    else:
        setattr(func, PROMPT_KEY_PATCH, prompt_key)


def get_prompt_key_patch(func: Callable) -> str | None:
    f"""
    Retrieves the custom attribute {PROMPT_KEY_PATCH} from the given function.

    Args:
        func (Callable): The function to retrieve the attribute from.

    Returns:
        str | None: The prompt key if it exists, otherwise None.
    """
    return getattr(func, PROMPT_KEY_PATCH, None)


def unset_prompt_key_patch(func: Callable) -> None:
    f"""
    Removes the custom attribute {PROMPT_KEY_PATCH} from the given function if it exists.

    Args:
        func (Callable): The function to remove the attribute from.
    """
    if hasattr(func, PROMPT_KEY_PATCH):
        delattr(func, PROMPT_KEY_PATCH)
    if (raw_func := getattr(func, "__wrapped__", None)) and getattr(func, PROMPT_BIND_DECORATOR, True):
        unset_prompt_key_patch(raw_func)


def get_effective_prompt_key(func: Callable) -> str | None:
    """
    Retrieves the effective prompt key from the function, prioritizing the patch key.

    Args:
        func (Callable): The function to retrieve the prompt key from.

    Returns:
        str | None: The effective prompt key if it exists, otherwise None.
    """
    patch_key = get_prompt_key_patch(func)
    if patch_key is not None:
        return patch_key
    return get_prompt_key(func)


def set_is_promptbind_decorator(wrapped: Callable) -> None:
    """
    Marks the wrapped function as a PromptBind decorator by setting a custom attribute.

    Args:
        wrapped (Callable): The function to be marked.
        impl (Callable): The original implementation function.
    """
    setattr(wrapped, PROMPT_BIND_DECORATOR, True)