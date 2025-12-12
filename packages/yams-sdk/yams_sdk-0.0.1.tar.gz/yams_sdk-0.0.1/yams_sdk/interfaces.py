"""Python bindings for YAMS plugin interfaces.

This module provides Python-friendly classes representing the standard
YAMS plugin interfaces defined in include/yams/plugins/.

These can be used for:
1. Documentation and type hints in Python plugins
2. Validation of interface contracts
3. Helpers for testing plugin implementations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class ExtractionResult:
    """Result from content extraction operation.

    Corresponds to yams_extraction_result_t from content_extractor_v1.h
    """

    text: str | None = None
    metadata: dict[str, str] = None
    error: str | None = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    @property
    def ok(self) -> bool:
        """Check if extraction succeeded."""
        return self.error is None and self.text is not None


class ContentExtractorV1(Protocol):
    """Protocol for content_extractor_v1 interface.

    Maps to the C interface defined in include/yams/plugins/content_extractor_v1.h
    """

    def supports(self, mime_type: str, extension: str) -> bool:
        """Check if this extractor can handle the given file type.

        Args:
            mime_type: MIME type (e.g., "application/pdf")
            extension: File extension (e.g., ".pdf")

        Returns:
            True if this extractor can handle this file type
        """
        ...

    def extract(self, content: bytes) -> ExtractionResult:
        """Extract text and metadata from file content.

        Args:
            content: File content as bytes

        Returns:
            ExtractionResult with text, metadata, and error status
        """
        ...


@dataclass
class EmbeddingResult:
    """Result from embedding generation.

    Maps to embedding generation methods in model_provider_v1.h
    """

    vector: list[float] | None = None
    dimension: int = 0
    error: str | None = None

    @property
    def ok(self) -> bool:
        """Check if embedding generation succeeded."""
        return self.error is None and self.vector is not None


@dataclass
class ModelInfo:
    """Model metadata and status information."""

    model_id: str
    loaded: bool = False
    backend: str | None = None
    dimension: int | None = None
    metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ModelLoadProgressCallback(Protocol):
    """Callback for model loading progress.

    Maps to yams_model_load_progress_cb from model_provider_v1.h
    """

    def __call__(
        self, model_id: str, phase: int, current: int, total: int, message: str | None = None
    ) -> None:
        """Report model loading progress.

        Args:
            model_id: Model identifier
            phase: Load phase (see ModelLoadPhase)
            current: Current progress value (bytes, steps, etc.)
            total: Total expected value (0 if unknown)
            message: Optional progress message
        """
        ...


class ModelLoadPhase:
    """Model loading phases from model_provider_v1.h"""

    UNKNOWN = 0
    PROBE = 1
    DOWNLOAD = 2
    LOAD = 3
    WARMUP = 4
    READY = 5


class ModelProviderV1(Protocol):
    """Protocol for model_provider_v1 interface.

    Maps to the C interface defined in include/yams/plugins/model_provider_v1.h
    """

    def set_progress_callback(self, callback: ModelLoadProgressCallback | None) -> int:
        """Set progress callback for async operations.

        Args:
            callback: Progress callback or None to clear

        Returns:
            0 on success, error code otherwise
        """
        ...

    def load_model(self, model_id: str, model_path: str, options_json: str | None = None) -> int:
        """Load a model (non-blocking).

        Args:
            model_id: Unique model identifier
            model_path: Path to model file or HF model identifier
            options_json: Optional JSON configuration

        Returns:
            0 on success, error code otherwise
        """
        ...

    def generate_embedding(self, model_id: str, input_text: str) -> EmbeddingResult:
        """Generate embedding for text.

        Args:
            model_id: Model to use
            input_text: Input text

        Returns:
            EmbeddingResult with vector and status
        """
        ...

    def is_model_loaded(self, model_id: str) -> bool:
        """Check if a model is loaded and ready.

        Args:
            model_id: Model identifier

        Returns:
            True if loaded and ready
        """
        ...

    def get_loaded_models(self) -> list[str]:
        """Get list of loaded model IDs.

        Returns:
            List of model identifiers
        """
        ...


@dataclass
class SymbolInfo:
    """Symbol information from binary analysis."""

    name: str
    address: str
    type: str  # "function", "variable", "label", etc.
    size: int | None = None
    metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SymbolExtractorV1(Protocol):
    """Protocol for symbol_extractor_v1 interface.

    Maps to include/yams/plugins/symbol_extractor_v1.h
    """

    def extract_symbols(
        self, content: bytes, options_json: str | None = None
    ) -> tuple[list[SymbolInfo], str | None]:
        """Extract symbols from binary content.

        Args:
            content: Binary file content
            options_json: Optional extraction options

        Returns:
            Tuple of (symbols list, error message or None)
        """
        ...

    def supports_format(self, mime_type: str, extension: str) -> bool:
        """Check if extractor supports this binary format.

        Args:
            mime_type: MIME type
            extension: File extension

        Returns:
            True if supported
        """
        ...


# Ghidra-specific analysis interface (external plugin)
@dataclass
class GhidraFunction:
    """Function information from Ghidra analysis."""

    name: str
    addr: str
    size: int | None = None
    body: str | None = None


@dataclass
class GhidraAnalysisResult:
    """Result from Ghidra binary analysis."""

    arch: str
    count: int
    functions: list[GhidraFunction]
    error: str | None = None

    @property
    def ok(self) -> bool:
        """Check if analysis succeeded."""
        return self.error is None


@dataclass
class GhidraDecompileResult:
    """Result from Ghidra function decompilation."""

    ok: bool
    decomp: str | None = None
    meta: dict[str, Any] | None = None
    error: str | None = None


class GhidraAnalysisV1(Protocol):
    """Protocol for ghidra_analysis_v1 interface (external plugin).

    This is a JSON-RPC based interface used by the Ghidra external plugin.
    """

    def analyze(
        self, source: dict[str, Any], opts: dict[str, Any] | None = None
    ) -> GhidraAnalysisResult:
        """Analyze a binary file with Ghidra.

        Args:
            source: Source descriptor with type ("path", "bytes") and data
            opts: Optional analysis options (e.g., max_functions)

        Returns:
            GhidraAnalysisResult with functions and metadata
        """
        ...

    def decompile_function(
        self, source: dict[str, Any], func: dict[str, Any], opts: dict[str, Any] | None = None
    ) -> GhidraDecompileResult:
        """Decompile a function.

        Args:
            source: Binary source descriptor
            func: Function descriptor with "name" or "addr"
            opts: Optional decompile options

        Returns:
            GhidraDecompileResult with decompiled code
        """
        ...

    def list_functions(
        self, source: dict[str, Any], opts: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """List functions in a binary with pagination.

        Args:
            source: Binary source descriptor
            opts: Optional parameters (limit, offset)

        Returns:
            Dict with "items" (functions) and "total"
        """
        ...
