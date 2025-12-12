from dataclasses import dataclass, field
from typing import Optional

from .bible_contents import BibleContents
from .bible_purpose import BiblePurpose
from .bible_reference_location import BibleReferenceLocation
from .bible_refname import BibleRefname
from .bible_shortname import BibleShortname
from .bible_text_feature import BibleTextFeature
from .bible_text_organization import BibleTextOrganization
from .bible_version import BibleVersion
from .list3 import List3
from .study_bible_type import StudyBibleType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Bible:
    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    bible_contents: list[BibleContents] = field(
        default_factory=list,
        metadata={
            "name": "BibleContents",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    bible_version: list[BibleVersion] = field(
        default_factory=list,
        metadata={
            "name": "BibleVersion",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    study_bible_type: Optional[StudyBibleType] = field(
        default=None,
        metadata={
            "name": "StudyBibleType",
            "type": "Element",
        },
    )
    bible_purpose: list[BiblePurpose] = field(
        default_factory=list,
        metadata={
            "name": "BiblePurpose",
            "type": "Element",
        },
    )
    bible_text_organization: Optional[BibleTextOrganization] = field(
        default=None,
        metadata={
            "name": "BibleTextOrganization",
            "type": "Element",
        },
    )
    bible_reference_location: Optional[BibleReferenceLocation] = field(
        default=None,
        metadata={
            "name": "BibleReferenceLocation",
            "type": "Element",
        },
    )
    bible_text_feature: list[BibleTextFeature] = field(
        default_factory=list,
        metadata={
            "name": "BibleTextFeature",
            "type": "Element",
        },
    )
    refname: Optional[BibleRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[BibleShortname] = field(
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
