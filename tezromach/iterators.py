"""
Iterators for NeuralNet
"""
from typing import Iterator, NamedTuple

import numpy as np

from tezromach.tensor import Tensor

Batch = NamedTuple("Batch", [("inputs", Tensor), ("targets", Tensor)])


class DataIterator:
    def __call__(self, inputs: Tensor, targets: Tensor) -> Iterator[Batch]:
        raise NotImplementedError


class BatchIterator(DataIterator):
    def __init__(self, batch_size: int = 32, shuffle: bool = True) -> None:
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __call__(self, inputs: Tensor, targets: Tensor) -> Iterator[Batch]:
        starts = np.arange(0, len(inputs), self.batch_size)
        if self.shuffle:
            np.random.shuffle(starts)

        for start in starts:
            end = start + self.batch_size
            batch_inputs = inputs[start:end]
            batch_targets = targets[start:end]
            yield Batch(batch_inputs, batch_targets)


class DataSetIterator(DataIterator):
    def __init__(self, shuffle: bool = True) -> None:
        self.shuffle = shuffle

    def __call__(self, inputs: Tensor, targets: Tensor) -> Iterator[Batch]:
        if self.shuffle:
            shuffled_index = list(range(inputs.shape[0]))
            np.random.shuffle(shuffled_index)
            batch_inputs = inputs[shuffled_index]
            batch_targets = targets[shuffled_index]
        else:
            batch_inputs = inputs
            batch_targets = targets
        yield Batch(batch_inputs, batch_targets)
