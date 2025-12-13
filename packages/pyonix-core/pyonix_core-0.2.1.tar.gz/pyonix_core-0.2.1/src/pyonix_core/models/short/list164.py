from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List164(Enum):
    """
    Work relation.

    Attributes:
        VALUE_01: Manifestation of Product A is or includes a
            manifestation of work X. (There is a direct parent–child
            relation between work X and the product). The instance of
            &lt;RelatedWork&gt; must include an identifier for work X
        VALUE_02: Derived from Product A is or includes a manifestation
            of a work X which is derived (directly) from related work W
            in one or more of the ways specified in the former ISTC
            rules. (There is a relationship between a grandparent work W
            and a parent work X, and between that parent work and the
            product.) This relation type is intended to enable products
            with a common ‘grandparent’ work to be linked without
            specifying the precise nature of their derivation, and
            without necessarily assigning an identifier to the product’s
            parent work X. The instance of &lt;RelatedWork&gt; must
            include an identifier for work W. Codes 20–30 may be used
            instead to provide details of the derivation of work X from
            work W
        VALUE_03: Related work is derived from this Product A is a
            manifestation of a work X from which related work Y is
            (directly) derived in one or more of the ways specified in
            the former ISTC rules. (There is a relationship between a
            parent work X and a child work Y, and between the parent
            work X and the product.) The instance of &lt;RelatedWork&gt;
            must include an identifier for work Y. Codes 40–50 may be
            used instead to provide details of the derivation of work Y
            from work X
        VALUE_04: Other work in same (bibliographic) collection Product
            A is a manifestation of a work X in the same (bibliographic)
            collection as related work Z. (There is a relationship
            between the parent work X and a ‘same collection’ work Z,
            and between the parent work X and the product.) The instance
            of &lt;RelatedWork&gt; must include an identifier for work Z
        VALUE_05: Other work by same contributor Product A is a
            manifestation of a work X by the same contributor(s) as
            related work Z. (There is a relationship between the parent
            work X and a work Z where X and Z have at least one
            contributor in common, and between the parent work X and the
            product.) The instance of &lt;RelatedWork&gt; must include
            an identifier for work Z
        VALUE_06: Manifestation of original work Product A is or
            includes a manifestation of work X. (There is a direct
            parent–child relation between work X and the product, and
            work X is original, ie not a derived work of any kind –
            there is no work W.) The instance of &lt;RelatedWork&gt;
            must include an identifier for work X. See code 01 if the
            originality of X is unspecified or unknown
        VALUE_21: Derived from by abridgement Product A is or includes a
            manifestation of a work X which is derived directly from
            related work W by abridgement. (There is a relationship
            between the grandparent [unabridged] work W and the parent
            [abridged] work X, and between the parent work X and the
            product.) The instance of &lt;RelatedWork&gt; must include
            an identifier for [unabridged] work W. &lt;EditionType&gt;
            of product A would normally be ABR. See code 02 if the
            method of derivation of X from W is unknown or unstated. The
            [abridged] parent work X may be identified using a separate
            instance of &lt;RelatedWork&gt; with relation code 01
        VALUE_22: Derived from by annotation Product A is or includes a
            manifestation of a work X which is derived directly from
            related work W by annotation. The instance of
            &lt;RelatedWork&gt; must include an identifier for
            [unannotated] work W. &lt;EditionType&gt; of product X would
            normally be ANN, VAR etc. See code 02 if the method of
            derivation of X from W is unknown or unstated. The
            [annotated] parent work X may be identified using a separate
            instance of &lt;RelatedWork&gt; with relation code 01
        VALUE_23: Derived from by compilation The content of the work X
            has been formed by compilation of work W and another work Z.
            The instance of &lt;RelatedWork&gt; must include an
            identifier for work W. &lt;EditionType&gt; of product A may
            be CMB. Work Z may be identified using a separate instance
            of &lt;RelatedWork&gt; with code 23. The compiled parent
            work X may be identified using a separate instance of
            &lt;RelatedWork&gt; with relation code 01
        VALUE_24: Derived from by criticism The content of the work W
            has been augmented by the addition of critical commentary to
            form work X. The instance of &lt;RelatedWork&gt; must
            include an identifier for work W. &lt;EditionType&gt; of
            Product A would normally be CRI
        VALUE_25: Derived from by excerption The content of the work X
            is an excerpt from work W. The instance of
            &lt;RelatedWork&gt; must include an identifier for
            [complete] work W
        VALUE_26: Derived from by expurgation Offensive or unsuitable
            text material has been removed from work W to form work X.
            The instance of &lt;RelatedWork&gt; must include an
            identifier for [unsuitable] work W. &lt;EditionType&gt; of
            Product A would normally be EXP
        VALUE_27: Derived from by addition (of non-text material) The
            content of work W has been augmented by the addition of
            significant non-textual elements to form work X. The
            instance of &lt;RelatedWork&gt; must include an identifier
            for [unaugmented] work W. &lt;EditionType&gt; of product A
            may be ILL, ENH etc
        VALUE_28: Derived from by revision The content of work W has
            been revised and/or expanded or enlarged to form work X
            [including addition, deletion or replacement of text
            material]. The instance of &lt;RelatedWork&gt; must include
            an identifier for [unrevised] work W. &lt;EditionType&gt; of
            product A may be REV, NED, etc, or A may be numbered
        VALUE_29: Derived from via translation The content of work W has
            been translated into another language to form work X. The
            instance of &lt;RelatedWork&gt; must include an identifier
            for [untranslated] work W
        VALUE_30: Derived from via adaptation The content of work W has
            been adapted [into a different literary form] to form work
            X. The instance of &lt;RelatedWork&gt; must include an
            identifier for [unadapted] work W. &lt;EditionType&gt; of
            product A would normally be ADP, ACT etc
        VALUE_31: Derived from by subtraction (of non-text material) The
            content of work W has been modified by the removal of
            significant non-textual elements to form work X. The
            instance of &lt;RelatedWork&gt; must include an identifier
            for work W
        VALUE_41: Related work is derived from this by abridgement
            Product A is a manifestation of a work X from which the
            related work Y is (directly) derived by abridgement. (There
            is a relationship between the parent [unabridged] work X and
            the child [abridged] work Y, and between parent work X and
            the product.) The instance of &lt;RelatedWork&gt; must
            include the identifier for [abridged] work Y. See code 03 if
            the method of derivation of Y from X is unknown or unstated.
            The [unabridged] parent work X may be identified using a
            separate instance of &lt;RelatedWork&gt; with relation code
            01 or 06
        VALUE_42: Related work is derived from this by annotation
        VALUE_43: Related work is derived from this by compilation
        VALUE_44: Related work is derived from this by criticism
        VALUE_45: Related work is derived from this by excerption
        VALUE_46: Related work is derived from this by expurgation
        VALUE_47: Related work is derived from this by addition (of non-
            text material)
        VALUE_48: Related work is derived from this by revision
        VALUE_49: Related work is derived from this via translation
        VALUE_50: Related work is derived from this via adaptation
        VALUE_51: Derived from this by subtraction (of non-text
            material)
        VALUE_98: Manifestation of LRM work Product A is or includes a
            manifestation of an expression of LRM work X. Do not use,
            except as a workaround for differences between LRM works and
            expressions, and ONIX works in LRM library practice, and
            always also include a relationship to an ONIX work using
            code 01
        VALUE_99: Manifestation of LRM expression Product A is or
            includes a manifestation of an LRM expression with the same
            content, same agents and in the same modality (text, audio,
            video etc) as work X. Do not use, except as a workaround for
            differences between LRM expressions and ONIX works in LRM
            library practice, and always also include a relationship to
            an ONIX work using code 01
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_44 = "44"
    VALUE_45 = "45"
    VALUE_46 = "46"
    VALUE_47 = "47"
    VALUE_48 = "48"
    VALUE_49 = "49"
    VALUE_50 = "50"
    VALUE_51 = "51"
    VALUE_98 = "98"
    VALUE_99 = "99"
