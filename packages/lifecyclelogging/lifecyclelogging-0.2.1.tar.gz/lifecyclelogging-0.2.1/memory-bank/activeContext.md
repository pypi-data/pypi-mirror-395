# Active Context

## lifecyclelogging

Lifecycle-aware logging utilities for Python applications.

### Features
- Structured logging handlers
- Lifecycle event tracking
- Context-aware log formatting
- Integration with standard logging

### Package Status
- **Registry**: PyPI
- **Python**: 3.9+
- **Dependencies**: None (pure Python)

### Development
```bash
uv sync --extra tests
uv run pytest tests/ -v
uvx ruff check src/ tests/
uvx ruff format src/ tests/
```

---
*Last updated: 2025-12-06*
