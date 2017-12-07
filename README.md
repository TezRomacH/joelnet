### Simple neural network lib
Use layers with different *Activations*
```python
from tezromach.network import NeuralNet
from tezromach.layers import Linear, Sigmoid, Tanh

net = NeuralNet([
    Linear(input_size=2, output_size=2),
    Sigmoid(),
    Linear(input_size=2, output_size=3),
    Tanh(),
    Linear(input_size=3, output_size=1)
])

net.fit(X, targets, num_epochs=10000, learning_rate=0.02)
```