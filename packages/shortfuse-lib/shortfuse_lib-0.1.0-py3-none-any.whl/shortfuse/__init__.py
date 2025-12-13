"""
<img src="banner.png" width="700" alt="Shortfuse Banner">

**Don't just raise exceptions—kill the process.**

`shortfuse` is a zero-tolerance "fail fast" utility for enforcing architectural boundaries.
It creates uncatchable traps in deprecated code paths to instantly halt execution and expose regressions.

---

## 💥 The "Loud" Failure Demo

When `shortfuse` halts, it prints a banner and the stack trace to `stderr` before killing the process.

**The Code:**
```python
import shortfuse

def legacy_handler():
    # Halt execution immediately if this function is called
    shortfuse.halt("Legacy V1 path is forbidden.")

legacy_handler()
```

**The Output (stderr):**

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[SHORTFUSE DETONATED]: Legacy V1 path is forbidden.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  File "demo.py", line 7, in <module>
    legacy_handler()
  File "demo.py", line 5, in legacy_handler
    shortfuse.halt("Legacy V1 path is forbidden.")
  File "/lib/shortfuse/__init__.py", line 35, in halt
    _die(message)

[SHORTFUSE] Terminating process immediately via os._exit(1).
```

---

## 🛠 API Usage

### halt(message)
Unconditionally stops execution. Use for dead code paths.

```python
shortfuse.halt("This endpoint is removed.")
```

### halt_if(condition, message)
Halts if the condition is True.

```python
shortfuse.halt_if(user.is_admin, "Admins cannot use this view")
```

### halt_unless(condition, message)
Halts if the condition is False.

```python
shortfuse.halt_unless(config.version == 3, "Only V3 config allowed")
```

### halt_if_not_none(obj, message)
Halts if the object is not None. Useful for ensuring optional legacy dependencies are removed.

```python
shortfuse.halt_if_not_none(legacy_manager, "Manager must be None")
```
"""
import sys
import traceback
import os

__version__ = "0.1.0"

def _die(message: str) -> None:
    """
    Internal helper: prints stack trace to stderr and kills the process
    via os._exit(1) to prevent interception.
    """
    # Visual separation for the logs
    print(f"\n{'!'*60}", file=sys.stderr)
    print(f"[SHORTFUSE DETONATED]: {message}", file=sys.stderr)
    print(f"{'!'*60}\n", file=sys.stderr)

    # Print the stack trace to stderr
    traceback.print_stack(file=sys.stderr)

    print("\n[SHORTFUSE] Terminating process immediately via os._exit(1).", file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()

    # Hard exit. Prevents 'except Exception', 'finally', and cleanup handlers.
    os._exit(1)

def halt(message: str = "Execution halted by Shortfuse.") -> None:
    """
    Unconditionally stops execution.
    Use for dead code paths or deprecated endpoints.
    """
    _die(message)

def halt_if(condition: bool, message: str = "Condition met: Halting execution.") -> None:
    """
    Halts if the condition is True.
    """
    if condition:
        _die(message)

def halt_unless(condition: bool, message: str = "Condition failed: Halting execution.") -> None:
    """
    Halts if the condition is False.
    """
    if not condition:
        _die(message)

def halt_if_not_none(obj, message: str = "Object should be None") -> None:
    """
    Halts if the object is not None.
    """
    if obj is not None:
        _die(f"{message} (Got type: {type(obj).__name__})")
