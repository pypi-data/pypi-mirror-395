from dataclasses import dataclass
from typing import Any, Dict, Optional

from jinja2 import Template


@dataclass
class Prompt:
    name: str
    template: str
    version_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def render(self, **kwargs) -> str:
        return Template(self.template).render(**kwargs)

    def with_version(self, version_id: str) -> "Prompt":
        return Prompt(
            name=self.name,
            template=self.template,
            version_id=version_id,
            metadata=self.metadata,
        )
