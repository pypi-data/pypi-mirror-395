import pytest

from qpysequence.acquisitions import Acquisitions
from qpysequence.program import Program
from qpysequence.sequence import Sequence
from qpysequence.waveforms import Waveforms
from qpysequence.weights import Weights


@pytest.fixture
def qpysequence():
    """_summary_

    Returns:
        _type_: _description_
    """
    return Sequence(Program(), Waveforms(), Acquisitions(), Weights())

@pytest.fixture
def qpysequence_no_weights():
    """_summary_

    Returns:
        _type_: _description_
    """
    return Sequence(Program(), Waveforms(), Acquisitions())

@pytest.fixture
def qpysequence_no_acquisitions():
    """_summary_

    Returns:
        _type_: _description_
    """
    return Sequence(Program(), Waveforms(), Weights())

@pytest.fixture
def qpysequence_no_waveforms():
    """_summary_

    Returns:
        _type_: _description_
    """
    return Sequence(Program(), Acquisitions(), Weights())

@pytest.fixture
def qpysequence_only_program():
    """_summary_

    Returns:
        _type_: _description_
    """
    return Sequence(Program())


class TestQPySequence:
    """Unitary tests checking the QPySequence initialization steps and values"""

    def test_qpysequence_constructor(self, qpysequence):
        """_summary_

        Args:
            qpysequence (_type_): _description_
        """
        assert isinstance(qpysequence, Sequence)

    def test_qpysequence_default_weights(self, qpysequence_no_weights):
        """_summary_

        Args:
            qpysequence_no_weights (_type_): _description_
        """
        assert isinstance(qpysequence_no_weights, Sequence)
 
    def test_qpysequence_default_acquisitions(self, qpysequence_no_acquisitions):
        """_summary_

        Args:
            qpysequence_no_weights (_type_): _description_
        """
        assert isinstance(qpysequence_no_acquisitions, Sequence)

    def test_qpysequence_default_waveforms(self, qpysequence_no_waveforms):
        """_summary_

        Args:
            qpysequence_no_weights (_type_): _description_
        """
        assert isinstance(qpysequence_no_waveforms, Sequence)
        
    def test_qpysequence_program(self, qpysequence_only_program):
        """_summary_

        Args:
            qpysequence_no_weights (_type_): _description_
        """
        assert isinstance(qpysequence_only_program, Sequence)
