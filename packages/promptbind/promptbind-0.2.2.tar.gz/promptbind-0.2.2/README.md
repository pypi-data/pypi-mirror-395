# PromptBind

PromptBind lets you bind prompts to functions and methods with a small decorator and TOML sidecar files. It keeps prompts close to your code, supports optional Jinja2 rendering, and allows hot-swapping prompt keys at runtime.

## Installation

```bash
pip install promptbind
```

## QuickStart

1) **Create a prompt file** next to your Python module (same name, `.toml` extension):

```toml
# example.toml
[greet]
prompt = "Hello, {{ name }}!"
use_jinja2 = true

[farewell]
prompt = "Goodbye."
use_jinja2 = false
```

2) **Bind prompts to functions** with the decorator. By default the prompt key is the function `__qualname__`, but you can override it with `key=...`.

```python
# example.py
from promptbind import with_prompt, PromptEntry

@with_prompt()
def greet(prompt: PromptEntry) -> str:
    return prompt.render(name="Ada")

@with_prompt(key="farewell")
def bye(prompt: PromptEntry) -> str:
    return prompt.render()

if __name__ == "__main__":
    print(greet())  # -> Hello, Ada!
    print(bye())    # -> Goodbye.
```

3) **Patch prompt keys at runtime** if you want to swap to another entry in the same TOML file:

```python
from promptbind import set_prompt_key_patch, unset_prompt_key_patch

set_prompt_key_patch(greet, "farewell")  # greet now uses the farewell prompt
print(greet())  # -> Goodbye.
unset_prompt_key_patch(greet)            # revert to original key
```

## How it works

- A `.toml` file lives next to each Python file and stores prompt entries.
- `with_prompt` checks the TOML at import time, injects the matching `PromptEntry`, and routes calls to your function with `prompt` as the first argument (methods get `self`/`cls` first, then `prompt`).
- `PromptEntry.render(**kwargs)` renders with Jinja2 when `use_jinja2 = true`; otherwise it returns the raw string (passing kwargs in that case is a no-op).

## Thread safety note

`set_prompt_key_patch`/`unset_prompt_key_patch` mutate shared process-wide state. Avoid calling them concurrently across threads, or you may observe races where a call picks up the wrong prompt key. If you must patch in a multithreaded context, guard these calls with your own locking.

## Minimal project layout

```
project/
├─ example.py
└─ example.toml
```

That is all you need to start binding prompts to your code. See `test/example.py` and `test/example.toml` in the repo for a runnable sample.
