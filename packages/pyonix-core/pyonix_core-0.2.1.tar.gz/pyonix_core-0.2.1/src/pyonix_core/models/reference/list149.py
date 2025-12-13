from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List149(Enum):
    """
    Title element level.

    Attributes:
        VALUE_01: Product The title element refers to an individual
            product
        VALUE_02: Collection level The title element refers to the top
            level of a bibliographic collection
        VALUE_03: Subcollection The title element refers to an
            intermediate level of a bibliographic collection that
            comprises two or more ‘sub-collections’
        VALUE_04: Content item The title element refers to a content
            item within a product, eg a work included in a combined or
            ‘omnibus’ edition, or a chapter in a book. Generally used
            only for titles within &lt;ContentItem&gt; (Block 3)
        VALUE_05: Master brand The title element names a multimedia
            franchise, licensed property or master brand where the use
            of the brand spans multiple collections and product forms,
            and possibly multiple imprints and publishers. It need not
            have a hierarchical relationship with title elements at
            other levels, or with other master brands. Used only for
            branded media properties carrying, for example, a children’s
            character brand or film franchise branding
        VALUE_06: Sub-subcollection The title element refers to an
            intermediate level of a bibliographic collection that is a
            subdivision of a sub-collection (a third level of collective
            identity)
        VALUE_07: Universe The title element names a ‘universe’, where
            parallel or intersecting narratives spanning multiple works
            and multiple characters occur in the same consistent
            fictional setting. It need not have a hierarchical
            relationship with title elements at other levels, in
            particular with master brands. Used primarily for comic
            books, but applicable to other fiction where appropriate
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
