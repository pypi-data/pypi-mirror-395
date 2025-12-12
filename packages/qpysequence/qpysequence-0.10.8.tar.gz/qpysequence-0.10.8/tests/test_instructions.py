import pytest

from unittest.mock import MagicMock
from qpysequence.program import Register
from qpysequence.enums import InstructionArgument
from qpysequence.program.instructions import (
    Instruction,
    Acquire,
    AcquireTtl,
    AcquireWeighed,
    Add,
    And,
    Asl,
    Asr,
    Jge,
    Jlt,
    Jmp,
    LatchRst,
    Move,
    Not,
    Or,
    Play,
    ResetPh,
    SetAwgGain,
    SetAwgOffs,
    SetCond,
    SetFreq,
    SetLatchEn,
    SetMrk,
    SetPh,
    SetPhDelta,
    Sub,
    UpdParam,
    Wait,
    WaitSync,
    WaitTrigger,
    Xor,
)


@pytest.fixture(name="allocated_register")
def fixture_register() -> Register:
    """Creates an allocated register

    Returns:
        Register: Instance of an allocated register
    """
    r = Register()
    r.allocate(0)
    return r

def test_constructor_invalid_immediate():
    """"Test invalid immediate arguments."""
    with pytest.raises(ValueError):
        Instruction(
            args=[200],  # Out of bounds
            types=[[InstructionArgument.IMMEDIATE]],
            bounds=[(0, 100)],
        )

def test_constructor_invalid_label():
    """Test invalid label arguments."""
    with pytest.raises(TypeError):
        Instruction(
            args=["not_a_label"],
            types=[[InstructionArgument.LABEL]],
        )

def test_constructor_invalid_rtd():
    """Test invalid duration."""
    with pytest.raises(ValueError):
        Instruction(
            args=[10],
            types=[[InstructionArgument.IMMEDIATE]],
            duration=2,  # Below the minimum duration
        )

def test_add_read_registers():
    """Test adding read registers."""
    reg = Register()
    instr = Instruction()
    instr.add_read_registers({reg, 5, "not_a_register"})
    assert reg in instr.read_registers
    assert 5 not in instr.read_registers

def test_add_write_registers():
    """Test adding write registers."""
    reg = Register()
    instr = Instruction()
    instr.add_write_registers({reg, 10})
    assert reg in instr.write_registers
    assert 10 not in instr.write_registers

def test_replace_register():
    """Test replacing a register."""
    reg_old = Register()
    reg_new = Register()
    instr = Instruction(args=[reg_old], types=[[InstructionArgument.REGISTER]])
    instr.replace_register(reg_old, reg_new)
    assert instr.args[0] == reg_new

def test_allocate_registers():
    """Test allocating registers."""
    reg = Register()
    memory = MagicMock()
    instr = Instruction(args=[reg], types=[[InstructionArgument.REGISTER]])
    instr.allocate_registers(memory)
    memory.allocate_register_and_mark_in_use.assert_called_once_with(reg)

def test_check_nops():
    """Test checking NOP requirements."""
    reg = Register()
    nopper = MagicMock()
    instr = Instruction()
    instr.read_registers.add(reg)
    instr.write_registers.add(reg)
    instr.check_nops(nopper, depth=2)
    nopper.check_intersection.assert_called_once_with({reg})
    nopper.set_write_registers.assert_called_once_with({reg})

def test_repr():
    """Test string representation."""
    instr = Instruction(args=[10, "@label"], types=[[InstructionArgument.IMMEDIATE], [InstructionArgument.LABEL]])
    instr.with_label("label").with_comment("comment")
    repr_instr = repr(instr)
    assert "label:" in repr_instr
    assert "10, @label" in repr_instr
    assert "# comment" in repr_instr

def test_with_label():
    """Test the with_label method."""
    instr = SetFreq(12345678).with_label("label")
    assert repr(instr).startswith("label:")

def test_with_comment():
    """Test the with_label method."""
    instr = SetFreq(12345678).with_comment("comment")
    assert repr(instr).strip().endswith("# comment")

def test_set_mrk():
    """Test the long_wait function."""
    instr = SetMrk(1)
    assert repr(instr).strip() == "set_mrk          1"

def test_set_freq():
    """Test the set_freq function."""
    instr = SetFreq(12345678)
    assert repr(instr).strip() == "set_freq         12345678"

def test_reset_ph():
    """Test the long_wait function."""
    instr = ResetPh()
    assert repr(instr).strip() == "reset_ph"

def test_set_ph():
    """Test the long_wait function."""
    instr = SetPh(123456789)
    assert repr(instr).strip() == "set_ph           123456789"

def test_set_ph_delta():
    """Test the long_wait function."""
    instr = SetPhDelta(123456789)
    assert repr(instr).strip() == "set_ph_delta     123456789"

def test_set_awg_gain():
    """Test the long_wait function."""
    instr = SetAwgGain(100, 200)
    assert repr(instr).strip() == "set_awg_gain     100, 200"

def test_set_awg_offs():
    """Test the long_wait function."""
    instr = SetAwgOffs(100, 200)
    assert repr(instr).strip() == "set_awg_offs     100, 200"

def test_upd_param():
    """Test the long_wait function."""
    instr = UpdParam(4)
    assert repr(instr).strip() == "upd_param        4"

def test_play():
    """Test the long_wait function."""
    instr = Play(0, 1, 4)
    assert repr(instr).strip() == "play             0, 1, 4"

def test_acquire():
    """Test the long_wait function."""
    instr = Acquire(0, 1, 4)
    assert repr(instr).strip() == "acquire          0, 1, 4"

def test_acquire_weighed():
    """Test the long_wait function."""
    instr = AcquireWeighed(0, 1, 2, 3, 4)
    assert repr(instr).strip() == "acquire_weighed  0, 1, 2, 3, 4"

def test_acquire_ttl():
    """Test the acquire_ttl function."""
    instr = AcquireTtl(0, 1, 1, 4)
    assert repr(instr).strip() == "acquire_ttl      0, 1, 1, 4"

def test_wait():
    """Test the long_wait function."""
    instr = Wait(100)
    assert repr(instr).strip() == "wait             100"

def test_wait_trigger():
    """Test the long_wait function."""
    instr = WaitTrigger(5, 100)
    assert repr(instr).strip() == "wait_trigger     5, 100"

def test_wait_sync():
    """Test the long_wait function."""
    instr = WaitSync(4)
    assert repr(instr).strip() == "wait_sync        4"

def test_move(allocated_register: Register):
    """Test the move function."""
    instr = Move(0, allocated_register)
    assert repr(instr).strip() == "move             0, R0"

def test_not(allocated_register: Register):
    """Test the not function."""
    instr = Not(0, allocated_register)
    assert repr(instr).strip() == "not              0, R0"

def test_add(allocated_register: Register):
    """Test the add function."""
    instr = Add(allocated_register, 0, allocated_register)
    assert repr(instr).strip() == "add              R0, 0, R0"

def test_sub(allocated_register: Register):
    """Test the sub function."""
    instr = Sub(allocated_register, 0, allocated_register)
    assert repr(instr).strip() == "sub              R0, 0, R0"

def test_and(allocated_register: Register):
    """Test the and function."""
    instr = And(allocated_register, 0, allocated_register)
    assert repr(instr).strip() == "and              R0, 0, R0"

def test_or(allocated_register: Register):
    """Test the or function."""
    instr = Or(allocated_register, 0, allocated_register)
    assert repr(instr).strip() == "or               R0, 0, R0"

def test_asl(allocated_register: Register):
    """Test the asl function."""
    instr = Asl(allocated_register, 0, allocated_register)
    assert repr(instr).strip() == "asl              R0, 0, R0"

def test_asr(allocated_register: Register):
    """Test the asr function."""
    instr = Asr(allocated_register, 0, allocated_register)
    assert repr(instr).strip() == "asr              R0, 0, R0"

def test_xor(allocated_register: Register):
    """Test the xor function."""
    instr = Xor(allocated_register, 0, allocated_register)
    assert repr(instr).strip() == "xor              R0, 0, R0"

def test_set_cond():
    """Test the set_cond function"""
    instr = SetCond(1, 16383, 2, 4)
    assert repr(instr).strip() == "set_cond         1, 16383, 2, 4"

def test_set_latch_en(allocated_register: Register):
    """Test the set_latch_en function"""
    instr = SetLatchEn(allocated_register, 4)
    assert repr(instr).strip() == "set_latch_en     R0, 4"

def test_latch_rst(allocated_register: Register):
    """Test the latch_rst function"""
    instr = LatchRst(allocated_register)
    assert repr(instr).strip() == "latch_rst        R0"

def test_jlt(allocated_register: Register):
    """Test the jlt function"""
    instr = Jlt(allocated_register, 123, "@label")
    assert repr(instr).strip() == "jlt              R0, 123, @label"

def test_jge(allocated_register: Register):
    """Test the jlt function"""
    instr = Jge(allocated_register, 123, "@label")
    assert repr(instr).strip() == "jge              R0, 123, @label"

def test_jmp(allocated_register: Register):
    """Test the jlt function"""
    instr = Jmp("@label")
    assert repr(instr).strip() == "jmp              @label"
