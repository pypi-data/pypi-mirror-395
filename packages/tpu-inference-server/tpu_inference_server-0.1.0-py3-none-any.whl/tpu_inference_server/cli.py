"""
Command-line interface for TPU Inference Server.

Usage:
    tpu-server serve [options]
    tpu-server --help
"""

import argparse
import sys
from pathlib import Path
from typing import Optional


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="tpu-server",
        description="TPU Inference Server - A Flask-based inference server for Google Cloud TPU",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server in single-threaded mode (default)
  tpu-server serve

  # Start server in multi-worker mode with batching
  tpu-server serve --mode multi --batch-size 4

  # Start with specific model
  tpu-server serve --model gpt2 --model-name gpt2 --dtype float32

  # Start with custom config and multi-worker mode
  tpu-server serve --config my-config.yaml --mode multi --batch-size 8

  # Generate example config
  tpu-server init-config

For more information, see: https://github.com/yourusername/tpu-inference-server
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the inference server")
    serve_parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config.yaml",
        help="Path to config file (default: config.yaml)",
    )
    serve_parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind (default: 0.0.0.0)",
    )
    serve_parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8080,
        help="Port to bind (default: 8080)",
    )
    serve_parser.add_argument(
        "--model",
        "-m",
        type=str,
        help="Model ID to load on startup (e.g., gpt2, mistralai/Mistral-7B-Instruct-v0.2)",
    )
    serve_parser.add_argument(
        "--model-name",
        type=str,
        help="Name for the model (defaults to model ID)",
    )
    serve_parser.add_argument(
        "--dtype",
        type=str,
        default="bfloat16",
        choices=["bfloat16", "float32", "float16"],
        help="Data type for model (default: bfloat16)",
    )
    serve_parser.add_argument(
        "--no-warmup",
        action="store_true",
        help="Skip warmup step on model load",
    )

    # Multi-worker mode options
    serve_parser.add_argument(
        "--mode",
        type=str,
        default="single",
        choices=["single", "multi"],
        help="Server mode: 'single' for single-threaded, 'multi' for batched multi-worker (default: single)",
    )
    serve_parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Maximum requests per batch in multi mode (default: 4)",
    )
    serve_parser.add_argument(
        "--batch-timeout",
        type=float,
        default=0.1,
        help="Seconds to wait for batch to fill in multi mode (default: 0.1)",
    )

    serve_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (not recommended for TPU)",
    )

    # Init-config command
    init_parser = subparsers.add_parser("init-config", help="Generate example config file")
    init_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="config.yaml",
        help="Output path for config file (default: config.yaml)",
    )
    init_parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing file",
    )
    init_parser.add_argument(
        "--multi",
        action="store_true",
        help="Generate config with multi-worker mode settings",
    )

    # Version
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s 0.1.0",
    )

    return parser


def cmd_serve(args: argparse.Namespace) -> int:
    """Run the serve command."""
    from tpu_inference_server.server import TPUInferenceServer

    server = TPUInferenceServer(
        config_path=args.config if Path(args.config).exists() else None,
        host=args.host,
        port=args.port,
        skip_warmup=args.no_warmup,
        mode=args.mode,
        batch_size=args.batch_size,
        batch_timeout=args.batch_timeout,
    )

    # Load model from command line if specified
    if args.model:
        model_name = args.model_name or args.model.split("/")[-1]
        server.load_model(args.model, model_name, args.dtype)

    # Start server
    server.run(debug=args.debug)
    return 0


def cmd_init_config(args: argparse.Namespace) -> int:
    """Generate example config file."""
    if args.multi:
        config_content = """\
# TPU Inference Server Configuration
# Multi-worker mode with batched inference

# Server settings
server:
  host: "0.0.0.0"
  port: 8080
  # Multi-worker mode settings
  mode: "multi"           # "single" or "multi"
  batch_size: 4           # Max requests per batch
  batch_timeout: 0.1      # Seconds to wait for batch to fill

# Models to load on startup
models:
  # Mistral 7B - Good general-purpose model
  - model_id: "mistralai/Mistral-7B-Instruct-v0.2"
    name: "mistral-7b"
    dtype: "bfloat16"

  # Gemma 2B - Smaller, faster model
  # - model_id: "google/gemma-2b-it"
  #   name: "gemma-2b"
  #   dtype: "bfloat16"

  # GPT-2 - Very small, good for testing
  # - model_id: "gpt2"
  #   name: "gpt2"
  #   dtype: "float32"
"""
    else:
        config_content = """\
# TPU Inference Server Configuration

# Server settings
server:
  host: "0.0.0.0"
  port: 8080
  # Uncomment for multi-worker mode with batching:
  # mode: "multi"
  # batch_size: 4
  # batch_timeout: 0.1

# Models to load on startup
# Comment out models you don't want to load automatically
models:
  # Mistral 7B - Good general-purpose model
  - model_id: "mistralai/Mistral-7B-Instruct-v0.2"
    name: "mistral-7b"
    dtype: "bfloat16"

  # Gemma 2B - Smaller, faster model
  # - model_id: "google/gemma-2b-it"
  #   name: "gemma-2b"
  #   dtype: "bfloat16"

  # GPT-2 - Very small, good for testing
  # - model_id: "gpt2"
  #   name: "gpt2"
  #   dtype: "float32"

  # Llama 2 7B Chat (requires HuggingFace access token)
  # - model_id: "meta-llama/Llama-2-7b-chat-hf"
  #   name: "llama-7b"
  #   dtype: "bfloat16"
"""

    output_path = Path(args.output)

    if output_path.exists() and not args.force:
        print(f"Error: {output_path} already exists. Use --force to overwrite.")
        return 1

    output_path.write_text(config_content)
    print(f"Config file created: {output_path}")
    return 0


def main(argv: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "serve":
        return cmd_serve(args)
    elif args.command == "init-config":
        return cmd_init_config(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
