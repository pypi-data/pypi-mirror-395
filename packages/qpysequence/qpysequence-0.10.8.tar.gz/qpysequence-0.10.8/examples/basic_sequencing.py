# This example demonstrates how to create the Q1ASM program shown in the basic sequencing example from the Qblox docs
# https://qblox-qblox-instruments.readthedocs-hosted.com/en/master/tutorials/basic_sequencing.html#Create-Q1ASM-program

from typing import List

from qpysequence.program import Block, Component, Loop, Program, Register

# Import the instructions to use
from qpysequence.program.instructions import Add, Move, Play, SetMrk, Stop, UpdParam, Wait

# Create an empty program
basic_sequencing = Program()

# For the first three instructions we only need to take care of the "Initial wait period in ns" variable allocation,
# since the loop iterator is automatically handled and the wait_sync is there by default.
# Recover the setup block from the program
setup = basic_sequencing.get_block("setup")

# We can use a register without worrying for its actual index
wait_period_reg = Register()

# Finally add the move instruction to the setup block, saving the last line for the wait_sync instruction
setup.append_component(Move(20, wait_period_reg), 1)

# Create the "loop" block
loop = Loop("loop", 100)

# Add all the instructions up to the loop
loop.append_component(SetMrk(1))
loop.append_component(Play(0, 1, 4))
loop.append_component(SetMrk(0))
loop.append_component(UpdParam(16))
loop.append_component(Wait(wait_period_reg))
loop.append_component(Play(1, 0, 20))
loop.append_component(Wait(1000))
loop.append_component(Add(wait_period_reg, 20, wait_period_reg))

# The loop instruction could be added manually as the previous ones, also setting the loop counter register in the
# setup block, or it can be automatically handled adding the block to the program with the method append_loop

basic_sequencing.append_block(loop)

# Finally, to add the stop instruction, we must create a block for it
cleanup = Block("cleanup")
cleanup.append_component(Stop())
basic_sequencing.append_block(cleanup)

# The Program is converted to its string representation when the str or repr method is called on it, which is done
# implicitly when is printed on screen.
print("# Basic Sequencing Q1ASM Program", basic_sequencing, f"{'-' * 80}\n", sep="\n")

# If writing block_name.append_component(instruction) becomes too tedious and causes bad readability, the method
# block.append_components can take a list of components (instructions and/or blocks) as a parameter
loop_v2 = Block("loop_v2")
loop_comps: List[Component] = [
    SetMrk(1),
    Play(0, 1, 4),
    SetMrk(0),
    UpdParam(16),
    Wait(wait_period_reg),
    Play(1, 0, 20),
    Wait(1000),
    Add(wait_period_reg, 20, wait_period_reg),
]
loop_v2.append_components(loop_comps)

print("# Alternative Block creation", loop_v2, sep="\n")
print(f"\nProgram duration: {basic_sequencing.duration} ns.")
