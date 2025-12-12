"""Ways to designate a DICOM tag or a group of dicom tags"""
import re
from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Tuple, Union

from pydicom._dicom_dict import RepeatersDictionary
from pydicom.datadict import keyword_for_tag, mask_match
from pydicom.dataelem import DataElement
from pydicom.tag import BaseTag, Tag


def clean_tag_string(x):
    """Remove common clutter from pydicom Tag.__str__() output"""
    return (
        x.replace("(", "").replace(",", "").replace(" ", "").replace(")", "")
    )


def get_keyword(tag):
    """Human-readable keyword for known dicom tags, or string representation of
    tag address, for example '(1010,001d)'
    """
    keyword = keyword_for_tag(tag)
    if keyword:
        return keyword
    else:
        return str(tag).replace(" ", "")


@total_ordering
class TagIdentifier(ABC):
    """Identifies a single DICOM tag or repeating group like (50xx,xxx)

    Using just single DICOM tags is too limited for defining deidentification. We want
    to be able to represent for example:

    * all curves (50xx,xxxx)
    * a private tag with private creator group (01[PrivateCreatorName],0010)

    TagIdentifier features:
    * Can match a single tag or any collection of tags using .matches(element)
    * Is uniquely defined by .key(). Instances with the same .key() will equate
      and key is a sufficient argument to recreate a new instance:
      Tag(tag.key()) == tag
    """

    @abstractmethod
    def matches(self, element: DataElement) -> bool:
        """The given element matches this identifier"""

    @abstractmethod
    def key(self) -> str:
        """String representation of this identifier.

        The following should hold:
           >>> tag(tag.key()) == tag
        """

    @abstractmethod
    def name(self) -> str:
        """Human-readable name for this tag"""
        raise NotImplementedError("This is an abstract base class")

    @abstractmethod
    def number_of_matchable_tags(self) -> int:
        """The number of distinct tags that this identifier could match

        Used to determine order of matching (specific -> general)
        """

    #   Override comparisons to be able to compare and sort
    def __le__(self, other):
        """Return ``True`` if `self`  is less than or equal to `other`"""
        return self.key() >= other.key()

    def __eq__(self, other):
        if isinstance(other, TagIdentifier):
            return self.key() == other.key()
        else:
            return False

    def __hash__(self):
        # TagIdentifiers are used as dictionary keys so hash is needed
        return hash(self.key())


class SingleTag(TagIdentifier):
    """Matches a single DICOM tag like (0010,0010) or 'PatientName'"""

    HEX_DICOM_TAG_REGEX = re.compile(
        r"\((?P<first>[0-9a-fA-F]{4}),(?P<second>[0-9a-fA-F]{4})\)",
        re.IGNORECASE,
    )

    def __init__(self, tag: Union[BaseTag, str, Tuple[int, int]]):
        """

        Parameters
        ----------
        tag: Union[Tag, str]
            Tag instance or string representing tag. Anything that Tag init accepts.
            For example: (0x1100,0x001f), '1100001f', 'PatientID', Tag('PatientID').
            In addition, excepts hex string with parenthesis "(1100,001f)".

        """

        try:
            tag = Tag(tag)
        except ValueError as e:
            match = self.HEX_DICOM_TAG_REGEX.fullmatch(str(tag))
            if not match:
                raise ValueError(
                    f"Could not parse '{tag}' as a DICOM tag"
                ) from e
            else:
                try:
                    tag = Tag(
                        (
                            int(match.group("first"), 16),
                            int(match.group("second"), 16),
                        )
                    )
                except ValueError as e:
                    raise ValueError(
                        f"Could not parse '{tag}' as a DICOM tag"
                    ) from e

        self.tag = tag

    def __str__(self):
        return str(self.tag)

    def name(self) -> str:
        """Human-readable name for this tag"""
        return get_keyword(self.tag)

    def matches(self, element: DataElement) -> bool:
        """The given element matches this identifier"""
        return element.tag == self.tag

    def key(self) -> str:
        """Return a valid Tag() string argument"""
        return self.name()

    def number_of_matchable_tags(self) -> int:
        return 1


class RepeatingTag:
    """Dicom tag with x's in it to denote wildcards, like (50xx,xxxx) for curve data

    See http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_7.6.html

    Raises
    ------
    ValueError
        on init if tag cannot be parsed as a DICOM repeater group

    Notes
    -----
    I would prefer to take any pydicom way of working with repeater tags, but
    the current version of pydicom (2.0) only offers limited lookup support
    as far as I can see
    """

    def __init__(self, tag: str):
        # check input
        try:
            self.tag = RepeatingTag.parse_tag_string(tag)
        except ValueError as e:
            raise ValueError(
                f'Invalid format "{tag}": {e}. Examples of valid tag '
                f'strings: "(0010, xx10)", "0010, xx10", "0010xx10"'
            ) from e

    def __str__(self):
        """Output format matches pydicom.tag.Tag.__str__()"""
        return f"({self.tag[:4]}, {self.tag[4:]})"

    @staticmethod
    def parse_tag_string(tag: str) -> str:
        """Cleans tag string and outputs it in standard format.
        Raises ValueError if tag is not of the correct format like
        (0010,10xx).

        Returns
        -------
        str
            standard format, 8 character hex string with 'x' for wildcard bytes.
            like 0010xx10 or 75f300xx
        """
        # remove potential brackets and comma. Make lower case to reduce clutter
        tag = clean_tag_string(tag).lower()
        if len(tag) != 8:
            raise ValueError("Tag should be 8 characters long")
        # check whether this is a valid hex string if you discount the x's
        try:
            int(f'0x{tag.replace("x", "0")}', 0)
        except ValueError as e:
            raise ValueError(
                'Non "x" parts of this tag are not hexadecimal'
            ) from e

        return tag

    def name(self) -> str:
        """Human-readable name for this repeater tag, from pydicom lists"""
        key = mask_match(self.static_component())
        if key:
            return RepeatersDictionary[key][
                4
            ]  # 4th item in tuple is no-space name
        else:
            return f"Unknown Repeater tag {self.tag}"

    def number_of_matchable_tags(self) -> int:
        """Number of x's in this wildcard"""
        return self.tag.count("x")

    def as_mask(self) -> int:
        """Byte mask that can remove the byte positions that have value 'x'

        RepeatingTag('0010,xx10').as_mask() -> 0xffff00ff
        RepeatingTag('50xx,xxxx').as_mask() -> 0xff000000
        """
        hex_string = (
            f"0x{''.join(map(lambda x: '0' if x == 'x' else 'f', self.tag))}"
        )
        return int(hex_string, 0)

    def static_component(self) -> int:
        """The int value of all bytes of this tag that are not 'x'
        RepeatingTag('0010,xx10').static_component() -> 0x00100010
        RepeatingTag('50xx,xxxx').static_component() -> 0x50000000
        """
        return int(f'0x{self.tag.replace("x", "0")}', 0)


class RepeatingGroup(TagIdentifier):
    """A DICOM tag where not all elements are filled. Like (50xx,xxxx)"""

    def __init__(self, tag: Union[str, RepeatingTag]):
        if isinstance(tag, str):  # allow string init for convenience
            tag = RepeatingTag(tag.replace(" ", ""))  # allow (xxxx, xxxx)
        self.tag = tag

    def __str__(self):
        return str(self.tag)

    def matches(self, element: DataElement) -> bool:
        """True if the tag values match this repeater in all places without an 'x'"""
        # Following pydicom in using byte operations for this
        return element.tag & self.tag.as_mask() == self.tag.static_component()

    def key(self) -> str:
        """For sane sorting, make sure this matches the key format of other
        identifiers
        """
        return clean_tag_string(str(self.tag))

    def name(self) -> str:
        """Human readable name for this tag"""
        return self.tag.name()

    def number_of_matchable_tags(self) -> int:
        return 16 ** self.tag.number_of_matchable_tags()


class PrivateAttributes(TagIdentifier):
    """Matches any private DICOM tag. A private tag has an uneven group number"""

    def __str__(self):
        return self.key()

    def matches(self, element: DataElement) -> bool:
        return element.tag.is_private

    def key(self) -> str:
        return "PrivateAttributes"

    def name(self) -> str:
        return "Private Attributes"

    def number_of_matchable_tags(self) -> int:
        # Private tags have an odd group number. So this identifier matches every
        # other possible tag
        return 2147483648  # ((16**8)/2)


class AnyAttribute(TagIdentifier):
    """Any DICOM Attribute. The catch-all default operation. Matches any DICOM tag."""

    def __str__(self):
        return self.key()

    def matches(self, element: DataElement) -> bool:
        return True

    def key(self) -> str:
        return "AnyAttribute"

    def name(self) -> str:
        return "Any Attribute"

    def number_of_matchable_tags(self) -> int:
        # Matches over four billion potential tags.
        return 4294967296  # ((16**8))


class PrivateBlockTagIdentifier(TagIdentifier):
    """A private DICOM tag with a private creator. Like '0013,[MyCompany]01'

    In this example [MyCompany] refers whatever block was reserved by private
    creator identifier 'MyCompany'

    For more info on private blocks, see DICOM standard part 5,
    section 7.8.1 ('Private Data Elements')
    """

    BLOCK_TAG_REGEX = re.compile(
        r"(?P<group>[0-9A-F]{4}),?\s?\["
        r"(?P<private_creator>.*)\](?P<element>[0-9,A-F]*)",
        re.IGNORECASE,
    )

    def __init__(self, tag: str):
        """

        Parameters
        ----------
        tag: str
            In the format 'xxxx,[private_creator]yy' where xxxx and yy are
            interpreted as hexadecimals

        Raises
        ------
        ValueError
            if tag is not in the correct format

        """
        self.group, self.private_creator, self.element = self.parse_tag(tag)

    @classmethod
    def init_explicit(cls, group: int, private_creator: str, element: int):
        """Create with explicit parameters. This cannot be the main init because
        TagIdentifier classes need to be instantiable from a single string and
        uphold cls(cls.tag)=cls

        Parameters
        ----------
        group: int
            DICOM group, between 0x0000 and 0xFFFF
        private_creator: str
            Name of the private creator for this tag
        element: int
            The two final bytes of the element. Between 0x00 and 0xFF
        """
        return cls(
            cls.to_tag(
                group=group, private_creator=private_creator, element=element
            )
        )

    @staticmethod
    def to_tag(group: int, private_creator: str, element: int) -> str:
        """Tag string like '1301,[creator]01' from individual elements

        Parameters
        ----------
        group: int
            DICOM group, between 0x0000 and 0xFFFF
        private_creator: str
            Name of the private creator for this tag
        element: int
            The two final bytes of the element. Between 0x00 and 0xFF
        """
        return f"{group:04x},[{private_creator}]{element:02x}"  # noqa #E231

    @property
    def tag(self) -> str:
        return self.to_tag(
            group=self.group,
            private_creator=self.private_creator,
            element=self.element,
        )

    @classmethod
    def parse_tag(cls, tag: str) -> Tuple[int, str, int]:
        """Parses 'xxxx,[creator]yy' into xxxx, creator and yy components.
        xxxx and yy are interpreted as hexadecimals

        Parameters
        ----------
        tag: str
            Format: 'xxxx,[creator]yy' where xxxx and yy are hexadecimals. Case
            insensitive.

        Returns
        -------
        Tuple[int, str, int]:
            xxxx: int, creator:str and yy:int from tag string 'xxxx,[creator]yy'
            where xxxx and yy are read as hexadecimals from string

        Raises
        ------
        ValueError:
            When input cannot be parsed
        """

        match = cls.BLOCK_TAG_REGEX.match(tag)
        if not match:
            raise ValueError(f'Could not parse "{tag}" as "xxxx, [creator]yy"')
        return (
            int(match.group("group"), 16),
            match.group("private_creator"),
            int(match.group("element"), 16),
        )

    def __str__(self):
        return str(self.tag)

    def matches(self, element: DataElement) -> bool:
        """True if private element has been created by private creator and the rest
        of the group and element match up
        """
        if element.tag.group != self.group:
            return False
        elif (
            element.tag.element & 0x00FF != self.element
        ):  # last 2 bytes match
            return False
        elif element.private_creator != self.private_creator:
            return False
        else:
            return True

    def key(self) -> str:
        """For sane sorting, make sure this matches the key format of other
        identifiers

        """
        return self.tag

    def name(self) -> str:
        """Human readable name for this tag"""
        return self.tag

    def number_of_matchable_tags(self) -> int:
        """How many tags could this identifier match?"""

        return 265  # Private creator part value can be 00-FF. So 16 * 16.


def tag_identifier_from_string(str_in):
    """Create TagIdentifier subclass instance from a string representation

    This is possible because all TagIdentifiers can be instantiated from string only
    and there is enough information to disambiguate them.

    Alternatively, we could add the type to all string representation but that is much
    more clunky to read.
    """
    if str_in.lower() in ["privatetags", "privateattributes"]:
        return PrivateAttributes()
    elif str_in.lower() in ["anyattribute"]:
        return AnyAttribute()
    else:
        try:
            return SingleTag(str_in)
        except ValueError:
            pass
        try:
            return PrivateBlockTagIdentifier(str_in)
        except ValueError:
            pass
        try:
            return RepeatingGroup(str_in)
        except ValueError as e:
            raise ValueError(
                f"'{str_in}' could not be parsed as PrivateAttributes, "
                f"SingleTags, PrivateBlockTagIdentifier or RepeatingGroup. "
                f"I really don't know what this is supposed to be"
            ) from e
