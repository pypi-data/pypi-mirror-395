from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List219(Enum):
    """
    Rights type.

    Attributes:
        C: Copyright Text or image copyright (normally indicated by the
            © symbol). The default if no &lt;CopyrightType&gt; is
            specified
        P: Phonogram right Phonogram copyright or neighboring right
            (normally indicated by the ℗ symbol)
        D: Database right Sui generis database right
    """

    C = "C"
    P = "P"
    D = "D"
