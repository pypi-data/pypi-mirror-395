"""Tests for library module"""
import math

import numpy as np
import pytest

from qpysequence.library import long_wait, multiply, set_awg_gain_relative, set_freq_hz, set_phase_rad
from qpysequence.program import Block, Register
from qpysequence.program.instructions import Add, And, Asl, Asr, Jge, Jlt, Move, Nop, SetAwgGain, SetFreq, SetPh
from qpysequence.constants import AWG_MAX_GAIN, INST_MAX_WAIT, NCO_HZ_TO_INT_MULTIPLIER, NCO_MAX_INT_PHASE


class TestLibrary:
    """Unitary tests checking the library module behavior"""

    def test_long_wait(self):
        """Test the long_wait function."""
        loops = 100
        remaining_time = 200
        wait_time = loops * INST_MAX_WAIT + remaining_time
        block = long_wait(wait_time)
        assert block.duration == wait_time

    def test_set_freq_hz(self):
        """Test the set_phase_rad function."""
        freq_in_hz = 250e6
        freq_in_q1asm = int(freq_in_hz * NCO_HZ_TO_INT_MULTIPLIER)
        direct_instruction = SetFreq(freq_in_q1asm)
        generated_instruction = set_freq_hz(freq_in_hz)
        assert repr(direct_instruction) == repr(generated_instruction)

    def test_set_phase_rad(self):
        """Test the set_phase_rad function."""
        q1asm_phase = 12345678
        phase_in_rad = (q1asm_phase / NCO_MAX_INT_PHASE) * 2 * np.pi
        direct_instruction = SetPh(q1asm_phase)
        generated_instruction = set_phase_rad(phase_in_rad)
        assert repr(direct_instruction) == repr(generated_instruction)

    def test_set_awg_gain_relative(self):
        """Test the set_awg_gain_relative function."""
        rel_gain_0 = 0.4
        rel_gain_1 = 0.6
        abs_gain_0 = int(AWG_MAX_GAIN * rel_gain_0)
        abs_gain_1 = int(AWG_MAX_GAIN * rel_gain_1)
        direct_instruction = SetAwgGain(abs_gain_0, abs_gain_1)
        generated_instruction = set_awg_gain_relative(rel_gain_0, rel_gain_1)
        assert repr(direct_instruction) == repr(generated_instruction)

    def test_multiply(self):
        """Tests the multiply function."""
        assert self.multiply_init()
        assert self.multiply_loop()
        assert self.multiply_skip_add()

    def multiply_init(self):
        """Tests the init block of multiply function."""
        op1 = Register()
        op2 = Register()
        target = Register()
        reg_aux_1 = Register()
        reg_aux_2 = Register()
        reg_aux_3 = Register()
        product = multiply(a=op1, b=op2, target=target, reg_aux_1=reg_aux_1, reg_aux_2=reg_aux_2, reg_aux_3=reg_aux_3)
        init = Block("multiply_init_1")
        init.append_components(
            [
                Move(var=op1, register=reg_aux_1),
                Move(var=op2, register=reg_aux_2),
                Move(var=0, register=target),
            ]
        )
        return repr(init) == repr(product.components[0])

    def multiply_loop(self):
        """Tests the loop block of multiply function."""
        op1 = Register()
        op2 = Register()
        target = Register()
        reg_aux_1 = Register()
        reg_aux_2 = Register()
        reg_aux_3 = Register()
        product = multiply(a=op1, b=op2, target=target, reg_aux_1=reg_aux_1, reg_aux_2=reg_aux_2, reg_aux_3=reg_aux_3)
        loop = Block("multiply_loop_2")
        loop.append_components(
            [
                And(origin=reg_aux_2, var=1, destination=reg_aux_3),
                Nop(),
                Jlt(a=reg_aux_3, b=1, instr="@multiply_skip_add_2"),
                Add(origin=target, var=reg_aux_1, destination=target),
            ]
        )
        return repr(loop) == repr(product.components[1])

    def multiply_skip_add(self):
        """Tests the skip_add block of multiply function."""
        op1 = Register()
        op2 = Register()
        target = Register()
        reg_aux_1 = Register()
        reg_aux_2 = Register()
        reg_aux_3 = Register()
        product = multiply(a=op1, b=op2, target=target, reg_aux_1=reg_aux_1, reg_aux_2=reg_aux_2, reg_aux_3=reg_aux_3)
        skip_add = Block("multiply_skip_add_3")
        skip_add.append_components(
            [
                Asr(origin=reg_aux_2, var=1, destination=reg_aux_2),
                Asl(origin=reg_aux_1, var=1, destination=reg_aux_1),
                Jge(a=reg_aux_2, b=1, instr="@multiply_loop_3"),
            ]
        )
        return repr(skip_add) == repr(product.components[2])
