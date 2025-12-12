import pandas as pd


def graph_density(graph, loops=False) -> float:
    """
    Calculate the density of the graph.

    The density of a graph is the ratio of the number of edges to the number of possible edges.
    For undirected graphs without loops, it is calculated as:
        Density = 2 * |E| / (|V| * (|V| - 1))
    For directed graphs or graphs with loops, the calculation adjusts accordingly.

    Parameters:
        graph (igraph.Graph):
            The input graph for which density is to be calculated.
        loops (bool, optional):
            If True, loops are considered in the density calculation.
            Defaults to False.

    Returns:
        float:
            The density of the graph.
    """
    return graph.density(loops=loops)


def graph_transitivity_undirected(graph, mode='nan') -> float:
    """
    Calculate the transitivity (clustering coefficient) of an undirected graph.

    Transitivity measures the likelihood that the adjacent vertices of a vertex are connected.
    It is also known as the clustering coefficient.

    If the input graph is directed, it will be converted to an undirected graph by collapsing
    multiple edges and treating them as single undirected edges.

    Parameters:
        graph (igraph.Graph):
            The input graph for which transitivity is to be calculated.
        mode (str, optional):
            Determines the behavior when the graph does not contain any triplets (triads).
            - `"zero"` or `TRANSITIVITY_ZERO`:
                Returns `0.0` if the graph does not have any triplets.
            - `"nan"` or `TRANSITIVITY_NAN`:
                Returns `NaN` (Not a Number) if the graph does not have any triplets.
            Defaults to `'nan'`.

    Returns:
        float:
            The transitivity of the graph. Returns either a floating-point number representing
            the transitivity or `NaN` based on the specified mode when no triplets are present.
    """
    if graph.is_directed():
        graph = graph.to_undirected(mode="collapse")
    return graph.transitivity_undirected(mode=mode)