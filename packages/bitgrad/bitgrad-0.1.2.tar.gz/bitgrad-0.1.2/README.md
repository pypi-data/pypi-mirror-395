BITGRAD:
A small autograd engine + neural network + visualization library
Bitgrad is a minimal neural network built from scratch in Python

Key Features:
> Value Class with reverse-mode autodiff
> Neurons, Layers and MLPs
> Graph Visualization (SVG)
> Structured project files and directories + packaging

INSTALLATION

Install from PyPI:
```bash
pip install bitgrad
```

Or install from source:
```bash
git clone https://github.com/falloficarus22/bitgrad
cd bitgrad
pip install -e .
```

Example Usage:
```python
from bitgrad import MLP, Value

# A simple 2 → 4 → 4 → 1 network
model = MLP(2, [4, 4, 1])

xs = [[2.0, 3.0], [1.0, -1.0], [-3.0, 0.5]]
ys = [1.0, -1.0, 1.0]

for k in range(200):
    ypred = [model(x)[0] for x in xs]
    loss = sum((yp - y)**2 for yp, y in zip(ypred, ys))

    # zero grads
    for p in model.parameters():
        p.grad = 0.0
    
    # backprop
    loss.backward()

    # SGD update
    for p in model.parameters():
        p.data -= 0.05 * p.grad

print("Final loss:", loss.data)
```

GRAPH VISUALIZATION

Bitgrad includes computational graph visualizer usin Graphviz

Saving a graph:
```python
from bitgrad.viz import save_graph

save_graph(loss, "loss.pkl")
```
Rendering it:
```bash
bitgrad viz --file loss.pkl
bitgrad viz -f loss.pkl
```

COMMAND LINE INTERFACE

Bitgrad installs a CLI called bitgrad

XOR Demo:
```bash
bitgrad xor
```
