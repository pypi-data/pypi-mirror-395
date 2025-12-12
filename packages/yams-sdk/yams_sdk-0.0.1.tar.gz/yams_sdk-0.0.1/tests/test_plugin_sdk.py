"""Basic tests for the plugin SDK."""

from yams_sdk import BasePlugin, rpc
from yams_sdk.abi import (
    InterfaceVersion,
    PluginErrorCode,
    PluginManifest,
    create_interface_descriptor,
    validate_interface_descriptor,
)
from yams_sdk.testing import validate_health, validate_manifest


class SimpleTestPlugin(BasePlugin):
    """Simple test plugin."""

    def __init__(self):
        super().__init__()
        # Register RPC methods (like Ghidra plugin does)
        for name in dir(self):
            fn = getattr(self, name)
            rpc_name = getattr(fn, "__rpc_name__", None)
            if rpc_name:
                self.register(rpc_name, fn)

    def manifest(self):
        return {"name": "test_plugin", "version": "1.0.0", "interfaces": ["test_v1"]}

    def init(self, config):
        self.config = config

    def health(self):
        return {"status": "ok"}

    @rpc("test.echo")
    def echo(self, message: str) -> dict:
        return {"echo": message}


def test_plugin_manifest():
    """Test plugin manifest creation."""
    plugin = SimpleTestPlugin()
    manifest = plugin.manifest()

    assert manifest["name"] == "test_plugin"
    assert manifest["version"] == "1.0.0"
    assert "test_v1" in manifest["interfaces"]


def test_manifest_validation():
    """Test manifest validation."""
    valid_manifest = {"name": "test", "version": "1.0.0", "interfaces": ["test_v1"]}
    errors = validate_manifest(valid_manifest)
    assert len(errors) == 0

    invalid_manifest = {"name": "test"}
    errors = validate_manifest(invalid_manifest)
    assert len(errors) > 0


def test_health_validation():
    """Test health response validation."""
    valid_health = {"status": "ok"}
    errors = validate_health(valid_health)
    assert len(errors) == 0

    invalid_health = {"status": "invalid_status"}
    errors = validate_health(invalid_health)
    assert len(errors) > 0


def test_interface_descriptor():
    """Test interface descriptor creation."""
    desc = create_interface_descriptor("test_v1", 1)
    assert desc["id"] == "test_v1"
    assert desc["version"] == 1
    assert validate_interface_descriptor(desc)


def test_plugin_manifest_class():
    """Test PluginManifest class."""
    manifest = PluginManifest(
        name="my_plugin",
        version="2.0.0",
        interfaces=[
            create_interface_descriptor(
                InterfaceVersion.CONTENT_EXTRACTOR_V1_ID,
                InterfaceVersion.CONTENT_EXTRACTOR_V1_VERSION,
            )
        ],
        description="Test plugin",
    )

    data = manifest.to_json()
    assert data["name"] == "my_plugin"
    assert data["version"] == "2.0.0"
    assert data["description"] == "Test plugin"
    assert len(data["interfaces"]) == 1

    # Round-trip test
    manifest2 = PluginManifest.from_json(data)
    assert manifest2.name == manifest.name
    assert manifest2.version == manifest.version


def test_error_codes():
    """Test error code constants."""
    assert PluginErrorCode.OK == 0
    assert PluginErrorCode.ERR_INVALID == -4
    assert PluginErrorCode.ERR_NOT_FOUND == -2


def test_interface_versions():
    """Test interface version constants."""
    assert InterfaceVersion.CONTENT_EXTRACTOR_V1_ID == "content_extractor_v1"
    assert InterfaceVersion.MODEL_PROVIDER_V1_ID == "model_provider_v1"
    assert InterfaceVersion.CONTENT_EXTRACTOR_V1_VERSION == 1
    assert InterfaceVersion.MODEL_PROVIDER_V1_VERSION == 2


def test_rpc_decorator():
    """Test RPC decorator."""
    plugin = SimpleTestPlugin()

    # Check that decorated method has __rpc_name__
    assert hasattr(plugin.echo, "__rpc_name__")
    assert plugin.echo.__rpc_name__ == "test.echo"

    # Check that it's registered
    assert "test.echo" in plugin._rpc_methods
