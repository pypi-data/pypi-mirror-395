from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .main_subject import MainSubject
from .subject_code import SubjectCode
from .subject_heading_text import SubjectHeadingText
from .subject_refname import SubjectRefname
from .subject_scheme_identifier import SubjectSchemeIdentifier
from .subject_scheme_name import SubjectSchemeName
from .subject_scheme_version import SubjectSchemeVersion
from .subject_shortname import SubjectShortname

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Subject:
    """
    Details of the subject or aboutness of the product – a subject classification
    code or heading ● Modified cardinality of &lt;SubjectHeadingText&gt; at
    revision 3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    main_subject: Optional[MainSubject] = field(
        default=None,
        metadata={
            "name": "MainSubject",
            "type": "Element",
        },
    )
    subject_scheme_identifier: Optional[SubjectSchemeIdentifier] = field(
        default=None,
        metadata={
            "name": "SubjectSchemeIdentifier",
            "type": "Element",
            "required": True,
        },
    )
    subject_scheme_name: Optional[SubjectSchemeName] = field(
        default=None,
        metadata={
            "name": "SubjectSchemeName",
            "type": "Element",
        },
    )
    subject_scheme_version: Optional[SubjectSchemeVersion] = field(
        default=None,
        metadata={
            "name": "SubjectSchemeVersion",
            "type": "Element",
        },
    )
    subject_code: Optional[SubjectCode] = field(
        default=None,
        metadata={
            "name": "SubjectCode",
            "type": "Element",
            "required": True,
        },
    )
    subject_heading_text: list[SubjectHeadingText] = field(
        default_factory=list,
        metadata={
            "name": "SubjectHeadingText",
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
