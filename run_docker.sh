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

# Run the container
echo "Running cycle detector..."
echo "---------------------------------------------------"
# We mount the input file to /app/input.txt
# We pass 'input.txt' as the first arg to the python script
# We then pass any remaining arguments ($@) to the script
docker run --rm -v "$(pwd)/$INPUT_FILE:/app/input.txt" cycle-detector input.txt "$@"