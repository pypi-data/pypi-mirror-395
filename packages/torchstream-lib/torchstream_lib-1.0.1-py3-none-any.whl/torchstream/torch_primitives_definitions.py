from torch import nn
from torch.nn import Conv1d, ConvTranspose1d
import importlib


DEFINITIONS = {
    Conv1d: ("conv1d_stream", "Conv1DStream.from_conv"),
    ConvTranspose1d: ("convtranspose1d_stream", "ConvTranspose1DStream.from_conv"),
}


def has_torch_primitive_implementation(mod: nn.Module):
    return type(mod) in DEFINITIONS


def get_torch_primitive_stream(mod: nn.Module, *args, **kwargs):
    mod_fname, fn_name = DEFINITIONS[type(mod)]

    inst_fn = importlib.import_module(f"torchstream.streams.{mod_fname}")
    for qual_name in fn_name.split("."):
        inst_fn = getattr(inst_fn, qual_name)

    stream = inst_fn(mod, *args, **kwargs)

    return stream
