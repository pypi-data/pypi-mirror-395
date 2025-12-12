import pandas as pd
from typing import Callable, Dict, Any, List
from ..ciga import TGraph
from .graph_centrality_analysis import graph_degree, graph_betweenness, graph_closeness, graph_eigenvector_centrality
from tqdm import tqdm


def sequential_analysis(tg: TGraph,
                       analysis_func: Callable[..., pd.DataFrame],
                       *,
                       accumulate=True,
                       start=None,
                       end=None,
                       w_normalized=False,
                       **analysis_kwargs) -> pd.DataFrame:
    """
    Perform a specified centrality analysis on a time-varying graph sequentially over its time steps.

    This function iterates through the defined time steps of the provided `TGraph` object, applies the
    given `analysis_func` to each snapshot of the graph, and aggregates the results into a single
    DataFrame. Optional parameters allow for accumulation of graph data, normalization of weights,
    and filtering of the analysis to specific time intervals.

    Parameters:
        tg (TGraph):
            The time-varying graph object on which the analysis is to be performed.

        analysis_func (Callable[..., pd.DataFrame]):
            The function to compute centrality measures on each graph snapshot. It should accept an
            `igraph.Graph` object and return a `pandas.DataFrame` with the analysis results.

        accumulate (bool, optional):
            If set to `True`, each graph snapshot will accumulate changes from previous snapshots.
            Defaults to `True`.

        start (optional):
            The starting time step for the analysis. If specified, only time steps >= start will be
            considered. Defaults to `None`, which includes all time steps.

        end (optional):
            The ending time step for the analysis. If specified, only time steps <= end will be considered.
            Defaults to `None`, which includes all time steps.

        w_normalized (bool, optional):
            If set to `True`, the graph weights will be normalized before analysis. Defaults to `False`.

        **analysis_kwargs:
            Additional keyword arguments to be passed to the `analysis_func`.

    Returns:
        pd.DataFrame:
            A DataFrame containing the aggregated centrality measures across the specified time steps.
            Each row corresponds to a vertex at a specific time step, including positional information
            and the computed centrality measures.

    Raises:
        ValueError:
            If any of the provided parameters are invalid or missing required information.
    """
    results = pd.DataFrame()
    # Add position columns to results
    for col in tg._position:
        results[col] = []
    results['character'] = []

    # Get time steps
    time_steps = tg.data.index.unique().tolist()
    if start:
        time_steps = [step for step in time_steps if step >= start]
    if end:
        time_steps = [step for step in time_steps if step <= end]

    for step in tqdm(time_steps, desc='Processing time steps', unit='step'):
        graph = tg.get_graph(step, accumulate=accumulate, w_normalized=w_normalized)

        measures = analysis_func(graph, **analysis_kwargs)
        for col, val in zip(tg._position, step):
            measures[col] = val
        measures['character'] = graph.vs['name']

        results = pd.concat([results, measures], axis=0).reset_index(drop=True)

    return results


def tgraph_degree(tgraph: TGraph, *,
                 start=None,
                 end=None,
                 accumulate=True,
                 weighted=False,
                 w_normalized=False,
                 normalized=False) -> pd.DataFrame:
    """
    Perform degree centrality analysis on a time-varying graph.

    This function calculates the degree centrality for each vertex across the specified time steps of the
    given `TGraph` object. Degree centrality measures the number of direct connections a vertex has.

    Parameters:
        tgraph (TGraph):
            The time-varying graph to analyze.

        start (optional):
            The starting time step for the analysis. Only time steps >= start will be included.
            Defaults to `None`.

        end (optional):
            The ending time step for the analysis. Only time steps <= end will be included.
            Defaults to `None`.

        accumulate (bool, optional):
            If `True`, the graph snapshots will accumulate over time, incorporating changes from all
            previous steps. If `False`, each snapshot represents only the changes at that time step.
            Defaults to `True`.

        weighted (bool, optional):
            If `True`, computes weighted degree centrality using edge weights. If `False`, computes
            unweighted degree centrality. Defaults to `False`.

        w_normalized (bool, optional):
            If `True`, normalizes the graph weights before computing centrality measures.
            Defaults to `False`.

        normalized (bool, optional):
            If `True`, normalizes the degree centrality by dividing by (n-1), where n is the number of vertices.
            This makes centrality scores comparable across graphs of different sizes.
            Defaults to `False`.

    Returns:
        pd.DataFrame:
            A DataFrame containing the degree centrality measures for each vertex at each time step.
            Columns include positional information, character names, and the calculated degree measures.

    Example:
        ```python
        degree_centrality = tgraph_degree(tg, weighted=True, normalized=True)
        print(degree_centrality)
        ```
    """
    return sequential_analysis(tgraph, accumulate=accumulate, analysis_func=graph_degree, start=start, end=end,
                              weighted=weighted, w_normalized=w_normalized, normalized=normalized)


def tgraph_betweenness(tgraph: TGraph, *,
                      start=None,
                      end=None,
                      accumulate=True,
                      weighted=False,
                      w_normalized=False,
                      normalized=True,
                      cutoff=None,
                      sources=None,
                      targets=None) -> pd.DataFrame:
    """
    Perform betweenness centrality analysis on a time-varying graph.

    This function calculates the betweenness centrality for each vertex across the specified time steps of the
    given `TGraph` object. Betweenness centrality measures the extent to which a vertex lies on paths between
    other vertices.

    Parameters:
        tgraph (TGraph):
            The time-varying graph to analyze.

        start (optional):
            The starting time step for the analysis. Only time steps >= start will be included.
            Defaults to `None`.

        end (optional):
            The ending time step for the analysis. Only time steps <= end will be included.
            Defaults to `None`.

        accumulate (bool, optional):
            If `True`, the graph snapshots will accumulate over time, incorporating changes from all
            previous steps. If `False`, each snapshot represents only the changes at that time step.
            Defaults to `True`.

        weighted (bool, optional):
            If `True`, computes weighted betweenness centrality using edge weights. If `False`, computes
            unweighted betweenness centrality. Defaults to `False`.

        w_normalized (bool, optional):
            If `True`, normalizes the graph weights before computing centrality measures.
            Defaults to `False`.

        normalized (bool, optional):
            If `True`, normalizes the betweenness centrality scores. This makes centrality scores
            comparable across graphs of different sizes. Defaults to `True`.

        cutoff (int, optional):
            Specifies the maximum path length to consider when calculating betweenness centrality.
            Paths longer than the cutoff are ignored. Defaults to `None`, which considers all paths.

        sources (list, optional):
            A list of vertex indices to be used as sources for the betweenness calculation.
            If specified, only paths originating from these sources are considered. Defaults to `None`,
            which includes all vertices as potential sources.

        targets (list, optional):
            A list of vertex indices to be used as targets for the betweenness calculation.
            If specified, only paths ending at these targets are considered. Defaults to `None`,
            which includes all vertices as potential targets.

    Returns:
        pd.DataFrame:
            A DataFrame containing the betweenness centrality measures for each vertex at each time step.
            Columns include positional information, character names, and the calculated betweenness measures.

    Example:
        ```python
        betweenness_centrality = tgraph_betweenness(tg, weighted=True, normalized=True)
        print(betweenness_centrality)
        ```
    """
    return sequential_analysis(tgraph, accumulate=accumulate, analysis_func=graph_betweenness, start=start, end=end,
                               weighted=weighted, w_normalized=w_normalized, normalized=normalized, cutoff=cutoff,
                               sources=sources, targets=targets)


def tgraph_closeness(tgraph: TGraph, *,
                    start=None,
                    end=None,
                    accumulate=True,
                    weighted=False,
                    w_normalized=False,
                    normalized=True,
                    cutoff=None) -> pd.DataFrame:
    """
    Perform closeness centrality analysis on a time-varying graph.

    This function calculates the closeness centrality for each vertex across the specified time steps of the
    given `TGraph` object. Closeness centrality measures how close a vertex is to all other vertices in the graph.

    Parameters:
        tgraph (TGraph):
            The time-varying graph to analyze.

        start (optional):
            The starting time step for the analysis. Only time steps >= start will be included.
            Defaults to `None`.

        end (optional):
            The ending time step for the analysis. Only time steps <= end will be included.
            Defaults to `None`.

        accumulate (bool, optional):
            If `True`, the graph snapshots will accumulate over time, incorporating changes from all
            previous steps. If `False`, each snapshot represents only the changes at that time step.
            Defaults to `True`.

        weighted (bool, optional):
            If `True`, computes weighted closeness centrality using edge weights. If `False`, computes
            unweighted closeness centrality. Defaults to `False`.

        w_normalized (bool, optional):
            If `True`, normalizes the graph weights before computing centrality measures.
            Defaults to `False`.

        normalized (bool, optional):
            If `True`, normalizes the closeness centrality scores. This makes centrality scores
            comparable across graphs of different sizes. Defaults to `True`.

        cutoff (int, optional):
            Specifies the maximum path length to consider when calculating closeness centrality.
            Paths longer than the cutoff are ignored. Defaults to `None`, which considers all paths.

    Returns:
        pd.DataFrame:
            A DataFrame containing the closeness centrality measures for each vertex at each time step.
            Columns include positional information, character names, and the calculated closeness measures.

    Example:
        ```python
        closeness_centrality = tgraph_closeness(tg, weighted=True, normalized=True)
        print(closeness_centrality)
        ```
    """
    return sequential_analysis(tgraph, accumulate=accumulate, analysis_func=graph_closeness, start=start, end=end,
                               weighted=weighted, w_normalized=w_normalized, normalized=normalized, cutoff=cutoff)

def tgraph_eigenvector_centrality(tgraph: TGraph,
                                  start=None,
                                  end=None,
                                  accumulate=True,
                                  weighted=False,
                                  w_normalized=False,
                                  scale=True,
                                  return_eigenvalue=False,
                                  pagerank=True,
                                  options=None) -> pd.DataFrame:
    """
    Perform eigenvector centrality analysis on a time-varying graph.

    This function calculates the eigenvector centrality for each vertex across the specified time steps of the
    given `TGraph` object. Eigenvector centrality measures a vertex's influence based on the influence of its neighbors.

    Parameters:
        tgraph (TGraph):
            The time-varying graph to analyze.

        start (optional):
            The starting time step for the analysis. Only time steps >= start will be included.
            Defaults to `None`.

        end (optional):
            The ending time step for the analysis. Only time steps <= end will be included.
            Defaults to `None`.

        accumulate (bool, optional):
            If `True`, the graph snapshots will accumulate over time, incorporating changes from all
            previous steps. If `False`, each snapshot represents only the changes at that time step.
            Defaults to `True`.

        weighted (bool, optional):
            If `True`, computes weighted eigenvector centrality using edge weights. If `False`, computes
            unweighted eigenvector centrality. Defaults to `False`.

        scale (bool, optional):
            If `True`, scales the eigenvector centrality scores to have a mean of 0 and a variance of 1.
            Defaults to `True`.

        return_eigenvalue (bool, optional):
            If `True`, returns the principal eigenvalue associated with the eigenvector centrality calculation.
            Defaults to `False`.

        options (dict, optional):
            Additional options to customize the eigenvector centrality computation. These will be passed
            directly to the underlying centrality computation function. Defaults to `None`.

    Returns:
        pd.DataFrame:
            A DataFrame containing the eigenvector centrality measures for each vertex at each time step.
            Columns include positional information, character names, and the calculated centrality measures.
            If `return_eigenvalue=True`, additional columns for eigenvalues are included.

    Example:
        ```python
        eigen_centrality = tgraph_eigenvector_centrality(tg, weighted=True, scale=True, return_eigenvalue=True)
        print(eigen_centrality)
        ```
    """
    return sequential_analysis(tgraph, accumulate=accumulate, analysis_func=graph_eigenvector_centrality,
                               start=start, end=end, weighted=weighted, w_normalized=w_normalized, scale=scale,
                               return_eigenvalue=return_eigenvalue, pagerank=pagerank)