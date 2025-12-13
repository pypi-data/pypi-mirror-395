from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List41(Enum):
    """
    Prize or award achievement.

    Attributes:
        VALUE_01: Winner
        VALUE_02: Runner-up Named as being in second place
        VALUE_03: Commended Cited as being worthy of special attention
            at the final stage of the judging process, but not named
            specifically as winner or runner-up. Possible terminology
            used by a particular prize includes ‘specially commended’ or
            ‘honored’
        VALUE_04: Short-listed Title named by the judging process to be
            one of the final list of candidates, such as a ‘short-list’
            from which the winner is selected, or a title named as
            ‘finalist’
        VALUE_05: Long-listed Title named by the judging process to be
            one of the preliminary list of candidates, such as a ‘long-
            list’ from which first a shorter list or set of finalists is
            selected, and then the winner is announced
        VALUE_06: Joint winner Or co-winner
        VALUE_07: Nominated Selected by judging panel or an official
            nominating process for final consideration for a prize,
            award or honor for which no ‘short-list’ or ‘long list’
            exists
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
