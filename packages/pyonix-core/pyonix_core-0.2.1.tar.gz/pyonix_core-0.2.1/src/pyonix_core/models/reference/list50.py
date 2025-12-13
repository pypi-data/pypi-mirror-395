from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List50(Enum):
    """
    Measure unit.

    Attributes:
        CM: Centimeters Millimeters are the preferred metric unit of
            length
        GR: Grams
        IN: Inches (US)
        KG: Kilograms Grams are the preferred metric unit of weight
        LB: Pounds (US) Ounces are the preferred US customary unit of
            weight
        MM: Millimeters
        OZ: Ounces (US)
        PX: Pixels
    """

    CM = "cm"
    GR = "gr"
    IN = "in"
    KG = "kg"
    LB = "lb"
    MM = "mm"
    OZ = "oz"
    PX = "px"
