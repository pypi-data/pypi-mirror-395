"""
Mini-FAISS: A minimal, easy-to-understand library for vector similarity search.

This package provides fast, SIMD-accelerated similarity search for dense float32
embeddings with a simple, NumPy-friendly API.

Example:
    >>> import numpy as np
    >>> from mini_faiss import IndexFlatL2
    >>>
    >>> d = 768  # vector dimension
    >>> index = IndexFlatL2(d)
    >>>
    >>> # Add vectors
    >>> xb = np.random.randn(10000, d).astype("float32")
    >>> index.add(xb)
    >>>
    >>> # Search
    >>> xq = np.random.randn(5, d).astype("float32")
    >>> distances, indices = index.search(xq, k=10)
    >>> print(distances.shape, indices.shape)  # (5, 10), (5, 10)
"""

__version__ = "1.0.0"
__author__ = "mini-faiss contributors"

from ._core import IndexFlatL2, IndexFlatIP

__all__ = [
    "IndexFlatL2",
    "IndexFlatIP",
]
