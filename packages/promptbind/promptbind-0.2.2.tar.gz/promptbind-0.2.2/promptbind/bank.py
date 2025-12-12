import toml

from pathlib import Path
from typing import Any

from .container import PromptEntry
from .util import flatten_nested_dict, deep_get


_prompt_bank: dict[str, dict[str, PromptEntry]] = {}


def _get_prompt_file(py_file: str|Path) -> dict[str, PromptEntry]:
    py_file_path = Path(py_file).resolve()
    # replate the extension with .toml
    assert py_file_path.suffix == ".py" and "Only .py files are supported"
    assert py_file_path.is_file(), f"File {py_file_path} does not exist"

    # replace the extension with .toml
    prompt_file_path = py_file_path.with_suffix(".toml")
    assert prompt_file_path.is_file(), f"Prompt file {prompt_file_path} does not exist"

    raw_toml = toml.load(prompt_file_path)
    flatten_toml = flatten_nested_dict(raw_toml, separator='.')
    prompt_entries: dict[str, PromptEntry] = {}
    for key in filter(lambda k: k.endswith(".prompt"), flatten_toml.keys()):
        key = key[:-7]  # remove the .prompt suffix
        prompt_entries[key] = PromptEntry(**deep_get(raw_toml, key.split(".")))
    
    return prompt_entries


def register_and_check(py_file: str|Path, key: str) -> None:
    """
    Register the prompt file for the given Python file and check if the key exists.
    """
    py_file_path = Path(py_file).resolve()
    file_key = str(py_file_path)

    if file_key not in _prompt_bank:
        _prompt_bank[file_key] = _get_prompt_file(py_file_path)

    assert key in _prompt_bank[file_key], f"Key '{key}' not found in prompt file for '{file_key}'"

def get_prompt_entry(py_file: str|Path, key: str) -> PromptEntry:
    """
    Get the PromptEntry for the given Python file and key.
    """
    py_file_path = Path(py_file).resolve()
    file_key = str(py_file_path)

    assert file_key in _prompt_bank, f"Prompt file for '{file_key}' not registered"
    assert key in _prompt_bank[file_key], f"Key '{key}' not found in prompt file for '{file_key}'"

    return _prompt_bank[file_key][key]

