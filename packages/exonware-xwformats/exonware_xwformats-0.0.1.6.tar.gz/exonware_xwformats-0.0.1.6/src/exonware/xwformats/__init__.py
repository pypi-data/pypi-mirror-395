#!/usr/bin/env python3
#exonware/xwformats/src/exonware/xwformats/__init__.py
"""
xwformats: Enterprise Serialization Formats

Extended serialization format support for enterprise applications.
This library provides heavyweight formats that are typically used in
specialized domains (scientific computing, big data, enterprise systems).

Company: eXonware.com
Author: Eng. Muhammad AlShehri
Email: connect@exonware.com
Version: 0.0.1.6
Generation Date: 02-Nov-2025

Formats provided:
- Schema: Protobuf, Avro, Parquet, Thrift, ORC, Cap'n Proto, FlatBuffers
- Scientific: HDF5, Feather, Zarr, NetCDF, MAT
- Database: LMDB, GraphDB, LevelDB
- Binary: BSON, UBJSON
- Text: XML (reserved)

Total: 17 enterprise formats (~87 MB dependencies)

Installation:
    # Install with all dependencies
    pip install exonware-xwformats[full]
    
    # Or minimal install (dependencies required separately)
    pip install exonware-xwformats
"""

from .version import __version__

# Version metadata constants
__author__ = "Eng. Muhammad AlShehri"
__email__ = "connect@exonware.com"
__company__ = "eXonware.com"

# LAZY INSTALLATION - Simple One-Line Configuration
# Auto-detects [lazy] extra and enables lazy installation hook
from exonware.xwsystem.utils.lazy_discovery import config_package_lazy_install_enabled
config_package_lazy_install_enabled("xwformats")  # Auto-detect [lazy] extra

# Import all format serializers
from .formats import *

# Auto-register all serializers with UniversalCodecRegistry
from exonware.xwsystem.io.codec.registry import get_registry

_codec_registry = get_registry()

# Get all serializer classes from formats
from .formats.schema import (
    XWProtobufSerializer, XWParquetSerializer, XWThriftSerializer,
    XWOrcSerializer, XWCapnProtoSerializer, XWFlatBuffersSerializer,
)
# Note: Avro excluded due to cramjam bug on Python 3.12 Windows - see KNOWN_ISSUES.md
from .formats.scientific import (
    XWHdf5Serializer, XWFeatherSerializer, XWZarrSerializer,
    XWNetcdfSerializer, XWMatSerializer,
)
from .formats.database import (
    XWLmdbSerializer, XWGraphDbSerializer, XWLeveldbSerializer,
)
from .formats.binary import (
    XWUbjsonSerializer,
)

# Register all serializers
for _serializer_class in [
    # Schema formats (Avro excluded - see KNOWN_ISSUES.md)
    XWProtobufSerializer, XWParquetSerializer, XWThriftSerializer,
    XWOrcSerializer, XWCapnProtoSerializer, XWFlatBuffersSerializer,
    # Scientific formats
    XWHdf5Serializer, XWFeatherSerializer, XWZarrSerializer,
    XWNetcdfSerializer, XWMatSerializer,
    # Database formats
    XWLmdbSerializer, XWGraphDbSerializer, XWLeveldbSerializer,
    # Binary formats
    XWUbjsonSerializer,
]:
    _codec_registry.register(_serializer_class)

__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    '__company__',
    
    # All formats exported from formats module
    # (will be populated by formats/__init__.py)
]

