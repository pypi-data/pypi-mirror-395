from typing import Tuple, Optional, List

import networkx as nx


def _draw_graph(graph):
    import matplotlib.pyplot as plt

    for layer, nodes in enumerate(nx.topological_generations(graph)):
        for node in nodes:
            graph.nodes[node]["layer"] = layer

    pos = nx.multipartite_layout(graph, subset_key="layer")

    fig, ax = plt.subplots()
    nx.draw_networkx(graph, pos=pos, ax=ax)
    ax.set_title("DAG layout in topological order")
    fig.tight_layout()
    plt.savefig("a.png")
    plt.show()


def _walk_tuple_list_graph(predecessors: tuple, node, conns):
    if isinstance(node, list):
        predecessors = [_walk_tuple_list_graph(predecessors, subnode, conns) for subnode in node]
        return tuple([c for b in predecessors for c in b])

    elif isinstance(node, tuple):
        # Shorthand for the identity
        if not node:
            return predecessors

        for subnode in node:
            predecessors = _walk_tuple_list_graph(predecessors, subnode, conns)
        return predecessors

    else:
        conns.append((predecessors, node))
        return (node,)


def tuple_list_graph_to_graph(graph) -> (nx.DiGraph, List):
    # Build the edge list
    edges = []
    _walk_tuple_list_graph(predecessors=("in",), node=(graph, "out"), conns=edges)

    # Create the DAG
    graph = nx.DiGraph()
    graph_sort = ["in"]
    for predecessors, node in edges:
        graph_sort.append(node)
        for predecessor in predecessors:
            graph.add_edge(predecessor, node)

    return graph, graph_sort


# TODO: LRU cache?
def _aligment_solver_dp(in_dims: Tuple[Optional[int], ...], expected_dims: Tuple[int, ...]):
    """
    Generic alignment solver.

    Doesn't exploit the structure of the problem. Considering the input sizes are almost always very small, the
    runtime remains negligible.

    >>> _aligment_solver_dp((None, None, 2, 1, None), (1, 1, 2, 1, 2, 1, 1))
    >>> [
    >>>     [(1,), (1,), 2, 1, (2, 1, 1)],
    >>>     [(1,), (1, 2, 1), 2, 1, (1,)],
    >>>     [(1, 1), (2, 1), 2, 1, (1,)],
    >>>     [(1, 1, 2), (1,), 2, 1, (1,)],
    >>> ]

    :param in_dims: incoming dimensions with None for wildcards e.g. (None, None, 2, 1, None)
    :param expected_dims: expected dimensions e.g. (1, 1, 2, 1, 2, 1, 1)
    :return: a list of solutions where each entry is a list of either:
        - an integer to designate the same integer in <in_dims>
        - a tuple of integers to designate the replacement of the same wildcard in <in_dims>
    """
    mem = [[[] for _ in range(len(expected_dims) + 1)] for _ in range(len(in_dims) + 1)]
    mem[0][0] = [[]]

    for i in range(1, len(in_dims) + 1):
        for j in range(1, len(expected_dims) + 1):
            if in_dims[i - 1] is None:
                for k in range(j):
                    for solution in mem[i - 1][k]:
                        mem[i][j].append(solution + [expected_dims[k:j]])
            elif i <= j and in_dims[i - 1] == expected_dims[j - 1]:
                for solution in mem[i - 1][j - 1]:
                    mem[i][j].append(solution + [in_dims[i - 1]])

    return mem[len(in_dims)][len(expected_dims)]


def _formulate_constraints(split_dims, merged_dims):
    """
    Yields all possible configurations of split_dims such that they can be concatenated to be equal to <merged_dims>

    :param split_dims: list of either None or tuple of ints. None implies a variable, while a tuple of ints is a
    known sequence of dimensions.
    :param merged_dims: known sequence of dimensions
    """
    # Flatten the dims
    split_dims = [d for dims in split_dims for d in (dims or (None,))]

    # Find solutions that will be formulated as new constraints
    constraints = _aligment_solver_dp(split_dims, merged_dims)

    # Discard the known dimensions
    constraints = [[c for c in constraint if isinstance(c, tuple)] for constraint in constraints]

    return constraints


def _backtrack(constraints, assignment):
    if not constraints:
        return [assignment]

    out = []
    targets, subconstraints = constraints[0]
    for constraint in subconstraints:
        new_assignment = assignment.copy()

        compatible = True
        for target, new_value in zip(targets, constraint):
            if new_assignment.setdefault(target, new_value) != new_value:
                compatible = False
                break

        if compatible:
            out.extend(_backtrack(constraints[1:], new_assignment))

    return out


def infer_dimensions(graph):
    """
    Infers unknowns out_dims in the graph by formulating the problem as a CSP.

    :return: a tuple:
        - assignments: the list of all possible output dimensions for nodes for which solutions could be found.
        Not all nodes with unknown output dimensions will necessarily be listed in the output. If there is a single
        element in the list, the solution is unique.
        - inconsistency_detected: True if abberrant dimensions were detected. This allows for disambiguating cases where
        <assigments> is empty. This value being False does NOT imply that the graph is consistent.
    """
    # Set the constraints on the unknowns
    constraints = []
    for node in graph:
        if node.in_dims is not None:
            predecessors = list(graph.pred[node])
            split_dims = [p.out_dims for p in predecessors]
            if not any(d is None for d in split_dims):
                continue
            possibilities = _formulate_constraints(split_dims, node.in_dims)
            constraints.append((predecessors, possibilities))

    # Solve for the constraints
    assignments =_backtrack(constraints, {})
    inconsistency_detected = not len(assignments) and len(constraints)
    return assignments, inconsistency_detected


def infer_and_assign_dimensions(graph):
    """
    Infers missing dimensions in the graph by formulating the problem as a CSP. Assigns in_dims and out_dims to nodes
    for which a unique solution could be found.
    """
    all_assignments, inconsistency_detected = infer_dimensions(graph)
    # TODO: better error message
    assert not inconsistency_detected

    if all_assignments:
        # In case of multiple possible solutions, we only select the assignments that are common across all solutions
        # and ignore the others
        assignments = {
            k: dims for k, dims in all_assignments[0].items()
            if all(assignments_i[k] == dims for assignments_i in all_assignments[1:])
        }

        # Assign the inferred output dimensions
        for node, dims in assignments.items():
            node.out_dims = dims

    # The inference only targets the output dimensions of given nodes because it is trivial to derive input
    # dimensions. We do this here.
    for node in graph:
        in_dims = [p.out_dims for p in graph.pred[node]]
        if in_dims and not any(d is None for d in in_dims):
            node.in_dims = [d for dims in in_dims for d in dims]
