"""Exporters for aiobs observability data.

Exporters handle the serialization and transport of observability data
to various destinations.

Supported exporters:
    - GCSExporter: Export to Google Cloud Storage
    - CustomExporter: User-defined export logic via callback
    - CompositeExporter: Export to multiple destinations

Example usage:
    from aiobs import observer
    from aiobs.exporters import GCSExporter

    exporter = GCSExporter(
        bucket="my-observability-bucket",
        prefix="traces/",
        project="my-gcp-project",
    )

    observer.observe()
    # ... your agent code ...
    observer.end()
    observer.flush(exporter=exporter)
"""

from .base import BaseExporter, ExportResult, ExportError
from .custom import CustomExporter, CompositeExporter

__all__ = [
    # Base classes
    "BaseExporter",
    "ExportResult",
    "ExportError",
    # Built-in exporters
    "GCSExporter",
    "CustomExporter",
    "CompositeExporter",
]


# Lazy imports for optional cloud exporters (to avoid requiring deps at import time)
def __getattr__(name: str):
    if name == "GCSExporter":
        from .gcs import GCSExporter
        return GCSExporter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

