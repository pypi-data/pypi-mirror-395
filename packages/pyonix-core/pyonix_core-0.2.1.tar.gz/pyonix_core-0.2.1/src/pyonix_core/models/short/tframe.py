from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class Tframe(Enum):
    VOID = "void"
    ABOVE = "above"
    BELOW = "below"
    HSIDES = "hsides"
    LHS = "lhs"
    RHS = "rhs"
    VSIDES = "vsides"
    BOX = "box"
    BORDER = "border"
