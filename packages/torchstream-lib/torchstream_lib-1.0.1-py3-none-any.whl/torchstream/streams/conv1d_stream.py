import torch
from torch.nn import Conv1d
from torch.nn import functional as F

from torchstream import Stream
from torchstream.sequence.sequence import Sequence
from torchstream.streams.sliding_window_stream import SlidingWindowStream
from torchstream.streams.stream_step import stream_step


class Conv1DStream(Stream):
    def __init__(
        self,
        weight: torch.Tensor,
        bias: torch.Tensor = None,
        stride=1,
        dilation=1,
        padding=(0, 0),
        groups=1,
        padding_mode="zeros",
        name: str = None,
    ):
        assert weight.ndim == 3, "Not implemented"

        self.weight = weight
        self.bias = bias
        self.stride = stride
        self.dilation = dilation
        self.groups = groups

        # F.conv1d has an optimization for padding with zeroes. See step() to see how we use it.
        if not isinstance(padding, tuple):
            padding = (padding, padding)
        self._optimize_padding = padding_mode == "zeros" and padding[0] == padding[1]
        # FIXME: re-enable once comfortable enough
        self._optimize_padding = False
        self._padding = padding[0] if self._optimize_padding else None

        self.kernel_size = weight.size(2)
        rfield = self.kernel_size + (self.kernel_size - 1) * (dilation - 1)
        self._sli_win = SlidingWindowStream(
            # FIXME: pad_mode/padding_mode name
            #   same with pad
            win_size=rfield,
            stride=stride,
            pad=(0 if self._optimize_padding else padding),
            pad_mode=padding_mode,
        )

        super().__init__((self._sli_win, self._conv_step), name or "Conv1D")

    @classmethod
    def from_conv(cls, conv: Conv1d) -> "Conv1DStream":
        # FIXME!
        assert conv.padding_mode == "zeros", "Not implemented"
        assert (
            len(conv.kernel_size) == 1 and len(conv.stride) == 1 and len(conv.padding) == 1 and len(conv.dilation) == 1
        ), "Not implemented"

        return Conv1DStream(
            weight=conv.weight.data,
            bias=conv.bias.data,
            stride=conv.stride[0],
            dilation=conv.dilation[0],
            padding=conv.padding[0],
            groups=conv.groups,
            padding_mode=conv.padding_mode,
        )

    # def _out_size(self, x_read: BufferRead) -> Union[int, Tuple]:
    #     return self._win_view.out_n_wins(x_read)

    @stream_step(2, 2)
    def _conv_step(self, x_buf: Sequence):
        x = x_buf.read()

        if x.size(2) < self.kernel_size:
            return x.new_empty(x.size(0), self.weight.shape[0], 0)

        # In general, we do the padding manually (self._sli_win applies it). But if F.conv1d can handle the padding for
        # us, we let it do so because it is faster. Even if only the left or the right side needs the padding, it's
        # preferable to make the call and trim the output after.
        if self._optimize_padding:
            do_left_pad = self._padding and self.n_steps == 0
            do_right_pad = self._padding and x_buf.output_closed
            padding = self._padding if (do_left_pad or do_right_pad) else 0
        else:
            do_left_pad, do_right_pad = False, False
            padding = 0

        x = F.conv1d(x, self.weight, self.bias, self.stride, padding, self.dilation, self.groups)

        # FIXME: isn't this broken with stride > 1?
        if not do_left_pad and do_right_pad:
            x = x[..., self._padding :]
        if do_left_pad and not do_right_pad:
            x = x[..., : -self._padding]

        return x
