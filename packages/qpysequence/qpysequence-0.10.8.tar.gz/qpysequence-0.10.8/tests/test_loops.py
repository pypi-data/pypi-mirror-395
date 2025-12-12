import pytest

from qpysequence.program import Block, InfiniteLoop, IterativeLoop, Loop, Register
from qpysequence.program.instructions import Add, Jge, Jlt, Jmp
from qpysequence.program.instructions import Loop as LoopInstr
from qpysequence.program.instructions import Move, Nop, Not, Sub, Wait


class TestLoops:
    """Unitary tests checking the Waveforms class behavior"""

    def test_infinite_loop(self):
        """Tests that simple loop instructions are generated correctly."""
        loop = InfiniteLoop("infinite_loop")
        assert len(loop.builtin_components) == 1
        assert isinstance(loop.builtin_components[0], Jmp)

    def test_simple_loop(self):
        """Tests that simple loop instructions are generated correctly."""
        loop = Loop("simple_loop", 100)
        assert len(loop.builtin_components) == 1
        assert isinstance(loop.loop_instr, LoopInstr)
        assert loop.init_counter_instr.args[0] == 100

    def test_jlt_loop(self):
        """Tests that jlt loop instructions are generated correctly."""
        loop = Loop("jlt_loop", 3, 98, 7)
        assert len(loop.builtin_components) == 3
        assert isinstance(incr_instr := loop.builtin_components[0], Add)
        assert incr_instr.args[1] == 7
        assert isinstance(loop.loop_instr, Jlt)
        assert loop.loop_instr.args[1] == 98
        assert loop.init_counter_instr.args[0] == 3
        assert isinstance(loop.builtin_components[1], Nop)

    def test_jge_loop(self):
        """Tests that jge loop instructions are generated correctly."""
        loop = Loop("jge_loop", 100, 10, -8)
        assert isinstance(incr_instr := loop.builtin_components[0], Sub)
        assert incr_instr.args[1] == 8
        assert isinstance(loop.loop_instr, Jge)
        assert loop.loop_instr.args[1] == 11
        assert loop.init_counter_instr.args[0] == 100
        assert isinstance(loop.builtin_components[1], Nop)

    def test_simple_iterative_loop(self):
        """Tests that a simple iterative loop instructions are generated correctly."""
        block = Block("block")
        loop = IterativeLoop("iterative_loop", iterations=100)
        loop.append_component(component=Wait(wait_time=123))
        assert isinstance(loop.iteration_register, Register)
        assert len(loop.loop_registers) == 0
        assert len(loop.builtin_components) == 1
        assert isinstance(loop.builtin_components[0], LoopInstr)
        assert loop.builtin_components[0].args[0] == loop.iteration_register
        assert loop.builtin_components[0].args[1] == "@iterative_loop"

        loop.be_appended(block)
        assert len(block.components) == 2
        assert isinstance(block.components[0], Move)
        assert block.components[0].args[0] == 100
        assert block.components[0].args[1] == loop.iteration_register

        assert loop.iterations == 100
        assert loop.duration_iter == 123
        assert loop.duration == 123 * 100

    def test_positive_step_iterative_loop(self):
        """Tests that a simple iterative loop instructions are generated correctly."""
        block = Block("block")
        loop = IterativeLoop("iterative_loop", iterations=100, loops=[(-50, 10)])
        assert isinstance(loop.iteration_register, Register)
        assert len(loop.loop_registers) == 1
        assert len(loop.builtin_components) == 2
        assert isinstance(loop.builtin_components[0], Add)
        assert loop.builtin_components[0].args[0] == loop.loop_registers[0]
        assert loop.builtin_components[0].args[1] == 10
        assert loop.builtin_components[0].args[2] == loop.loop_registers[0]
        assert isinstance(loop.builtin_components[1], LoopInstr)
        assert loop.builtin_components[1].args[0] == loop.iteration_register
        assert loop.builtin_components[1].args[1] == "@iterative_loop"

        loop.be_appended(block)
        assert len(block.components) == 6
        assert isinstance(block.components[0], Move)
        assert block.components[0].args[0] == 100
        assert block.components[0].args[1] == loop.iteration_register

        assert isinstance(block.components[1], Move)
        assert block.components[1].args[0] == 50
        assert block.components[1].args[1] == loop.loop_registers[0]

        assert isinstance(block.components[2], Not)
        assert block.components[2].args[0] == loop.loop_registers[0]
        assert block.components[2].args[1] == loop.loop_registers[0]

        assert isinstance(block.components[3], Nop)

        assert isinstance(block.components[4], Add)
        assert block.components[4].args[0] == loop.loop_registers[0]
        assert block.components[4].args[1] == 1
        assert block.components[4].args[2] == loop.loop_registers[0]

    def test_negative_step_iterative_loop(self):
        """Tests that a simple iterative loop instructions are generated correctly."""
        block = Block("block")
        loop = IterativeLoop("iterative_loop", iterations=100, loops=[(50, -10)])
        assert isinstance(loop.iteration_register, Register)
        assert len(loop.loop_registers) == 1
        assert len(loop.builtin_components) == 2
        assert isinstance(loop.builtin_components[0], Sub)
        assert loop.builtin_components[0].args[0] == loop.loop_registers[0]
        assert loop.builtin_components[0].args[1] == 10
        assert loop.builtin_components[0].args[2] == loop.loop_registers[0]
        assert isinstance(loop.builtin_components[1], LoopInstr)
        assert loop.builtin_components[1].args[0] == loop.iteration_register
        assert loop.builtin_components[1].args[1] == "@iterative_loop"

        loop.be_appended(block)

        assert len(block.components) == 3
        assert isinstance(block.components[0], Move)
        assert block.components[0].args[0] == 100
        assert block.components[0].args[1] == loop.iteration_register

        assert isinstance(block.components[1], Move)
        assert block.components[1].args[0] == 50
        assert block.components[1].args[1] == loop.loop_registers[0]
