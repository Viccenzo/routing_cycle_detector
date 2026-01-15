# Routing Cycle Detector

A memory-efficient tool to find the longest routing cycle in large datasets.

## How to use

### Running with Python
Ensure you have Python 3 installed.
```bash
python3 my_solution.py <input_file>
```
Optional: use `--memory-limit` for the system `sort` command (e.g., `--memory-limit 512M`).

### Running with Docker
Use the provided script to build and run the application in a containerized environment. This setup is specifically used to collect resource metrics and validate that the solution adheres to strict memory constraints:
```bash
./run_docker.sh <input_file>
```
Optional: use `--memory-limit` for the system `sort` command (e.g., `--memory-limit 512M`).

## Output
The script prints the result to stdout and saves it to `solution.txt` in the format:
`claim_id,status_code,max_cycle_length`