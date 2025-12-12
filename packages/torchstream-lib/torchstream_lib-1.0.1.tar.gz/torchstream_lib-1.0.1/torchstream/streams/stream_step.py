from typing import Callable, Tuple, Union


_STREAM_STEP_ATTR = "_stream_step_meta"


class StreamStepMeta:
    def __init__(
        self,
        in_dims: Union[int, Tuple[int, ...], None]=None,
        out_dims: Union[int, Tuple[int, ...], None]=None,
        inputs_as_buffers: bool=True,
        force_same_size_inputs: bool=False
    ):
        self.in_dims = in_dims
        self.out_dims = out_dims
        self.inputs_as_buffers = inputs_as_buffers
        self.force_same_size_inputs = force_same_size_inputs


# Decorator
def stream_step(
    in_dims: Union[int, Tuple[int, ...], None]=None, out_dims: Union[int, Tuple[int, ...], None]=None,
    inputs_as_buffers: bool=True, force_same_size_inputs: bool=False
):
    def decorator(fn):
        setattr(fn, _STREAM_STEP_ATTR, StreamStepMeta(in_dims, out_dims, inputs_as_buffers, force_same_size_inputs))
        return fn
    return decorator


def has_stream_step_meta(fn: Callable):
    return hasattr(fn, _STREAM_STEP_ATTR)


def get_stream_step_meta(fn: Callable) -> StreamStepMeta:
    if has_stream_step_meta(fn):
        return getattr(fn, _STREAM_STEP_ATTR)
    else:
        return StreamStepMeta(
            in_dims=None,
            out_dims=None,
            inputs_as_buffers=False,
            force_same_size_inputs=True,
        )
