from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Lists:
    class Meta:
        name = "lists"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )
