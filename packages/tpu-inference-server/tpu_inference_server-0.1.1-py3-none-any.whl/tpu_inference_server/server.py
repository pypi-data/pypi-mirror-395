"""
TPU Inference Server for Google Cloud TPU v5e

Flask-based server with OpenAI-compatible API endpoints.

Supports two modes:
- single: Single-threaded mode (threaded=False), all work on main thread
- multi: Multi-worker mode with batched inference, Flask uses threaded=True
         but only the worker thread touches TPU/XLA tensors

TPU Requirements:
- Must use manual token generation (not model.generate())
- Must call xm.mark_step() after each token
- Only ONE thread should touch TPU tensors
"""

import os
import sys
import time
import logging
import gc
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Literal

# Set PJRT_DEVICE before importing torch_xla
os.environ.setdefault("PJRT_DEVICE", "TPU")

import yaml
import torch
from flask import Flask, request, jsonify, Response
from transformers import AutoModelForCausalLM, AutoTokenizer

# Import torch_xla after setting environment variable
try:
    import torch_xla.core.xla_model as xm

    XLA_AVAILABLE = True
except ImportError:
    XLA_AVAILABLE = False
    xm = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def log_progress(message: str) -> None:
    """Log progress with flush for real-time output."""
    logger.info(message)
    sys.stdout.flush()


class TPUInferenceServer:
    """
    TPU Inference Server class.

    Manages model loading, inference, and the Flask application.

    Supports two modes:
    - "single": Traditional single-threaded mode (Flask threaded=False)
    - "multi": Multi-worker batched mode (Flask threaded=True, dedicated TPU worker)
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        host: str = "0.0.0.0",
        port: int = 8080,
        skip_warmup: bool = False,
        mode: Literal["single", "multi"] = "single",
        batch_size: int = 4,
        batch_timeout: float = 0.1,
    ):
        """
        Initialize the TPU Inference Server.

        Args:
            config_path: Path to YAML config file
            host: Host to bind server
            port: Port to bind server
            skip_warmup: Skip model warmup step
            mode: Server mode - "single" (default) or "multi" (batched)
            batch_size: Maximum requests per batch (multi mode only)
            batch_timeout: Seconds to wait for batch to fill (multi mode only)
        """
        self.host = host
        self.port = port
        self.skip_warmup = skip_warmup
        self.mode = mode
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout

        self.loaded_models: Dict[str, Dict[str, Any]] = {}
        self._device: Optional[Any] = None
        self._batch_workers: Dict[str, Any] = {}  # model_name -> BatchWorker

        # Load config
        self.config = self._load_config(config_path) if config_path else {}

        # Override from config if present
        server_config = self.config.get("server", {})
        if "mode" in server_config:
            self.mode = server_config["mode"]
        if "batch_size" in server_config:
            self.batch_size = server_config["batch_size"]
        if "batch_timeout" in server_config:
            self.batch_timeout = server_config["batch_timeout"]

        # Create Flask app
        self.app = create_app(self)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        path = Path(config_path)
        if path.exists():
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        return {}

    @property
    def device(self) -> Any:
        """Get TPU device (lazy initialization)."""
        if self._device is None:
            if XLA_AVAILABLE:
                self._device = xm.xla_device()
                log_progress(f"Using TPU device: {self._device}")
            else:
                self._device = torch.device(
                    "cuda" if torch.cuda.is_available() else "cpu"
                )
                log_progress(f"XLA not available, using: {self._device}")
        return self._device

    def warmup_model(
        self, model: Any, tokenizer: Any, model_name: str, num_tokens: int = 5
    ) -> None:
        """
        Warmup model to trigger XLA compilation.

        Args:
            model: The loaded model
            tokenizer: The model's tokenizer
            model_name: Name of the model for logging
            num_tokens: Number of warmup tokens to generate
        """
        if self.skip_warmup:
            log_progress(f"Skipping warmup for {model_name}")
            return

        log_progress(f"Starting warmup for {model_name} ({num_tokens} tokens)...")

        warmup_text = "Hello"
        inputs = tokenizer(warmup_text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        for i in range(num_tokens):
            with torch.no_grad():
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits[:, -1, :]
                next_token = torch.argmax(logits, dim=-1, keepdim=True)

                if XLA_AVAILABLE:
                    xm.mark_step()

                input_ids = torch.cat([input_ids, next_token], dim=-1)
                attention_mask = torch.cat(
                    [
                        attention_mask,
                        torch.ones(
                            (attention_mask.shape[0], 1),
                            device=self.device,
                            dtype=attention_mask.dtype,
                        ),
                    ],
                    dim=-1,
                )

            log_progress(f"  Warmup token {i+1}/{num_tokens}")

        log_progress(f"Warmup complete for {model_name}")

    def load_model(
        self, model_id: str, name: Optional[str] = None, dtype: str = "bfloat16"
    ) -> Dict[str, Any]:
        """
        Load a model onto TPU.

        Args:
            model_id: HuggingFace model ID or path
            name: Name to reference the model by
            dtype: Data type (bfloat16, float32, float16)

        Returns:
            Model info dictionary
        """
        name = name or model_id.split("/")[-1]
        log_progress(f"Loading model: {model_id} as '{name}'")

        # Parse dtype
        dtype_map = {
            "bfloat16": torch.bfloat16,
            "float32": torch.float32,
            "float16": torch.float16,
        }
        torch_dtype = dtype_map.get(dtype, torch.bfloat16)
        log_progress(f"  Using dtype: {dtype}")

        # Load tokenizer
        log_progress("  Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Load model
        log_progress("  Loading model weights...")
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )

        # Move to device
        log_progress(f"  Moving model to {self.device}...")
        model = model.to(self.device)
        model.eval()

        if XLA_AVAILABLE:
            xm.mark_step()

        # Warmup
        self.warmup_model(model, tokenizer, name)

        model_info = {
            "model": model,
            "tokenizer": tokenizer,
            "model_id": model_id,
            "name": name,
            "dtype": dtype,
            "loaded_at": datetime.now().isoformat(),
        }

        self.loaded_models[name] = model_info
        log_progress(f"Model '{name}' loaded successfully")

        # Start batch worker if in multi mode
        if self.mode == "multi":
            self._start_batch_worker(name)

        return {"name": name, "model_id": model_id, "dtype": dtype, "status": "loaded"}

    def _start_batch_worker(self, model_name: str) -> None:
        """Start a batch worker for a model."""
        from tpu_inference_server.batch_worker import BatchWorker

        model_info = self.loaded_models[model_name]

        worker = BatchWorker(
            model=model_info["model"],
            tokenizer=model_info["tokenizer"],
            device=self.device,
            batch_size=self.batch_size,
            batch_timeout=self.batch_timeout,
        )
        worker.start()

        self._batch_workers[model_name] = worker
        log_progress(f"BatchWorker started for model '{model_name}'")

    def _stop_batch_worker(self, model_name: str) -> None:
        """Stop a batch worker for a model."""
        if model_name in self._batch_workers:
            self._batch_workers[model_name].stop()
            del self._batch_workers[model_name]
            log_progress(f"BatchWorker stopped for model '{model_name}'")

    def unload_model(self, name: str) -> bool:
        """
        Unload a model from memory.

        Args:
            name: Name of the model to unload

        Returns:
            True if successful, False if model not found
        """
        if name not in self.loaded_models:
            return False

        log_progress(f"Unloading model: {name}")

        # Stop batch worker first
        self._stop_batch_worker(name)

        del self.loaded_models[name]["model"]
        del self.loaded_models[name]["tokenizer"]
        del self.loaded_models[name]

        gc.collect()

        log_progress(f"Model '{name}' unloaded")
        return True

    def generate(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        max_new_tokens: int = 50,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop_sequences: Optional[List[str]] = None,
    ) -> str:
        """
        Generate text from a prompt.

        In single mode: directly generates tokens
        In multi mode: submits to batch worker queue

        Args:
            prompt: Input text prompt
            model_name: Name of model to use (uses first loaded if None)
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling probability
            stop_sequences: Sequences that stop generation

        Returns:
            Generated text
        """
        # Select model
        if model_name:
            if model_name not in self.loaded_models:
                raise ValueError(f"Model '{model_name}' is not loaded")
        elif self.loaded_models:
            model_name = list(self.loaded_models.keys())[0]
        else:
            raise ValueError("No models loaded")

        model_info = self.loaded_models[model_name]

        # Multi mode: use batch worker
        if self.mode == "multi":
            return self._generate_batched(
                prompt=prompt,
                model_name=model_name,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                stop_sequences=stop_sequences,
            )

        # Single mode: direct generation
        return generate_tokens(
            model=model_info["model"],
            tokenizer=model_info["tokenizer"],
            prompt=prompt,
            device=self.device,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            stop_sequences=stop_sequences,
        )

    def _generate_batched(
        self,
        prompt: str,
        model_name: str,
        max_new_tokens: int = 50,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop_sequences: Optional[List[str]] = None,
    ) -> str:
        """
        Generate text using the batch worker.

        Args:
            prompt: Input text prompt
            model_name: Name of model to use
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling probability
            stop_sequences: Sequences that stop generation

        Returns:
            Generated text
        """
        from tpu_inference_server.batch_worker import create_request

        if model_name not in self._batch_workers:
            raise ValueError(f"No batch worker for model '{model_name}'")

        worker = self._batch_workers[model_name]

        # Create and submit request
        req = create_request(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            stop_sequences=stop_sequences,
            model_name=model_name,
        )

        request_id = worker.submit(req)

        # Wait for result
        result = worker.get_result(request_id)

        if result.error:
            raise RuntimeError(result.error)

        return result.generated_text

    def load_models_from_config(self) -> None:
        """Load models specified in config file."""
        models_config = self.config.get("models", [])
        for model_config in models_config:
            try:
                self.load_model(
                    model_config["model_id"],
                    model_config.get("name"),
                    model_config.get("dtype", "bfloat16"),
                )
            except Exception as e:
                logger.error(f"Failed to load model {model_config['model_id']}: {e}")

    def run(self, debug: bool = False) -> None:
        """
        Start the Flask server.

        Args:
            debug: Enable debug mode (not recommended for TPU)
        """
        log_progress("=" * 50)
        log_progress("TPU Inference Server Starting")
        log_progress(f"Mode: {self.mode}")
        if self.mode == "multi":
            log_progress(f"Batch size: {self.batch_size}")
            log_progress(f"Batch timeout: {self.batch_timeout}s")
        log_progress("=" * 50)

        # Initialize device
        _ = self.device

        # Load models from config
        self.load_models_from_config()

        log_progress("=" * 50)
        log_progress(f"Server ready on http://{self.host}:{self.port}")
        log_progress(f"Loaded models: {list(self.loaded_models.keys())}")
        log_progress("=" * 50)

        # Start Flask server
        # single mode: threaded=False (all on main thread)
        # multi mode: threaded=True (Flask threads, TPU work on worker thread)
        threaded = self.mode == "multi"

        if threaded:
            log_progress("Flask running with threaded=True (multi-worker mode)")
        else:
            log_progress("Flask running with threaded=False (single-threaded mode)")

        self.app.run(host=self.host, port=self.port, threaded=threaded, debug=debug)

    def shutdown(self) -> None:
        """Shutdown the server and cleanup resources."""
        log_progress("Shutting down server...")

        # Stop all batch workers
        for model_name in list(self._batch_workers.keys()):
            self._stop_batch_worker(model_name)

        log_progress("Server shutdown complete")


def generate_tokens(
    model: Any,
    tokenizer: Any,
    prompt: str,
    device: Any,
    max_new_tokens: int = 50,
    temperature: float = 0.7,
    top_p: float = 0.9,
    stop_sequences: Optional[List[str]] = None,
) -> str:
    """
    Generate tokens manually (required for TPU/XLA compatibility).

    Does NOT use model.generate() which has XLA issues.

    Args:
        model: The loaded model
        tokenizer: The model's tokenizer
        prompt: Input text prompt
        device: Torch device
        max_new_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        top_p: Nucleus sampling probability
        stop_sequences: Sequences that stop generation

    Returns:
        Generated text
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    generated_tokens = []
    stop_sequences = stop_sequences or []

    log_progress(f"Generating {max_new_tokens} tokens...")

    for i in range(max_new_tokens):
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits[:, -1, :].float()

            if temperature > 0:
                logits = logits / temperature

                if top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                    cumulative_probs = torch.cumsum(
                        torch.softmax(sorted_logits, dim=-1), dim=-1
                    )

                    sorted_indices_to_remove = cumulative_probs > top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
                        ..., :-1
                    ].clone()
                    sorted_indices_to_remove[..., 0] = 0

                    indices_to_remove = sorted_indices_to_remove.scatter(
                        1, sorted_indices, sorted_indices_to_remove
                    )
                    logits[indices_to_remove] = float("-inf")

                probs = torch.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
            else:
                next_token = torch.argmax(logits, dim=-1, keepdim=True)

            if XLA_AVAILABLE:
                xm.mark_step()

            input_ids = torch.cat([input_ids, next_token], dim=-1)
            attention_mask = torch.cat(
                [
                    attention_mask,
                    torch.ones(
                        (attention_mask.shape[0], 1),
                        device=device,
                        dtype=attention_mask.dtype,
                    ),
                ],
                dim=-1,
            )

            generated_tokens.append(next_token.item())

            if next_token.item() == tokenizer.eos_token_id:
                log_progress(f"  EOS reached at token {i+1}")
                break

            current_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
            if any(stop_seq in current_text for stop_seq in stop_sequences):
                log_progress(f"  Stop sequence reached at token {i+1}")
                break

            if (i + 1) % 10 == 0:
                log_progress(f"  Generated {i+1}/{max_new_tokens} tokens")

    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    log_progress(f"Generation complete: {len(generated_tokens)} tokens")

    return generated_text


def format_chat_messages(messages: List[Dict[str, str]], tokenizer: Any) -> str:
    """
    Format chat messages into a prompt string.

    Args:
        messages: List of message dicts with 'role' and 'content'
        tokenizer: The model's tokenizer

    Returns:
        Formatted prompt string
    """
    try:
        if hasattr(tokenizer, "apply_chat_template"):
            return tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
    except Exception:
        pass

    formatted = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")

        if role == "system":
            formatted += f"System: {content}\n\n"
        elif role == "user":
            formatted += f"User: {content}\n\n"
        elif role == "assistant":
            formatted += f"Assistant: {content}\n\n"

    formatted += "Assistant:"
    return formatted


def create_app(server: "TPUInferenceServer") -> Flask:
    """
    Create Flask application with all routes.

    Args:
        server: TPUInferenceServer instance

    Returns:
        Flask application
    """
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health() -> Response:
        """Health check endpoint."""
        return jsonify(
            {
                "status": "healthy",
                "mode": server.mode,
                "device": str(server.device),
                "loaded_models": list(server.loaded_models.keys()),
                "timestamp": datetime.now().isoformat(),
            }
        )

    @app.route("/models", methods=["GET"])
    def list_models() -> Response:
        """List all loaded models."""
        models_info = []
        for name, info in server.loaded_models.items():
            models_info.append(
                {
                    "name": name,
                    "model_id": info["model_id"],
                    "dtype": info["dtype"],
                    "loaded_at": info["loaded_at"],
                    "has_batch_worker": name in server._batch_workers,
                }
            )
        return jsonify({"models": models_info})

    @app.route("/models/load", methods=["POST"])
    def api_load_model() -> Response:
        """Load a model dynamically."""
        try:
            data = request.get_json()
            model_id = data.get("model_id")
            name = data.get("name", model_id)
            dtype = data.get("dtype", "bfloat16")

            if not model_id:
                return jsonify({"error": "model_id is required"}), 400

            if name in server.loaded_models:
                return jsonify({"error": f"Model '{name}' is already loaded"}), 400

            result = server.load_model(model_id, name, dtype)
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/models/unload", methods=["POST"])
    def api_unload_model() -> Response:
        """Unload a model."""
        try:
            data = request.get_json()
            name = data.get("name")

            if not name:
                return jsonify({"error": "name is required"}), 400

            if name not in server.loaded_models:
                return jsonify({"error": f"Model '{name}' is not loaded"}), 404

            success = server.unload_model(name)
            if success:
                return jsonify({"status": "unloaded", "name": name})
            else:
                return jsonify({"error": "Failed to unload model"}), 500

        except Exception as e:
            logger.error(f"Error unloading model: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/generate", methods=["POST"])
    def generate() -> Response:
        """Generate text completion."""
        try:
            data = request.get_json()
            inputs = data.get("inputs", data.get("prompt", ""))
            model_name = data.get("model")
            max_new_tokens = data.get("max_new_tokens", 50)
            temperature = data.get("temperature", 0.7)
            top_p = data.get("top_p", 0.9)

            if not inputs:
                return jsonify({"error": "inputs is required"}), 400

            if not server.loaded_models:
                return jsonify({"error": "No models loaded"}), 400

            if model_name and model_name not in server.loaded_models:
                return jsonify({"error": f"Model '{model_name}' is not loaded"}), 404

            log_progress(
                f"Request: model={model_name}, max_tokens={max_new_tokens}, temp={temperature}"
            )

            generated_text = server.generate(
                prompt=inputs,
                model_name=model_name,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
            )

            return jsonify(
                {
                    "generated_text": generated_text,
                    "model": model_name or list(server.loaded_models.keys())[0],
                    "usage": {"max_new_tokens": max_new_tokens},
                }
            )

        except Exception as e:
            logger.error(f"Error generating: {e}")
            import traceback

            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @app.route("/v1/models", methods=["GET"])
    def openai_list_models() -> Response:
        """OpenAI-compatible models list endpoint."""
        models = []
        for name, info in server.loaded_models.items():
            models.append(
                {
                    "id": name,
                    "object": "model",
                    "created": int(
                        datetime.fromisoformat(info["loaded_at"]).timestamp()
                    ),
                    "owned_by": "local",
                    "permission": [],
                    "root": info["model_id"],
                    "parent": None,
                }
            )

        return jsonify({"object": "list", "data": models})

    @app.route("/v1/chat/completions", methods=["POST"])
    def openai_chat_completions() -> Response:
        """OpenAI-compatible chat completions endpoint."""
        try:
            data = request.get_json()
            model_name = data.get("model")
            messages = data.get("messages", [])
            max_tokens = data.get("max_tokens", 50)
            temperature = data.get("temperature", 0.7)
            top_p = data.get("top_p", 0.9)
            stop = data.get("stop", [])

            if not messages:
                return (
                    jsonify(
                        {
                            "error": {
                                "message": "messages is required",
                                "type": "invalid_request_error",
                            }
                        }
                    ),
                    400,
                )

            if not server.loaded_models:
                return (
                    jsonify(
                        {
                            "error": {
                                "message": "No models loaded",
                                "type": "invalid_request_error",
                            }
                        }
                    ),
                    400,
                )

            if model_name and model_name not in server.loaded_models:
                return (
                    jsonify(
                        {
                            "error": {
                                "message": f"Model '{model_name}' not found",
                                "type": "invalid_request_error",
                            }
                        }
                    ),
                    404,
                )

            # Get model info
            if model_name:
                model_info = server.loaded_models[model_name]
            else:
                model_name = list(server.loaded_models.keys())[0]
                model_info = server.loaded_models[model_name]

            # Format messages
            prompt = format_chat_messages(messages, model_info["tokenizer"])

            log_progress(f"Chat request: model={model_name}, max_tokens={max_tokens}")

            # Generate response
            generated_text = server.generate(
                prompt=prompt,
                model_name=model_name,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop_sequences=(
                    stop if isinstance(stop, list) else [stop] if stop else None
                ),
            )

            response = {
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model_name,
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": generated_text},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": -1,
                    "completion_tokens": -1,
                    "total_tokens": -1,
                },
            }

            return jsonify(response)

        except Exception as e:
            logger.error(f"Error in chat completions: {e}")
            import traceback

            traceback.print_exc()
            return (
                jsonify({"error": {"message": str(e), "type": "internal_error"}}),
                500,
            )

    return app


# For backwards compatibility
def load_model(model_id: str, name: str, dtype: str = "bfloat16") -> Dict[str, Any]:
    """
    Standalone function to load a model.

    Deprecated: Use TPUInferenceServer.load_model() instead.
    """
    raise NotImplementedError(
        "Use TPUInferenceServer class instead. "
        "Example: server = TPUInferenceServer(); server.load_model(...)"
    )


def unload_model(name: str) -> bool:
    """
    Standalone function to unload a model.

    Deprecated: Use TPUInferenceServer.unload_model() instead.
    """
    raise NotImplementedError(
        "Use TPUInferenceServer class instead. "
        "Example: server = TPUInferenceServer(); server.unload_model(...)"
    )
