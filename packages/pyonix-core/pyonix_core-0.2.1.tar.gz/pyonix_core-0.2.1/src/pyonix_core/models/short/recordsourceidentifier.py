from dataclasses import dataclass, field
from typing import Optional

from .b233 import B233
from .b244 import B244
from .list3 import List3
from .recordsourceidentifier_refname import RecordsourceidentifierRefname
from .recordsourceidentifier_shortname import RecordsourceidentifierShortname
from .x311 import X311

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Recordsourceidentifier:
    """
    An identifier for the organization that is the source of the metadata record.
    """

    class Meta:
        name = "recordsourceidentifier"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x311: Optional[X311] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b233: Optional[B233] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b244: Optional[B244] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[RecordsourceidentifierRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[RecordsourceidentifierShortname] = field(
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
