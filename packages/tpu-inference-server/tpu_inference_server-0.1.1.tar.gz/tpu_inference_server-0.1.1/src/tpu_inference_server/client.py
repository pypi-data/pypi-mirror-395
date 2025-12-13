"""
TPU Inference Server - Python Client

A Python client for interacting with the TPU Inference Server API.
"""

import json
from typing import Dict, Any, Optional, List, Union

import requests


class TPUInferenceClient:
    """
    Client for the TPU Inference Server API.

    Example:
        >>> client = TPUInferenceClient("http://localhost:8080")
        >>> client.health()
        {'status': 'healthy', 'loaded_models': ['mistral-7b']}
        >>> client.generate("Hello, world!", max_new_tokens=50)
        {'generated_text': '...', 'model': 'mistral-7b'}
    """

    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 300):
        """
        Initialize the client.

        Args:
            base_url: Base URL of the inference server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the server."""
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == "POST":
                response = self.session.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=self.timeout,
                )
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Could not connect to server at {self.base_url}"
            ) from e
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request timed out after {self.timeout}s") from e
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                error_msg = error_data.get("error", str(e))
            except (json.JSONDecodeError, AttributeError):
                error_msg = str(e)
            raise RuntimeError(f"Server error: {error_msg}") from e

    def health(self) -> Dict[str, Any]:
        """
        Check server health status.

        Returns:
            Health status dict with 'status', 'device', 'loaded_models', 'timestamp'
        """
        return self._request("GET", "/health")

    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all loaded models.

        Returns:
            List of model info dicts
        """
        response = self._request("GET", "/models")
        return response.get("models", [])

    def load_model(
        self, model_id: str, name: Optional[str] = None, dtype: str = "bfloat16"
    ) -> Dict[str, Any]:
        """
        Load a model onto the server.

        Args:
            model_id: HuggingFace model ID or path
            name: Name to reference the model by
            dtype: Data type (bfloat16, float32, float16)

        Returns:
            Model info dict with loading status
        """
        return self._request(
            "POST",
            "/models/load",
            data={"model_id": model_id, "name": name or model_id, "dtype": dtype},
        )

    def unload_model(self, name: str) -> Dict[str, Any]:
        """
        Unload a model from the server.

        Args:
            name: Name of the model to unload

        Returns:
            Status dict
        """
        return self._request("POST", "/models/unload", data={"name": name})

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_new_tokens: int = 50,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> Dict[str, Any]:
        """
        Generate text completion.

        Args:
            prompt: Input text prompt
            model: Name of model to use (uses first loaded if None)
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling probability

        Returns:
            Dict with 'generated_text', 'model', and 'usage'
        """
        data = {
            "inputs": prompt,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
        }
        if model:
            data["model"] = model

        return self._request("POST", "/generate", data=data)

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 50,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop: Optional[Union[str, List[str]]] = None,
    ) -> Dict[str, Any]:
        """
        Send a chat completion request (OpenAI-compatible).

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Name of model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling probability
            stop: Stop sequence(s)

        Returns:
            OpenAI-compatible chat completion response
        """
        data = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
        }
        if model:
            data["model"] = model
        if stop:
            data["stop"] = stop

        return self._request("POST", "/v1/chat/completions", data=data)

    def chat_simple(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 50,
        temperature: float = 0.7,
    ) -> str:
        """
        Simple chat interface that returns just the response text.

        Args:
            message: User message
            model: Name of model to use
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Assistant's response text
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        response = self.chat(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response["choices"][0]["message"]["content"]

    def openai_models(self) -> List[Dict[str, Any]]:
        """
        List models using OpenAI-compatible endpoint.

        Returns:
            List of model dicts in OpenAI format
        """
        response = self._request("GET", "/v1/models")
        return response.get("data", [])

    def is_healthy(self) -> bool:
        """
        Check if server is healthy.

        Returns:
            True if server is healthy
        """
        try:
            health = self.health()
            return health.get("status") == "healthy"
        except Exception:
            return False

    def wait_for_ready(self, timeout: int = 60, interval: float = 1.0) -> bool:
        """
        Wait for server to be ready.

        Args:
            timeout: Maximum time to wait in seconds
            interval: Check interval in seconds

        Returns:
            True if server became ready, False if timeout
        """
        import time

        start = time.time()
        while time.time() - start < timeout:
            if self.is_healthy():
                return True
            time.sleep(interval)
        return False


def demo():
    """Run demo of all client features."""
    print("=" * 60)
    print("TPU Inference Server Client Demo")
    print("=" * 60)

    client = TPUInferenceClient()

    # Check health
    print("\n1. Health Check")
    try:
        health = client.health()
        print(f"   Status: {health['status']}")
        print(f"   Device: {health['device']}")
        print(f"   Models: {health['loaded_models']}")
    except Exception as e:
        print(f"   Error: {e}")
        print("   Make sure the server is running!")
        return

    # List models
    print("\n2. List Models")
    models = client.list_models()
    for model in models:
        print(f"   - {model['name']} ({model['model_id']})")

    if not models:
        print("   No models loaded. Loading GPT-2 for demo...")
        try:
            client.load_model("gpt2", "gpt2", "float32")
        except Exception as e:
            print(f"   Failed to load model: {e}")
            return

    # Generate text
    print("\n3. Generate Text")
    try:
        result = client.generate(
            prompt="The meaning of life is",
            max_new_tokens=30,
            temperature=0.8,
        )
        print(f"   Generated: {result['generated_text']}")
    except Exception as e:
        print(f"   Error: {e}")

    # Chat
    print("\n4. Chat Completion")
    try:
        response = client.chat_simple(
            message="What is Python?",
            max_tokens=50,
        )
        print(f"   Response: {response}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    demo()
