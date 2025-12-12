from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List12(Enum):
    """
    Trade category.

    Attributes:
        VALUE_01: UK open market edition An edition from a UK publisher
            sold only in territories where exclusive rights are not
            held. Rights details should be carried in PR.21 (in ONIX
            2.1) OR P.21 (in ONIX 3.0 or later) as usual
        VALUE_02: Airport edition In UK, an edition intended primarily
            for airside sales in UK airports, though it may be available
            for sale in other territories where exclusive rights are not
            held. Rights details should be carried in PR.21 (in ONIX
            2.1) OR P.21 (in ONIX 3.0 or later) as usual
        VALUE_03: Sonderausgabe In Germany, a special printing sold at a
            lower price than the regular hardback
        VALUE_04: Pocket book In countries where recognized as a
            distinct trade category, eg France « livre de poche »,
            Germany ,Taschenbuch‘, Italy «tascabile», Spain «libro de
            bolsillo»
        VALUE_05: International edition (US) Edition produced solely for
            sale in designated export markets
        VALUE_06: Library audio edition Audio product sold in special
            durable packaging and with a replacement guarantee for the
            contained cassettes or CDs for a specified shelf-life
        VALUE_07: US open market edition An edition from a US publisher
            sold only in territories where exclusive rights are not
            held. Rights details should be carried in PR.21 (in ONIX
            2.1) OR P.21 (in ONIX 3.0 or later) as usual
        VALUE_08: Livre scolaire, déclaré par l’éditeur In France, a
            category of book that has a particular legal status, claimed
            by the publisher
        VALUE_09: Livre scolaire (non spécifié) In France, a category of
            book that has a particular legal status, designated
            independently of the publisher
        VALUE_10: Supplement to newspaper Edition published for sale
            only with a newspaper or periodical
        VALUE_11: Precio libre textbook In Spain, a school textbook for
            which there is no fixed or suggested retail price and which
            is supplied by the publisher on terms individually agreed
            with the bookseller
        VALUE_12: News outlet edition For editions sold only through
            newsstands/newsagents
        VALUE_13: US textbook In the US and Canada, a book that is
            published primarily for use by students in school or college
            education as a basis for study. Textbooks published for the
            elementary and secondary school markets are generally
            purchased by school districts for the use of students.
            Textbooks published for the higher education market are
            generally adopted for use in particular classes by the
            instructors of those classes. Textbooks are usually not
            marketed to the general public, which distinguishes them
            from trade books. Note that trade books adopted for course
            use are not considered to be textbooks (though a specific
            education edition of a trade title may be)
        VALUE_14: E-book short ‘Short’ e-book (sometimes also called a
            ‘single’), typically containing a single short story, an
            essay or piece of long-form journalism
        VALUE_15: Superpocket book In countries where recognized as a
            distinct trade category, eg Italy «supertascabile». Only for
            use in ONIX 3.0 or later
        VALUE_16: Beau-livre Category of books, usually hardcover and of
            a large format (A4 or larger) and printed on high-quality
            paper, where the primary features are illustrations, and
            these are more important than text. Sometimes called
            ‘coffee-table books’ or ‘art books’ in English. Only for use
            in ONIX 3.0 or later
        VALUE_17: Podcast Category of audio products typically
            distinguished by being free of charge (but which may be
            monetized through advertising content) and episodic. Only
            for use in ONIX 3.0 or later
        VALUE_18: Periodical Category of books or e-books which are
            single issues of a periodical publication, sold as
            independent products. Only for use in ONIX 3.0 or later
        VALUE_19: Catalog Publisher’s or supplier’s catalog (when
            treated as a product in its own right). Only for use in ONIX
            3.0 or later
        VALUE_20: Atlas Category of books containing a linked group of
            plates, tables, diagrams, lists, often but not always
            combined with maps or a geographical theme or approach. Only
            for use in ONIX 3.0 or later
        VALUE_21: Newspaper Daily or weekly. Only for use in ONIX 3.0 or
            later
    """

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
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
