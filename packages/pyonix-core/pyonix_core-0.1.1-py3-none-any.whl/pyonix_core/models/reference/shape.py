from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class Shape(Enum):
    RECT = "rect"
    CIRCLE = "circle"
    POLY = "poly"
    DEFAULT = "default"
