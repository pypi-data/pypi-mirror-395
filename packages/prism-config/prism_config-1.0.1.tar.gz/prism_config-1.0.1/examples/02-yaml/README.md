# Example 02: YAML File Configuration

This example demonstrates loading configuration from a YAML file - the recommended approach for most applications.

## What You'll Learn

- ✅ How to load configuration from YAML files
- ✅ How to use Path objects for file paths
- ✅ How to export configuration to different formats
- ✅ How to save configuration to files

## Files

- `config.yaml` - Example YAML configuration file
- `yaml_example.py` - Main example script
- `README.md` - This file

## Running the Example

```bash
# From the prism-config root directory
python examples/02-yaml/yaml_example.py
```

## Expected Output

```
🔮 YAML File Configuration Example
==================================================
Loading from: examples/02-yaml/config.yaml

📋 Configuration values:
  App Name: yaml-example-app
  Environment: staging
  Database Host: staging-db.example.com
  Database Port: 5432

🌈 Beautiful Display:

[Colorful table output]

💾 Export to JSON:
{
  "app": {
    "name": "yaml-example-app",
    ...
  }
}

✅ Saved to: examples/02-yaml/config_export.json
```

## Configuration File Format

The `config.yaml` file follows the standard prism-config schema:

```yaml
app:
  name: yaml-example-app
  environment: staging
  api_key: staging_api_key_xyz789

database:
  host: staging-db.example.com
  port: 5432
  name: staging_database
  password: staging_db_password
```

## Key Concepts

### 1. File Loading

```python
from pathlib import Path
config = PrismConfig.from_file("config.yaml")

# Using Path objects (recommended)
config_path = Path(__file__).parent / "config.yaml"
config = PrismConfig.from_file(config_path)
```

### 2. Error Handling

prism-config provides clear, actionable error messages:

```python
# File not found
try:
    config = PrismConfig.from_file("missing.yaml")
except ConfigFileNotFoundError as e:
    print(e)
    # "Configuration file not found: missing.yaml
    #   Searched at: /absolute/path/to/missing.yaml
    #   Suggestion: Check if the file exists and the path is correct"

# Invalid YAML syntax
try:
    config = PrismConfig.from_file("invalid.yaml")
except ConfigParseError as e:
    print(e)
    # "YAML parsing failed at line 5
    #   Reason: expected <block end>, but found ':'
    #   Suggestion: Check YAML syntax and indentation"
```

### 3. Export Formats

Export your configuration to different formats:

```python
# To YAML string
yaml_str = config.to_yaml()

# To JSON string
json_str = config.to_json(indent=2)

# To dict
config_dict = config.to_dict()

# Save to file
config.to_yaml_file("output.yaml")
config.to_json_file("output.json")
```

## Next Steps

- **Example 03**: Override configuration with environment variables
- **Example 04**: Use secret references for sensitive data
- **Example 05**: Docker and Kubernetes integration
