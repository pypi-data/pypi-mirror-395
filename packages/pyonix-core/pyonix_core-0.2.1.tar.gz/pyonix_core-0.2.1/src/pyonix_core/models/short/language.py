from dataclasses import dataclass, field
from typing import Optional

from .b251 import B251
from .b252 import B252
from .b253 import B253
from .b398 import B398
from .language_refname import LanguageRefname
from .language_shortname import LanguageShortname
from .list3 import List3
from .x420 import X420

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Language:
    """
    Details of a language and its relation to the product (eg language of text
    used, or original language from which the text was translated) ● Added
    &lt;RegionCode at revision 3.0.7.
    """

    class Meta:
        name = "language"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    b253: Optional[B253] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b252: Optional[B252] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b251: Optional[B251] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b398: Optional[B398] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x420: Optional[X420] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[LanguageRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[LanguageShortname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    datestamp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"(19|20)\d\d(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-8])(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|(19|20)\d\d(0[13-9]|1[0-2])(29|30)(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|(19|20)\d\d(0[13578]|1[02])31(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|19(0[48]|[13579][26]|[2468][048])0229(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|20(0[048]|[13579][26]|[2468][048])0229(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?",
        },
    )
    sourcename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"\S(.*\S)?",
        },
    )
    sourcetype: Optional[List3] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
