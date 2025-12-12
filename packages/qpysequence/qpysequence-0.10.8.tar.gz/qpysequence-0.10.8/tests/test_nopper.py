import pytest

from qpysequence.program.nopper import Nopper
from qpysequence.program.register import Register


@pytest.fixture(name="nopper")
def fixture_nopper() -> Nopper:
    """Loads Program

    Returns:
        Program: Instance of the Program class
    """
    return Nopper()


class TestNopper:
    """Unitary tests checking the Program class behavior"""

    def test_initialization(self, nopper: Nopper):
        """Tests that a Nopper has been initialized as expected."""

        assert isinstance(nopper.write_registers, set)
        assert nopper.current_block_index == [0]
        assert nopper.last_block_index == [0]
        assert nopper.current_nop_counter == 0
        assert nopper.last_nop_counter == 0
        assert nopper.index_list == []

    def test_reset(self, nopper: Nopper):
        """Tests that a Nopper has been reseted as expected."""

        nopper.write_registers = {Register()}
        nopper.index_list = [[1]]
        nopper.current_block_index = [2]
        nopper.last_block_index = [3]
        nopper.current_nop_counter = 4
        nopper.last_nop_counter = 5

        nopper.reset()

        assert not nopper.write_registers
        assert not nopper.index_list
        assert nopper.current_block_index == [0]
        assert nopper.last_block_index == [0]
        assert nopper.current_nop_counter == 0
        assert nopper.last_nop_counter == 0

    def test_get_list_of_indices(self, nopper: Nopper):
        """Tests that the getter get_list_of_indices works correctly"""

        nopper.index_list = [[1, 2, 3], [4, 5]]
        assert nopper.get_list_of_indices() == [[1, 2, 3], [4, 5]]
        nopper.index_list = [[1, 1], [2, 2]]
        assert nopper.get_list_of_indices() != [[1, 1, 2, 2]]
        nopper.index_list = []
        assert nopper.get_list_of_indices() == []

    def test_check_intersection(self, nopper: Nopper):
        """Tests that check_intersection instersecates correctly"""
        register1 = Register()
        register1.allocate(1)
        register2 = Register()
        register2.allocate(2)

        nopper.set_write_registers({register1})
        assert nopper.check_intersection({register1})
        assert nopper.current_nop_counter == 1

        assert not nopper.check_intersection({register2})
        assert nopper.current_nop_counter == 1
