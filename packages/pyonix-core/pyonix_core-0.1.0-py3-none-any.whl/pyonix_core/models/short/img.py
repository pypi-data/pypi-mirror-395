from dataclasses import dataclass, field
from typing import Optional

from .img_dir import ImgDir
from .img_ismap import ImgIsmap

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Img:
    class Meta:
        name = "img"
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
    dir: Optional[ImgDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    longdesc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[str] = field(
        default=None,
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
    usemap: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ismap: Optional[ImgIsmap] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
