from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List53(Enum):
    """
    Returns conditions code type.

    Attributes:
        VALUE_00: Proprietary returns coding scheme Note that a
            distinctive &lt;ReturnsCodeTypeName&gt; is required with
            proprietary coding schemes. Only for use in ONIX 3.0 or
            later
        VALUE_01: French book trade returns conditions code Maintained
            by CLIL (Commission Interprofessionnel du Livre). Returns
            conditions values in &lt;ReturnsCode&gt; should be taken
            from the CLIL list
        VALUE_02: BISAC Returnable Indicator code Maintained by BISAC:
            Returns conditions values in &lt;ReturnsCode&gt; should be
            taken from List 66
        VALUE_03: UK book trade returns conditions code NOT CURRENTLY
            USED – BIC has decided that it will not maintain a code list
            for this purpose, since returns conditions are usually at
            least partly based on the trading relationship
        VALUE_04: ONIX Returns conditions code Returns conditions values
            in &lt;ReturnsCode&gt; should be taken from List 204
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
