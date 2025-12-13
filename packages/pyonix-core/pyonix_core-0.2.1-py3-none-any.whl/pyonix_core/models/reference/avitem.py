from dataclasses import dataclass, field
from typing import Optional

from .avduration import Avduration
from .avitem_identifier import AvitemIdentifier
from .avitem_refname import AvitemRefname
from .avitem_shortname import AvitemShortname
from .avitem_type import AvitemType
from .list3 import List3
from .time_run import TimeRun

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Avitem:
    """
    Details of an audiovisual content item (eg a chapter) ● Added at revision
    3.0.5.
    """

    class Meta:
        name = "AVItem"
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    avitem_type: Optional[AvitemType] = field(
        default=None,
        metadata={
            "name": "AVItemType",
            "type": "Element",
            "required": True,
        },
    )
    avitem_identifier: list[AvitemIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "AVItemIdentifier",
            "type": "Element",
        },
    )
    time_run: list[TimeRun] = field(
        default_factory=list,
        metadata={
            "name": "TimeRun",
            "type": "Element",
        },
    )
    avduration: Optional[Avduration] = field(
        default=None,
        metadata={
            "name": "AVDuration",
            "type": "Element",
        },
    )
    refname: Optional[AvitemRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[AvitemShortname] = field(
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
