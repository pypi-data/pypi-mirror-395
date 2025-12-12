from xml.dom import NotFoundErr

import pytest
from unittest.mock import MagicMock, PropertyMock, patch
from qpysequence.program import Program, Memory
from qpysequence.program.instructions import WaitSync, Nop, Wait
from qpysequence.program.block import Block
from qpysequence.program.loop import Loop
from qpysequence.constants import PROG_MAX_REGISTERS

@pytest.fixture(name="program")
def fixture_program() -> Program:
    """Loads Program

    Returns:
        Program: Instance of the Program class
    """
    return Program()

def are_q1asm_equal(a: str, b: str):
    """Compare two Q1ASM strings and parse them to remove spaces, new lines and long_wait counters"""
    return "".join([cmd for cmd in a.strip().split() if "long_wait" not in cmd]) == "".join(
        [cmd for cmd in b.strip().split() if "long_wait" not in cmd]
    )

def test_initialization(program: Program):
    """Test that a Program initializes as expected."""
    # Check setup block with wait_sync=True
    setup = program.get_block("setup")
    assert isinstance(setup.components[-1], WaitSync)
    assert setup.components[-1].args[0] == 4

    # Initialize without wait_sync
    program_no_wait = Program(wait_sync=False)
    setup_no_wait = program_no_wait.get_block("setup")
    assert len(setup_no_wait.components) == 0  # No WaitSync added

def test_duration(program: Program):
    with patch('qpysequence.program.block.Block.duration', new_callable=PropertyMock) as mock_block_duration:
        mock_block_duration.return_value = 100

        block1 = Block("block1")
        block2 = Block("block2")
        program.append_block(block1)
        program.append_block(block2)

        _ = program.duration

        mock_block_duration.assert_called()


def test_append_block(program: Program):
    """Test appending blocks to the program."""
    block1 = Block("block1")
    block2 = Block("block2")
    program.append_block(block1)
    program.append_block(block2)

    # Check both blocks are added
    assert program.blocks[-2].name == "block1"
    assert program.blocks[-1].name == "block2"

    # Test duplicate block name
    with pytest.raises(KeyError):
        program.append_block(Block("block1"))

def test_append_loop(program: Program):
    """Test appending loops to the program."""
    loop = Loop("loop1", 10)
    program.append_block(loop)
    assert program.blocks[-1].name == "loop1"

    setup_block = program.get_block("setup")
    assert loop.init_counter_instr not in setup_block.components

def test_get_block(program: Program):
    """Test retrieving blocks by name."""
    block = Block("test_block")
    program.append_block(block)

    retrieved_block = program.get_block("test_block")
    assert retrieved_block == block

    with pytest.raises(NotFoundErr):
        program.get_block("non_existent_block")

def test_allocate_registers(program: Program):
    """Test that allocate_registers is called for each block."""
    # Create mock blocks
    block1 = Block("block1")
    block2 = Block("block2")

    # Replace allocate_registers with a mock
    block1.allocate_registers = MagicMock()
    block2.allocate_registers = MagicMock()

    # Add the blocks to the program
    program.append_block(block1)
    program.append_block(block2)

    # Call allocate_registers
    program.allocate_registers()

    # Check that allocate_registers was called on both blocks
    block1.allocate_registers.assert_called_once_with(program._memory)
    block2.allocate_registers.assert_called_once_with(program._memory)

def test_check_nops(program: Program):
    """Test checking for where NOPs are needed."""
    block = Block("block1")
    program.append_block(block)

    program.check_nops()
    # Assuming Nopper state is updated after check_nops
    assert program._nopper.get_list_of_indices() == []

def test_place_nops():
    """Test the place_nops method of Program."""
    program = Program()
    program.blocks.pop()

    # Mock blocks with a nested structure
    block1 = Block("block1")
    block2 = Block("block2")
    sub_block1 = Block("sub_block1")
    sub_block2 = Block("sub_block2")

    # Add sub_blocks to block1 and block2
    block1.components.append(sub_block1)
    block2.components.append(sub_block2)

    # Add blocks to the program
    program.blocks.extend([block1, block2])

    # Mock Nopper behavior
    program._nopper = MagicMock()
    program._nopper.get_list_of_indices.return_value = [
        [0, 0, 0],  # Place Nop in sub_block1
        [1, 0, 0],  # Place Nop in sub_block2
    ]

    # Mock append_component method for sub-blocks
    sub_block1.append_component = MagicMock()
    sub_block2.append_component = MagicMock()

    # Call the method under test
    program.place_nops()

    # Assert append_component was called with a Nop instance at the correct index
    sub_block1.append_component.assert_called_once()
    sub_block2.append_component.assert_called_once()

    # Verify arguments (avoiding direct Nop instance comparison)
    sub_block1_call_args = sub_block1.append_component.call_args
    sub_block2_call_args = sub_block2.append_component.call_args

    assert isinstance(sub_block1_call_args[0][0], Nop)  # First arg is a Nop instance
    assert sub_block1_call_args[0][1] == len(sub_block1.components) - 1  # Correct index

    assert isinstance(sub_block2_call_args[0][0], Nop)  # First arg is a Nop instance
    assert sub_block2_call_args[0][1] == len(sub_block2.components) - 1  # Correct index

    # Assert nopper was reset and check_nops was called
    program._nopper.reset.assert_called_once()
    program._nopper.get_list_of_indices.assert_called_once()

def test_compilation(program: Program):
    """Test compilation pipeline."""
    block = Block("block1")
    program.append_block(block)
    program.compile()

    assert program._compiled is True
    assert repr(program)  # Check that __repr__ works

def test_repr(program: Program):
    """Test the string representation of the program."""
    block = Block("block1")
    program.append_block(block)

    program.compile()
    program_repr = repr(program)
    assert "block1" in program_repr

def test_allocate_registers_with_reuse_registers():
    """Test that allocate_registers marks registers out of use when a Block has reuse_registers. The last iteration falls back onto RO that has been freed"""
    memory = Memory(PROG_MAX_REGISTERS)
    memory.mark_out_of_use = MagicMock()

    register = MagicMock()
    block = Block("block")
    block.reuse_registers = [register]

    # Make the block contain itself so isinstance(component, Block) is True
    block.components = [block]

    block.allocate_registers = MagicMock()
    Block.allocate_registers(block, memory)

    block.allocate_registers.assert_called_once_with(memory)
    memory.mark_out_of_use.assert_called_once_with(register)

def test_block_reusing_register():
    """Test that reuses previously used registers in a loop."""
    block = Block("block")
    memory = Memory(4)
    block.allocate_registers(memory)
    
    for x in range(5):
        loop = Loop(f"loop_{x}", begin=0, end=100, step=1)
        loop.append_component(Wait(1000))
        block._append_block(loop)
        block.allocate_registers(memory)
    block = repr(block)


    q1asm = """block:
                    move             0, R0          
    loop_0:
                    wait             1000           
                    add              R0, 1, R0      
                    nop                             
                    jlt              R0, 100, @loop_0
                    move             0, R1          
    loop_1:
                    wait             1000           
                    add              R1, 1, R1      
                    nop                             
                    jlt              R1, 100, @loop_1
                    move             0, R2          
    loop_2:
                    wait             1000           
                    add              R2, 1, R2      
                    nop                             
                    jlt              R2, 100, @loop_2
                    move             0, R3          
    loop_3:
                    wait             1000           
                    add              R3, 1, R3      
                    nop                             
                    jlt              R3, 100, @loop_3
                    move             0, R0          
    loop_4:
                    wait             1000           
                    add              R0, 1, R0      
                    nop                             
                    jlt              R0, 100, @loop_4"""
        
    are_q1asm_equal(q1asm,block)
