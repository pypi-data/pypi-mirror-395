from dataclasses import dataclass, field
from typing import Optional

from .collection_sequence_number import CollectionSequenceNumber
from .collection_sequence_refname import CollectionSequenceRefname
from .collection_sequence_shortname import CollectionSequenceShortname
from .collection_sequence_type import CollectionSequenceType
from .collection_sequence_type_name import CollectionSequenceTypeName
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class CollectionSequence:
    """
    Details of a product’s sequential position in a collection ● Added at revision
    3.0.1.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    collection_sequence_type: Optional[CollectionSequenceType] = field(
        default=None,
        metadata={
            "name": "CollectionSequenceType",
            "type": "Element",
            "required": True,
        },
    )
    collection_sequence_type_name: Optional[CollectionSequenceTypeName] = (
        field(
            default=None,
            metadata={
                "name": "CollectionSequenceTypeName",
                "type": "Element",
            },
        )
    )
    collection_sequence_number: Optional[CollectionSequenceNumber] = field(
        default=None,
        metadata={
            "name": "CollectionSequenceNumber",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[CollectionSequenceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[CollectionSequenceShortname] = field(
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
