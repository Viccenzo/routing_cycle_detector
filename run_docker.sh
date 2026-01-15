#!/bin/bash

# Check if input file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

INPUT_FILE=$1

# Build the Docker image
echo "Building Docker image..."
docker build -t cycle-detector .

# Run the container
# -v "$(pwd)/$INPUT_FILE:/app/input.txt": Mounts the input file to /app/input.txt inside the container
# --rm: Removes the container after it exits
echo "Running cycle detector..."
echo "---------------------------------------------------"
docker run --rm -v "$(pwd)/$INPUT_FILE:/app/input.txt" cycle-detector input.txt
