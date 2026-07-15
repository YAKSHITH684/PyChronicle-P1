"""
delta_tracker.py

Tracks changes in variables during program execution.
"""

from copy import deepcopy


class DeltaTracker:
    """
    Tracks previous and current values of variables.
    """

    def __init__(self):
        self.previous = {}
        self.history = []

    def update(self, variable_name, value):
        """
        Update a variable and detect changes.
        """

        old_value = deepcopy(
            self.previous.get(variable_name)
        )

        changed = old_value != value

        record = {
            "variable": variable_name,
            "old_value": old_value,
            "new_value": deepcopy(value),
            "changed": changed,
        }

        self.history.append(record)

        self.previous[variable_name] = deepcopy(value)

        return record

    def get_history(self):
        """
        Return change history.
        """

        return self.history

    def last_change(self):
        """
        Return latest change.
        """

        if self.history:
            return self.history[-1]

        return None

    def clear(self):
        """
        Reset tracker.
        """

        self.previous.clear()
        self.history.clear()