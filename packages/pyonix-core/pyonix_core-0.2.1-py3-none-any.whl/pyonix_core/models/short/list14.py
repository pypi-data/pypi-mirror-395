from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List14(Enum):
    """
    Text case flag.

    Attributes:
        VALUE_00: Undefined Default
        VALUE_01: Sentence case Initial capitals on first word and
            subsequently on proper names only, eg ‘The conquest of
            Mexico’
        VALUE_02: Title case Initial capitals on first word and
            subsequently on all significant words (nouns, pronouns,
            adjectives, verbs, adverbs, subordinate conjunctions)
            thereafter. Unless they appear as the first word, articles,
            prepositions and coordinating conjunctions remain lower
            case, eg ‘The Conquest of Mexico’
        VALUE_03: All capitals For example, ‘THE CONQUEST OF MEXICO’.
            Use only when Sentence or Title case are not possible (for
            example because of system limitations). Do NOT use simply
            because title is (correctly) in all caps (eg ‘BBQ USA’)
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
