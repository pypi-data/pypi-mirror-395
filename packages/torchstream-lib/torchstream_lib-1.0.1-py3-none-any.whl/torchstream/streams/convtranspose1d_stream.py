import torch
from torch.nn import ConvTranspose1d
from torch.nn import functional as F

from torchstream import Stream
from torchstream.sequence.sequence import Sequence
from torchstream.streams.left_right_pad_stream import LeftRightPadStream
from torchstream.streams.stream_step import stream_step


class ConvTranspose1DStream(Stream):
    # FIXME: follow exactly the torch signature
    def __init__(
        self,
        weight: torch.Tensor,
        bias: torch.Tensor = None,
        stride=1,
        padding=0,
        output_padding=0,
        groups=1,
        dilation=1,
    ):
        assert output_padding == 0, "Not implemented"
        assert dilation == 1, "Not implemented"
        assert padding >= 0, "Padding must be positive"

        self._weight = weight
        self._bias = bias
        self._kernel_size = self._weight.size(-1)
        self._stride = stride
        self._output_padding = output_padding
        self._groups = groups
        self._dilation = dilation

        self.upcoming_out_buff = None

        # On a 1D transposed convolution, padding amounts to trimming the output
        out_trim = LeftRightPadStream(-padding) if padding else None

        super().__init__((self._conv_step, out_trim))

    @classmethod
    def from_conv(cls, conv: ConvTranspose1d) -> "ConvTranspose1DStream":
        assert (
            len(conv.kernel_size) == 1 and len(conv.stride) == 1 and len(conv.padding) == 1 and len(conv.dilation) == 1
        ), "Not implemented"
        assert conv.padding_mode == "zeros", "Not implemented"

        return cls(
            weight=conv.weight.data,
            bias=conv.bias.data.view(1, -1, 1),
            stride=conv.stride[0],
            padding=conv.padding[0],
            output_padding=conv.output_padding[0],
            groups=conv.groups,
            dilation=conv.dilation[0],
        )

    # def _out_size(self, read: BufferRead) -> int:
    #     # How much stepping will generate
    #     n_out = read.size * self._stride
    #     if read.is_last_output:
    #         n_out += self._kernel_size - self._stride
    #     return max(n_out, 0)

    @stream_step(2, 2)
    def _conv_step(self, x_buf: Sequence) -> torch.Tensor:
        x = x_buf.read()

        # Get the output of the convolution
        conv_out = F.conv_transpose1d(
            # N.B.: we add the bias later to avoid adding multiple times on overlapping regions
            x,
            self._weight,
            bias=None,
            stride=self._stride,
            groups=self._groups,
            dilation=self._dilation,
            padding=0,
            output_padding=0,
        )

        # Sum the previously held output with this one to get the correct values
        if self.upcoming_out_buff is not None:
            assert conv_out.size(-1) > self.upcoming_out_buff.size(-1), "Internal error"
            conv_out[..., : self.upcoming_out_buff.size(-1)] += self.upcoming_out_buff

        # Yield good outputs, store the ones that still need to be added to upcoming outputs
        split_idx = conv_out.size(-1) if x_buf.output_closed else x.size(-1) * self._stride
        good_output = conv_out[..., :split_idx]
        if self._bias is not None:
            good_output = good_output + self._bias
        self.upcoming_out_buff = conv_out[..., split_idx:]

        return good_output
