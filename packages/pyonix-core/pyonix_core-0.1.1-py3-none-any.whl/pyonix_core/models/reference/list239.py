from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List239(Enum):
    """
    Supply contact role.

    Attributes:
        VALUE_07: Return authorization contact Eg for use where
            authorization must be gained from the supplier (distributor
            or wholesaler)
        VALUE_10: Product safety contact Eg for EU General product
            safety regulation (GPSR) compliance where the supplier acts
            on behalf of the publisher or publisher representative as an
            importer into the EU. See
            https://commission.europa.eu/business-economy-euro/product-
            safety-and-requirements/product-safety/general-product-
            safety-regulation_en
        VALUE_11: Product raw materials contact Eg for EU Deforestation
            regulation (EUDR) compliance where the supplier acts on
            behalf of the publisher or publisher representative as an
            importer into the EU. See https://eur-lex.europa.eu/legal-
            content/EN/TXT/?uri=CELEX%3A32023R1115&amp;qid=1687867231461
        VALUE_99: Customer services contact For general enquiries
    """

    VALUE_07 = "07"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_99 = "99"
