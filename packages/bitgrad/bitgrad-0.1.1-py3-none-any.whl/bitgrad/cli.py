import argparse
from bitgrad import MLP, Value
from bitgrad.viz import render_graph, load_graph

def main():
    parser = argparse.ArgumentParser(
        prog = "bitgrad",
        description = "Command-line interface for the Bitgrad engine"
    )

    parser.add_argument(
        "command",
        help = "Command to run xor / viz"
    )

    parser.add_argument(
        '--file',
        '-f',
        help = "Path to saved graph file (for viz)"
    )

    args = parser.parse_args()

    if args.command == 'xor':
        run_xor()
    
    elif args.command == 'viz':
        if args.file is None:
            print('Please provide --file path to a saved Value object')
            return
        visualize(args.file)

    else:
        print(f"Unknown command: {args.command}")

def run_xor():
    print('Runnning xor demo using Bitgrad MLP...')

    model = MLP(2, [4, 4, 1])
    data = [[0, 0], [0, 1], [1, 0], [1, 1]]

    print('\nPredictions:')
    for x in data:
        out = model(x)[0].data
        print(f"    Input {x} -> Output {out:.4f}")

def visualize(path):
    print(f'Loading saved graph from: {path}')
    
    try:
        root = load_graph(path)
    except Exception as e:
        print(f"Error loading graph: {e}")
        return

    print('Loading computational graph...')
    output = render_graph(root, filename = 'bitgrad_graph', view = True)

    print(f"Graph saved to: {output}")