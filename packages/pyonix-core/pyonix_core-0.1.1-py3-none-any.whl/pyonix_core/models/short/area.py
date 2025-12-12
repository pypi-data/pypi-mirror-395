from dataclasses import dataclass, field
from typing import Optional

from .area_dir import AreaDir
from .area_nohref import AreaNohref
from .shape import Shape

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Area:
    class Meta:
        name = "area"
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
    dir: Optional[AreaDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shape: Shape = field(
        default=Shape.RECT,
        metadata={
            "type": "Attribute",
        },
    )
    coords: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nohref: Optional[AreaNohref] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
