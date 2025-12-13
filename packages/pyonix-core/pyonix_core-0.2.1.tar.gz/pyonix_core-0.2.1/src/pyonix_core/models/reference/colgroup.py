from dataclasses import dataclass, field
from typing import Optional

from .col import Col
from .colgroup_align import ColgroupAlign
from .colgroup_dir import ColgroupDir
from .colgroup_valign import ColgroupValign

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Colgroup:
    class Meta:
        name = "colgroup"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    col: list[Col] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
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
    dir: Optional[ColgroupDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    span: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[ColgroupAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[ColgroupValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
