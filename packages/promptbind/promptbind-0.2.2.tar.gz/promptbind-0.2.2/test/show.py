import prelude

from example import example_function, ExampleClass, function_with_key
from promptbind.util import get_prompt_key, set_prompt_key_patch, unset_prompt_key_patch

if __name__ == "__main__":
    print("Prompt key for example_function:", get_prompt_key(example_function))
    
    # Set a prompt key patch and test
    set_prompt_key_patch(example_function, "patched_key_for_example_function")
    example_function()

    # Unset the prompt key patch and test
    unset_prompt_key_patch(example_function)
    example_function()

    # Test class method
    obj = ExampleClass()
    obj.class_method()

    # Test function with specified key
    function_with_key()
