import pandas as pd
from typing import Callable, Dict, Any, List, Optional
from ..ciga import TGraph
from .graph_properties import graph_density, graph_transitivity_undirected
from tqdm import tqdm
import igraph as ig


def sequential_analysis(
        tg: TGraph,
        analysis_func: Callable[..., Any],
        *,
        accumulate=True,
        start: Optional[int] = None,
        end: Optional[int] = None,
        w_normalized: bool = False,
        property_name: str = None,
        **analysis_kwargs
) -> pd.DataFrame:
    """
    Perform a sequential analysis on a time-varying graph.

    This function iterates through specified time steps of the provided `TGraph` object,
    applies the given analysis function to each graph snapshot, and aggregates the results
    into a single pandas DataFrame. It supports optional accumulation of graph data,
    normalization of weights, and filtering of analysis to specific time intervals.

    Parameters:
        tg (TGraph):
            The time-varying graph instance to analyze.
        
        analysis_func (Callable[..., Any]):
            The analysis function to apply to each graph snapshot. It should accept an `igraph.Graph`
            object and return a measurable property.
        
        accumulate (bool, optional):
            If `True`, each graph snapshot will include changes from all previous snapshots.
            Defaults to `True`.
        
        start (Optional[int], optional):
            The starting time step for the analysis. Only time steps >= `start` will be considered.
            Defaults to `None`, which includes all time steps from the beginning.
        
        end (Optional[int], optional):
            The ending time step for the analysis. Only time steps <= `end` will be considered.
            Defaults to `None`, which includes all time steps until the end.
        
        w_normalized (bool, optional):
            If `True`, the graph weights will be normalized before applying the analysis function.
            Defaults to `False`.
        
        property_name (str, optional):
            The name of the property being analyzed. This will be used as a column in the results DataFrame.
            Defaults to `None`.
        
        **analysis_kwargs:
            Additional keyword arguments to pass to the analysis function.

    Returns:
        pd.DataFrame:
            A DataFrame containing the results of the analysis for each time step.
            Includes positional information and the corresponding property value.
    """
    results = pd.DataFrame()
    # add position columns to results
    for col in tg._position:
        results[col] = []
    results[property_name] = []

    # get time steps
    time_steps = tg.data.index.unique().tolist()
    if start:
        time_steps = [step for step in time_steps if step >= start]
    if end:
        time_steps = [step for step in time_steps if step <= end]

    for step in tqdm(time_steps, desc='Processing time steps', unit='step'):
        graph = tg.get_graph(step, w_normalized=w_normalized)
        measure = {
            property_name: analysis_func(graph, **analysis_kwargs)
        }
        for col, val in zip(tg._position, step):
            measure[col] = val
        results = pd.concat([results, measure], axis=0).reset_index(drop=True)

    return results


def tgraph_density(tgraph: TGraph, *,
                   accumulate=True,
                   start: Optional[int] = None,
                   end: Optional[int] = None,
                   loops=False) -> pd.DataFrame:
    """
    Calculate the density of a time-varying graph over specified time steps.

    This function leverages the `sequential_analysis` function to compute the density
    of the graph at each time step. Density is a measure of how many edges are in the graph
    compared to the maximum possible number of edges.

    Parameters:
        tgraph (TGraph):
            The time-varying graph instance to analyze.
        
        accumulate (bool, optional):
            If `True`, each graph snapshot will include changes from all previous snapshots.
            Defaults to `True`.
        
        start (Optional[int], optional):
            The starting time step for the density calculation.
            Only time steps >= `start` will be considered.
            Defaults to `None`.
        
        end (Optional[int], optional):
            The ending time step for the density calculation.
            Only time steps <= `end` will be considered.
            Defaults to `None`.
        
        loops (bool, optional):
            If `True`, self-loops will be considered in the density calculation.
            Defaults to `False`.

    Returns:
        pd.DataFrame:
            A DataFrame containing the density of the graph for each specified time step.
            Includes positional information and the density value.
    """
    return sequential_analysis(tgraph, accumulate=accumulate, analysis_func=graph_density, start=start, end=end,
                               w_normalized=False, loops=loops, property_name="density")


def tgraph_transitivity_undirected(tgraph: TGraph, *,
                        accumulate=True,
                        start: Optional[int] = None,
                        end: Optional[int] = None,
                        mode='nan'
                        ) -> pd.DataFrame:
    """
    Calculate the transitivity (clustering coefficient) of an undirected time-varying graph.

    This function uses the `sequential_analysis` function to compute the transitivity of the
    graph at each time step. Transitivity measures the likelihood that the adjacent vertices
    of a vertex are connected.

    Parameters:
        tgraph (TGraph):
            The time-varying graph instance to analyze.
        
        accumulate (bool, optional):
            If `True`, each graph snapshot will include changes from all previous snapshots.
            Defaults to `True`.
        
        start (Optional[int], optional):
            The starting time step for the transitivity calculation.
            Only time steps >= `start` will be considered.
            Defaults to `None`.
        
        end (Optional[int], optional):
            The ending time step for the transitivity calculation.
            Only time steps <= `end` will be considered.
            Defaults to `None`.
        
        mode (str, optional):
            The mode for calculating transitivity. Defaults to `'nan'`.
            Other modes can be specified as supported by the underlying analysis function.

    Returns:
        pd.DataFrame:
            A DataFrame containing the transitivity of the graph for each specified time step.
            Includes positional information and the transitivity value.

    Raises:
        Warning:
            If the provided graphs are directed, a warning is raised indicating that they will be converted to undirected.
    """
    if tgraph.is_directed():
        raise Warning("The graphs are directed. They will be converted to undirected.")
    return sequential_analysis(tgraph, accumulate=accumulate, analysis_func=graph_transitivity_undirected,
                               start=start, end=end, mode=mode, property_name="transitivity")