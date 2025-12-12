import numpy as np
import pytest

from qpysequence.acquisitions import Acquisitions


@pytest.fixture(name="acquisitions")
def fixture_acquisitions() -> Acquisitions:
    """Loads Acquisitions

    Returns:
        Acquisitions: Instance of the Acquisitions class
    """
    return Acquisitions()


class TestAcquisitions:
    """Unitary tests checking the Acquisitions class behavior"""

    def test_single_add(self, acquisitions: Acquisitions):
        """Tests that a waveform is properly added to the Acquisitions object."""
        acquisitions.add("single", 1)
        expected = {"single": {"num_bins": 1, "index": 0}}
        assert acquisitions.to_dict() == expected
