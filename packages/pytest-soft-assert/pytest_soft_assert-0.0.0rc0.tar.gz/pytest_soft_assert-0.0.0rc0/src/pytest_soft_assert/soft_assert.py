import pytest
from contextlib import contextmanager
from typing import Literal


class SoftAssertionError(Exception): ...


class SoftAssert:

    def __init__(self, failure_mode = "xfail"):
        self.errors = []
        self.already_failed = False
        self.failure_mode = failure_mode

    def setFailureMode(self, mode: Literal['fail', 'xfail']):
        self.failure_mode = mode

    # Method-style assertion
    def check(self, condition, msg=None):
        if not condition:
            self.errors.append(msg or "Soft assertion failed")

    # Context manager style
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        # Do NOT swallow real exceptions
        if exc:
            return False
        self.assert_all()
        return True

    # -----------------------
    # Soft raise context manager
    # -----------------------
    @contextmanager
    def raises(self, expected_exception, msg=None):
        """Softly assert that a block raises `expected_exception`."""
        try:
            yield
        except expected_exception as e:
            # Correct exception was raised → do nothing
            pass
        except Exception as e:
            # Wrong exception type → record as soft failure
            self.errors.append(
                msg or f"Expected {expected_exception.__name__}, got {type(e).__name__}: {e}"
            )
        else:
            # No exception was raised → record as soft failure
            self.errors.append(
                msg or f"Expected {expected_exception.__name__} to be raised, but nothing was raised"
            )

    def assert_all(self):
        if self.already_failed:
            return 
        if self.errors:
            msg = "\n".join(self.errors)
            self.already_failed = True
            if self.failure_mode == "fail":
                raise SoftAssertionError(msg)
            else:
                pytest.xfail(msg)
