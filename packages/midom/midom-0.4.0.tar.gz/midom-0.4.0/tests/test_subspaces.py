from pydicom.datadict import repeater_has_keyword, tag_for_keyword

from midom.subspaces import E1_1SubSpace, ImageTypeIDSubspace


def check_dicom_tag_validity(tag_name):
    """Raise exception if input is not a valid DICOM tag name"""

    # Missing valid tags in pydicom 2.4.4.
    # TODO fix this in pydicom (issue, pr)
    valid_but_not_in_pydicom = [
        "ROICreatorSequence",
        "ROIDateTime",
        "ROIInterpreterSequence",
        "ROIObservationDateTime",
        "TableTopPositionAlignmentUID",
    ]

    if (
        tag_for_keyword(tag_name)
        or repeater_has_keyword(tag_name)
        or tag_name in valid_but_not_in_pydicom
    ):
        return  # We know this one. It's fine
    else:
        raise ValueError(f"unknown DICOM tag '{tag_name}'")


def test_subspaces():
    """Just check that all of them contain only valid dicom keywords"""
    for tag in ImageTypeIDSubspace.tags:
        check_dicom_tag_validity(tag)

    for tag in E1_1SubSpace.tags:
        check_dicom_tag_validity(tag)
