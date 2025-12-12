from graphviz import Digraph
import pickle

def trace(root):
    nodes = set()
    edges = set()

    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    
    build(root)
    return nodes, edges

def draw_graph(root, format = 'svg'):
    nodes, edges = trace(root)
    dot = Digraph(format = format, graph_attr = {'rankdir': 'LR'})
    
    for n in nodes:
        uid = str(id(n))
        label = f"{n._op} | val = {n.data:.4f} | grad = {n.grad:.4f}"
        dot.node(name = uid, label = label, shape = 'record')

    for child, parent in edges:
        dot.edge(str(id(child)), str(id(parent)))

    return dot

def save_graph(root, path):

    def strip_backward(v, visited):
        if v in visited:
            return
        visited.add(v)
        v._backward = None

        for child in v._prev:
            strip_backward(child, visited)

    strip_backward(root, set())

    with open(path, 'wb') as f:
        pickle.dump(root, f)

def load_graph(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def render_graph(root, filename = 'graph', view = True, format = 'svg'):
    dot = draw_graph(root, format = format)
    dot.render(filename = filename, view = view)
    return filename + '.' + format