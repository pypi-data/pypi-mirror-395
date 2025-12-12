"""Python definition of the parts"""
from typing import Dict, List, Union

from dicomcriterion import Criterion
from dicomcriterion.exceptions import CriterionError
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.functional_serializers import field_serializer
from pydicom.valuerep import VR

from midom.constants import ActionCode, ActionCodes
from midom.identifiers import (
    PrivateBlockTagIdentifier,
    TagIdentifier,
    tag_identifier_from_string,
)


class PixelArea(BaseModel):
    area: tuple[int, int, int, int]


class TagAction(BaseModel):
    """Describes the action to take for a single identifier (tag or tag group) and the
    reason for this action.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  # for TagIdentifier

    identifier: TagIdentifier
    action: ActionCode
    justification: str

    @field_serializer("identifier")
    def serialize_identifier(self, value, _info):
        return value.key()

    @field_validator("identifier", mode="before")
    @classmethod
    def deserialize_identifier(cls, value):
        if isinstance(value, TagIdentifier):
            return value
        elif isinstance(value, str):
            return tag_identifier_from_string(value)
        else:
            raise ValueError(
                f'Invalid input data for TagAction.identifier: "{value}"'
            )

    @field_serializer("action")
    def serialize_action(self, value, _info):
        return value.key

    @field_validator("action", mode="before")
    @classmethod
    def deserialize_action(cls, value):
        if isinstance(value, ActionCode):
            return value
        elif isinstance(value, str):
            return ActionCodes.from_string(value)
        else:
            raise ValueError(
                f'Invalid input data for TagAction.identifier: "{value}"'
            )


class PrivateElement(BaseModel):
    """A private DICOM element with human-readable name."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  # for TagIdentifier

    identifier: Union[PrivateBlockTagIdentifier, str]
    description: str
    value_representation: VR  # any DICOM VR string
    value_multiplicity: str = "1"

    @field_serializer("identifier")
    def serialize_identifier(self, value, _info):
        return value.key()

    @field_validator("identifier", mode="before")
    @classmethod
    def deserialize_identifier(cls, value):
        if isinstance(value, TagIdentifier):
            return value
        elif isinstance(value, str):
            return tag_identifier_from_string(value)
        else:
            raise ValueError(
                f'Invalid input data for TagAction.identifier: "{value}"'
            )


class CriterionString(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    content: Criterion

    @field_serializer("content")
    def serialize_identifier(self, value, _info):
        return value._expression

    @field_validator("content", mode="before")
    @classmethod
    def deserialize_tag(cls, value):
        if isinstance(value, Criterion):
            return value
        elif isinstance(value, str):
            try:
                return Criterion(value)
            except CriterionError as e:
                raise ValueError(
                    f'Could not parse "{value}" as criterion. Original error: {e}'
                ) from e
        else:
            raise ValueError(
                f"Expected Criterion or str as input but "
                f'found f"{type(value)}" for "{value}'
            )


class Filter(BaseModel):
    criterion: CriterionString
    justification: str


class PixelOperation(BaseModel):
    description: str
    criterion: CriterionString
    areas: List[PixelArea]


class PrivateAllowGroup(BaseModel):
    # Allow arbitrary for PrivateBlockTagIdentifier
    model_config = ConfigDict(arbitrary_types_allowed=True)

    elements: List[PrivateElement]
    justification: str


class Protocol(BaseModel):
    """Defines how to handle the deidentification of any incoming dataset. It does
    not say anything about implementation, it only prescribes what should be done
    to each part of a dataset and under which circumstances to reject it outright.

    Overview of elements:
    tags: Dict[str, List[TagAction]]
        SOPInstanceUID that can contain wildcards: List of what to do with DICOM tags

    filters: List[Filter]
        If any of these filters matches, reject the DICOM dataset

    pixel: List[PixelOperation]
        What to do with pixel data. Where to put black boxes if a rule matches

    private: List[PrivateAllowGroup]
        Which private tags to allow and why
    """

    tags: Dict[str, List[TagAction]]
    filters: List[Filter]
    pixel: List[PixelOperation]
    private: List[PrivateAllowGroup]

    def sort_tags(self):
        """Sort tag list for each SOPInstanceUID according to generality. The more
        general, the lower in the list. This means you can take any DICOM tag and
        try to match each element in the list until one hits.
        """
        for key, action_list in self.tags.items():
            self.tags[key] = sorted(
                action_list,
                key=lambda x: x.identifier.number_of_matchable_tags(),
            )
