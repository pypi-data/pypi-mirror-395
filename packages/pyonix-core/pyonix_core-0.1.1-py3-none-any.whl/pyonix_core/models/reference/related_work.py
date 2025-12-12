from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .related_work_refname import RelatedWorkRefname
from .related_work_shortname import RelatedWorkShortname
from .work_identifier import WorkIdentifier
from .work_relation_code import WorkRelationCode

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class RelatedWork:
    """
    Details of a work related to the product (eg is the work of which the product
    is a manifestation)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    work_relation_code: Optional[WorkRelationCode] = field(
        default=None,
        metadata={
            "name": "WorkRelationCode",
            "type": "Element",
            "required": True,
        },
    )
    work_identifier: list[WorkIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "WorkIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[RelatedWorkRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[RelatedWorkShortname] = field(
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
