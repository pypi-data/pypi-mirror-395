# prism-config v2.1.0 Release Notes

## 🎉 Release Highlights

Version 2.1.0 adds developer-friendly features for debugging and fixes visual alignment issues in the terminal output.

---

## ✨ New Features

### Secret Visibility Option

New `redact_secrets` parameter for `dump()` and `display()` methods allows developers to view actual secret values during debugging:

```python
# Show actual secret values (use with caution!)
config.display(redact_secrets=False)

# Or get unredacted dump as string
table = config.dump(redact_secrets=False)
```

⚠️ **Warning**: Only use `redact_secrets=False` in secure development environments. Never expose secrets in logs or production output.

### Version Display in Banner

The Neon Dump banner now shows the prism-config version:

```
    ██████╗ ██████╗ ██╗███████╗███╗   ███╗
    ██╔══██╗██╔══██╗██║██╔════╝████╗ ████║
    ██████╔╝██████╔╝██║███████╗██╔████╔██║
    ██╔═══╝ ██╔══██╗██║╚════██║██║╚██╔╝██║
    ██║     ██║  ██║██║███████║██║ ╚═╝ ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚═╝

    CONFIGURATION LOADED  (v2.1.0)
```

---

## 🐛 Bug Fixes

### Emoji Width Alignment

Fixed table column alignment for emojis with variation selectors (e.g., ⏱️ Rate Limit, 🖥️ Frontend).

**Before:** Rows with these emojis were misaligned by 1 space
**After:** Perfect column alignment across all emoji types

Technical details:
- Updated `display_width()` to handle Unicode variation selectors (VS1-VS16)
- Characters followed by emoji variation selector (VS16/U+FE0F) now correctly calculate as wide (2 columns)
- Zero-width joiners and combining marks are properly skipped

---

## 📊 Testing

- **297 tests passing** (unchanged from v2.0.0)
- All existing functionality verified
- New features covered by existing test infrastructure

---

## ⬆️ Upgrade Guide

This is a **non-breaking** patch release. Simply upgrade:

```bash
pip install --upgrade prism-config
```

All v2.0.0 code works without modification.

---

## 📦 Installation

```bash
pip install prism-config==2.1.0
```

---

## 🔗 Links

- [Full Changelog](https://github.com/lukeudell/prism-config/blob/main/CHANGELOG.md)
- [Documentation](https://github.com/lukeudell/prism-config#readme)
- [PyPI Package](https://pypi.org/project/prism-config/)

---

**Full Changelog**: v2.0.0...v2.1.0
