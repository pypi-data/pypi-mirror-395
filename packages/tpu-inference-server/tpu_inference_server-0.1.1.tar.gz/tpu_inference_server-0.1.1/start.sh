#!/bin/bash
# TPU Inference Server Startup Script

set -e

# Configuration
CONDA_ENV_NAME="tpu-server"
CONFIG_FILE="config.yaml"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting TPU Inference Server${NC}"

# Initialize conda
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "/opt/conda/etc/profile.d/conda.sh" ]; then
    source "/opt/conda/etc/profile.d/conda.sh"
else
    echo -e "${YELLOW}Warning: Could not find conda. Trying to continue...${NC}"
fi

# Activate environment
if conda env list | grep -q "^${CONDA_ENV_NAME} "; then
    conda activate ${CONDA_ENV_NAME}
    echo "Activated conda environment: ${CONDA_ENV_NAME}"
else
    echo -e "${YELLOW}Warning: Environment '${CONDA_ENV_NAME}' not found. Run setup.sh first.${NC}"
    exit 1
fi

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}Warning: $CONFIG_FILE not found. Using default settings.${NC}"
fi

# Start server
echo "Starting server..."
echo ""

# Pass any command line arguments to the server
python server.py --config "$CONFIG_FILE" "$@"
