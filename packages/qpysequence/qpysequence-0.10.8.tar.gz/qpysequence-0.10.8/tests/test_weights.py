import numpy as np
import pytest

from qpysequence.weights import Weights


@pytest.fixture(name="weights")
def fixture_weights() -> Weights:
    """Loads Weights

    Returns:
        Weights: Instance of the Weights class
    """
    return Weights()


class TestWeights:
    """Unitary tests checking the Weights class behavior"""

    def test_single_add(self, weights: Weights):
        """Tests that a weight is properly added to the Weights object."""
        array = np.arange(0, 10, 1)
        weights.add(array)
        expected_repr = {"weight_0": {"data": array.tolist(), "index": 0}}
        assert weights.to_dict() == expected_repr

    def test_add_pair(self, weights: Weights):
        """Tests that a weight pair is properly added to the Weights object."""
        array_0 = np.arange(0, 10, 1)
        array_1 = np.arange(10, 0, -1)
        weights.add_pair((array_0, array_1))
        expected_repr = {
            "pair_0_I": {"data": array_0.tolist(), "index": 0},
            "pair_0_Q": {"data": array_1.tolist(), "index": 1},
        }
        assert weights.to_dict() == expected_repr

    def test_add_from_complex(self, weights: Weights):
        """Tests that a complex weight is properly added to the Weights object."""
        array_real = np.arange(0, 10, 1)
        array_imag = np.arange(10, 0, -1)
        array_complex = array_real + 1j * array_imag
        weights.add_pair_from_complex(array_complex)
        expected_repr = {
            "pair_0_I": {"data": array_real.tolist(), "index": 0},
            "pair_0_Q": {"data": array_imag.tolist(), "index": 1},
        }
        assert weights.to_dict() == expected_repr

    def test_find_by_name(self, weights: Weights):
        """Tests that a weight search by name is successful."""
        expected_array = np.arange(0, 10, 1)
        weights.add(expected_array, name="test")
        weight = weights.find_by_name("test")
        assert weight.name == "test"

    def test_find_by_name_raises_exception(self, weights: Weights):
        """Tests if NameError exception is raised."""
        with pytest.raises(NameError):
            weights.find_by_name("no name")
