"""
Demo script for PyChronicle

Run this file after enabling the AST rewriter
to generate execution history.
"""

from tracer.execution_tracer import ExecutionTracer


tracer = ExecutionTracer()


x = 10
tracer.trace("x", x, 1)

y = 25
tracer.trace("y", y, 2)

z = x + y
tracer.trace("z", z, 3)

x = x + 5
tracer.trace("x", x, 4)

y *= 2
tracer.trace("y", y, 5)

average = (x + y + z) / 3
tracer.trace("average", average, 6)


numbers = [1, 2, 3]

tracer.trace("numbers", numbers, 7)

numbers.append(4)

tracer.trace("numbers", numbers, 8)


student = {
    "name": "Alice",
    "marks": 92
}

tracer.trace(
    "student",
    student,
    9
)

student["marks"] = 95

tracer.trace(
    "student",
    student,
    10
)


print("\nExecution History\n")

for row in tracer.history():

    print(row)


print("\nDelta History\n")

for row in tracer.delta_history():

    print(row)


tracer.close()