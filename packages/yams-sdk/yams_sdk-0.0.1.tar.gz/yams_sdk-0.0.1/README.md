# yams-sdk

[![builds.sr.ht status](https://builds.sr.ht/~trvon/yams-sdk.svg)](https://builds.sr.ht/~trvon/yams-sdk)
[![PyPI](https://img.shields.io/pypi/v/yams-sdk)](https://pypi.org/project/yams-sdk/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Python SDK for building [YAMS](https://sr.ht/~trvon/yams/) plugins.

## Installation

```bash
pip install yams-sdk
```

## Quick Start

Create a plugin:

```python
from yams_sdk import BasePlugin, rpc

class MyPlugin(BasePlugin):
    def manifest(self):
        return {
            "name": "my_plugin",
            "version": "1.0.0",
            "interfaces": ["content_extractor_v1"]
        }

    @rpc("extractor.extract")
    def extract(self, source: dict) -> dict:
        return {"text": "extracted content", "metadata": {}}

if __name__ == "__main__":
    MyPlugin().run()
```

Test it:

```bash
echo '{"id":1,"method":"handshake.manifest"}' | python my_plugin.py
```

## Use with YAMS

```bash
# Trust your plugin
yams plugin trust add /path/to/my_plugin.py

# Load it
yams plugin load my_plugin.py

# Verify
yams plugin list
```

## Documentation

- [Developer Guide](docs/development.md) - Testing, contributing, publishing
- [API Reference](docs/api.md) - Module and interface documentation
- [Examples](https://git.sr.ht/~trvon/yams/tree/main/item/plugins/) - Real plugin implementations

## License

GPL-3.0-only
