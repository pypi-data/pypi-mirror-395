from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List240(Enum):
    """
    AV Item type code.

    Attributes:
        VALUE_01: Audiovisual work A complete audiovisual work which is
            published as a content item in a product which carries two
            or more such works, eg when two or three AV works are
            published in a single omnibus package
        VALUE_02: Front matter Audiovisual components such as a scene
            index or introduction which appear before the main content
            of the product
        VALUE_03: Body matter Audiovisual components such as scenes or
            ‘chapters’ which appear as part of the main body of the AV
            material in the product
        VALUE_04: End matter Audiovisual components such as advertising
            which appear after the main content of the product
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
