import pandas as pd

def graph_community_leiden(graph,
                           weights='weight',
                           objective_function='CPM',
                           resolution=1.0,
                           beta=0.01,
                           initial_membership=None,
                           n_iterations=2,
                           node_weights=None,
                           **kwds) -> pd.DataFrame:
    """
    Detect communities in a graph using the Leiden algorithm.
    
    The Leiden algorithm is a method for detecting communities in large networks. It optimizes
    the partitioning of the graph to maximize the quality function (e.g., CPM - Constant Potts Model).
    This function supports both weighted and unweighted graphs and allows for various customizations
    through its parameters.

    Parameters:
        graph (igraph.Graph):
            The input graph on which community detection is to be performed.
            Must be an instance of igraph's `Graph` class.

        weights (str or list, optional):
            The edge attribute used as weights for the community detection algorithm.
            If set to `None`, the graph is treated as unweighted. Defaults to `'weight'`.

        objective_function (str, optional):
            The objective function to optimize during community detection.
            Common options include:
                - `'CPM'`: Constant Potts Model
                - `'Modularity'`
                - `'Negative Log-likelihood'`
            Defaults to `'CPM'`.

        resolution (float, optional):
            The resolution parameter that influences the size of the communities detected.
            Higher values lead to detecting smaller communities. Only applicable for certain
            objective functions like CPM. Defaults to `1.0`.

        beta (float, optional):
            The resolution limit parameter. It influences the balance between the
            quality of the partitioning and computational efficiency. Defaults to `0.01`.

        initial_membership (list or None, optional):
            A list specifying the initial community membership of each vertex.
            If `None`, the algorithm starts with a random partition. Useful for initializing
            the algorithm with a known partition. Defaults to `None`.

        n_iterations (int, optional):
            The number of iterations the Leiden algorithm should perform.
            More iterations can lead to more refined community structures but increase computation time.
            Defaults to `2`.

        node_weights (list or None, optional):
            A list of weights for each node, influencing the community detection.
            If `None`, all nodes are treated with equal weight. Useful for emphasizing certain nodes.
            Defaults to `None`.

        **kwds:
            Additional keyword arguments passed to the underlying Leiden implementation.
            Allows for further customization and fine-tuning of the algorithm.

    Returns:
        pd.DataFrame:
            A pandas DataFrame containing the community assignments for each vertex in the graph.
            The DataFrame includes the following columns:
            
            - `character`: The name or identifier of the vertex.
            - `community`: The community index to which the vertex belongs.

    Raises:
        ValueError:
            - If the specified `weights` attribute does not exist in the graph's edge attributes.
            - If `initial_membership` length does not match the number of vertices in the graph.
            - If invalid parameters are provided to the Leiden algorithm.

    Example:
        ```python:ciga/analysis/graph_community_analysis.py
        import igraph as ig
        import pandas as pd
        from ciga.analysis.graph_community_analysis import graph_community_leiden

        # Create a sample undirected graph
        g = ig.Graph(edges=[(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)])
        g.vs['name'] = ['A', 'B', 'C', 'D']
        g.es['weight'] = [1, 2, 1, 3]

        # Perform community detection using the Leiden algorithm
        communities_df = graph_community_leiden(
            graph=g,
            weights='weight',
            objective_function='CPM',
            resolution=1.0,
            beta=0.01,
            n_iterations=3
        )

        print(communities_df)
        ```
    """
    communities = graph.community_leiden(weights=weights, objective_function=objective_function, resolution=resolution,
                                         beta=beta, initial_membership=initial_membership, n_iterations=n_iterations,
                                         node_weights=node_weights, **kwds)
    data = []
    for community_index, community in enumerate(communities):
        community_nodes = [graph.vs[node_id]['name'] for node_id in community]
        for node_name in community_nodes:
            data.append({
                    'character': node_name,
                    'community': community_index
                })
    result = pd.DataFrame(data)
    return result

# community = graph.community_multilevel(weights='weight')
# community = graph.community_leiden(weights='weight')
# community = graph.community_label_propagation(weights='weight')
