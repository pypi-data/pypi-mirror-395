import inspect
import logging
from typing import Union

import networkx as nx
import numpy as np
from torch import Tensor, nn

from torchstream.sequence.sequence import Sequence
from torchstream.streams.stream_step import StreamStepMeta, get_stream_step_meta
from torchstream.torch_primitives_definitions import get_torch_primitive_stream, has_torch_primitive_implementation

logger = logging.getLogger(__name__)


# def _get_max_out_sizes(self):
#     # FIXME: take into account closings
#     max_out_sizes = {}
#     for stream in self._resolution_order:
#         in_reads = []
#         # FIXME: order
#         for buffer in self.graph.predecessors(stream):
#             max_buf_read = buffer.get_max_read(stream)
#
#             try:
#                 buffer_input = next(self.graph.predecessors(buffer))
#                 extra_buf_size = max_out_sizes[buffer_input]
#                 max_buf_read = Read(max_buf_read.size + extra_buf_size, max_buf_read.with_close)
#             except StopIteration:
#                 pass
#
#             in_reads.append(max_buf_read)
#
#         max_out_sizes[stream] = stream.out_size(*in_reads)
#
#     return max_out_sizes


def _insert_name(graph: nx.DiGraph, new_name: str) -> str:
    assert not new_name[-1].isnumeric(), "Not implemented yet"

    parts = new_name.split(".")
    existing_keys = {tuple(k.split(".")[: len(parts)]) for k in graph}
    while len(parts) > 1:
        existing_keys = {k[1:] for k in existing_keys if k[0] == parts[0]}
        del parts[0]

    if not existing_keys:
        return new_name

    dupe_values = {
        int(numeric_part)
        for parts in existing_keys
        if (numeric_part := (parts[0].replace(new_name, "").replace("-", "") or "1")).isnumeric()
    }

    if dupe_values:
        return f"{new_name}-{max(dupe_values) + 1}"
    else:
        return new_name


def _connect_successors(nodes: tuple, successor, graph: nx.DiGraph):
    """
    Given a set of nodes and their successor, act the edge(s) to the graph and returns the leaf successor nodes.

    Responsibilities of this function:
        - Walk a complex graph of composite objects to yield nodes and connections
        - Uniquely name nodes
    """
    # The successor equates to False (typically None or an empty tuple): shorthand for identity, the current nodes are
    # the leaf successors
    if not successor:
        return nodes

    # Lists equate to forking the output of the nodes.
    #   - Act an edge to every item in the list
    #   - The resulting set of leaf nodes is the concatenation of the leaf nodes of all items in the list
    elif isinstance(successor, list):
        leafs = []
        for successor_i in successor:
            leaf_i = _connect_successors(nodes, successor_i, graph)
            leafs.extend(leaf_i)
        return tuple(leafs)

    # Nodes in a tuple are executed in a sequence, one feeding into the next. The leaf of the last item is the leaf
    # of the entire tuple.
    elif isinstance(successor, tuple):
        for successor_i in successor:
            nodes = _connect_successors(nodes, successor_i, graph)
        return nodes

    # A stream is another graph, so it's swallowed into this one. The leaf nodes are the output nodes of the graph.
    elif isinstance(successor, Stream):
        prefix = _insert_name(graph, name_of(successor))

        # Include all nodes of the Stream with a prefix
        for subnode_name, subnode_data in successor.graph.nodes(data=True):
            if subnode_name in ("in", "out"):
                continue
            graph.add_node(f"{prefix}.{subnode_name}", **subnode_data)

        # Bridge connection between predecessors and the entrypoint of the graph
        for entry_subnode in successor.graph.succ["in"]:
            for node_name in nodes:
                # FIXME!! multiple outputs
                input_idx = [graph.in_degree(f"{prefix}.{entry_subnode}")]
                graph.add_edge(node_name, f"{prefix}.{entry_subnode}", input_idx=input_idx)

        # Include all connections from the stream graph
        for subnode, subnode_succ, edge_data in successor.graph.edges(data=True):
            if subnode not in ("in", "out") and subnode_succ not in ("in", "out"):
                graph.add_edge(f"{prefix}.{subnode}", f"{prefix}.{subnode_succ}", **edge_data)

        # The exit nodes of the Stream are returned
        return tuple([f"{prefix}.{out_subnode}" for out_subnode in successor.graph.pred["out"]])

    # TODO: interface?
    elif hasattr(successor, "get_stream_graph"):
        successor = successor.get_stream_graph()  # , *args, **kwargs) FIXME
        return _connect_successors(nodes, successor, graph)

    elif isinstance(successor, nn.Module):
        if has_torch_primitive_implementation(successor):
            successor = get_torch_primitive_stream(successor)  # , *args, **kwargs) FIXME
            return _connect_successors(nodes, successor, graph)
        else:
            raise "TODO"  # FIXME

    # if isinstance(obj, nn.Module):
    #     raise TypeError(
    #         f"Cannot obtain a stream from {obj.__class__.__name__} module. Either it is not a (yet) supported torch "
    #         f"layer, or it is a custom module for which you didn't implement a get_stream_graph() method."
    #     )
    # else:
    #     raise TypeError(
    #         f"Cannot obtain a stream from {obj.__class__.__name__} object. Maybe you forgot to implement a "
    #         f"get_stream_graph() method?"
    #     )

    else:
        # We should be left with a callable object, except for "out"
        # FIXME (?): dangerous, leads to a normal module being considered a stream
        # FIXME (?): stream step meta check higher

        node_name = _insert_name(graph, name_of(successor))
        graph.add_node(node_name, stream_step=successor if successor != "out" else None)

        for node_name in nodes:
            # FIXME!! multiple outputs
            input_idx = [graph.in_degree(node_name)]
            graph.add_edge(node_name, node_name, input_idx=input_idx)

        return (node_name,)


def name_of(var):
    if isinstance(var, str):
        return var
    if inspect.ismethod(var):
        var = var.__func__
    return var.__name__ if hasattr(var, "__name__") else var.__class__.__name__


def to_streamstep_graph(raw_graph) -> (nx.DiGraph, List):
    # Parse the raw graph in a DiGraph
    graph = nx.DiGraph()
    graph.add_node("in", stream_step=None)
    _connect_successors(nodes=("in",), successor=(raw_graph, "out"), graph=graph)

    # Check for cycles
    # TODO: use nx.find_cycles
    # TODO: check that all are connected
    # TODO: proper exception
    assert nx.is_weakly_connected(graph), "Graph is not connected"

    for node_name, data in graph.nodes(data=True):
        assert "stream_step" in data

        if "stream_step_meta" not in data:
            # FIXME
            if node_name == "out" or node_name == "in":
                data["stream_step_meta"] = StreamStepMeta(inputs_as_buffers=False, force_same_size_inputs=False)
            else:
                data["stream_step_meta"] = get_stream_step_meta(data["stream_step"])

        if "in_buffs" not in data:
            data["in_buffs"] = []

    return graph


class Stream:
    def __init__(self, graph, name: str = None):
        self.n_steps = 0
        self._name = name

        self.graph = to_streamstep_graph(graph)
        print(nx.write_network_text(self.graph))

        # TODO
        # infer_and_assign_dimensions(self.graph)
        for node, data in self.graph.nodes(data=True):
            if node != "in":
                data["in_buffs"] = [
                    # FIXME: dimension & output size
                    Sequence(dim=2)
                    for _ in self.graph.predecessors(node)
                ]

    # @property
    # def input_closed(self) -> bool:
    #     return all(in_buf.input_closed for in_buf in self.in_buffers)
    #
    # @property
    # def running(self) -> bool:
    #     """
    #     Returns whether this stream can still take or output more data
    #     """
    #     return (not self.input_closed) or self.can_step()
    #
    # def can_step(self) -> bool:
    #     """
    #     If this is False, calling step() will have undefined behaviour
    #     """
    #     return self.out_size() != 0

    # TODO: allow passing buffers as well
    def __call__(self, *inputs: Union[Tensor, np.ndarray], is_last_input=False):
        # FIXME: size, type, number checks
        print("\n\n\n")

        # Execute each node in the graph in the order the user has given
        for node, step_data in self.graph.nodes(data=True):
            if node == "in":
                outputs, is_last_output = inputs, is_last_input
            else:
                print(f"Node: {node}")

                # Forward the inputs to the node
                # Inputs are to be given as buffers
                if step_data["stream_step_meta"].inputs_as_buffers:
                    shapes = [tuple(buf.peek().shape) for buf in step_data["in_buffs"]]
                    print(f"\tIn:   {', '.join(str(s) for s in shapes)}")
                    inputs = step_data["in_buffs"]

                # Inputs are to be given as is (tensors, arrays, ...)
                else:
                    if step_data["stream_step_meta"].force_same_size_inputs:
                        size = min(buf.size for buf in step_data["in_buffs"])
                        inputs = tuple(buf.read(size) for buf in step_data["in_buffs"])
                    else:
                        inputs = tuple(buf.read() for buf in step_data["in_buffs"])
                    shapes = [tuple(i.shape) for i in inputs]
                    print(f"\tIn:   {', '.join(str(s) for s in shapes)}")

                if node == "out":
                    self.n_steps += 1
                    return inputs

                outputs = step_data["stream_step"](*inputs)
                # FIXME!
                is_last_output = is_last_input

            if not isinstance(outputs, tuple):
                outputs = (outputs,)
            print("\tOut: ", ", ".join(str(tuple(o.shape)) for o in outputs))

            # Store output as input to the successors of this node
            for _, succ, edge_data in self.graph.edges(node, data=True):
                input_idx = edge_data["input_idx"]
                assert len(input_idx) == len(outputs)

                for input_idx_i, output_i in zip(input_idx, outputs):
                    buffer = self.graph.nodes[succ]["in_buffs"][input_idx_i]
                    print(f"\tFeed: {tuple(output_i.shape)} ({'?' if buffer._buff is None else buffer._buff.shape})")
                    buffer.feed(output_i, close_input=is_last_output)

        raise RuntimeError()

    # def _step(self, out_size: Optional[int]):
    #     # Determine the output size needed for each layer
    #     out_sizes = [out_size]
    #     max_out_sizes = self._max_out_sizes(0, False)
    #     for stream_idx in range(len(self.streams) - 1, 0, -1):  # Iterates backwards and skips the very first stream
    #         stream = self.streams[stream_idx]
    #
    #         # Different gotchas:
    #         #   - the current stream doesn't know how much it will ouput, so no output constraint on the previous one
    #         #   - the current stream has its input closed, so the previous one must ouput nothing
    #         #   - we can't tell yet whether streams will close in this pass, if they do they might output more data
    #         #       for a smaller input size. <self._max_out_sizes> does make this assumption, therefore it is the
    #         #       upper bound for the output sizes.
    #         if out_sizes[0] is None:
    #             prev_out_size = None
    #         else:
    #             prev_out_size = 0 if stream.input_closed else stream.in_needed(out_sizes[0])
    #             if max_out_sizes[stream_idx - 1] is not None:
    #                 prev_out_size = min(max_out_sizes[stream_idx - 1], prev_out_size)
    #
    #         out_sizes.insert(0, prev_out_size)
    #
    #     out = None
    #     prev_stream = None
    #     out_sizes_iter = iter(out_sizes)
    #     for stream_or_fn in self.streams_or_fns[self._first_stream_idx:]:
    #         if isinstance(stream_or_fn, Stream):
    #             # Feed the previous output
    #             if prev_stream is not None:
    #                 stream_or_fn.feed(
    #                     *(out if isinstance(out, tuple) else (out,)),
    #                     close_input=not prev_stream.running
    #                 )
    #
    #             # Step with this stream
    #             out_size = next(out_sizes_iter)
    #             if stream_or_fn.running and (out_size is None or out_size > 0):
    #                 # Verify that we can actually output what was requested
    #                 if out_size is not None and not any(m is None for m in max_out_sizes):
    #                     assert stream_or_fn.max_out_size() >= out_size, \
    #                         f"Internal error: stream {stream_or_fn.name} can only output " \
    #                         f"size {stream_or_fn.max_out_size()}, but size {out_size} was requested. " \
    #                         f"Previous input: {out}, " \
    #                         f"Previous stream: {'None' if prev_stream is None else prev_stream.name}"
    #
    #                 out = stream_or_fn.step(out_size)
    #                 prev_stream = stream_or_fn
    #
    #         elif out is not None:
    #             # Apply the function
    #             # N.B.: the case where out is None is when the previous stream has finished execution. It is thus
    #             # safe to skip the function execution, the next stream that can generate an output will do so.
    #             out = stream_or_fn(*(out if isinstance(out, tuple) else (out,)))
    #
    #     return out
    #
    # # TODO: output tuples
    # @overload
    # def out_size(self, in_size: int, is_last_input=False) -> int: ...
    # @overload
    # def out_size(self, *reads: BufferRead) -> int: ...
    # def out_size(self, *args, **kwargs) -> int:
    #     """
    #     Given an input buffer of size <in_size>, returns the size of the output that will be produced by this step
    #     in its current state. Because some steps may behave differently depending on whether the input is the last,
    #     this function also takes a boolean <is_last_input> as input.
    #
    #     # TODO: explain the case for streams where in-out relations are not possible
    #
    #     # FIXME: explain the relation with stepping
    #     """
    #     # Resolve args
    #     if args and isinstance(args[0], tuple):
    #         assert not kwargs
    #         reads = args
    #     else:
    #         if "in_size" in kwargs:
    #             args = (kwargs["in_size"],)
    #         if len(args) == 1:
    #             args += (kwargs.get("is_last_input", False),)
    #         reads = [BufferRead(*args)]
    #
    #     # Compute the output size
    #     out_size = self._out_size(*reads)
    #     assert out_size >= 0, f"_out_size must return a positive integer, got out_size={out_size} for {self.name}"
    #
    #     return out_size
    #
    # # TODO: give buffers as inputs instead?
    # def _out_size(self, *reads) -> Union[int, Tuple]:
    #     """
    #     Must implement the behaviour of out_size() documented above.
    #     """
    #     raise NotImplementedError()

    # def in_needed(self, out_size: int) -> int:
    #     """
    #     This function is the inverse of out_size(). It returns the minimum size of input needed to obtain an
    #     output that is at least of size <out_size>.
    #     """
    #     if self.out_size(0, is_last_input=self.output_closed) >= out_size:
    #         return 0
    #
    #     in_size_to_out_size = lambda n: self.out_size(*self.in_buffer.get_read(n))
    #     if self.input_closed and in_size_to_out_size(None) < out_size:
    #         pass
    #
    #     # Find an initial range for binary search
    #     right = 1
    #     while in_size_to_out_size(right) < out_size:
    #         right *= 10
    #     left = right // 10
    #
    #     # Perform the binary search
    #     in_size = left + bisect_left(range(left, right), out_size, key=in_size_to_out_size)
    #
    #     return in_size

    @property
    def name(self) -> str:
        return self._name or self.__class__.__name__

    def __repr__(self):
        return self.name


def get_stream(obj, *args, **kwargs) -> Stream:
    return Stream(obj, name=obj.__class__.__name__)
    # graph, nodes = to_streamstep_graph(obj)
    # _draw_graph(graph)
    # quit()
