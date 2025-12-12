from typing import Iterable, List

from pydantic import ConfigDict
from pydicom import Dataset

from midom.validation import (
    DatasetRejected,
    DatasetRejectedError,
    DeidentificationReference,
    Domain,
    RegionSampleSet,
    ValidationSet,
)
from tests.factories import quick_dataset


class InMemorySampleSet(RegionSampleSet):
    """Dummy implementation of RegionSampleSet"""

    model_config = ConfigDict(arbitrary_types_allowed=True)  # for Dataset

    datasets: List[Dataset]

    def all_samples(self) -> Iterable[Dataset]:
        return self.datasets


class InMemoryDeidentificationReference(DeidentificationReference):
    """Dummy implementation"""

    iteration: int = 0

    def get_reference(self, ds: Dataset) -> Dataset:
        """Will just alternate between returning a dataset and raising rejected"""
        self.iteration += 1
        if self.iteration % 2 == 1:
            return ds
        else:
            raise DatasetRejectedError("I don't want to!")


def test_validation():
    """Just build and combine some objects, see whether they make sense"""

    _ = Domain(description="Images used in tests")
    sample_set = InMemorySampleSet(
        description="Some test images",
        datasets=[
            quick_dataset(PatientName="Patient1"),
            quick_dataset(PatientName="Patient2"),
            quick_dataset(PatientName="Patient3"),
        ],
    )
    reference = InMemoryDeidentificationReference(
        description="A test reference"
    )
    validation_set = ValidationSet(
        sample_sets=[sample_set], reference=reference
    )

    items = [x for x in validation_set.items()]

    assert len(items) == 3
    assert type(items[1][1]) == DatasetRejected  # item should be
