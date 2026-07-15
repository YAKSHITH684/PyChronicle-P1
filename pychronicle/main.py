from pychronicle.tracer.execution_tracer import ExecutionTracer

tracer = ExecutionTracer()

x = 10
tracer.trace("x", x, 1)

y = 20
tracer.trace("y", y, 2)

z = x + y
tracer.trace("z", z, 3)

print(tracer.history())

tracer.close()