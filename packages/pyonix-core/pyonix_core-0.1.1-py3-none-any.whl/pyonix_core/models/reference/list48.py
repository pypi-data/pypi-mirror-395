from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List48(Enum):
    """
    Measure type.

    Attributes:
        VALUE_01: Height For a book, the overall height when standing on
            a shelf. For a folded map, the height when folded. For
            packaged products, the height of the retail packaging, and
            for trade-only products, the height of the trade packaging.
            In general, the height of a product in the form in which it
            is presented or packaged for retail sale
        VALUE_02: Width For a book, the overall horizontal dimension of
            the cover when standing upright. For a folded map, the width
            when folded. For packaged products, the width of the retail
            packaging, and for trade-only products, the width of the
            trade packaging. In general, the width of a product in the
            form in which it is presented or packaged for retail sale
        VALUE_03: Thickness For a book, the overall thickness of the
            spine. For a folded map, the thickness when folded. For
            packaged products, the depth of the retail packaging, and
            for trade-only products, the depth of the trade packaging.
            In general, the thickness or depth of a product in the form
            in which it is presented or packaged for retail sale
        VALUE_04: Page trim height Overall height (code 01) is preferred
            for general use, as it includes the board overhang for
            hardbacks
        VALUE_05: Page trim width Overall width (code 02) is preferred
            for general use, as it includes the board overhang and spine
            thickness for hardbacks
        VALUE_06: Unit volume The volume of the product, including any
            retail packaging. Note the &lt;MeasureUnit&gt; is
            interpreted as a volumetric unit – for example code cm =
            cubic centimetres (ie millilitres), and code oz = (US) fluid
            ounces. Only for use in ONIX 3.0 or later
        VALUE_07: Unit capacity Volume of the internal (fluid) contents
            of a product (eg of paint in a can). Note the
            &lt;MeasureUnit&gt; is interpreted as a volumetric unit –
            for example code cm = cubic centimetres (ie millilitres),
            and code oz = (US) fluid ounces. Only for use in ONIX 3.0 or
            later
        VALUE_08: Unit weight The overall weight of the product,
            including any retail packaging
        VALUE_09: Diameter (sphere) Of a globe, for example
        VALUE_10: Unfolded/unrolled sheet height The height of a folded
            or rolled sheet map, poster etc when unfolded
        VALUE_11: Unfolded/unrolled sheet width The width of a folded or
            rolled sheet map, poster etc when unfolded
        VALUE_12: Diameter (tube or cylinder) The diameter of the cross-
            section of a tube or cylinder, usually carrying a rolled
            sheet product. Use 01 ‘Height’ for the height or length of
            the tube
        VALUE_13: Rolled sheet package side measure The length of a side
            of the cross-section of a long triangular or square package,
            usually carrying a rolled sheet product. Use 01 ‘Height’ for
            the height or length of the package
        VALUE_14: Unpackaged height As height, but of the product
            without packaging (use only for products supplied in retail
            packaging, must also supply overall size when packaged using
            code 01). Only for use in ONIX 3.0 or later
        VALUE_15: Unpackaged width As width, but of the product without
            packaging (use only for products supplied in retail
            packaging, must also supply overall size when packaged using
            code 02). Only for use in ONIX 3.0 or later
        VALUE_16: Unpackaged thickness As thickness, but of the product
            without packaging (use only for products supplied in retail
            packaging, must also supply overall size when packaged using
            code 03). Only for use in ONIX 3.0 or later
        VALUE_17: Total battery weight Weight of batteries built-in,
            pre-installed or supplied with the product. Details of the
            batteries should be provided using
            &lt;ProductFormFeature&gt;. A per-battery unit weight may be
            calculated from the number of batteries if required. Only
            for use in ONIX 3.0 or later
        VALUE_18: Total weight of Lithium Mass or equivalent mass of
            elemental Lithium within the batteries built-in, pre-
            installed or supplied with the product (eg a Lithium Iron
            phosphate battery with 160g of cathode material would have a
            total of around 7g of Lithium). Details of the batteries
            must be provided using &lt;ProductFormFeature&gt;. A per-
            battery unit mass of Lithium may be calculated from the
            number of batteries if required. Only for use in ONIX 3.0 or
            later
        VALUE_19: Assembled length For use where product or part of
            product requires assembly, for example the size of a
            completed kit, puzzle or assembled display piece. The
            assembled dimensions may be larger than the product size as
            supplied. Use only when the unassembled dimensions as
            supplied (including any retail or trade packaging) are also
            provided using codes 01, 02 and 03. Only for use in ONIX 3.0
            or later
        VALUE_20: Assembled width
        VALUE_21: Assembled height
        VALUE_22: Unpackaged unit weight Overall unit weight (code 08)
            is preferred for general use, as it includes the weight of
            any packaging. Use Unpackaged unit weight only for products
            supplied in retail packaging, and must also supply overall
            unit weight. Only for use in ONIX 3.0 or later
        VALUE_23: Carton length Includes packaging. See
            &lt;PackQuantity&gt; for number of copies of the product per
            pack, and used only when dimensions of individual copies
            (codes 01, 02, 03) AND &lt;PackQuantity&gt; are supplied.
            Note that neither orders nor deliveries have to be aligned
            with multiples of the pack quantity, but such orders and
            deliveries may be more convenient to handle. Only for use in
            ONIX 3.0 or later
        VALUE_24: Carton width
        VALUE_25: Carton height
        VALUE_26: Carton weight Includes the weight of product(s) within
            the carton. See &lt;PackQuantity&gt; for number of copies
            per pack, and used only when the weight of individual copies
            (code 08) AND &lt;PackQuantity&gt; are supplied. Only for
            use in ONIX 3.0 or later
        VALUE_27: Pallet length Includes pallet and packaging. See
            &lt;PalletQuantity&gt; for number of copies of the product
            per pallet, and used only when dimensions of individual
            copies (codes 01, 02, 03) AND &lt;PalletQuantity&gt; are
            supplied. Note that neither orders nor deliveries have to be
            aligned with multiples of the pallet quantity, but such
            orders and deliveries may be more convenient to handle. Only
            for use in ONIX 3.0 or later
        VALUE_28: Pallet width
        VALUE_29: Pallet height
        VALUE_30: Pallet weight Includes the weight of product(s) and
            cartons stacked on the pallet. See &lt;PalletQuantity&gt;
            for the number of copies per pallet, and used only when the
            weight of individual copies (code 08) AND
            &lt;PalletQuantity&gt; are supplied. Only for use in ONIX
            3.0 or later
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
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_30 = "30"
