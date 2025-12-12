# 🔮 Project Prism - Master Overview

> **READ THIS FIRST:** This file provides context for all Prism libraries across all languages.

---

## What is Project Prism?

A suite of **6 production-ready, standardized libraries** for Java (Spring Boot) and Python that provide:

- 🧱 **prism-config** - Typed configuration with secret resolution
- 👁️ **prism-view** - Structured logging and observability  
- 🛡️ **prism-guard** - Authentication, authorization, PQC crypto
- 💾 **prism-data** - Database pooling and migrations
- 🔌 **prism-api** - HTTP response envelopes and pagination
- 🚀 **prism-boot** - Application lifecycle and health checks

Each library exists in **two implementations:**
- `python/prism-[name]/` - Python 3.10+ with Pydantic
- `java/prism-[name]/` - Java 17+ with Spring Boot

---

## Core Design Principles

### 1. Test-Driven Development (TDD)
**Every feature follows Red → Green → Refactor:**
- ❌ **RED:** Write a failing test first
- ✅ **GREEN:** Write minimal code to pass
- 🔄 **REFACTOR:** Clean up, optimize, document

**No code exists without a test.**

### 2. Cross-Language Parity
Python and Java implementations must have **identical behavior**:
- Same configuration format
- Same API surface
- Same error messages
- Validated by shared parity test suite

### 3. Quantum Readiness (PQC)
All libraries must support **Post-Quantum Cryptography:**
- Handle values up to **16KB** (Kyber-1024 keys)
- Crypto-agile design (swap algorithms via config)
- Future-proof against quantum threats

### 4. Aesthetic by Default
Beautiful terminal output for local development:
- ANSI colors and gradients
- Emoji taxonomy (ℹ️ info, 🔥 error, 💾 database)
- Box-drawing tables
- Configurable via `prism-palette.toml`
- Disabled in production (JSON logs only)

### 5. Modular Independence
Each library can be used **standalone** or as part of the full suite:
- Zero dependencies on other Prism libraries (except explicit imports)
- Install only what you need
- Full suite provides orchestrated startup experience

---

## Architecture: Dependency Flow

```
┌─────────────────┐
│  prism-config   │ ← Foundation (no dependencies)
└────────┬────────┘
         ↓ exports: ConfigResolver
┌─────────────────┐
│   prism-view    │ ← Depends on: prism-config
└────────┬────────┘
         ↓ exports: Logger, ExceptionHandler
┌─────────────────┐
│  prism-guard    │ ← Depends on: prism-config, prism-view
└────────┬────────┘
         ↓ exports: AuthProvider, CryptoProvider
┌─────────────────┐
│  prism-data     │ ← Depends on: prism-config, prism-view, prism-guard
└────────┬────────┘
         ↓ exports: DataSource, MigrationRunner
┌─────────────────┐
│   prism-api     │ ← Depends on: prism-view
└────────┬────────┘
         ↓ exports: ResponseEnvelope, Paginator
┌─────────────────┐
│  prism-boot     │ ← Depends on: all above
└─────────────────┘
```

**Key Rule:** Libraries higher in the stack **cannot** depend on libraries lower in the stack.

---

## Technology Stack

### Python
- **Version:** 3.10+ (for match statements, better type hints)
- **Build:** Hatchling
- **Testing:** pytest + pytest-cov + Hypothesis
- **Type Checking:** mypy (strict mode)
- **Linting:** ruff
- **Framework:** FastAPI (preferred), Flask (supported)

### Java
- **Version:** Java 17+ (for records, sealed classes)
- **Build:** Gradle 8+ (Kotlin DSL)
- **Testing:** JUnit 5 + Mockito + jqwik
- **Framework:** Spring Boot 3.x

---

## Development Workflow

### When Starting Work on a Library

1. **Read context files in order:**
   - `00-PRISM-OVERVIEW.md` (this file)
   - `library-context.md` (specific library details)
   - `todo.md` (current tasks)
   - `progress.md` (what's done)

2. **Identify next task:**
   - Check `todo.md` for next unchecked item
   - Read the task requirements

3. **Follow TDD cycle:**
   - Write test (RED)
   - Run: `pytest -v` → should fail
   - Implement feature (GREEN)
   - Run: `pytest -v` → should pass
   - Refactor if needed
   - Run: `pytest --cov` → maintain 100% coverage

4. **Update documentation:**
   - Update `progress.md` (mark task complete)
   - Update `CODEX.md` if design changed
   - Update `README.md` if public API changed

5. **Commit:**
   - Format: `type(scope): description`
   - Example: `feat(config): add YAML file loading`
   - Types: `feat`, `fix`, `test`, `docs`, `refactor`, `perf`

### When Switching Between Languages

**Going from Python → Java:**
- Read the Python implementation first
- Understand the test patterns
- Implement equivalent Java code
- Use Java idioms (Streams, Optional, etc.)

**Going from Java → Python:**
- Read the Java implementation first
- Translate to Pythonic patterns
- Use Python idioms (list comprehensions, context managers, etc.)

---

## Definition of Done (DoD)

A library is complete when:

- ✅ All tasks in `todo.md` are checked
- ✅ All tests pass (pytest/JUnit)
- ✅ 100% code coverage (implemented features)
- ✅ All property tests pass (Hypothesis/jqwik)
- ✅ Golden Path test passes (end-to-end)
- ✅ Cross-language parity tests pass
- ✅ CODEX.md fully updated
- ✅ README.md has examples
- ✅ No linter errors (ruff/checkstyle)
- ✅ No type checker errors (mypy/javac)
- ✅ PQC stress test passes (16KB values)
- ✅ Aesthetic output works in 4 terminals

---

## File Organization Standards

### Python Structure
```
prism-[name]/
├── .claude/
│   ├── context.md          # Symlink to root
│   ├── library-context.md  # Library details
│   ├── todo.md             # Tasks
│   └── progress.md         # Progress
├── src/prism/[name]/
├── tests/
├── pyproject.toml
├── README.md
└── CODEX.md
```

### Java Structure
```
prism-[name]/
├── .claude/
├── src/main/java/io/prism/[name]/
├── src/test/java/io/prism/[name]/
├── build.gradle.kts
├── README.md
└── CODEX.md
```

---

## Aesthetic System

All visual output controlled by `prism-palette.toml`:

```toml
[colors]
pink = "213"
cyan = "51"
purple = "141"

[emojis]
info = "ℹ️"
error = "🔥"
database = "💾"

[styles]
box_style = "double"
```

---

## Common Patterns

### Configuration
```python
from prism.config import PrismConfig
config = PrismConfig.from_file("config.yaml")
```

### Logging
```python
from prism.view import get_logger
logger = get_logger(__name__)
logger.info("Event occurred", user_id=123)
```

### Secrets
```yaml
database:
  password: REF::ENV::DB_PASSWORD
```

---

## Current Status

**Phase:** Foundation - Building prism-config first  
**Active:** prism-config (Python) - Iteration 1 complete, Iteration 2 in progress  
**Next:** prism-view (Python)

---

## Getting Help

1. Check `CODEX.md` for design decisions
2. Check `README.md` for API examples
3. Look at existing tests for patterns
4. Check other language implementation

---

**Version:** 1.0  
**Last Updated:** 2024-12-03