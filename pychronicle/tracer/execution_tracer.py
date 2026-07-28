"""
execution_tracer.py

Runtime execution tracer for PyChronicle.

Unlike parser.py (which only looks at source text), this module
actually *runs* the target program and watches it happen. It uses
sys.settrace to get a callback on every executed line, and on each
callback it diffs the current frame's local namespace against what it
saw last time in that same frame. Any new or changed name is reported
as an assignment via a callback, in real execution order, with the
real runtime value (not just the source expression that produced it).

This is what makes the "time travel debugger" possible: every entry
recorded downstream in the database corresponds to a real moment in
the program's execution, in the order it actually happened.
"""

import sys
import types
from typing import Any, Callable, Dict, Optional

# Runtime objects that show up as "new names" in a frame but aren't
# meaningful data assignments to surface in the timeline (a `def` or
# `class` statement binds a name too, but nobody wants "my_function ="
# cluttering their variable history).
_NON_DATA_TYPES = (
    types.FunctionType,
    types.MethodType,
    types.ModuleType,
    type,
)

# Names that live in every frame's locals/globals but aren't "user"
# variables and should never be reported as assignments.
_IGNORED_NAMES = {
    "__builtins__", "__name__", "__doc__", "__file__",
    "__package__", "__loader__", "__spec__", "__annotations__",
    "__cached__",
}

_SENTINEL = object()

OnAssignment = Callable[[str, Any, int, str], None]


def _values_equal(a: Any, b: Any) -> bool:
    """Compare two values for equality defensively. Some objects
    (numpy arrays, custom __eq__ implementations, etc.) don't return a
    plain bool from ==, so we fall back to identity comparison rather
    than raising or misbehaving."""
    if a is b:
        return True
    try:
        result = a == b
        if isinstance(result, bool):
            return result
        return bool(result)
    except Exception:
        return False


def _snapshot_for_diff(value: Any) -> Any:
    """Best-effort shallow copy so an in-place mutation (e.g.
    list.append) of a previously-seen variable is still detected as a
    change the next time we diff, instead of comparing a container
    against itself by identity."""
    if isinstance(value, list):
        try:
            return list(value)
        except Exception:
            return value
    if isinstance(value, dict):
        try:
            return dict(value)
        except Exception:
            return value
    if isinstance(value, set):
        try:
            return set(value)
        except Exception:
            return value
    return value


class ExecutionTracer:
    """
    Traces a running Python program and reports every variable
    assignment as it happens, in execution order.

    Usage:
        tracer = ExecutionTracer(on_assignment, target_filename=path)
        tracer.start()
        try:
            ... run the target program ...
        finally:
            tracer.stop()

    `on_assignment(name, value, line_number, scope)` is invoked
    synchronously for every detected change, so the caller (typically
    executor.run_and_trace) can persist it immediately.
    """

    def __init__(
        self,
        on_assignment: OnAssignment,
        target_filename: Optional[str] = None,
    ):
        self._on_assignment = on_assignment
        self._target_filename = target_filename
        # frame -> {var_name: last-seen-snapshot}
        self._frame_state: Dict[types.FrameType, Dict[str, Any]] = {}

    # ------------------------------------------------------------------

    def start(self) -> None:
        sys.settrace(self._trace_dispatch)

    def stop(self) -> None:
        sys.settrace(None)
        self._frame_state.clear()

    # ------------------------------------------------------------------

    def _is_target_frame(self, frame: types.FrameType) -> bool:
        if self._target_filename is None:
            return True
        return frame.f_code.co_filename == self._target_filename

    @staticmethod
    def _scope_name(frame: types.FrameType) -> str:
        name = frame.f_code.co_name
        if name == "<module>":
            return "module"
        return name

    def _trace_dispatch(self, frame, event, arg):
        # Only trace frames that belong to the file we were asked to
        # run (not, say, importlib or FastAPI machinery), but still
        # return a local-trace function for calls *into* other files
        # so we don't lose the ability to trace back out via 'return'.
        if event == "call":
            if self._is_target_frame(frame):
                self._frame_state[frame] = {}
            return self._trace_dispatch

        if not self._is_target_frame(frame):
            return self._trace_dispatch

        if event == "line":
            self._check_assignments(frame)
            return self._trace_dispatch

        if event == "return":
            self._check_assignments(frame)
            self._frame_state.pop(frame, None)
            return self._trace_dispatch

        return self._trace_dispatch

    def _check_assignments(self, frame: types.FrameType) -> None:
        prev = self._frame_state.setdefault(frame, {})

        for name, value in frame.f_locals.items():
            if name in _IGNORED_NAMES or name.startswith("__"):
                continue
            if isinstance(value, _NON_DATA_TYPES):
                continue

            prev_value = prev.get(name, _SENTINEL)
            changed = prev_value is _SENTINEL or not _values_equal(prev_value, value)

            if changed:
                prev[name] = _snapshot_for_diff(value)
                self._on_assignment(
                    name,
                    value,
                    frame.f_lineno,
                    self._scope_name(frame),
                )