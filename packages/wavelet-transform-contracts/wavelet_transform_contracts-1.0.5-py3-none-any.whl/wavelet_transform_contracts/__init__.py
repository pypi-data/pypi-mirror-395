"""WaveletTransform Protobuf Contracts"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("wavelet-transform-contracts")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
