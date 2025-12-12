# This example illustrates the way loops are actually generated. It is intended only for demonstrative purposes; any
# type of Loop can be generated without having to be aware of the actual type of loop that is generated internally.

from qpysequence.program import Loop, Program
from qpysequence.program.instructions import Acquire, Play

program = Program()

# Depending on the combination of the parameters <begin>, <end> and <step>, three types of loops will be generated
# If begin = 0 and step = 1 (default value), a simple loop is generated
loop = Loop("loop", 10)
# Otherwise, a loop with the jlt instruction is generated if begin < end (requiring step > 0)
up = Loop("up", 5, 60, 3)
# Or a jge instruction loop if begin > end (requiring step < 0)
down = Loop("down", 100, 0, -2)
# Any other combination raises an exception.
# The actual values that the counter gets, replicate those of the python built-in range(begin, end, step) function.

loop.append_components([Play(0, 1), Acquire(0, loop.counter_register)])
up.append_components([Play(2, 3), Acquire(1, up.counter_register)])
down.append_components([Play(4, 5), Acquire(2, down.counter_register)])

program.append_block(loop)
program.append_block(up)
program.append_block(down)

print(program)
