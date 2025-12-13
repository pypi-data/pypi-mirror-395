from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List146(Enum):
    """
    Usage status.

    Attributes:
        VALUE_01: Permitted unlimited
        VALUE_02: Permitted subject to limit Limit should be specified
            in &lt;EpubUsageLimit&gt; or &lt;PriceConstraintLimit&gt;
        VALUE_03: Prohibited
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
