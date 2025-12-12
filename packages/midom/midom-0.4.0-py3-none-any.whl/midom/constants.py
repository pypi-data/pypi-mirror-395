"""Implementations of some of the MIDOM constants and objects"""
from pydantic.dataclasses import dataclass


class DeltaCodes:
    """How has a DICOM element changed?"""

    UNCHANGED = "UNCHANGED"
    CHANGED = "CHANGED"
    REMOVED = "REMOVED"
    EMPTIED = "EMPTIED"
    CREATED = "CREATED"

    ALL = {UNCHANGED, CHANGED, REMOVED, EMPTIED, CREATED}


@dataclass(frozen=True)
class ActionCode:
    key: str
    var_name: str


class ActionCodes:
    """NEMA specifications from table E1-1. Indicates what to do with each tag"""

    DUMMY = ActionCode("D", "DUMMY")  # replace with dummy
    EMPTY = ActionCode("Z", "EMPTY")  # replace with zero length
    REMOVE = ActionCode("X", "REMOVE")  # remove
    KEEP = ActionCode("K", "KEEP")  # keep
    CLEAN = ActionCode("C", "CLEAN")  # clean
    UID = ActionCode("U", "UID")  # replace with consistent UID
    EMPTY_OR_DUMMY = ActionCode("Z/D", "EMPTY_OR_DUMMY")
    REPLACE_OR_DUMMY = ActionCode("X/Z", "REPLACE_OR_DUMMY")  # X unless Z is
    # required for consistency
    REMOVE_OR_EMPTY = ActionCode("X/Z", "REMOVE_OR_EMPTY")  # X unless Z is
    # required for consistency
    REMOVE_OR_DUMMY = ActionCode("X/D", "REMOVE_OR_DUMMY")  # X unless D is
    # required for consistency
    REMOVE_OR_EMPTY_OR_DUMMY = ActionCode(
        "X/Z/D", "REMOVE_OR_EMPTY_OR_DUMMY"
    )  # X unless Z or D is required
    REMOVE_OR_EMPTY_OR_UID = ActionCode(
        "X/Z/U*", "REMOVE_OR_EMPTY_OR_UID"
    )  # X unless Z or U is required
    UNDEFINED = ActionCode(
        "?", "Undefined"
    )  # not part of ALL below, special case

    ALL = {
        DUMMY,
        EMPTY,
        REMOVE,
        KEEP,
        CLEAN,
        UID,
        EMPTY_OR_DUMMY,
        REMOVE_OR_EMPTY,
        REMOVE_OR_DUMMY,
        REMOVE_OR_EMPTY_OR_DUMMY,
        REMOVE_OR_EMPTY_OR_UID,
    }

    PER_KEY = {x.key: x for x in ALL}
    PER_VAR_NAME = {x.var_name: x for x in ALL}

    @classmethod
    def from_string(cls, key_or_var_name: str):
        """I've got a string with either a full name or a key. Which action
        code is this?
        """
        try:
            return (cls.PER_KEY | cls.PER_VAR_NAME)[key_or_var_name]
        except KeyError as e:
            raise ValueError(
                f"Unknown action code '{key_or_var_name}'. I "
                f"know {','.join([str(x) for x in cls.ALL])}"
            ) from e
