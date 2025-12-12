from typing import Union, Optional, List
from pyonix_core.models.short.product import Product as ProductShort
from pyonix_core.models.reference.product import Product as ProductRef
from pyonix_core.codelists.enums import (
    ProductIdentifierType, 
    TitleType, 
    ContributorRole, 
    PriceType
)

class ProductFacade:
    def __init__(self, product: Union[ProductShort, ProductRef]):
        self._p = product
        self._is_short = isinstance(product, ProductShort)

    @property
    def record_reference(self) -> Optional[str]:
        if self._is_short:
            return self._p.a001.value if self._p.a001 else None
        else:
            return self._p.record_reference.value if self._p.record_reference else None

    @property
    def isbn13(self) -> Optional[str]:
        return self.get_identifier(ProductIdentifierType.VALUE_15)

    @property
    def title(self) -> Optional[str]:
        """Returns the distinctive title of the product."""
        details = []
        if self._is_short:
            if self._p.descriptivedetail:
                details = self._p.descriptivedetail.titledetail
        else:
            if self._p.descriptive_detail:
                details = self._p.descriptive_detail.title_detail
        
        for d in details:
            # Check TitleType (b202 / title_type)
            t_type = None
            if self._is_short:
                t_type = d.b202.value if d.b202 else None
            else:
                t_type = d.title_type.value if d.title_type else None
            
            # print(f"DEBUG: Found TitleDetail with type {t_type}, expected {TitleType.VALUE_01.value}")
            
            # Handle both Enum object and raw value comparison
            is_match = False
            if hasattr(t_type, 'value'):
                is_match = t_type.value == TitleType.VALUE_01.value
            else:
                is_match = t_type == TitleType.VALUE_01.value
                
            if is_match:
                # Found distinctive title
                elements = d.titleelement if self._is_short else d.title_element
                for el in elements:
                    # Get TitleText (b203 / title_text)
                    # Or TitlePrefix (b030) + TitleWithoutPrefix (b031)
                    text = None
                    if self._is_short:
                        if el.b203:
                            text = el.b203[0].value
                        elif el.b031:
                            prefix = el.b030[0].value if el.b030 else ""
                            text = (prefix + " " + el.b031[0].value).strip()
                    else:
                        if el.title_text:
                            text = el.title_text[0].value
                        elif el.title_without_prefix:
                            prefix = el.title_prefix[0].value if el.title_prefix else ""
                            text = (prefix + " " + el.title_without_prefix[0].value).strip()
                    
                    if text:
                        return text
        return None

    @property
    def contributors(self) -> List[str]:
        """Returns a list of contributor names (PersonName or KeyNames)."""
        contribs = []
        source_contribs = []
        
        if self._is_short:
            if self._p.descriptivedetail:
                source_contribs = self._p.descriptivedetail.contributor
        else:
            if self._p.descriptive_detail:
                source_contribs = self._p.descriptive_detail.contributor
                
        for c in source_contribs:
            # Try to get PersonName (b036 / person_name)
            name = None
            if self._is_short:
                if c.b036:
                    name = c.b036[0].value
                elif c.b037: # PersonNameInverted
                    name = c.b037[0].value
            else:
                if c.person_name:
                    name = c.person_name[0].value
                elif c.person_name_inverted:
                    name = c.person_name_inverted[0].value
            
            if name:
                contribs.append(name)
                
        return contribs

    @property
    def price_amount(self) -> Optional[float]:
        """Returns the first available price amount."""
        supplies = []
        if self._is_short:
            for ps in self._p.productsupply:
                supplies.extend(ps.supplydetail)
        else:
            for ps in self._p.product_supply:
                supplies.extend(ps.supply_detail)
                
        for supply in supplies:
            prices = supply.price if self._is_short else supply.price
            for p in prices:
                # Check PriceType (x462 / price_type) optional but good to know
                # Get PriceAmount (j151 / price_amount)
                amount = None
                if self._is_short:
                    if p.j151:
                        amount = p.j151.value
                else:
                    if p.price_amount:
                        amount = p.price_amount.value
                
                if amount is not None:
                    return float(amount)
        return None

    def get_identifier(self, id_type: ProductIdentifierType) -> Optional[str]:
        identifiers = []
        if self._is_short:
            identifiers = self._p.productidentifier
        else:
            identifiers = self._p.product_identifier
            
        for ident in identifiers:
            # Check type
            current_type = None
            value = None
            
            if self._is_short:
                # b221 is ProductIDType, b244 is IDValue
                if ident.b221 and ident.b221.value:
                    current_type = ident.b221.value
                if ident.b244 and ident.b244.value:
                    value = ident.b244.value
            else:
                # product_idtype, idvalue
                if ident.product_idtype and ident.product_idtype.value:
                    current_type = ident.product_idtype.value
                if ident.idvalue and ident.idvalue.value:
                    value = ident.idvalue.value
            
            # Compare Enums. 
            # The Enums in short and reference models are technically different classes 
            # but have same values (e.g. '15').
            # ProductIdentifierType is aliased to List5 from short model.
            
            if current_type and current_type.value == id_type.value:
                return value
                
        return None
