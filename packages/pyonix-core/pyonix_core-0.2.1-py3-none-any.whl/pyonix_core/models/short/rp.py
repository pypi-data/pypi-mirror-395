from dataclasses import dataclass, field
from typing import Optional

from .rp_dir import RpDir

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Rp:
    class Meta:
        name = "rp"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dir: Optional[RpDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )
