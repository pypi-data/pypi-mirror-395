from typing import Union

import numpy as np
import torch

from torchstream import Stream
from torchstream.sequence.sequence import Sequence
from torchstream.streams.stream_step import stream_step


def _pad(x: Union[np.ndarray, torch.Tensor], dim: int, pad: tuple, pad_mode: str):
    if pad == (0, 0):
        return x

    dim = (x.ndim + dim) % x.ndim
    if torch.is_tensor(x):
        paddings = tuple(list(pad) + [0] * ((x.ndim - dim - 1) * 2))
        return torch.nn.functional.pad(x, paddings, mode="constant" if pad_mode == "zeros" else pad_mode)
    else:
        paddings = [(0, 0)] * x.ndim
        paddings[dim] = pad
        return np.pad(x, paddings, mode=pad_mode)


class LeftRightPadStream(Stream):
    def __init__(self, pad: Union[tuple, int], pad_mode="constant", name=None):
        """
        TODO: doc
        """
        if isinstance(pad, tuple):
            self.pad = pad
        else:
            self.pad = (pad, pad)
        self.pad_mode = pad_mode

        self._left_pad_to_apply, self._right_pad_to_apply = self.pad

        super().__init__(self._apply_pad, name=name)

    @stream_step()
    def _apply_pad(self, buf: Sequence):
        left_pad = 0
        if self._left_pad_to_apply > 0:
            # Left padding is applied in one go on the first step
            # FIXME: holdback for reflect
            left_pad = self._left_pad_to_apply
            self._left_pad_to_apply = 0

        elif self._left_pad_to_apply < 0:
            # Left trimming drops inputs until the trim size has been reached
            drop_size = min(-self._left_pad_to_apply, buf.size)
            buf.drop(drop_size)
            self._left_pad_to_apply += drop_size

        right_pad = 0
        right_holdback = 0
        if self._right_pad_to_apply > 0 and buf.input_closed:
            # Right padding is applied in one go on the last step
            right_pad = self._right_pad_to_apply
            self._right_pad_to_apply = 0

        elif self._right_pad_to_apply < 0:
            # Right trimming keeps holding a fixed input size throughout the whole execution, and never yields it
            right_holdback = -self._right_pad_to_apply

        # Apply the holdback
        read_size = max(0, buf.size - right_holdback)
        x = buf.read(read_size)

        # To avoid keeping tensors in memory, we drop the holdback on the last step
        if buf.input_closed:
            buf.drop()

        return _pad(x, buf.dim, (left_pad, right_pad), self.pad_mode)
