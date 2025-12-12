import networkx as nx

from torchstream.transforms.graphs import infer_dimensions
from torchstream.transforms.node import Node


def test_complex_inference():
    fn1 = Node(lambda a: a)
    fn2 = Node(lambda b: b)
    fn3 = Node(lambda c: (c, c[None, ...]))
    fn4 = Node(lambda c, d: None)
    fn5 = Node(lambda e: e)
    stream1 = Node(
        lambda a, b, c, d: None,
        (0, 1, 2, 3),
        (0,)
    )
    stream2 = Node(
        lambda c, d, e: None,
        (2, 3, 0),
        (0,)
    )

    graph = nx.DiGraph()
    graph.add_edge(fn1, stream1)
    graph.add_edge(fn2, stream1)
    graph.add_edge(fn3, stream1)
    graph.add_edge(fn3, fn4)
    graph.add_edge(fn3, stream2)
    graph.add_edge(fn5, stream2)

    inferred_shapes, inconsistency_detected = infer_dimensions(graph)
    assert not inconsistency_detected
    assert len(inferred_shapes) == 1
    inferred_shapes = inferred_shapes[0]

    assert inferred_shapes[fn1] == (0,)
    assert inferred_shapes[fn2] == (1,)
    assert inferred_shapes[fn3] == (2, 3)
    assert not fn4 in inferred_shapes
    assert inferred_shapes[fn5] == (0,)


def test_inconsistent_graph_no_unknowns():
    """
    On a graph with incompatible shape assigments, the inference doesn't fail and returns an empty solution. No
    inconsistency is detected however because there are no unknowns.
    """
    fn1 = Node(lambda a: a, (0,), (0,))
    fn2 = Node(lambda b: b, (1,), (1,))

    graph = nx.DiGraph()
    graph.add_edge(fn1, fn2)

    inferred_shapes, inconsistency_detected = infer_dimensions(graph)
    assert not inconsistency_detected
    assert len(inferred_shapes) == 1
    assert not inferred_shapes[0]


def test_inconsistent_graph_with_unknowns():
    """
    On a graph with shape assigments where unknowns cannot resolve into a correct solution, the algo returns an empty
    list
    """
    fn1 = Node(lambda a: a)
    fn2 = Node(lambda a: a, (0,), (0,))
    fn3 = Node(lambda a: a, (1,), (1,))

    graph = nx.DiGraph()
    graph.add_edge(fn1, fn2)
    graph.add_edge(fn1, fn3)

    inferred_shapes, inconsistency_detected = infer_dimensions(graph)
    assert inconsistency_detected
    assert len(inferred_shapes) == 0


def test_ambiguous_shapes():
    """
    On a graph with multiple shape assignments possible, the function returns them all
    """
    fn1 = Node(lambda a: a)
    fn2 = Node(lambda b: b)
    fn3 = Node(lambda x, y, z: None, (0, 1, 2,), (-1,))

    graph = nx.DiGraph()
    graph.add_edge(fn1, fn3)
    graph.add_edge(fn2, fn3)

    inferred_shapes, inconsistency_detected = infer_dimensions(graph)
    assert not inconsistency_detected
    assert len(inferred_shapes) == 2
