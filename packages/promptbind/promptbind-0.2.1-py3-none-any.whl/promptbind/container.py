import jinja2
import warnings
from dataclasses import dataclass

@dataclass(frozen=True)
class PromptEntry:
    prompt: str
    use_jinja2: bool = False

    def render(self, **kwargs) -> str: 
        if self.use_jinja2:
            template = jinja2.Template(self.prompt)
            return template.render(**kwargs)
        
        if not kwargs:
            warnings.warn("Rendering a prompt without jinja2 but with kwargs has no effect.", UserWarning)

        return self.prompt