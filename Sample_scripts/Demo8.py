"""PyChronicle sample: exception handling."""

value = 10
try:
    result = value / 2
except ZeroDivisionError:
    result = None
print(result)
