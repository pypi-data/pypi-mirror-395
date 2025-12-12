# prism-config CODEX

**Version:** 1.0.0 (Production Ready)
**Status:** Production Release
**Last Updated:** 2025-12-05

> For comprehensive technical documentation, architecture details, and implementation guide, see [docs/CODEX.md](docs/CODEX.md).

---

## Design Decisions

### Why Pydantic?
- **Strict typing:** Catches errors at load time, not runtime
- **Validation:** Built-in validators for common patterns (URLs, emails, etc.)
- **JSON Schema:** Can auto-generate schema for documentation
- **Performance:** Written in Rust (v2), extremely fast

### Why Tiered Loading?
Follows the [12-Factor App](https://12factor.net/config) methodology:
- Code has sensible defaults
- Config files override defaults (for local dev)
- Env vars override config files (for Docker/K8s)
- CLI args override everything (for one-off commands)

### Why Immutable Config?
- **Thread safety:** No risk of concurrent modification
- **Predictability:** Config doesn't change during runtime
- **Simplicity:** No need for watchers, locks, or reload logic

---

## Interface Contract

### Exports
- `PrismConfig`: Main config loader class
- `SecretProvider`: Protocol for secret resolution
- Custom exception hierarchy for error handling

### Imports
- None (foundation library)

---

## Test Coverage

| Feature              | Unit | Integration | Property | Status |
|----------------------|------|-------------|----------|--------|
| Dict loading         | Yes  | N/A         | Yes      | Done   |
| Type validation      | Yes  | N/A         | Yes      | Done   |
| Error messages       | Yes  | N/A         | Yes      | Done   |
| YAML loading         | Yes  | Yes         | Yes      | Done   |
| Env var override     | Yes  | Yes         | Yes      | Done   |
| CLI arg override     | Yes  | Yes         | Yes      | Done   |
| Secret resolution    | Yes  | Yes         | Yes      | Done   |
| Neon Dump            | Yes  | Yes         | Yes      | Done   |
| PQC stress test      | Yes  | Yes         | Yes      | Done   |
| Property testing     | Yes  | N/A         | Yes      | Done   |
| Advanced features    | Yes  | Yes         | Yes      | Done   |
| Performance tests    | Yes  | Yes         | N/A      | Done   |
| Error handling       | Yes  | Yes         | Yes      | Done   |

**Total:** 107 tests (101 unit + 6 parity), 86% code coverage

---

## Known Limitations

### By Design
- YAML anchors/aliases not supported (use env vars for DRY)
- Config is immutable after startup (restart to reload)
- No hot-reload mechanism

---

## Extension Points

### Custom Validation
```python
class MyConfig(ConfigRoot):
    @field_validator('database.host')
    def validate_host(cls, v):
        # Custom validation logic
        return v
```

### Custom Secret Providers
```python
from prism.config.providers import register_provider

class VaultProvider:
    def resolve(self, key: str) -> str:
        # Fetch from HashiCorp Vault
        return vault_client.read(key)

register_provider("VAULT", VaultProvider())
```

---

## Version History

### v1.0.0 (2025-12-03) - Production Release
- All 14 development iterations complete
- 107 tests passing (101 unit + 6 parity)
- 86% code coverage
- Comprehensive documentation
- PyPI package ready
- GitHub Actions CI/CD

See [CHANGELOG.md](CHANGELOG.md) for full version history.
