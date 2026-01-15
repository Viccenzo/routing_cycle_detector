import sys
import subprocess
import collections
import argparse

def get_sorted_stream(file_path, memory_limit=None):
    """
    Spawns a subprocess to sort the input file by claim_id and status_code.
    Returns the stdout stream of the sort process.
    """
    # We use LC_ALL=C for faster sorting (byte comparison)
    # Sort key: fields 3 (claim_id) and 4 (status_code)
    sort_cmd = ["sort", "-t|", "-k3,3", "-k4,4"]
    
    # Add memory limit flag if provided (e.g., "256M", "1G")
    if memory_limit:
        sort_cmd.extend(["-S", memory_limit])
        
    sort_cmd.append(file_path)
    
    try:
        process = subprocess.Popen(
            sort_cmd,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            universal_newlines=True,
            env={"LC_ALL": "C"} 
        )
        return process
    except FileNotFoundError:
        sys.stderr.write("Error: 'sort' command not found or input file missing.\n")
        sys.exit(1)

def generate_groups(stream):
    """
    Generator that yields ((claim_id, status_code), edges) pairs from the sorted stream.
    """
    current_key = None
    edges = []

    for line in stream:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split('|')
        if len(parts) != 4:
            continue
            
        src, dst, claim_id, status_code = parts
        key = (claim_id, status_code)
        
        if key != current_key:
            if current_key is not None:
                yield current_key, edges
            current_key = key
            edges = []
        
        edges.append((src, dst))
    
    if current_key is not None:
        yield current_key, edges

def find_longest_cycle(edges):
    """
    Constructs a graph from the list of edges and finds the length of the
    longest simple cycle using DFS.
    """
    if not edges:
        return 0

    adj = collections.defaultdict(list)
    nodes = set()
    for u, v in edges:
        adj[u].append(v)
        nodes.add(u)
        nodes.add(v)
    
    longest_cycle = 0
    
    def dfs(current_node, start_node, path_nodes, path_length):
        nonlocal longest_cycle
        
        if current_node in adj:
            for neighbor in adj[current_node]:
                if neighbor == start_node:
                    longest_cycle = max(longest_cycle, path_length + 1)
                elif neighbor not in path_nodes:
                    path_nodes.add(neighbor)
                    dfs(neighbor, start_node, path_nodes, path_length + 1)
                    path_nodes.remove(neighbor)

    # Optimization: Iterate over all nodes to find cycles starting from them.
    for start_node in nodes:
        dfs(start_node, start_node, {start_node}, 0)
        
    return longest_cycle

def main():
    parser = argparse.ArgumentParser(description="Find longest routing cycle in a large file.")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("--memory-limit", help="Memory limit for the sort command (e.g., 256M, 1G). If omitted, uses default.")
    
    args = parser.parse_args()

    process = get_sorted_stream(args.input_file, args.memory_limit)
    
    max_length = 0
    best_claim_id = None
    best_status_code = None

    for (claim_id, status_code), edges in generate_groups(process.stdout):
        cycle_len = find_longest_cycle(edges)
        if cycle_len > max_length:
            max_length = cycle_len
            best_claim_id = claim_id
            best_status_code = status_code

    process.wait()

    if best_claim_id is not None:
        print(f"{best_claim_id},{best_status_code},{max_length}")

if __name__ == "__main__":
    main()
