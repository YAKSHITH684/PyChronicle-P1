"""PyChronicle sample: function scope tracing."""

def calculate(value):
    doubled = value * 2
    return doubled

result = calculate(7)
print(result)
