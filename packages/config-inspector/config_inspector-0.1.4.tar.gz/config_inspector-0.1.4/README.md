# Config Inspector

![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

## Overview

Config Inspector is a Python package designed to help you manage and interact with text-based config files in a robust and extensible way. It allows you to:

- **Register files** for tracking and easily gather their metadata (such as size, modification time, and type).
- **Read and write files** with built-in format validation for common configuration formats like INI, TOML, and JSON.
- **Update configuration files** safely, merging new content with existing data where appropriate.
- **Download and extract files** from remote sources, supporting ZIP and tar.gz archives.
- **Extend functionality** by registering custom file updaters for new file types.

This package is useful for applications that need to manage, validate, or automate configuration and content updates across a variety of file formats.

## Installation

```bash
uv pip install config-inspector
```

## Development

To get a list of all commands with descriptions simply run `make`.

```bash
make env
make pip_install_editable
```

## Testing

```bash
make pytest
make coverage
make open_coverage
```

## Issues

If you experience any issues, please create an [issue](https://bitbucket.org/tsantor/config-inspector/issues) on Bitbucket.

## Example Usage

```python
from pathlib import Path
from config_inspector.manager import ConfigManager
from config_inspector.registry import FileRegistry
from config_inspector.services import FileMetadataService

class SizeFormatter:
    def format(self, size_bytes: int) -> str:
        return f"{size_bytes} bytes"

class DateTimeFormatter:
    def format(self, dt) -> str:
        # return dt.isoformat()
        return dt.strftime("%a, %b %d, %Y %-I:%M %p")

manager = ConfigManager()

config_files = [
    Path("settings.json"),
    Path("settings.toml"),
    Path("settings.ini"),
    Path("settings.cfg"),
    Path("script.bat"),
    Path("script.sh"),
    Path("script.cmd")
]

log_files = [
    Path("log.txt"),
    Path("log.log"),
]

# Register and get metadata for all files
metadata_service = FileMetadataService(size_formatter=SizeFormatter(), datetime_formatter=DateTimeFormatter())
config_registry = FileRegistry(metadata_service)
log_registry = FileRegistry(metadata_service)

for fname in config_files:
    config_registry.register(Path(fname))

for fname in log_files:
    log_registry.register(Path(fname))

metadata = config_registry.get_all_metadata()
for meta in metadata:
    print(meta)

metadata = log_registry.get_all_metadata()
for meta in metadata:
    print(meta)

# Load/Update a Config file
from config_inspector.services import FileContentService
import json

filecontent_service = FileContentService(metadata_service, max_size_bytes=50_000)
payload = filecontent_service.get_payload(Path("settings.json"), key="config")

# Inject a new key
content = json.loads(payload['config']['content'])
content['foo'] = 'bar'

# Create/update various config files
manager.update(Path("settings.json"), content)
```
