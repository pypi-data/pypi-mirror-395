from dataclasses import dataclass, field
from typing import Optional

from .alternative_name import AlternativeName
from .biographical_note import BiographicalNote
from .contributor_date import ContributorDate
from .contributor_description import ContributorDescription
from .contributor_place import ContributorPlace
from .contributor_refname import ContributorRefname
from .contributor_role import ContributorRole
from .contributor_shortname import ContributorShortname
from .corporate_name import CorporateName
from .corporate_name_inverted import CorporateNameInverted
from .from_language import FromLanguage
from .gender import Gender
from .key_names import KeyNames
from .letters_after_names import LettersAfterNames
from .list3 import List3
from .name_identifier import NameIdentifier
from .name_type import NameType
from .names_after_key import NamesAfterKey
from .names_before_key import NamesBeforeKey
from .person_name import PersonName
from .person_name_inverted import PersonNameInverted
from .prefix_to_key import PrefixToKey
from .prize import Prize
from .professional_affiliation import ProfessionalAffiliation
from .sequence_number import SequenceNumber
from .suffix_to_key import SuffixToKey
from .titles_after_names import TitlesAfterNames
from .titles_before_names import TitlesBeforeNames
from .to_language import ToLanguage
from .unnamed_persons import UnnamedPersons
from .website import Website

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Contributor:
    """
    Details of a person, persona or corporate identity – a contributor to the
    product (eg the author) ● Added &lt;Gender&gt;, &lt;Prize&gt; at revision 3.0.3
    ● Modified to allow &lt;NameIdentifier&gt; and &lt;AlternativeName&gt; with
    &lt;UnnamedPersons&gt; at revision 3.0.3 ● Modified cardinality of
    &lt;BiographicalNote&gt;, &lt;ContributorDescription&gt; at revision 3.0.1 ●
    Added &lt;CorporateNameInverted&gt; at revision 3.0 (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    sequence_number: Optional[SequenceNumber] = field(
        default=None,
        metadata={
            "name": "SequenceNumber",
            "type": "Element",
        },
    )
    contributor_role: list[ContributorRole] = field(
        default_factory=list,
        metadata={
            "name": "ContributorRole",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    from_language: list[FromLanguage] = field(
        default_factory=list,
        metadata={
            "name": "FromLanguage",
            "type": "Element",
        },
    )
    to_language: list[ToLanguage] = field(
        default_factory=list,
        metadata={
            "name": "ToLanguage",
            "type": "Element",
        },
    )
    name_type: Optional[NameType] = field(
        default=None,
        metadata={
            "name": "NameType",
            "type": "Element",
        },
    )
    name_identifier: list[NameIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "NameIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    person_name: list[PersonName] = field(
        default_factory=list,
        metadata={
            "name": "PersonName",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    person_name_inverted: list[PersonNameInverted] = field(
        default_factory=list,
        metadata={
            "name": "PersonNameInverted",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    titles_before_names: list[TitlesBeforeNames] = field(
        default_factory=list,
        metadata={
            "name": "TitlesBeforeNames",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    names_before_key: list[NamesBeforeKey] = field(
        default_factory=list,
        metadata={
            "name": "NamesBeforeKey",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    prefix_to_key: list[PrefixToKey] = field(
        default_factory=list,
        metadata={
            "name": "PrefixToKey",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    key_names: list[KeyNames] = field(
        default_factory=list,
        metadata={
            "name": "KeyNames",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    names_after_key: list[NamesAfterKey] = field(
        default_factory=list,
        metadata={
            "name": "NamesAfterKey",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    suffix_to_key: list[SuffixToKey] = field(
        default_factory=list,
        metadata={
            "name": "SuffixToKey",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    letters_after_names: list[LettersAfterNames] = field(
        default_factory=list,
        metadata={
            "name": "LettersAfterNames",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    titles_after_names: list[TitlesAfterNames] = field(
        default_factory=list,
        metadata={
            "name": "TitlesAfterNames",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    gender: list[Gender] = field(
        default_factory=list,
        metadata={
            "name": "Gender",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    corporate_name: list[CorporateName] = field(
        default_factory=list,
        metadata={
            "name": "CorporateName",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    corporate_name_inverted: list[CorporateNameInverted] = field(
        default_factory=list,
        metadata={
            "name": "CorporateNameInverted",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    unnamed_persons: list[UnnamedPersons] = field(
        default_factory=list,
        metadata={
            "name": "UnnamedPersons",
            "type": "Element",
            "max_occurs": 3,
        },
    )
    alternative_name: list[AlternativeName] = field(
        default_factory=list,
        metadata={
            "name": "AlternativeName",
            "type": "Element",
        },
    )
    contributor_date: list[ContributorDate] = field(
        default_factory=list,
        metadata={
            "name": "ContributorDate",
            "type": "Element",
        },
    )
    professional_affiliation: list[ProfessionalAffiliation] = field(
        default_factory=list,
        metadata={
            "name": "ProfessionalAffiliation",
            "type": "Element",
        },
    )
    prize: list[Prize] = field(
        default_factory=list,
        metadata={
            "name": "Prize",
            "type": "Element",
        },
    )
    biographical_note: list[BiographicalNote] = field(
        default_factory=list,
        metadata={
            "name": "BiographicalNote",
            "type": "Element",
        },
    )
    website: list[Website] = field(
        default_factory=list,
        metadata={
            "name": "Website",
            "type": "Element",
        },
    )
    contributor_description: list[ContributorDescription] = field(
        default_factory=list,
        metadata={
            "name": "ContributorDescription",
            "type": "Element",
        },
    )
    contributor_place: list[ContributorPlace] = field(
        default_factory=list,
        metadata={
            "name": "ContributorPlace",
            "type": "Element",
        },
    )
    refname: Optional[ContributorRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ContributorShortname] = field(
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
