from dataclasses import dataclass, field
from typing import Optional

from .bible import Bible
from .list3 import List3
from .religious_text_feature import ReligiousTextFeature
from .religious_text_identifier import ReligiousTextIdentifier
from .religious_text_refname import ReligiousTextRefname
from .religious_text_shortname import ReligiousTextShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ReligiousText:
    """
    Details of the special features of a religious text, eg the Bible, the Qur’an.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    bible: Optional[Bible] = field(
        default=None,
        metadata={
            "name": "Bible",
            "type": "Element",
        },
    )
    religious_text_identifier: Optional[ReligiousTextIdentifier] = field(
        default=None,
        metadata={
            "name": "ReligiousTextIdentifier",
            "type": "Element",
        },
    )
    religious_text_feature: list[ReligiousTextFeature] = field(
        default_factory=list,
        metadata={
            "name": "ReligiousTextFeature",
            "type": "Element",
        },
    )
    refname: Optional[ReligiousTextRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ReligiousTextShortname] = field(
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
