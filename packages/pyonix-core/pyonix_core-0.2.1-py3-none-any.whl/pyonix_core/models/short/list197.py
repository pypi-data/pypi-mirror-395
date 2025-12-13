from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List197(Enum):
    """
    Collection sequence type.

    Attributes:
        VALUE_01: Proprietary collection sequence type A short
            explanatory label for the sequence should be provided in
            &lt;CollectionSequenceTypeName&gt;
        VALUE_02: Title order Order as specified by the title, eg by
            volume or part number sequence, provided for confirmation
        VALUE_03: Publication order Order of publication of products
            within the collection
        VALUE_04: Temporal/narrative order Order defined by a continuing
            narrative or temporal sequence within products in the
            collection. Applicable to either fiction or to non-fiction
            (eg within a collection of history textbooks)
        VALUE_05: Original publication order Original publication order,
            for a republished collection or collected works originally
            published outside a collection
        VALUE_06: Suggested reading order Where it is different from the
            title order, publication order, narrative order etc
        VALUE_07: Suggested display order Where it is different from the
            title order, publication order, narrative order, reading
            order etc
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
