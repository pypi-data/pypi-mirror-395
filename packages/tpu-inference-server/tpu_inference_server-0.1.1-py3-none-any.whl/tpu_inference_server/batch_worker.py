"""
Batch Worker for TPU Inference Server

Provides thread-safe batched inference for multi-worker mode.
Only the worker thread touches TPU/XLA tensors.
"""

import os
import sys
import time
import uuid
import logging
import threading
from queue import Queue, Empty
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Callable

import torch

# Set PJRT_DEVICE before importing torch_xla
os.environ.setdefault("PJRT_DEVICE", "TPU")

try:
    import torch_xla.core.xla_model as xm

    XLA_AVAILABLE = True
except ImportError:
    XLA_AVAILABLE = False
    xm = None

logger = logging.getLogger(__name__)


def log_progress(message: str) -> None:
    """Log progress with flush for real-time output."""
    logger.info(message)
    sys.stdout.flush()


@dataclass
class InferenceRequest:
    """A single inference request."""

    request_id: str
    prompt: str
    max_new_tokens: int = 50
    temperature: float = 0.7
    top_p: float = 0.9
    stop_sequences: Optional[List[str]] = None
    model_name: Optional[str] = None


@dataclass
class InferenceResult:
    """Result of an inference request."""

    request_id: str
    generated_text: str = ""
    error: Optional[str] = None
    tokens_generated: int = 0


class BatchWorker:
    """
    Background worker that processes inference requests in batches.

    Only this worker thread touches TPU/XLA tensors, making it safe
    for Flask to run with threaded=True.
    """

    def __init__(
        self,
        model: Any,
        tokenizer: Any,
        device: Any,
        batch_size: int = 4,
        batch_timeout: float = 0.1,
    ):
        """
        Initialize the batch worker.

        Args:
            model: The loaded model
            tokenizer: The model's tokenizer
            device: Torch device (TPU)
            batch_size: Maximum requests per batch
            batch_timeout: Seconds to wait for batch to fill
        """
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout

        # Request queue and results storage
        self.request_queue: Queue[InferenceRequest] = Queue()
        self.results: Dict[str, InferenceResult] = {}
        self.results_lock = threading.Lock()
        self.result_events: Dict[str, threading.Event] = {}
        self.events_lock = threading.Lock()

        # Worker thread
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the worker thread."""
        if self._running:
            return

        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
        log_progress("BatchWorker started")

    def stop(self) -> None:
        """Stop the worker thread."""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5.0)
            self._worker_thread = None
        log_progress("BatchWorker stopped")

    def submit(self, request: InferenceRequest) -> str:
        """
        Submit an inference request.

        Args:
            request: The inference request

        Returns:
            Request ID for retrieving results
        """
        # Create event for this request
        with self.events_lock:
            self.result_events[request.request_id] = threading.Event()

        # Submit to queue
        self.request_queue.put(request)
        return request.request_id

    def get_result(self, request_id: str, timeout: float = 300.0) -> InferenceResult:
        """
        Wait for and retrieve a result.

        Args:
            request_id: The request ID
            timeout: Maximum time to wait in seconds

        Returns:
            The inference result

        Raises:
            TimeoutError: If result not ready within timeout
        """
        # Get event for this request
        with self.events_lock:
            event = self.result_events.get(request_id)

        if event is None:
            raise ValueError(f"Unknown request ID: {request_id}")

        # Wait for result
        if not event.wait(timeout=timeout):
            raise TimeoutError(f"Request {request_id} timed out after {timeout}s")

        # Get result
        with self.results_lock:
            result = self.results.pop(request_id, None)

        # Cleanup event
        with self.events_lock:
            self.result_events.pop(request_id, None)

        if result is None:
            return InferenceResult(request_id=request_id, error="Result not found")

        return result

    def _worker_loop(self) -> None:
        """Main worker loop - runs in dedicated thread."""
        log_progress("BatchWorker loop started")

        while self._running:
            try:
                # Collect batch of requests
                batch = self._collect_batch()

                if not batch:
                    continue

                # Process batch
                log_progress(f"Processing batch of {len(batch)} requests")
                results = self._process_batch(batch)

                # Store results and signal completion
                for result in results:
                    with self.results_lock:
                        self.results[result.request_id] = result

                    with self.events_lock:
                        event = self.result_events.get(result.request_id)
                        if event:
                            event.set()

            except Exception as e:
                logger.error(f"Error in worker loop: {e}")
                import traceback

                traceback.print_exc()

        log_progress("BatchWorker loop ended")

    def _collect_batch(self) -> List[InferenceRequest]:
        """Collect a batch of requests from the queue."""
        batch = []
        deadline = time.time() + self.batch_timeout

        # Get first request (blocking)
        try:
            first = self.request_queue.get(timeout=0.5)
            batch.append(first)
        except Empty:
            return []

        # Try to fill batch until timeout or full
        while len(batch) < self.batch_size and time.time() < deadline:
            try:
                remaining = deadline - time.time()
                if remaining <= 0:
                    break
                request = self.request_queue.get(timeout=min(remaining, 0.01))
                batch.append(request)
            except Empty:
                break

        return batch

    def _process_batch(self, batch: List[InferenceRequest]) -> List[InferenceResult]:
        """
        Process a batch of requests.

        Args:
            batch: List of inference requests

        Returns:
            List of inference results
        """
        try:
            # Extract prompts and parameters
            prompts = [req.prompt for req in batch]
            max_tokens = max(req.max_new_tokens for req in batch)

            # Batch tokenize with padding
            self.tokenizer.padding_side = "left"  # Left padding for generation
            inputs = self.tokenizer(
                prompts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=2048,
            )

            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)

            # Track generated tokens per sequence
            batch_size = len(batch)
            generated_tokens: List[List[int]] = [[] for _ in range(batch_size)]
            finished = [False] * batch_size

            # Get per-request parameters (use first request's params for batch)
            # In production, you might want smarter handling of mixed params
            temperature = batch[0].temperature
            top_p = batch[0].top_p

            log_progress(f"Generating up to {max_tokens} tokens for batch of {batch_size}")

            # Generate tokens
            for token_idx in range(max_tokens):
                if all(finished):
                    break

                with torch.no_grad():
                    outputs = self.model(
                        input_ids=input_ids, attention_mask=attention_mask
                    )
                    logits = outputs.logits[:, -1, :].float()

                    # Apply temperature
                    if temperature > 0:
                        logits = logits / temperature

                        # Apply top-p sampling
                        if top_p < 1.0:
                            sorted_logits, sorted_indices = torch.sort(
                                logits, descending=True
                            )
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
                        next_tokens = torch.multinomial(probs, num_samples=1)
                    else:
                        next_tokens = torch.argmax(logits, dim=-1, keepdim=True)

                    # Critical: mark step for TPU
                    if XLA_AVAILABLE:
                        xm.mark_step()

                    # Update sequences
                    input_ids = torch.cat([input_ids, next_tokens], dim=-1)
                    attention_mask = torch.cat(
                        [
                            attention_mask,
                            torch.ones(
                                (batch_size, 1),
                                device=self.device,
                                dtype=attention_mask.dtype,
                            ),
                        ],
                        dim=-1,
                    )

                    # Store generated tokens and check for EOS
                    for i in range(batch_size):
                        if finished[i]:
                            continue

                        token_id = next_tokens[i].item()
                        generated_tokens[i].append(token_id)

                        # Check for EOS
                        if token_id == self.tokenizer.eos_token_id:
                            finished[i] = True

                        # Check for stop sequences
                        if batch[i].stop_sequences:
                            text = self.tokenizer.decode(
                                generated_tokens[i], skip_special_tokens=True
                            )
                            for stop_seq in batch[i].stop_sequences:
                                if stop_seq in text:
                                    finished[i] = True
                                    break

                        # Check max tokens for this request
                        if len(generated_tokens[i]) >= batch[i].max_new_tokens:
                            finished[i] = True

                if (token_idx + 1) % 10 == 0:
                    log_progress(
                        f"  Generated {token_idx + 1}/{max_tokens} tokens (batch)"
                    )

            # Decode results
            results = []
            for i, req in enumerate(batch):
                text = self.tokenizer.decode(
                    generated_tokens[i], skip_special_tokens=True
                )
                results.append(
                    InferenceResult(
                        request_id=req.request_id,
                        generated_text=text,
                        tokens_generated=len(generated_tokens[i]),
                    )
                )

            log_progress(f"Batch complete: {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            import traceback

            traceback.print_exc()

            # Return error results for all requests
            return [
                InferenceResult(request_id=req.request_id, error=str(e))
                for req in batch
            ]


def create_request(
    prompt: str,
    max_new_tokens: int = 50,
    temperature: float = 0.7,
    top_p: float = 0.9,
    stop_sequences: Optional[List[str]] = None,
    model_name: Optional[str] = None,
) -> InferenceRequest:
    """
    Create an inference request with a unique ID.

    Args:
        prompt: Input text prompt
        max_new_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        top_p: Nucleus sampling probability
        stop_sequences: Sequences that stop generation
        model_name: Name of model to use

    Returns:
        InferenceRequest with unique ID
    """
    return InferenceRequest(
        request_id=str(uuid.uuid4()),
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        stop_sequences=stop_sequences,
        model_name=model_name,
    )
