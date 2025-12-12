from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class Scope(Enum):
    ROW = "row"
    COL = "col"
    ROWGROUP = "rowgroup"
    COLGROUP = "colgroup"
