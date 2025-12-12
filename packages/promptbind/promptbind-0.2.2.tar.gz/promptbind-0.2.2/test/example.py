import prelude
import timeit
from promptbind import with_prompt, PromptEntry

@with_prompt()
def example_function(prompt: PromptEntry) -> None:
    print("Prompt:", prompt.render(name="User"))
    # time render
    print("Render time:", timeit.timeit(lambda: prompt.render(name="User"), number=1000))
    print("This is an example function.")


@with_prompt(key="special_function_key")
def function_with_key(prompt: PromptEntry) -> None:
    print("Prompt:", prompt.render())
    print("This function has a specified prompt key.")

class ExampleClass:
    @with_prompt()
    def class_method(self, prompt: PromptEntry) -> None:
        print("Prompt:", prompt.render())
        print("This is a class method.")
