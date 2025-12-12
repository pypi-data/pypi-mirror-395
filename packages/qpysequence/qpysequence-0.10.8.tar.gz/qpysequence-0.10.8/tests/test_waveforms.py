import numpy as np
import pytest

from qpysequence.waveforms import Waveforms


@pytest.fixture(name="waveforms")
def fixture_waveforms() -> Waveforms:
    """Loads Waveforms

    Returns:
        Waveforms: Instance of the Waveforms class
    """
    return Waveforms()


class TestWaveforms:
    """Unitary tests checking the Waveforms class behavior"""

    def test_single_add(self, waveforms: Waveforms):
        """Tests that a waveform is properly added to the Waveforms object."""
        array = np.arange(0, 10, 1)
        waveforms.add(array)
        expected_repr = {"waveform_0": {"data": array.tolist(), "index": 0}}
        assert waveforms.to_dict() == expected_repr

    def test_add_pair(self, waveforms: Waveforms):
        """Tests that a waveform pair is properly added to the Waveforms object."""
        array_0 = np.arange(0, 10, 1)
        array_1 = np.arange(10, 0, -1)
        waveforms.add_pair((array_0, array_1))
        expected_repr = {
            "pair_0_I": {"data": array_0.tolist(), "index": 0},
            "pair_0_Q": {"data": array_1.tolist(), "index": 1},
        }
        assert waveforms.to_dict() == expected_repr

    def test_add_from_complex(self, waveforms: Waveforms):
        """Tests that a complex waveform is properly added to the Waveforms object."""
        array_real = np.arange(0, 10, 1)
        array_imag = np.arange(10, 0, -1)
        array_complex = array_real + 1j * array_imag
        waveforms.add_pair_from_complex(array_complex)
        expected_repr = {
            "pair_0_I": {"data": array_real.tolist(), "index": 0},
            "pair_0_Q": {"data": array_imag.tolist(), "index": 1},
        }
        assert waveforms.to_dict() == expected_repr

    def test_modify(self, waveforms: Waveforms):
        """Tests that a waveform is properly modified to the Waveforms object."""
        array = np.arange(0, 10, 1)
        new_array = np.arange(0, 20, 1)

        waveforms.add(array)
        waveforms.modify("waveform_0", new_array)

        expected_repr = {"waveform_0": {"data": new_array.tolist(), "index": 0}}

        assert waveforms.to_dict() == expected_repr

    def test_modify_pair(self, waveforms: Waveforms):
        """Tests that a waveform pair is properly modified to the Waveforms object."""
        array_0 = np.arange(0, 10, 1)
        array_1 = np.arange(10, 0, -1)
        new_array_0 = np.arange(0, 20, 1)
        new_array_1 = np.arange(20, 0, -1)

        waveforms.add_pair((array_0, array_1))
        waveforms.modify_pair("pair_0", (new_array_0, new_array_1))

        expected_repr = {
            "pair_0_I": {"data": new_array_0.tolist(), "index": 0},
            "pair_0_Q": {"data": new_array_1.tolist(), "index": 1},
        }
        assert waveforms.to_dict() == expected_repr

    def test_find_by_name(self, waveforms: Waveforms):
        """Tests that a waveform search by name is successful."""
        expected_array = np.arange(0, 10, 1)
        waveforms.add(expected_array, name="test")
        waveform = waveforms.find_by_name("test")
        assert waveform.name == "test"

    def test_find_by_name_raises_exception(self, waveforms: Waveforms):
        """Tests if NameError exception is raised."""
        with pytest.raises(NameError):
            waveforms.find_by_name("no name")
