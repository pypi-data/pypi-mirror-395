from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List198(Enum):
    """
    Product contact role.

    Attributes:
        VALUE_00: Metadata contact For queries and feedback concerning
            the metadata record itself
        VALUE_01: Accessibility request contact Eg for requests for
            supply of mutable digital files for conversion to other
            formats
        VALUE_02: Promotional contact Eg for requests relating to
            interviews, author events
        VALUE_03: Advertising contact Eg for co-op advertising
        VALUE_04: Review copy contact Eg for requests for review copies
        VALUE_05: Evaluation copy contact Eg for requests for approval
            or evaluation copies (particularly within education)
        VALUE_06: Permissions contact Eg for requests to reproduce or
            repurpose parts of the publication
        VALUE_07: Return authorization contact Eg for use where
            authorization must be gained from the publisher rather than
            the distributor or wholesaler
        VALUE_08: CIP / Legal deposit contact Eg for legal deposit or
            long-term preservation
        VALUE_09: Rights and licensing contact Eg for subrights
            licensing, collective licensing
        VALUE_10: Product safety contact Eg for EU General product
            safety regulation (GPSR) compliance. See
            https://commission.europa.eu/business-economy-euro/product-
            safety-and-requirements/product-safety/general-product-
            safety-regulation_en
        VALUE_11: Product raw materials contact Eg for EU Deforestation
            regulation (EUDR) compliance. See https://eur-
            lex.europa.eu/legal-
            content/EN/TXT/?uri=CELEX%3A32023R1115&amp;qid=1687867231461
        VALUE_99: Customer services contact For general enquiries
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_99 = "99"
