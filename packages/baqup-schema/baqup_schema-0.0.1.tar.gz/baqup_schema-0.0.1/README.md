# baqup-schema

JSON Schema validation and environment variable loading for baqup agent configuration.

> ⚠️ **This is a placeholder package.** Full implementation coming soon.

## What is baqup?

[baqup](https://github.com/baqupio/baqup) is a container-native backup orchestration system. It uses a controller-agent architecture where:

- The **controller** discovers workloads via Docker labels
- **Agents** perform backup/restore operations
- Configuration is defined via JSON Schema

This package provides schema validation for agent configuration, used by both:
- Agents (to validate their own configuration at startup)
- Controller (to pre-flight validate before spawning agents)

## Planned Features

- JSON Schema validation (draft-2020-12)
- Environment variable loading with type coercion
- Custom format validators (`path`, `hostname`, etc.)
- Conditional validation support

## Installation

```bash
pip install baqup-schema
```

## Usage (Preview API)

```python
from baqup_schema import load_from_env, validate

# Load and validate from environment variables
config = load_from_env("agent-schema.json")

# Or validate an existing dict
result = validate(schema, config_dict)
if not result.valid:
    for error in result.errors:
        print(f"{error.path}: {error.message}")
```

## Related Packages

| Package | Description |
|---------|-------------|
| `baqup-schema` | Schema validation (this package) |
| `baqup-agent` | Agent SDK for Python |

## Links

- [GitHub](https://github.com/baqupio/baqup)
- [Documentation](https://github.com/baqupio/baqup/blob/main/AGENT-CONTRACT-SPEC.md)

## License

Fair Source License - see [LICENSE](./LICENSE) for details.
