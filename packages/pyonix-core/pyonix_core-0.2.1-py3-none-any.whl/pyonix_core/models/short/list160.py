from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List160(Enum):
    """
    Resource feature type.

    Attributes:
        VALUE_01: Required credit Credit that must be displayed when a
            resource is used (eg ‘Photo Jerry Bauer’ or ‘© Magnum
            Photo’). Credit text should be carried in
            &lt;FeatureNote&gt;
        VALUE_02: Caption Explanatory caption that may accompany a
            resource (eg use to identify an author in a photograph).
            Caption text should be carried in &lt;FeatureNote&gt;
        VALUE_03: Copyright holder Copyright holder of resource
            (indicative only, as the resource can be used without
            consultation). Copyright text should be carried in
            &lt;FeatureNote&gt;
        VALUE_04: Length in minutes Approximate length in minutes of an
            audio or video resource. &lt;FeatureValue&gt; should contain
            the length of time as an integer number of minutes
        VALUE_05: ISNI of resource contributor Use to link resource such
            as a contributor image to a contributor unambiguously. Use
            for example with Resource Content types 04, 11–14 from List
            158, particularly where the product has more than a single
            contributor. &lt;FeatureValue&gt; contains the 16-digit
            ISNI, which must match an ISNI given in an instance of
            &lt;Contributor&gt;
        VALUE_06: Proprietary ID of resource contributor Use to link
            resource such as a contributor image to a contributor
            unambiguously. Use for example with Resource Content types
            04, 11–14 from List 158, particularly where the product has
            more than a single contributor. &lt;FeatureValue&gt;
            contains the proprietary ID, which must match a proprietary
            ID given in an instance of &lt;Contributor&gt;
        VALUE_07: Resource alternative text &lt;FeatureNote&gt; is
            Alternative text for the resource, which might be presented
            to visually-impaired readers
        VALUE_08: Background color of image resource
            &lt;FeatureValue&gt; is a 24-bit RGB or 32-bit RBGA color in
            hexadecimal, eg fff2de for an opaque warm cream. Used when
            the resource – for example a 3D image of the product –
            includes a background, or if used with an alpha channel,
            when the image is irregularly shaped or contains a semi-
            transparent shadow thrown against a background
        VALUE_09: Attribute of product image resource
            &lt;FeatureValue&gt; is an ONIX code from List 256 that
            describes an attribute of a product image resource (eg
            perspective of 3D view, content)
        VALUE_10: Background color of page &lt;FeatureValue&gt; is a
            24-bit RGB color in hexadecimal, eg ffc300 for a rich
            yellow-orange, used when the resource supplier requests a
            specific background color be displayed behind the resource
            on a web page
        VALUE_11: ORCID of resource contributor Use to link resource
            such as a contributor image to a contributor unambiguously,
            for example with Resource Content types 04, 11–14 from List
            158, particularly where the product has more than a single
            contributor. &lt;FeatureValue&gt; contains the 16-digit
            ISNI, which must match an ORCID given in an instance of
            &lt;Contributor&gt;
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
