""" 
Layers:
* Linear
* Tanh Activation
* Sigmoid Activation
"""
from typing import Dict, Callable

import numpy as np
from tezromach.tensor import Tensor


class Layer:
    def __init__(self) -> None:
        self.params: Dict[str, Tensor] = {}
        self.grads: Dict[str, Tensor] = {}

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Produce the outputs corresponding to these inputs
        """
        raise NotImplementedError

    def backward(self, grad: Tensor) -> Tensor:
        """
        Backpropagate this gradient through the layer
        """
        raise NotImplementedError


class Linear(Layer):
    """
    computes output = inputs @ w + b
    """

    def __init__(self, input_size: int, output_size: int) -> None:
        # inputs will be (batch_size, input_size)
        # outputs will be (batch_size, output_size)
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.params["w"] = np.random.randn(input_size, output_size)
        self.params["b"] = np.random.randn(output_size)
        self.inputs: Tensor = []

    def forward(self, inputs: Tensor) -> Tensor:
        """
        outputs = inputs @ w + b
        """
        self.inputs = inputs
        return inputs @ self.params["w"] + self.params["b"]

    def backward(self, grad: Tensor) -> Tensor:
        """
        if y = f(x) and x = a * b + c
        then dy/da = f'(x) * b
        and dy/db = f'(x) * a
        and dy/dc = f'(x)

        if y = f(x) and x = a @ b + c
        then dy/da = f'(x) @ b.T
        and dy/db = a.T @ f'(x)
        and dy/dc = f'(x)
        """
        self.grads["b"] = np.sum(grad, axis=0)
        self.grads["w"] = self.inputs.T @ grad
        return grad @ self.params["w"].T


F = Callable[[Tensor], Tensor]


class Activation(Layer):
    """
    An activation layer just applies a function
    elementwise to its inputs
    """

    def __init__(self, f: F, f_deriv: F) -> None:
        super().__init__()
        self.f = f
        self.f_deriv = f_deriv
        self.inputs: Tensor = []

    def forward(self, inputs: Tensor) -> Tensor:
        self.inputs = inputs
        return self.f(inputs)

    def backward(self, grad: Tensor) -> Tensor:
        """
        if y = f(x) and x = g(z)
        then dy/dz = f'(x) * g'(z)
        """
        return self.f_deriv(self.inputs) * grad


def tanh(x: Tensor) -> Tensor:
    return np.tanh(x)


def tanh_deriv(x: Tensor) -> Tensor:
    y = tanh(x)
    return 1 - y ** 2


class Tanh(Activation):
    def __init__(self):
        super().__init__(tanh, tanh_deriv)


def sigmoid(x: Tensor) -> Tensor:
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid_deriv(x: Tensor) -> Tensor:
    y = sigmoid(x)
    return y * (1 - y)


class Sigmoid(Activation):
    def __init__(self):
        super().__init__(sigmoid, sigmoid_deriv)
