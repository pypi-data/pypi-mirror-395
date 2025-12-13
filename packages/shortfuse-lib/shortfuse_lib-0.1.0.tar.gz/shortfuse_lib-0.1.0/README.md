<img src="banner.png" width="700" alt="Shortfuse Banner">

<img src="logo.png" width="200" alt="Shortfuse Logo">

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/shortfuse-lib/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)]()

**Don't just raise exceptions—kill the process.**

`shortfuse` is a zero-tolerance "fail fast" utility for enforcing architectural boundaries. It creates uncatchable traps in deprecated code paths to instantly halt execution and expose regressions.

---

## 📚 Documentation
[**Click here for Full API Docs & Examples**](https://lbrichards.github.io/shortfuse/shortfuse.html)

## 🚀 Quick Start

### Installation
```bash
pip install shortfuse-lib
```

### The "Loud" Failure
When shortfuse halts, it bypasses try/except blocks and finally handlers by using `os._exit(1)`.

```python
import shortfuse

# 1. Dead Code Trap
shortfuse.halt("Legacy endpoint is dead")

# 2. Conditional Trap
shortfuse.halt_unless(config.v3_enabled, "Must use V3 Config")

# 3. Dependency Trap
shortfuse.halt_if_not_none(legacy_client, "Legacy client must be removed")
```

For the full visual demonstration of the stack trace, see the [Documentation](https://lbrichards.github.io/shortfuse/shortfuse.html).
