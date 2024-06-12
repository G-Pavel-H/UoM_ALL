import sys
# To run the code: python3 myprogram.py input.txt output.txt
# If output.txt already exists it will be overwritten.

# Define the maximum number of colours
MAX_COLOURS = 26

# Function to read the interference graph from a file
def read_graph(filename):
    graph = {}
    with open(filename, 'r') as f:
        inp = f.read().split("\n")
        for line in inp:
            if line:
                parts = list(line.split(" "))
                # print(parts)
                node = int(parts[0])
                neighbours = [int(x) for x in parts[1:]]
                graph[node] = neighbours
    # print(graph)
    return graph

# Function to write the colouring to a file
def write_colouring(filename, colouring):
    with open(filename, 'w') as f:
        for node in sorted(colouring.keys()):
            f.write(f"{node}{colouring[node]}\n")

# Function to apply the top-down colouring algorithm
def top_down_colouring(graph):
    # Initialize the colouring
    colouring = {}
    # Initialize the list of available colours
    available_colours = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:MAX_COLOURS]
    # Sort the nodes by degree (number of neighbours)
    node_ranks = sorted(graph.keys(), key=lambda n: (-len(graph[n]), n))
    # print(node_ranks)

    # Assign colours to each node
    for node in node_ranks:
        # Find the colours used by the node's neighbours
        neighbour_colours = set(colouring.get(neighbour) for neighbour in graph[node])
        # Find the first available colour
        for colour in available_colours:
            if colour not in neighbour_colours:
                colouring[node] = colour
                break
        # If no colour is available, give up and return None
        else:
            return None
    
    # print(colouring)

    # If all nodes are coloured, return the colouring
    return colouring

def main(input_file, output_file):
    # Read input file and colour nodes.
    try:
        graph = read_graph(input_file)
        node_colours = top_down_colouring(graph)

        # Check for errors.
        if node_colours is None:
            print("Error: could not colour nodes with 26 colours or less.")
            return

        # Write output file.
        write_colouring(output_file, node_colours)
        print("Done... \nCheck the output file!")

    except FileNotFoundError:
        print("File doesn't exist, please make sure it is in the same directory or give the full path.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python myprogram.py input_file output_file")
    else:
        main(sys.argv[1], sys.argv[2])

