from dataclasses import dataclass, field
from typing import Optional

from .ancillary_content_description import AncillaryContentDescription
from .ancillary_content_refname import AncillaryContentRefname
from .ancillary_content_shortname import AncillaryContentShortname
from .ancillary_content_type import AncillaryContentType
from .list3 import List3
from .number import Number

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class AncillaryContent:
    """
    Details of illustrations, maps, table of contents, index, bibliography or other
    ancillary content ● Modified cardinality of &lt;AncillaryContentDescription&gt;
    at revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    ancillary_content_type: Optional[AncillaryContentType] = field(
        default=None,
        metadata={
            "name": "AncillaryContentType",
            "type": "Element",
            "required": True,
        },
    )
    ancillary_content_description: list[AncillaryContentDescription] = field(
        default_factory=list,
        metadata={
            "name": "AncillaryContentDescription",
            "type": "Element",
        },
    )
    number: Optional[Number] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Element",
        },
    )
    refname: Optional[AncillaryContentRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[AncillaryContentShortname] = field(
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
