from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class InlineAbstract:
    class Meta:
        name = "inline"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )
