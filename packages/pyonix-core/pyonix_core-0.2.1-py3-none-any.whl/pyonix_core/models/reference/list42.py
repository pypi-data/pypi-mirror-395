from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List42(Enum):
    """
    Text item type.

    Attributes:
        VALUE_01: Textual work A complete work which is published as a
            content item in a product which carries two or more such
            works, eg when two or three novels are published in a single
            omnibus volume
        VALUE_02: Front matter Text components such as Preface,
            Introduction etc which appear as preliminaries to the main
            body of text content in a product
        VALUE_03: Body matter Text components such as Part, Chapter,
            Section etc which appear as part of the main body of text
            content in a product
        VALUE_04: Back matter Text components such as Index which appear
            after the main body of text in a product
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
