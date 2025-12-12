from dataclasses import dataclass, field
from typing import Optional

from .epub_usage_constraint_refname import EpubUsageConstraintRefname
from .epub_usage_constraint_shortname import EpubUsageConstraintShortname
from .epub_usage_limit import EpubUsageLimit
from .epub_usage_status import EpubUsageStatus
from .epub_usage_type import EpubUsageType
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class EpubUsageConstraint:
    """
    Details of a limitation on usage of a digital product (whether or not this
    constraint is enforced by DRM)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    epub_usage_type: Optional[EpubUsageType] = field(
        default=None,
        metadata={
            "name": "EpubUsageType",
            "type": "Element",
            "required": True,
        },
    )
    epub_usage_status: Optional[EpubUsageStatus] = field(
        default=None,
        metadata={
            "name": "EpubUsageStatus",
            "type": "Element",
            "required": True,
        },
    )
    epub_usage_limit: list[EpubUsageLimit] = field(
        default_factory=list,
        metadata={
            "name": "EpubUsageLimit",
            "type": "Element",
        },
    )
    refname: Optional[EpubUsageConstraintRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[EpubUsageConstraintShortname] = field(
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
