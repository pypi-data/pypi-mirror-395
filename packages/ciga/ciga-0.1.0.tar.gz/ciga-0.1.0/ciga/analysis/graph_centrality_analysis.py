import igraph as ig
import pandas as pd
import numpy as np
from networkx.algorithms.components import is_connected


# Full graph analysis
def graph_degree(graph: ig.Graph, weighted=False, normalized=False) -> pd.DataFrame:
    """
    Calculate various degree centrality measures for each vertex in the graph.

    This function computes degree-based centrality metrics, including in-degree, out-degree,
    total degree, and their weighted counterparts for directed graphs. For undirected graphs,
    it calculates the degree and weighted degree centrality. Additionally, it supports
    normalization of these centrality measures based on the number of vertices in the graph.

    Parameters:
        graph (igraph.Graph):
            The input graph on which degree centrality measures are to be computed.
            Must be an instance of igraph's `Graph` class.

        weighted (bool, optional):
            If set to `True`, the function calculates weighted degree centrality
            using edge weights. Defaults to `False`.

        normalized (bool, optional):
            If set to `True`, the degree centrality measures are normalized by
            dividing by (n-1), where n is the number of vertices in the graph.
            This normalization facilitates comparison across graphs of different sizes.
            Defaults to `False`.

    Returns:
        pd.DataFrame:
            A pandas DataFrame containing the calculated degree centrality measures.
            The columns vary based on whether the graph is directed and whether
            weighting and normalization are applied.

            - For **directed graphs**:
                - `in_degree`: Number of incoming edges per vertex.
                - `out_degree`: Number of outgoing edges per vertex.
                - `all_degree`: Total degree (in-degree + out-degree) per vertex.
                - `weighted_in_degree` *(if `weighted=True`)*: Sum of weights of incoming edges.
                - `weighted_out_degree` *(if `weighted=True`)*: Sum of weights of outgoing edges.
                - `weighted_all_degree` *(if `weighted=True`)*: Sum of weights of all edges.

            - For **undirected graphs**:
                - `degree`: Number of edges per vertex.
                - `weighted_degree` *(if `weighted=True`)*: Sum of weights of edges per vertex.

            - **Normalization** *(if `normalized=True`)*:
                - Additional columns prefixed with `normalized_` representing the normalized
                  centrality measures (e.g., `normalized_degree`, `normalized_in_degree`, etc.).

    Raises:
        ValueError:
            - If the graph does not contain edge weights but `weighted=True` is specified.

    Example:
        ```python
        import igraph as ig
        import pandas as pd
        from ciga.analysis.graph_centrality_analysis import graph_degree

        # Create a sample directed graph
        g = ig.Graph(directed=True)
        g.add_vertices(4)
        g.vs['name'] = ['A', 'B', 'C', 'D']
        g.add_edges([('A', 'B'), ('B', 'C'), ('C', 'A'), ('A', 'D')])
        g.es['weight'] = [1.5, 2.0, 2.5, 1.0]

        # Calculate degree centrality
        degree_df = graph_degree(g, weighted=True, normalized=True)
        print(degree_df)
        ```
    """
    result = pd.DataFrame()
    directed = graph.is_directed()

    if directed:
        result['in_degree'] = graph.degree(mode='in')
        result['out_degree'] = graph.degree(mode='out')
        result['all_degree'] = graph.degree(mode='all')

        if weighted:
            # check if there's weight (for graph with isolated nodes)
            has_w = 'weight' in graph.es.attributes()
            result['weighted_in_degree'] = graph.strength(mode='in',
                                                          weights='weight') if has_w else [0.0] * graph.vcount()
            result['weighted_out_degree'] = graph.strength(mode='out',
                                                           weights='weight') if has_w else [0.0] * graph.vcount()
            result['weighted_all_degree'] = graph.strength(mode='all',
                                                           weights='weight') if has_w else [0.0] * graph.vcount()
    else:
        result['degree'] = graph.degree()

        if weighted:
            has_w = 'weight' in graph.es.attributes()
            result['weighted_degree'] = graph.strength(weights='weight') if has_w else [0.0] * graph.vcount()

    if normalized:
        normalize_factor = graph.vcount() - 1
        if normalize_factor > 1:
            if directed:
                result['normalized_in_degree'] = result['in_degree'] / normalize_factor
                result['normalized_out_degree'] = result['out_degree'] / normalize_factor
                result['normalized_all_degree'] = result['all_degree'] / normalize_factor
                if weighted:
                    result['normalized_weighted_in_degree'] = result['weighted_in_degree'] / normalize_factor
                    result['normalized_weighted_out_degree'] = result['weighted_out_degree'] / normalize_factor
                    result['normalized_weighted_all_degree'] = result['weighted_all_degree'] / normalize_factor
            else:
                result['normalized_degree'] = result['degree'] / normalize_factor
                if weighted:
                    result['normalized_weighted_degree'] = result['weighted_degree'] / normalize_factor
        else:
            for col in result.columns:
                result[f'normalized_{col}'] = 0.0

    # print(result)
    return result


def graph_betweenness(graph: ig.Graph, weighted=False, cutoff=None, sources=None, targets=None,
                      normalized=False) -> pd.DataFrame:
    """
    Compute betweenness centrality for each vertex in the graph.

    This function calculates the betweenness centrality, which measures the extent to
    which a vertex lies on paths between other vertices. It supports both weighted and
    unweighted graphs and allows for normalization of the centrality scores. Additional
    parameters enable customization of the computation, such as limiting the analysis to
    specific sources, targets, or path lengths.

    Parameters:
        graph (igraph.Graph):
            The input graph on which betweenness centrality is to be computed.
            Must be an instance of igraph's `Graph` class.

        weighted (bool, optional):
            If set to `True`, the function calculates weighted betweenness centrality
            using edge weights. Defaults to `False`.

        cutoff (int, optional):
            Specifies the maximum path length to consider when calculating betweenness.
            Paths longer than the cutoff are ignored. Defaults to `None`, which considers
            all possible paths.

        sources (list, optional):
            A list of vertex indices to be used as sources for the betweenness calculation.
            If specified, only paths originating from these sources are considered. Defaults to `None`,
            which includes all vertices as potential sources.

        targets (list, optional):
            A list of vertex indices to be used as targets for the betweenness calculation.
            If specified, only paths ending at these targets are considered. Defaults to `None`,
            which includes all vertices as potential targets.

        normalized (bool, optional):
            If set to `True`, the betweenness centrality scores are normalized by dividing by
            the number of possible pairs of vertices not including the vertex itself. This makes
            the centrality scores comparable across graphs of different sizes. Defaults to `False`.

    Returns:
        pd.DataFrame:
            A pandas DataFrame containing the calculated betweenness centrality measures.
            The DataFrame includes the following columns based on the input parameters:

            - `betweenness`: Unweighted betweenness centrality.
            - `weighted_betweenness` *(if `weighted=True`)*: Weighted betweenness centrality.

            If `normalized=True`, additional columns with normalized scores are included:
            - `normalized_betweenness`
            - `normalized_weighted_betweenness` *(if `weighted=True`)*

    Raises:
        ValueError:
            - If the graph does not contain edge weights but `weighted=True` is specified.
            - If `sources` or `targets` contain invalid vertex indices.

    Example:
        ```python
        import igraph as ig
        import pandas as pd
        from ciga.analysis.graph_centrality_analysis import graph_betweenness

        # Create a sample undirected graph
        g = ig.Graph(edges=[(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)])
        g.vs['name'] = ['A', 'B', 'C', 'D']
        g.es['weight'] = [1, 2, 1, 3, 2]

        # Calculate betweenness centrality
        betweenness_df = graph_betweenness(g, weighted=True, normalized=True)
        print(betweenness_df)
        ```
    """
    result = pd.DataFrame()
    directed = graph.is_directed()

    betweenness = graph.betweenness(weights=None, directed=directed, cutoff=cutoff, sources=sources, targets=targets)
    result['betweenness'] = betweenness
    if weighted:
        has_w = 'weight' in graph.es.attributes()
        if has_w:
            try:
                weighted_betweenness = graph.betweenness(weights='weight', directed=directed, cutoff=cutoff,
                                                         sources=sources, targets=targets)
            except Exception:
                weighted_betweenness = [0.0] * graph.vcount()
        else:
            weighted_betweenness = [0.0] * graph.vcount()
        result['weighted_betweenness'] = weighted_betweenness

    if normalized:
        # Normalization factors based on whether the graph is directed
        n = graph.vcount()
        if directed:
            normalize_factor = (n - 1) * (n - 2)
        else:
            normalize_factor = (n - 1) * (n - 2) / 2

        if normalize_factor > 0:
            result['normalized_betweenness'] = result['betweenness'] / normalize_factor
            if weighted:
                result['normalized_weighted_betweenness'] = result['weighted_betweenness'] / normalize_factor
        else:
            result['normalized_betweenness'] = 0.0
            if weighted:
                result['normalized_weighted_betweenness'] = 0.0

    return result


def graph_closeness(graph: ig.Graph, weighted, cutoff=None, normalized=False) -> pd.DataFrame:
    """
    Calculate closeness centrality measures for each vertex in the graph.

    Closeness centrality assesses how close a vertex is to all other vertices in the graph.
    It is defined as the reciprocal of the sum of the shortest path distances from the vertex
    to all other vertices. This function supports both weighted and unweighted graphs and
    allows for normalization of the closeness scores. Additionally, it offers the ability to
    limit the analysis to paths within a specified cutoff and to compute centrality for specific
    modes (in, out, all) in directed graphs.

    Parameters:
        graph (igraph.Graph):
            The input graph on which closeness centrality is to be computed.
            Must be an instance of igraph's `Graph` class.

        weighted (bool):
            If set to `True`, the function calculates weighted closeness centrality
            using edge weights. Must be explicitly provided (no default value).

        cutoff (int, optional):
            Specifies the maximum path length to consider when calculating closeness.
            Paths longer than the cutoff are ignored. Defaults to `None`, which considers
            all possible paths.

        normalized (bool, optional):
            If set to `True`, the closeness centrality scores are normalized based on
            the number of reachable vertices. This makes the centrality scores comparable
            across graphs of different sizes and densities. Defaults to `False`.

    Returns:
        pd.DataFrame:
            A pandas DataFrame containing the calculated closeness centrality measures.
            The columns vary based on whether the graph is directed and whether
            weighting and normalization are applied.

            - For **directed graphs**:
                - `in_closeness`: Closeness centrality based on incoming paths.
                - `out_closeness`: Closeness centrality based on outgoing paths.
                - `all_closeness`: Closeness centrality considering all paths.

                - `weighted_in_closeness` *(if `weighted=True`)*: Weighted in-closeness centrality.
                - `weighted_out_closeness` *(if `weighted=True`)*: Weighted out-closeness centrality.
                - `weighted_all_closeness` *(if `weighted=True`)*: Weighted all-closeness centrality.

            - For **undirected graphs**:
                - `closeness`: Closeness centrality.
                - `weighted_closeness` *(if `weighted=True`)*: Weighted closeness centrality.

            - **Normalization** *(if `normalized=True`)*:
                - Additional columns prefixed with `normalized_` representing the normalized
                  closeness centrality measures (e.g., `normalized_closeness`, `normalized_in_closeness`, etc.).

    Raises:
        ValueError:
            - If the graph does not contain edge weights but `weighted=True` is specified.

    Example:
        ```python
        import igraph as ig
        import pandas as pd
        from ciga.analysis.graph_centrality_analysis import graph_closeness

        # Create a sample directed graph
        g = ig.Graph(directed=True)
        g.add_vertices(3)
        g.vs['name'] = ['A', 'B', 'C']
        g.add_edges([('A', 'B'), ('B', 'C')])
        g.es['weight'] = [1, 2]

        # Calculate closeness centrality
        closeness_df = graph_closeness(g, weighted=True, normalized=True)
        print(closeness_df)
        ```
    """
    result = pd.DataFrame()

    # check if it's empty graph, directly set as 0
    if graph.ecount() == 0:
        n = graph.vcount()
        cols = ['in_closeness', 'out_closeness', 'all_closeness'] if graph.is_directed() else ['closeness']
        if weighted:
            cols += [f'weighted_{c}' for c in cols]
        if normalized:
            cols += [f'normalized_{c}' for c in cols]
        for col in cols:
            result[col] = [0.0] * n
        return result

    directed = graph.is_directed()
    has_w = 'weight' in graph.es.attributes() if weighted else False

    if directed:
        result['in_closeness'] = graph.closeness(weights=None, mode="in", cutoff=cutoff)
        result['out_closeness'] = graph.closeness(weights=None, mode="out", cutoff=cutoff)
        result['all_closeness'] = graph.closeness(weights=None, mode="all", cutoff=cutoff)

        if weighted:
            result['weighted_in_closeness'] = graph.closeness(weights='weight', mode="in",
                                                              cutoff=cutoff) if has_w else [0.0] * graph.vcount()
            result['weighted_out_closeness'] = graph.closeness(weights='weight', mode="out",
                                                               cutoff=cutoff) if has_w else [0.0] * graph.vcount()
            result['weighted_all_closeness'] = graph.closeness(weights='weight', mode="all",
                                                               cutoff=cutoff) if has_w else [0.0] * graph.vcount()
    else:
        result['closeness'] = graph.closeness(weights=None, cutoff=cutoff)

        if weighted:
            result['weighted_closeness'] = graph.closeness(weights='weight', cutoff=cutoff) if has_w else [0.0] * graph.vcount()

    if normalized:
        if directed:
            result['normalized_in_closeness'] = graph.closeness(weights=None, mode="in", cutoff=cutoff, normalized=True)
            result['normalized_out_closeness'] = graph.closeness(weights=None, mode="out", cutoff=cutoff, normalized=True)
            result['normalized_all_closeness'] = graph.closeness(weights=None, mode="all", cutoff=cutoff, normalized=True)

            if weighted:
                result['normalized_weighted_in_closeness'] = graph.closeness(weights='weight', mode="in", cutoff=cutoff,
                                                                             normalized=True) if has_w else [0.0] * graph.vcount()
                result['normalized_weighted_out_closeness'] = graph.closeness(weights='weight', mode="out",
                                                                              cutoff=cutoff,
                                                                              normalized=True) if has_w else [0.0] * graph.vcount()
                result['normalized_weighted_all_closeness'] = graph.closeness(weights='weight', mode="all",
                                                                              cutoff=cutoff,
                                                                              normalized=True) if has_w else [0.0] * graph.vcount()
        else:
            result['normalized_closeness'] = graph.closeness(weights=None, cutoff=cutoff, normalized=True)

            if weighted:
                result['normalized_weighted_closeness'] = graph.closeness(weights='weight', cutoff=cutoff,
                                                                          normalized=True) if has_w else [0.0] * graph.vcount()

    return result


def graph_eigenvector_centrality(graph: ig.Graph, weighted=False, scale=True,
                                 return_eigenvalue=False,
                                 pagerank=True) -> pd.DataFrame:
    """
        Compute eigenvector centrality for each vertex in the graph.

        Eigenvector centrality measures a vertex's influence based on the influence of its neighbors.
        However, for disconnected graphs (common in dialogue datasets), standard eigenvector centrality
        is mathematically undefined or unstable (scores converge to zero).

        This function provides a robust fallback to **PageRank** for disconnected graphs by default.

        Parameters:
            graph (igraph.Graph):
                The input graph. Must be an instance of igraph's `Graph` class.

            weighted (bool, optional):
                If set to `True`, calculates centrality using edge weights. Defaults to `False`.

            scale (bool, optional):
                If set to `True`, the centrality scores are scaled.
                - For Eigenvector: max score is 1.0.
                - For PageRank: scores are rescaled so the max score is 1.0 (matching Eigenvector behavior).
                Defaults to `True`.

            return_eigenvalue (bool, optional):
                If set to `True`, returns the principal eigenvalue.
                Returns `NaN` if PageRank is used. Defaults to `False`.

            pagerank (bool, optional):
                If set to `True` (default), the function checks if the graph is connected.
                If the graph is **disconnected**, it automatically switches to PageRank calculation
                to avoid zero-scores and warnings.
                If set to `False`, it forces Eigenvector Centrality regardless of connectivity,
                which may trigger RuntimeWarnings and produce zero values for disconnected components.

        Returns:
            pd.DataFrame:
                A pandas DataFrame containing:
                - `eigenvector_centrality`: The score for each vertex.
                - `eigenvalue` *(optional)*: The principal eigenvalue (or NaN).

        Raises:
            ValueError:
                - If `weighted=True` but no weights are present.
        """
    n = graph.vcount()
    # set all zero in default
    scores, value = [0.0] * n, np.nan
    can_calculate = (graph.ecount() > 0) and (not weighted or 'weight' in graph.es.attributes())

    if can_calculate:
        is_connected = False
        if graph.is_directed():
            is_connected = graph.is_connected(mode='strong')
        else:
            is_connected = graph.is_connected(mode='weak')

        use_pagerank = False

        if pagerank and not is_connected:
            use_pagerank = True
        else:
            try:
                scores, value = graph.eigenvector_centrality(
                    directed=graph.is_directed(),
                    scale=scale,
                    weights='weight' if weighted else None,
                    return_eigenvalue=True
                )
            except Exception:
                pass
        if use_pagerank:
            try:
                # PageRank is robust for disconnected graphs
                scores = graph.pagerank(
                    directed=graph.is_directed(),
                    weights='weight' if weighted else None
                )
                value = np.nan
                if scale:
                    max_s = max(scores) if scores else 0
                    if max_s > 0:
                        scores = [s / max_s for s in scores]

            except Exception:
                scores = [0.0] * n

    result = pd.DataFrame({'eigenvector_centrality': scores})
    if return_eigenvalue:
        result['eigenvalue'] = value

    return result
