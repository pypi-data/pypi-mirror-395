from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List62(Enum):
    """
    Tax rate type.

    Attributes:
        H: Higher rate Specifies that tax is applied at a higher rate
            than standard
        P: Tax paid at source (Italy) Under Italian tax rules, VAT on
            books may be paid at source by the publisher, and subsequent
            transactions through the supply chain are tax-exempt
        R: Lower rate Specifies that tax is applied at a lower rate than
            standard. In the EU, use code R for ‘Reduced rates’, and for
            rates lower than 5%, use code T (‘Super-reduced’) or Z
            (Zero-rated)
        S: Standard rate
        T: Super-low rate Specifies that tax is applied at a rate lower
            than the Lower rate(s). In the EU, use code T for ‘Super-
            reduced rates’, and for Reduced rates (5% or above) use code
            R (Lower rate). Only for use in ONIX 3.0 or later
        Z: Zero-rated
    """

    H = "H"
    P = "P"
    R = "R"
    S = "S"
    T = "T"
    Z = "Z"
