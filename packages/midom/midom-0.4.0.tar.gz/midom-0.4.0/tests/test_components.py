import pytest
from pydantic_core._pydantic_core import ValidationError

from midom.components import PrivateElement


def test_private_element():
    """A private element should have a name in addition to an identifier.

    For regular DICOM elements, you can look up the name in a general dictionary.
    But for private elements, by definition, they could be anything. Therefore, they
    need to be recorded in the data structure.
    """
    elem = PrivateElement(
        identifier="0029,[A private creator]10",
        description="A test description",
        value_representation="LO",
    )

    as_json = elem.model_dump_json()
    loaded = elem.model_validate_json(as_json)

    assert loaded.identifier == elem.identifier
    assert loaded.description == elem.description


@pytest.mark.parametrize("identifier", [("Modality"), ("(1000,1010)")])
def test_loading_non_private(identifier):
    """You can only use private tag identifiers in a private element."""
    with pytest.raises(ValidationError):
        _ = PrivateElement(identifier=identifier, description="")
