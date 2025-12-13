"""
TPU Inference Server

A Flask-based inference server optimized for Google Cloud TPU v5e.
Supports multiple models, dynamic loading/unloading, and provides
OpenAI-compatible API endpoints.

Modes:
- single: Single-threaded mode (default), all work on main thread
- multi: Multi-worker mode with batched inference for higher throughput
"""

from tpu_inference_server.server import (
    TPUInferenceServer,
    create_app,
    load_model,
    unload_model,
    generate_tokens,
)
from tpu_inference_server.client import TPUInferenceClient
from tpu_inference_server.batch_worker import (
    BatchWorker,
    InferenceRequest,
    InferenceResult,
    create_request,
)

__version__ = "0.1.0"
__author__ = "Your Name"

__all__ = [
    # Server
    "TPUInferenceServer",
    "create_app",
    "load_model",
    "unload_model",
    "generate_tokens",
    # Client
    "TPUInferenceClient",
    # Batch worker
    "BatchWorker",
    "InferenceRequest",
    "InferenceResult",
    "create_request",
    # Metadata
    "__version__",
]
