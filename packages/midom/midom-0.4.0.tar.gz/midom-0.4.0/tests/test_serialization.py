import pytest
from dicomcriterion import Criterion

from midom.components import (
    CriterionString,
    Filter,
    PixelArea,
    PixelOperation,
    PrivateAllowGroup,
    PrivateElement,
    Protocol,
    TagAction,
)
from midom.constants import ActionCodes
from midom.identifiers import (
    PrivateAttributes,
    PrivateBlockTagIdentifier,
    RepeatingGroup,
    SingleTag,
)


@pytest.fixture()
def a_protocol():
    return Protocol(
        tags={
            "1.2.840.10008.5.1.4.1.1.2": [
                TagAction(
                    identifier=SingleTag("PatientID"),
                    action=ActionCodes.REMOVE,
                    justification="",
                ),
                TagAction(
                    identifier=SingleTag("Modality"),
                    action=ActionCodes.KEEP,
                    justification="",
                ),
                TagAction(
                    identifier=PrivateAttributes(),
                    action=ActionCodes.REMOVE,
                    justification="",
                ),
                TagAction(
                    identifier=PrivateBlockTagIdentifier("112d['company']3f"),
                    action=ActionCodes.KEEP,
                    justification="",
                ),
                TagAction(
                    identifier=RepeatingGroup("50xx,xxxx"),
                    action=ActionCodes.DUMMY,
                    justification="",
                ),
                TagAction(
                    identifier=SingleTag(0x3313001D),
                    action=ActionCodes.KEEP,
                    justification="",
                ),  # unknown tag
            ],
            "1.2.840.10008*": [
                TagAction(
                    identifier=SingleTag("PatientID"),
                    action=ActionCodes.REMOVE,
                    justification="",
                ),
                TagAction(
                    identifier=SingleTag("Modality"),
                    action=ActionCodes.REMOVE,
                    justification="",
                ),
                TagAction(
                    identifier=PrivateAttributes(),
                    action=ActionCodes.REMOVE,
                    justification="",
                ),
            ],
        },
        filters=[
            Filter(
                criterion=CriterionString(
                    content="Modality.equals('US') and BurntInAnnotation.equals('No')"
                ),
                justification="important",
            ),
            Filter(
                criterion=CriterionString(
                    content="SOPClassUID.equals('123456')"
                ),
                justification="this sopclass is bad",
            ),
        ],
        pixel=[
            PixelOperation(
                description="Model this and that",
                criterion=CriterionString(
                    content="Rows.equals(1024) and Columns.equals(720) and "
                    "Modelname.equals('Toshiba bla')"
                ),
                areas=[PixelArea(area=(0, 0, 720, 50))],
            ),
            PixelOperation(
                description="Another test operation",
                criterion=CriterionString(
                    content="Rows.equals(1024) and Columns.equals(740) and "
                    "Modelname.equals('Canon bla')"
                ),
                areas=[PixelArea(area=(0, 0, 720, 150))],
            ),
        ],
        private=[
            PrivateAllowGroup(
                justification="Is really safe. See https://a_link_to_dicom_"
                "conformance_statement",
                elements=[
                    PrivateElement(
                        identifier='0075["company"]01',
                        description="Amount of contrast used",
                        value_representation="LO",
                    ),
                    PrivateElement(
                        identifier='0075["company"]02',
                        description="algorithm settings",
                        value_representation="LO",
                        value_multiplicity="2",
                    ),
                ],
            )
        ],
    )


def test_pydantic_serialiazation():
    action = TagAction(
        identifier=SingleTag("PatientID"),
        action=ActionCodes.REMOVE,
        justification="",
    )
    serialized = action.model_dump()
    reserialized = TagAction.model_validate(serialized)
    assert reserialized


def test_protocol_serialization(a_protocol):
    serialized = a_protocol.model_dump_json(indent=2)
    reserialized = Protocol.model_validate_json(serialized)

    # serialization should not have changed any data
    assert a_protocol.model_dump_json(
        indent=2
    ) == reserialized.model_dump_json(indent=2)


def test_dicom_criterion_serialization():
    """A criterion is serialized to JSON as a string, but as an object it has
    a fully parsed rich inner structure.

    Make sure this all works

    """
    crit = Criterion('Modality.equals("US") and BurntInAnnotation.exists()')
    critstr = CriterionString(content=crit)
    critstr_from_str = CriterionString(
        content='Modality.equals("US") and BurntInAnnotation.exists()'
    )

    assert str(critstr) == str(critstr_from_str)

    as_json = critstr.model_dump_json()
    back_again = CriterionString.model_validate_json(as_json)

    assert as_json == back_again.model_dump_json()
