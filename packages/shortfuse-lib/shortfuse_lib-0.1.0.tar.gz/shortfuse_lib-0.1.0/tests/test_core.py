import multiprocessing
import os
import pytest
import shortfuse

def run_in_process(target_func, args=()):
    """
    Helper: Runs a function in a separate process.
    Returns the exit code of that process.
    0 = Success, 1 = Shortfuse Triggered
    """
    # Use fork context to avoid pickling issues on macOS
    ctx = multiprocessing.get_context('fork')
    p = ctx.Process(target=target_func, args=args)
    p.start()
    p.join()
    return p.exitcode

# =============================================================================
#  Helper Functions (Module-level for pickling compatibility)
# =============================================================================

def _halt_scenario():
    shortfuse.halt("Legacy code accessed!")

def _halt_if_true():
    shortfuse.halt_if(True, "Die")

def _halt_if_false():
    shortfuse.halt_if(False, "Die")

def _halt_unless_true():
    shortfuse.halt_unless(True, "Live")

def _halt_unless_false():
    shortfuse.halt_unless(False, "Die")

def _halt_if_not_none_with_none():
    shortfuse.halt_if_not_none(None)

def _halt_if_not_none_with_data():
    shortfuse.halt_if_not_none("Data")

# =============================================================================
#  Tests
# =============================================================================

def test_halt_basic():
    """
    ### Scenario: Unconditional Halt
    Use Case: Booby-trapping dead code.
    """
    # Expect exit code 1 (Crash)
    assert run_in_process(_halt_scenario) == 1

def test_halt_if():
    """
    ### Scenario: Halt if Condition is True
    Use Case: "Stop if X happens"
    """
    # Case A: True condition (Should Crash)
    assert run_in_process(_halt_if_true) == 1

    # Case B: False condition (Should Pass)
    assert run_in_process(_halt_if_false) == 0

def test_halt_unless():
    """
    ### Scenario: Halt unless Condition is True
    Use Case: "Only proceed if X is valid"
    """
    # Case A: True condition (Should Pass)
    assert run_in_process(_halt_unless_true) == 0

    # Case B: False condition (Should Crash)
    assert run_in_process(_halt_unless_false) == 1

def test_halt_if_not_none():
    """
    ### Scenario: Halt if object exists
    Use Case: Forbidden optional dependencies
    """
    # Case A: Object is None (Should Pass)
    assert run_in_process(_halt_if_not_none_with_none) == 0

    # Case B: Object exists (Should Crash)
    assert run_in_process(_halt_if_not_none_with_data) == 1
