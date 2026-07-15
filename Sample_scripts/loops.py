"""
loops.py

Example program containing loops to demonstrate
PyChronicle variable tracking.
"""

from tracer.execution_tracer import ExecutionTracer

tracer = ExecutionTracer()

total = 0
tracer.trace("total", total, 1)

for i in range(1, 6):

    tracer.trace("i", i, 4)

    total += i

    tracer.trace("total", total, 6)

numbers = [10, 20, 30, 40]

tracer.trace("numbers", numbers, 9)

sum_numbers = 0

for value in numbers:

    tracer.trace("value", value, 13)

    sum_numbers += value

    tracer.trace("sum_numbers", sum_numbers, 15)

count = 0

while count < 3:

    tracer.trace("count", count, 21)

    count += 1

    tracer.trace("count", count, 23)

print("Loop execution finished.")

tracer.close()