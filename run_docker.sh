#!/bin/bash

# Check if input file is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input_file> [args...]"
    exit 1
fi

INPUT_FILE=$1
shift # Shift arguments so $@ contains the rest

# Build the Docker image
echo "Building Docker image..."
docker build -t cycle-detector . > /dev/null

# Run the container with a memory limit (e.g., 128MB) to validate memory efficiency
docker run --rm --memory="128m" -v "$(pwd)/$INPUT_FILE:/app/input.txt" cycle-detector input.txt "$@"