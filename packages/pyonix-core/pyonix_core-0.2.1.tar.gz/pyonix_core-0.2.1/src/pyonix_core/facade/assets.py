from typing import Optional, List, Any

class AssetHelper:
    def __init__(self, product_model: Any):
        self.product = product_model

    @property
    def cover_url(self) -> Optional[str]:
        return self.get_cover_image()

    def get_cover_image(self, size_preference: str = "large") -> Optional[str]:
        """
        Returns the URL of the front cover.
        size_preference: 'large' (prioritizes unconstrained), 'small' (thumbnails)
        """
        if not hasattr(self.product, 'collateral_detail') or not self.product.collateral_detail:
            return None

        collateral = self.product.collateral_detail
        if not collateral.supporting_resource:
            return None

        # 1. Filter SupportingResources where ContentType == '01' (Front Cover)
        # We need to handle the fact that content_type_code might be an object with a value property
        # or an enum. The generated code usually uses Enums or strings.
        candidates = []
        for res in collateral.supporting_resource:
            is_front_cover = False
            for c_type in res.resource_content_type:
                # Check if it's '01'. It might be an object with .value or just a string/enum
                val = getattr(c_type, 'value', c_type)
                if str(val) == '01':
                    is_front_cover = True
                    break
            if is_front_cover:
                candidates.append(res)

        if not candidates:
            return None

        # 2. Inspect ResourceVersions to find the link
        # TODO: Implement size preference logic (checking ResourceVersionFeature)
        
        for res in candidates:
            for version in res.resource_version:
                # Check for URL link
                for link in version.resource_link:
                    # link might be a string or object with value
                    return getattr(link, 'value', str(link))
        
        return None
