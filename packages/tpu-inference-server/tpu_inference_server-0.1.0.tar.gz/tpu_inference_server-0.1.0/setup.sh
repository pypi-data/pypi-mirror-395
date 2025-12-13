#!/bin/bash
# TPU Inference Server Setup Script
# Installs Miniconda, creates environment, and installs dependencies

set -e

echo "=========================================="
echo "TPU Inference Server Setup"
echo "=========================================="

# Configuration
CONDA_ENV_NAME="tpu-server"
PYTHON_VERSION="3.10"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on TPU VM
check_tpu() {
    if [ -d "/dev/accel" ] || [ -f "/usr/share/tpu/tpu_version" ]; then
        print_status "TPU device detected"
        return 0
    else
        print_warning "TPU device not detected. This script is designed for TPU VMs."
        print_warning "Continuing anyway (useful for testing setup)..."
        return 0
    fi
}

# Install Miniconda if not present
install_miniconda() {
    if command -v conda &> /dev/null; then
        print_status "Conda already installed"
        return 0
    fi

    print_status "Installing Miniconda..."

    # Download Miniconda
    MINICONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
    wget -q "https://repo.anaconda.com/miniconda/${MINICONDA_INSTALLER}" -O /tmp/${MINICONDA_INSTALLER}

    # Install silently
    bash /tmp/${MINICONDA_INSTALLER} -b -p $HOME/miniconda3

    # Initialize conda
    eval "$($HOME/miniconda3/bin/conda shell.bash hook)"

    # Add to bashrc
    $HOME/miniconda3/bin/conda init bash

    print_status "Miniconda installed successfully"
    print_warning "You may need to restart your shell or run: source ~/.bashrc"
}

# Create conda environment
create_environment() {
    # Source conda
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    elif [ -f "/opt/conda/etc/profile.d/conda.sh" ]; then
        source "/opt/conda/etc/profile.d/conda.sh"
    fi

    # Check if environment exists
    if conda env list | grep -q "^${CONDA_ENV_NAME} "; then
        print_status "Environment '${CONDA_ENV_NAME}' already exists"
        print_status "Activating existing environment..."
        conda activate ${CONDA_ENV_NAME}
    else
        print_status "Creating conda environment '${CONDA_ENV_NAME}' with Python ${PYTHON_VERSION}..."
        conda create -n ${CONDA_ENV_NAME} python=${PYTHON_VERSION} -y
        conda activate ${CONDA_ENV_NAME}
    fi
}

# Install PyTorch and PyTorch XLA for TPU
install_pytorch_xla() {
    print_status "Installing PyTorch and PyTorch XLA for TPU..."

    # Install from Google's TPU index
    pip install torch torch_xla \
        -f https://storage.googleapis.com/libtpu-releases/index.html \
        -f https://storage.googleapis.com/libtpu-wheels/index.html

    print_status "PyTorch XLA installed"
}

# Install transformers and other dependencies
install_dependencies() {
    print_status "Installing transformers and dependencies..."

    pip install transformers accelerate sentencepiece protobuf

    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        pip install flask pyyaml requests
    fi

    print_status "Dependencies installed"
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."

    python -c "
import sys
print(f'Python: {sys.version}')

import torch
print(f'PyTorch: {torch.__version__}')

try:
    import torch_xla
    print(f'PyTorch XLA: {torch_xla.__version__}')
except ImportError:
    print('PyTorch XLA: Not installed')

import transformers
print(f'Transformers: {transformers.__version__}')

import flask
print(f'Flask: {flask.__version__}')

print('\\nAll packages installed successfully!')
"
}

# Print usage instructions
print_usage() {
    echo ""
    echo "=========================================="
    echo "Setup Complete!"
    echo "=========================================="
    echo ""
    echo "To start the server:"
    echo ""
    echo "  1. Activate the environment:"
    echo "     conda activate ${CONDA_ENV_NAME}"
    echo ""
    echo "  2. Edit config.yaml to configure your models"
    echo ""
    echo "  3. Start the server:"
    echo "     python server.py"
    echo ""
    echo "     Or use the start script:"
    echo "     ./start.sh"
    echo ""
    echo "  4. Test the server:"
    echo "     curl http://localhost:8080/health"
    echo ""
    echo "Quick start with GPT-2 (for testing):"
    echo "     python server.py --model gpt2 --model-name gpt2 --dtype float32"
    echo ""
    echo "For more information, see README.md"
    echo ""
}

# Main installation flow
main() {
    check_tpu
    install_miniconda
    create_environment
    install_pytorch_xla
    install_dependencies
    verify_installation
    print_usage
}

# Run main
main
