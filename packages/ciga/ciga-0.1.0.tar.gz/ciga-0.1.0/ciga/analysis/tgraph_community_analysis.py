from typing import Callable

import pandas as pd
from ..ciga import TGraph
from .graph_community_analysis import graph_community_leiden
from tqdm import tqdm


def sequential_analysis(tg: TGraph,
                        cluster_func: Callable[..., pd.DataFrame],
                        *,
                        accumulate=True,
                        start=None,
                        end=None,
                        w_normalized=False,
                        **analysis_kwargs) -> pd.DataFrame:
    """
    Perform community detection analysis on a time-varying graph sequentially across specified time steps.

    This function iterates through the time steps of the provided `TGraph` object, applies the
    specified community detection function to each graph snapshot, and aggregates the results
    into a single pandas DataFrame. Optional parameters allow for accumulation of graph data,
    normalization of weights, and filtering of analysis to specific time intervals.

    Parameters:
        tg (TGraph):
            The time-varying graph instance on which community detection is to be performed.

        cluster_func (Callable[..., pd.DataFrame]):
            The community detection function to apply. It should accept an `igraph.Graph` object
            and return a pandas DataFrame with community assignments.

        accumulate (bool, optional):
            If set to `True`, each graph snapshot will include changes from all previous snapshots.
            Defaults to `True`.

        start (optional):
            The starting time step for the analysis. Only time steps >= `start` will be considered.
            Defaults to `None`, which includes all time steps from the beginning.

        end (optional):
            The ending time step for the analysis. Only time steps <= `end` will be considered.
            Defaults to `None`, which includes all time steps until the end.

        w_normalized (bool, optional):
            If set to `True`, the graph weights will be normalized before community detection.
            Defaults to `False`.

        **analysis_kwargs:
            Additional keyword arguments to be passed to the `cluster_func`.

    Returns:
        pd.DataFrame:
            A DataFrame containing community assignments for each vertex at each time step.
            The DataFrame includes positional information and the corresponding community index.

    Raises:
        ValueError:
            If invalid parameters are provided or required data is missing.
    """
    results = pd.DataFrame()
    # Add position columns to results
    for col in tg._position:
        results[col] = []
    results['character'] = []
    results['community'] = []

    # Retrieve unique time steps from the graph data
    time_steps = tg.data.index.unique().tolist()
    if start:
        time_steps = [step for step in time_steps if step >= start]
    if end:
        time_steps = [step for step in time_steps if step <= end]

    # Iterate through each time step and perform community detection
    for step in tqdm(time_steps, desc='Processing time steps', unit='step'):
        graph = tg.get_graph(step, w_normalized=w_normalized)

        communities = cluster_func(graph, **analysis_kwargs)
        # Assign positional information to the communities DataFrame
        for col, val in zip(tg._position, step):
            communities[col] = val

        # Concatenate the results for each time step
        results = pd.concat([results, communities], axis=0).reset_index(drop=True)

    return results

def tgraph_community_leiden(tgraph: TGraph, *,
                            accumulate=True,
                            start=None,
                            end=None,
                            weights='weight',
                            objective_function='CPM',
                            resolution=1.0,
                            beta=0.01,
                            initial_membership=None,
                            n_iterations=2,
                            node_weights=None,
                            **kwds) -> pd.DataFrame:
    """
    Execute community detection on a temporal graph using the Leiden algorithm.

    This function leverages the `sequential_analysis` function to perform community detection
    on each snapshot of the provided `TGraph` object. It utilizes the Leiden algorithm to
    identify communities within each graph snapshot based on specified parameters.

    Parameters:
        tgraph (TGraph):
            The temporal graph instance to analyze.

        accumulate (bool, optional):
            If set to `True`, each graph snapshot will accumulate changes from all previous snapshots.
            Defaults to `True`.

        start (optional):
            The starting time step for the analysis. Only time steps >= `start` will be considered.
            Defaults to `None`, which includes all time steps from the beginning.

        end (optional):
            The ending time step for the analysis. Only time steps <= `end` will be considered.
            Defaults to `None`, which includes all time steps until the end.

        weights (str, optional):
            The edge attribute used as weights for the community detection algorithm.
            Defaults to `'weight'`.

        objective_function (str, optional):
            The objective function to optimize during community detection.
            Common options include:
                - `'CPM'`: Constant Potts Model
                - `'Modularity'`
                - `'Negative Log-likelihood'`
            Defaults to `'CPM'`.

        resolution (float, optional):
            The resolution parameter influencing the size of detected communities.
            Higher values lead to smaller communities. Defaults to `1.0`.

        beta (float, optional):
            The resolution limit parameter balancing partition quality and computational efficiency.
            Defaults to `0.01`.

        initial_membership (list or None, optional):
            A list specifying initial community memberships for each vertex.
            If `None`, the algorithm starts with a random partition. Defaults to `None`.

        n_iterations (int, optional):
            The number of iterations the Leiden algorithm should perform.
            More iterations can refine community structures but increase computation time.
            Defaults to `2`.

        node_weights (list or None, optional):
            A list of weights for each node, influencing community detection.
            If `None`, all nodes are treated equally. Useful for emphasizing certain nodes.
            Defaults to `None`.

        **kwds:
            Additional keyword arguments to customize the Leiden algorithm further.

    Returns:
        pd.DataFrame:
            A DataFrame containing community assignments for each vertex at each time step.
            Includes positional information and the corresponding community index.

    Raises:
        ValueError:
            If invalid parameters are provided or required data is missing.
    """

    return sequential_analysis(tgraph, graph_community_leiden, accumulate=accumulate, start=start, end=end,
                               weights=weights, objective_function=objective_function, resolution=resolution,
                               beta=beta, initial_membership=initial_membership, n_iterations=n_iterations,
                               node_weights=node_weights, **kwds)
