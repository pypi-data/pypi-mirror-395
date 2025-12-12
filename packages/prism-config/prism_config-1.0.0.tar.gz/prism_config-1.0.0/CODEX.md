# prism-config CODEX

## 🎯 Design Decisions

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

## 🔌 Interface Contract

### Exports
- `PrismConfig`: Main config loader class
- `SecretProvider`: Protocol for secret resolution (coming in Iteration 4)

### Imports
- None (foundation library)

## 🧪 Test Coverage Map

| Feature              | Unit | Integration | Property | Status |
|----------------------|------|-------------|----------|--------|
| Dict loading         | ✅   | N/A         | ⏳       | ✅ Done |
| Type validation      | ✅   | N/A         | ⏳       | ✅ Done |
| Error messages       | ✅   | N/A         | ⏳       | ✅ Done |
| YAML loading         | ⏳   | ⏳          | ⏳       | 🚧 Next |
| Env var override     | ⏳   | ⏳          | ⏳       | 📋 Todo |
| Secret resolution    | ⏳   | ⏳          | ⏳       | 📋 Todo |
| Neon Dump            | ⏳   | ⏳          | ⏳       | 📋 Todo |
| PQC stress test      | ⏳   | ⏳          | ⏳       | 📋 Todo |

## 🚨 Known Limitations

### Current (v0.1.0)
- Only supports dict loading (no YAML files yet)
- No environment variable override
- No secret resolution
- No aesthetic output

### By Design
- YAML anchors/aliases not supported (use env vars for DRY)
- Config is immutable after startup (restart to reload)
- No hot-reload mechanism

## 🔮 Extension Points

### Custom Validation (Coming Soon)
```python
class MyConfig(ConfigRoot):
    @field_validator('database.host')
    def validate_host(cls, v):
        # Custom validation logic
        return v