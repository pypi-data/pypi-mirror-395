from dataclasses import dataclass, field
from typing import Optional

from .b067 import B067
from .b068 import B068
from .b069 import B069
from .b070 import B070
from .b171 import B171
from .list3 import List3
from .subject_refname import SubjectRefname
from .subject_shortname import SubjectShortname
from .x425 import X425

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Subject:
    """
    Details of the subject or aboutness of the product – a subject classification
    code or heading ● Modified cardinality of &lt;SubjectHeadingText&gt; at
    revision 3.0.1.
    """

    class Meta:
        name = "subject"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x425: Optional[X425] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b067: Optional[B067] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b171: Optional[B171] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b068: Optional[B068] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    b069: Optional[B069] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    b070: list[B070] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    refname: Optional[SubjectRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[SubjectShortname] = field(
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
