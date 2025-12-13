from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class Trules(Enum):
    NONE = "none"
    GROUPS = "groups"
    ROWS = "rows"
    COLS = "cols"
    ALL = "all"
