from dataclasses import dataclass, field
from typing import Optional

from .hr_dir import HrDir

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Hr:
    class Meta:
        name = "hr"
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
    dir: Optional[HrDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
