# Use a lightweight Python base image
FROM python:3.11-slim

# Install system dependencies
# 'time' is needed for the /usr/bin/time command to measure resource usage
# 'procps' gives us tools like 'ps' and 'top' (optional but good for debugging)
RUN apt-get update && apt-get install -y \
    time \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the solution script into the container
COPY my_solution.py .

# Define the entrypoint to run the script using the 'time' command for metrics
# We use 'sh -c' to allow passing arguments flexibly
ENTRYPOINT ["/usr/bin/time", "-v", "python3", "my_solution.py"]
