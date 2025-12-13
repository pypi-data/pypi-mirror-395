# TPU Inference Server

A Flask-based inference server optimized for Google Cloud TPU v5e. Supports multiple models, dynamic loading/unloading, and provides OpenAI-compatible API endpoints.

## Installation

### From PyPI (recommended)

```bash
pip install tpu-inference-server
```

### From Source

```bash
git clone https://github.com/yourusername/tpu-inference-server.git
cd tpu-inference-server
pip install -e .
```

### TPU Dependencies

PyTorch XLA for TPU must be installed separately from Google's index:

```bash
pip install torch torch_xla \
  -f https://storage.googleapis.com/libtpu-releases/index.html \
  -f https://storage.googleapis.com/libtpu-wheels/index.html
```

Or use the setup script on a TPU VM:

```bash
./setup.sh
```

## Features

- **TPU Optimized**: Uses PyTorch XLA with manual token generation for reliable TPU inference
- **Multiple Models**: Load and serve multiple models simultaneously
- **Dynamic Loading**: Load/unload models at runtime via API
- **OpenAI Compatible**: `/v1/chat/completions` endpoint works with OpenAI client libraries
- **Memory Efficient**: Uses bfloat16 by default for 7B parameter models
- **XLA Warmup**: Automatic warmup step to pre-compile XLA graphs
- **CLI Tool**: Easy-to-use command-line interface
- **Python Client**: Built-in client library for programmatic access

## Supported Models

| Model | ID | Recommended dtype | Memory |
|-------|-----|------------------|--------|
| Mistral 7B | `mistralai/Mistral-7B-Instruct-v0.2` | bfloat16 | ~14GB |
| Llama 2 7B | `meta-llama/Llama-2-7b-chat-hf` | bfloat16 | ~14GB |
| Gemma 2B | `google/gemma-2b-it` | bfloat16 | ~4GB |
| GPT-2 | `gpt2` | float32 | ~0.5GB |

## Quick Start

### CLI Usage

```bash
# Generate example config file
tpu-server init-config

# Start server with config
tpu-server serve --config config.yaml

# Start with specific model
tpu-server serve --model gpt2 --model-name gpt2 --dtype float32

# Start with custom host/port
tpu-server serve --host 0.0.0.0 --port 9000
```

### Python Usage

```python
from tpu_inference_server import TPUInferenceServer, TPUInferenceClient

# Start server programmatically
server = TPUInferenceServer(port=8080)
server.load_model("gpt2", "gpt2", "float32")
server.run()
```

```python
# Use the client
from tpu_inference_server import TPUInferenceClient

client = TPUInferenceClient("http://localhost:8080")

# Check health
print(client.health())

# Generate text
result = client.generate("Hello, world!", max_new_tokens=50)
print(result["generated_text"])

# Chat completion
response = client.chat_simple("What is Python?", max_tokens=100)
print(response)
```

### Module Execution

```bash
python -m tpu_inference_server serve --model gpt2
```

## Google Cloud TPU Setup

### 1. Create a TPU v5e Instance

```bash
# Create TPU v5e-4 (4 chips)
gcloud compute tpus queued-resources create my-tpu-qr \
    --node-id=my-tpu \
    --zone=us-central1-a \
    --accelerator-type=v5litepod-4 \
    --runtime-version=v2-alpha-tpuv5-lite

# Wait for TPU to be ready
gcloud compute tpus queued-resources describe my-tpu-qr \
    --zone=us-central1-a

# SSH into the TPU VM
gcloud compute tpus tpu-vm ssh my-tpu --zone=us-central1-a
```

### 2. Install and Run

```bash
# Install the package
pip install tpu-inference-server

# Install TPU dependencies
pip install torch torch_xla \
  -f https://storage.googleapis.com/libtpu-releases/index.html \
  -f https://storage.googleapis.com/libtpu-wheels/index.html

# Generate config
tpu-server init-config

# Start server
tpu-server serve
```

## API Reference

> **Note:** The first request after loading a model will take longer (30-60+ seconds) as XLA compiles the computation graph. Subsequent requests will be much faster.

### Health Check

```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "device": "xla:0",
  "loaded_models": ["mistral-7b"],
  "timestamp": "2024-01-15T10:30:00"
}
```

### List Models

```bash
curl http://localhost:8080/models
```

### Load Model Dynamically

```bash
curl http://localhost:8080/models/load \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"model_id": "gpt2", "name": "gpt2", "dtype": "float32"}'
```

### Unload Model

```bash
curl http://localhost:8080/models/unload \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "gpt2"}'
```

### Generate Text

```bash
curl http://localhost:8080/generate \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "What is artificial intelligence?",
    "model": "mistral-7b",
    "max_new_tokens": 100,
    "temperature": 0.7
  }'
```

Response:
```json
{
  "generated_text": "Artificial intelligence (AI) is...",
  "model": "mistral-7b",
  "usage": {"max_new_tokens": 100}
}
```

### OpenAI-Compatible Chat Completions

```bash
curl http://localhost:8080/v1/chat/completions \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-7b",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

Response:
```json
{
  "id": "chatcmpl-1705312200",
  "object": "chat.completion",
  "created": 1705312200,
  "model": "mistral-7b",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! I'm doing well, thank you for asking..."
    },
    "finish_reason": "stop"
  }]
}
```

### OpenAI-Compatible Models List

```bash
curl http://localhost:8080/v1/models
```

## Configuration

### config.yaml

```yaml
server:
  host: "0.0.0.0"    # Bind address
  port: 8080          # Port number

models:
  - model_id: "mistralai/Mistral-7B-Instruct-v0.2"
    name: "mistral-7b"     # Name to reference model by
    dtype: "bfloat16"      # bfloat16, float32, or float16
```

### CLI Options

```bash
tpu-server serve --help

Options:
  --config, -c     Path to config file (default: config.yaml)
  --host           Host to bind (default: 0.0.0.0)
  --port, -p       Port to bind (default: 8080)
  --model, -m      Model ID to load on startup
  --model-name     Name for the model
  --dtype          Data type: bfloat16, float32, float16 (default: bfloat16)
  --no-warmup      Skip warmup step on model load
  --debug          Enable debug mode
```

## External Access

### Create Firewall Rule

```bash
gcloud compute firewall-rules create allow-inference-8080 \
  --allow tcp:8080 \
  --source-ranges="0.0.0.0/0" \
  --description="Allow inference server access"
```

### Get External IP

```bash
# From the TPU VM
curl -s ifconfig.me
```

### Access from External Client

```bash
curl http://<EXTERNAL_IP>:8080/health
```

## Memory Requirements

| TPU Type | HBM Memory | Recommended Models |
|----------|------------|-------------------|
| v5litepod-1 | 16GB | Gemma 2B, GPT-2 |
| v5litepod-4 | 64GB | Mistral 7B, Llama 2 7B, multiple small models |
| v5litepod-8 | 128GB | Multiple 7B models, 13B models |

## Using with OpenAI Python Client

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"  # API key not required for local server
)

response = client.chat.completions.create(
    model="mistral-7b",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=50
)

print(response.choices[0].message.content)
```

## Troubleshooting

### "No TPU devices found"

Ensure you're running on a TPU VM:
```bash
ls /dev/accel*
```

Verify TPU is healthy:
```bash
gcloud compute tpus tpu-vm describe my-tpu --zone=us-central1-a
```

### "Out of memory"

- Use `bfloat16` instead of `float32`
- Load fewer models simultaneously
- Try a smaller model (Gemma 2B, GPT-2)

### Slow first request

This is normal - XLA needs to compile the graph. The warmup step reduces this, but the first real request may still be slower.

### "XLA compilation failed"

Ensure you're using the correct PyTorch XLA version:
```bash
pip install torch torch_xla \
  -f https://storage.googleapis.com/libtpu-releases/index.html \
  -f https://storage.googleapis.com/libtpu-wheels/index.html
```

### Model download fails

For gated models (Llama 2), you need to:
1. Accept the license on HuggingFace
2. Login: `huggingface-cli login`

## Cleanup

### Delete TPU Resources

```bash
# Delete TPU
gcloud compute tpus queued-resources delete my-tpu-qr \
  --zone=us-central1-a \
  --force \
  --quiet

# Delete firewall rule (optional)
gcloud compute firewall-rules delete allow-inference-8080 --quiet
```

## Architecture Notes

### Why Manual Token Generation?

The standard `model.generate()` method in Transformers has known issues with XLA/TPU:
- Causes excessive recompilation
- Can hang or produce incorrect outputs
- Memory usage is unpredictable

This server uses a manual generation loop that:
- Calls the model forward pass directly
- Uses `xm.mark_step()` after each token
- Provides predictable memory usage and performance

### Why Single-Threaded Flask?

TPU/XLA requires single-threaded execution:
- XLA compilation is not thread-safe
- Model state cannot be shared across threads safely
- Flask's `threaded=False` ensures correct behavior

For production deployments with high concurrency, consider:
- Running multiple server instances behind a load balancer
- Using a queue-based architecture

## Development

### Install dev dependencies

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Format code

```bash
black src/
ruff check src/ --fix
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

MIT License
