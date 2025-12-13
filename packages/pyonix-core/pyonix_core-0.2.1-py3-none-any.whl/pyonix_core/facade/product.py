from typing import Union, Optional, List, Dict, Any
from pyonix_core.models.short.product import Product as ProductShort
from pyonix_core.models.reference.product import Product as ProductRef
from pyonix_core.codelists.enums import (
    ProductIdentifierType, 
    TitleType, 
    ContributorRole, 
    PriceType,
    TextType
)
from pyonix_core.utils.identifiers import ISBN
from pyonix_core.utils.flatten import ProductFlattener
from pyonix_core.utils.text import to_markdown, clean_html
from pyonix_core.facade.assets import AssetHelper

class ProductFacade:
    def __init__(self, product: Union[ProductShort, ProductRef]):
        self._p = product
        self._is_short = isinstance(product, ProductShort)
        self._helper = AssetHelper(product)

    @property
    def helper(self) -> AssetHelper:
        return self._helper

    def to_dict(self, flattener: Optional[ProductFlattener] = None) -> Dict[str, Any]:
        f = flattener or ProductFlattener()
        return f.flatten(self)

    @property
    def record_reference(self) -> Optional[str]:
        if self._is_short:
            return self._p.a001.value if self._p.a001 else None
        else:
            return self._p.record_reference.value if self._p.record_reference else None

    @property
    def isbn13(self) -> Optional[str]:
        # Try direct ISBN-13
        val = self.get_identifier(ProductIdentifierType.VALUE_15)
        if val:
            return ISBN.clean(val)
        
        # Try ISBN-10 and convert
        val_10 = self.get_identifier(ProductIdentifierType.VALUE_02)
        if val_10:
            try:
                return ISBN.to_13(val_10)
            except ValueError:
                pass
        
        return None

    @property
    def description_html(self) -> str:
        """Returns the sanitized HTML description (TextType 03)."""
        raw = self._get_text_content('03')
        return clean_html(raw) if raw else ""

    @property
    def description_markdown(self) -> str:
        """Returns the description converted to Markdown."""
        raw = self._get_text_content('03')
        return to_markdown(raw) if raw else ""

    def _get_text_content(self, type_code: str) -> Optional[str]:
        collateral = None
        if self._is_short:
            collateral = self._p.collateraldetail
        else:
            collateral = self._p.collateral_detail
            
        if not collateral:
            return None
            
        texts = collateral.textcontent if self._is_short else collateral.text_content
        for t in texts:
            # Check type
            t_type = None
            if self._is_short:
                t_type = t.x426.value if t.x426 else None
            else:
                t_type = t.text_type.value if t.text_type else None
                
            if t_type == type_code:
                # Return text
                if self._is_short:
                    return t.d104[0].value if t.d104 else None
                else:
                    return t.text[0].value if t.text else None
        return None

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

    # Methods for Flattener
    def get_isbn13(self) -> Optional[str]:
        return self.isbn13

    def get_main_title(self) -> Optional[str]:
        return self.title

    def get_primary_author(self) -> Optional[str]:
        c = self.contributors
        return c[0] if c else None

    def get_publisher_name(self) -> Optional[str]:
        pub_detail = self._p.publishingdetail if self._is_short else self._p.publishing_detail
        if not pub_detail:
            return None
        
        publishers = pub_detail.publisher
        for pub in publishers:
            # We want the main publisher, usually role 01
            # But for simplicity, just take the first one with a name
            name = None
            if self._is_short:
                if pub.b081:
                    name = pub.b081[0].value
            else:
                if pub.publisher_name:
                    name = pub.publisher_name[0].value
            
            if name:
                return name
        return None

    def get_publication_date(self) -> Optional[str]:
        pub_detail = self._p.publishingdetail if self._is_short else self._p.publishing_detail
        if not pub_detail:
            return None
            
        dates = pub_detail.publishingdate if self._is_short else pub_detail.publishing_date
        for d in dates:
            # Role 01 is Publication Date
            role = None
            if self._is_short:
                role = d.b163.value if d.b163 else None
            else:
                role = d.publishing_date_role.value if d.publishing_date_role else None
                
            if role == '01':
                # Date value
                if self._is_short:
                    return d.b306.value if d.b306 else None
                else:
                    return d.date.value if d.date else None
        return None

    def get_publishing_status_code(self) -> Optional[str]:
        pub_detail = self._p.publishingdetail if self._is_short else self._p.publishing_detail
        if not pub_detail:
            return None
            
        status = None
        if self._is_short:
            status = pub_detail.b394.value if pub_detail.b394 else None
        else:
            status = pub_detail.publishing_status.value if pub_detail.publishing_status else None
            
        return status

    def get_price(self, currency: str = "USD") -> Optional[float]:
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
                # Check Currency (j152 / currency_code)
                curr = None
                if self._is_short:
                    curr = p.j152.value if p.j152 else None
                else:
                    curr = p.currency_code.value if p.currency_code else None
                
                if curr == currency:
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
