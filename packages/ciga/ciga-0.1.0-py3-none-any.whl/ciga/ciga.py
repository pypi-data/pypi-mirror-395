import warnings

import pandas as pd
import numpy as np
from igraph import Graph

class TGraph:
    """
    TGraph is a class for managing and analyzing temporal graphs using the igraph library.

    Attributes:
        data (pd.DataFrame): The dataset containing graph edges and their attributes.
        _position (tuple): The positional indices used for temporal positioning in the data.
        _layout (Any): The layout of the graph (currently unused).
        _directed (bool): Indicates whether the graph is directed.
        _vnames (list): List of vertex names.
        name_to_id (dict): Mapping from vertex names to their IDs.
        id_to_name (dict): Mapping from vertex IDs to their names.
        _cache_graph (Graph): Cached version of the graph for performance optimization.
        _cache_time_point (tuple): Cached time point corresponding to the cached graph.
    """

    def __init__(self, init_graph=None, data=None, position=None, directed=True):
        """
        Initializes a new instance of the TGraph class.

        Args:
            init_graph (Graph, optional): An existing igraph.Graph object to initialize the graph.
                If not provided, a new graph is created.
            data (pd.DataFrame): The dataset containing graph edges and their attributes. **Required**.
            position (list or tuple): The positional indices or keys used for temporal positioning in the data. **Required**.
            directed (bool, optional): Determines whether the graph is directed. Defaults to True.

        Raises:
            ValueError: If `data` or `position` is not provided.
            ValueError: If the `weight` column is missing in the data.
        """
        if data is None:
            raise ValueError("Data must be provided.")
        if position is None:
            raise ValueError("Position must be provided.")
        if 'weight' not in data.columns:
            raise ValueError("Weight column not found in data. Run calculate_weights() first.")

        self.data = data.copy()
        self._position = position
        self._layout = None
        self._directed = directed
        self._vnames = []
        self.name_to_id = {}
        self.id_to_name = {}
        self._cache_graph = None
        self._cache_time_point = tuple([-np.inf] * len(self._position))

        # Set multi-index if not already set
        if not isinstance(self.data.index, pd.MultiIndex):
            self.data.set_index(list(self._position), inplace=True)
            self.data.sort_index(inplace=True) # new

        # For undirected graphs, ensure consistent edge ordering
        if not self._directed:
            idx = self.data['source'] > self.data['target']
            self.data.loc[idx, ['source', 'target']] = self.data.loc[idx, ['target', 'source']].values

        if init_graph is None:
            self._init_graph = Graph(directed=self._directed)
            self._init_graph.vs['name'] = []
            # good for optimization but char havnt appear shouldn't be added
            # all_nodes = np.unique(self.data[['source', 'target']].values)
            # self._init_graph.add_vertices(all_nodes)
        else:
            self._init_graph = init_graph
            self._directed = init_graph.is_directed()

        # Create name to ID mappings
        self._vnames = self._init_graph.vs['name']
        self._create_vnames()

        # Initialize the cached graph
        self._cache_graph = self._init_graph.copy()

    def _create_vnames(self):
        """
        Creates mappings between vertex names and their corresponding IDs.

        Returns:
            list: A list of vertex names.
        """
        self.name_to_id = {name: idx for idx, name in enumerate(self._vnames)}
        self.id_to_name = {idx: name for idx, name in enumerate(self._vnames)}
        return self._vnames

    @property
    def is_directed(self):
        """
        Checks if the graph is directed.

        Returns:
            bool: True if the graph is directed, False otherwise.
        """
        return self._directed

    def _normalize_graph_weight(self, graph):
        """
        Normalizes the weights of the graph's edges so that the maximum weight becomes 1.

        Args:
            graph (Graph): The graph whose edge weights are to be normalized.

        Returns:
            Graph: The graph with normalized edge weights.

        Raises:
            Warning: If the total weight is 0 and no normalization is performed.
        """
        # safety
        if graph.ecount() == 0 or 'weight' not in graph.es.attributes():
            return graph

        weights = graph.es['weight']
        if not weights:
            return graph
        max_weight = max(weights)
        if max_weight > 0:
            graph.es['weight'] = [w / max_weight for w in graph.es['weight']]
        else:
            warnings.warn("Max weight <= 0. No normalization is done.")
        return graph

    def _invert_graph_weight(self, graph):
        """
        Inverts the weights of the graph's edges.

        Args:
            graph (Graph): The graph whose edge weights are to be inverted.

        Returns:
            Graph: The graph with inverted edge weights.
        """
        # safety
        if graph.ecount() == 0 or 'weight' not in graph.es.attributes():
            return graph
        weights = np.array(graph.es['weight'])
        adjusted_weights = 1 / (weights + 1e-6)
        graph.es['weight'] = adjusted_weights
        return graph

    # consider separate this into two function: get_data() and get_graph()
    # decay calculation can be done in get_data()
    def get_graph(
        self,
        time_point=None,
        *,
        accumulate=True,
        w_normalized=False,
        invert_weight=False,
        # fade_function=None,
        # fade_step=None
        decay=0
    ):
        """
        Retrieves the graph at a specific time point with various transformation options.

        Args:
            time_point (tuple, optional): The time point at which to retrieve the graph.
                Defaults to infinity for all positions.
            accumulate (bool, optional): Whether to accumulate changes up to the specified time point.
                Defaults to True.
            w_normalized (bool, optional): Whether to normalize edge weights. Defaults to False.
            invert_weight (bool, optional): Whether to invert edge weights. Defaults to False.
            fade_function (callable, optional): A function to apply fading effects to edge weights.
            fade_step (list or tuple, optional): Steps at which to apply the fading function.

        Returns:
            Graph or None: The transformed graph at the specified time point or None if no data is available.

        Raises:
            ValueError: If `fade_function` is provided while `accumulate` is False.
            ValueError: If `fade_step` is not a sublist of position columns when provided as a tuple.
        """
        if time_point is None:
            time_point = tuple([np.inf] * len(self._position))
        if len(time_point) < len(self._position):
            time_point = tuple(list(time_point) + [np.inf] * (len(self._position) - len(time_point)))

        def adjust_graph_weight(graph):
            if w_normalized:
                graph = self._normalize_graph_weight(graph)
            if invert_weight:
                graph = self._invert_graph_weight(graph)
            # ensure weight > 0
            if graph.ecount() > 0:
                bad_edges = [e.index for e in graph.es if e['weight'] <= 0]
                if bad_edges:
                    graph.delete_edges(bad_edges)
            return graph

        if not accumulate:
            # if fade_function is not None:
            if decay > 0:
                # raise ValueError("Fade function is not supported for non-accumulative graphs.")
                raise ValueError("Decay is not supported for non-accumulative graphs.")
            moment_graph = Graph(directed=self._directed)
            moment_graph.vs['name'] = []
            idx = pd.IndexSlice
            # Get subset data where position matches time_point
            moment_data = self.data.loc[idx[time_point], :].copy()
            if moment_data.empty:
                return None
            self._update_graph(moment_graph, moment_data)
            return adjust_graph_weight(moment_graph)

        if decay == 0:
            if self._cache_time_point and self._cache_time_point < time_point:
                start = list(self._cache_time_point)
                start[-1] += 1
                delta_data = self.take_interval(start=start, end=time_point)
            else:
                delta_data = self.take_interval(start=None, end=time_point)
                self._cache_graph = self._init_graph.copy()

            if delta_data.empty:
                return adjust_graph_weight(self._cache_graph.copy())

            self._update_graph(self._cache_graph, delta_data)
            self._cache_time_point = time_point

            return adjust_graph_weight(self._cache_graph.copy())
        else: # Do we need fade function?
            if decay < 0 or decay > 1:
                raise ValueError("Decay must be in the interval [0, 1].")
            graph = self._init_graph.copy()
            full_data = self.take_interval(start=None, end=time_point)
            grouped = full_data.groupby(level=list(self._position), sort=True)

            for _, group_data in grouped:
                if graph.ecount() > 0:
                    current_w = np.array(graph.es['weight'])
                    # 向量化乘法
                    graph.es['weight'] = current_w * (1.0 - decay)
                self._update_graph(graph, group_data)

            return adjust_graph_weight(graph)
            # self._cache_graph = self._init_graph.copy()

            # fading_data = self.take_interval(start=None, end=time_point)
            # if fading_data.empty:
            #     return adjust_graph_weight(self._cache_graph.copy())
            #
            # # Reset index to access time positions as columns
            # # fading_data = fading_data.reset_index()

            # fading_graph = self._init_graph.copy()
            #
            # if isinstance(fade_step, list):
            #     start = [-np.inf] * len(self._position)
            #     idx = pd.IndexSlice
            #     for step in fade_step:
            #         fading_data.loc[
            #             idx[tuple(start): tuple(step)], 'weight'
            #         ] = fading_data.loc[
            #             idx[tuple(start): tuple(step)], ['weight']
            #         ].apply(fade_function, axis=1)
            #         # Apply fade function to fading_graph edges
            #         if fading_graph.ecount() > 0:
            #             fading_graph.es['weight'] = [
            #                 fade_function(edge) for edge in fading_graph.es['weight']
            #             ]
            # elif isinstance(fade_step, tuple):
            #     # If fade_step not a sublist of self._position, raise error
            #     if not all([step in self._position for step in fade_step]):
            #         raise ValueError(
            #             "Fade step must be a sublist of position columns."
            #         )
            #     # Group by fade_step and apply fade function to cumulative groups
            #     grouped = fading_data.groupby(list(fade_step))
            #     all_group_keys = list(grouped.groups.keys())
            #     for i, key in enumerate(all_group_keys):
            #         # fade all groups before <=i
            #         selected_group_keys = all_group_keys[:i+1]
            #         mask = fading_data.index.isin(selected_group_keys, level=list(fade_step))
            #         fading_data.loc[mask, 'weight'] = fading_data.loc[mask, 'weight'].apply(fade_function)
            #         if fading_graph.ecount() > 0:
            #             fading_graph.es['weight'] = [fade_function(edge) for edge in fading_graph.es['weight']]
            # self._update_graph(fading_graph, fading_data)
            # return adjust_graph_weight(fading_graph)

    def graph_sub(self, graph1, graph2):
        """
        Subtracts the weights of graph2 from graph1.

        Args:
            graph1 (Graph): The base graph.
            graph2 (Graph): The graph to subtract from graph1.

        Returns:
            Graph: The resulting graph after subtraction.

        Raises:
            ValueError: If the directedness of graph1 and graph2 do not match.
            ValueError: If either graph lacks the 'name' attribute for vertices.
        """
        # Ensure both graphs have the same directedness
        if graph1.is_directed() != graph2.is_directed():
            raise ValueError("Both graphs must be either directed or undirected.")

        # Copy graph1 to avoid modifying the original
        result_graph = graph1.copy()

        # Ensure that 'name' attribute exists in both graphs
        if 'name' not in result_graph.vs.attributes() or 'name' not in graph2.vs.attributes():
            raise ValueError("Both graphs must have 'name' attribute for vertices.")

        # Build a dictionary for quick edge weight lookup in graph2
        graph2_edge_weights = {}
        for e in graph2.es:
            source_name = graph2.vs[e.source]['name']
            target_name = graph2.vs[e.target]['name']
            key = (source_name, target_name)
            graph2_edge_weights[key] = e['weight']

        # Subtract weights in result_graph
        edges_to_delete = []
        for e in result_graph.es:
            source_name = result_graph.vs[e.source]['name']
            target_name = result_graph.vs[e.target]['name']
            key = (source_name, target_name)

            # Get the weight to subtract from graph2 if the edge exists
            weight_to_subtract = graph2_edge_weights.get(key, 0)

            # Subtract the weights
            new_weight = e['weight'] - weight_to_subtract

            if new_weight <= 0: # only positive weight
                # Mark edge for deletion
                edges_to_delete.append(e.index)
            else:
                # Update the edge weight
                e['weight'] = new_weight

        # Delete edges with zero or negative weights
        result_graph.delete_edges(edges_to_delete)

        # Remove isolated vertices (nodes with no edges)
        degrees = result_graph.degree()
        isolated_vertices = [idx for idx, deg in enumerate(degrees) if deg == 0]
        result_graph.delete_vertices(isolated_vertices)

        return result_graph

    def get_delta_graph(
        self,
        start=None,
        end=None,
        *,
        dw_normalized=False,
        w_normalized=False,
        invert_weight=False,
        fade_function=None,
        fade_step=None
    ):
        """
        Computes the delta (difference) between two graph states over a time interval.

        Args:
            start (tuple, optional): The starting time point of the interval.
            end (tuple, optional): The ending time point of the interval.
            dw_normalized (bool, optional): Whether to consider normalized weights for delta computation.
                Defaults to False.
            w_normalized (bool, optional): Whether to normalize weights in the resulting graph.
                Defaults to False.
            invert_weight (bool, optional): Whether to invert weights in the resulting graph.
                Defaults to False.
            fade_function (callable, optional): A function to apply fading effects to edge weights.
            fade_step (list or tuple, optional): Steps at which to apply the fading function.

        Returns:
            Graph: The delta graph representing the changes between `start` and `end` time points.
        """
        if dw_normalized or fade_function is not None:
            g1 = self.get_graph(time_point=start, w_normalized=dw_normalized, fade_function=fade_function, fade_step=fade_step)
            g2 = self.get_graph(time_point=end, w_normalized=dw_normalized, fade_function=fade_function, fade_step=fade_step)
            return self.graph_sub(g2, g1)
        else:
            if start is not None and len(start) == len(self._position):
                start = list(start)
                start[-1] += 1

            delta_data = self.take_interval(start=start, end=end)
            if delta_data.empty:
                interval_graph = Graph(directed=self._directed)
            else:
                agg_data = delta_data.groupby(['source', 'target'], as_index=False)['weight'].sum()
                # filter out <= weight
                agg_data = agg_data[agg_data['weight'] > 0]
                if agg_data.empty:
                    return Graph(directed=self._directed)

                nodes = set(agg_data['source']).union(set(agg_data['target']))
                temp_node_to_id = {node: idx for idx, node in enumerate(nodes)}

                agg_data['source_id'] = agg_data['source'].map(temp_node_to_id)
                agg_data['target_id'] = agg_data['target'].map(temp_node_to_id)

                edges = list(zip(agg_data['source_id'], agg_data['target_id']))
                weights = agg_data['weight'].tolist()

                interval_graph = Graph(edges=edges, directed=self._directed)
                interval_graph.vs['name'] = list(temp_node_to_id.keys())
                interval_graph.es['weight'] = weights

            if w_normalized:
                interval_graph = self._normalize_graph_weight(interval_graph)
            if invert_weight:
                interval_graph = self._invert_graph_weight(interval_graph)
            return interval_graph

    def _update_graph(self, graph, data):
        """
        Updates the graph with new data by adding new nodes and edges or updating existing ones.

        Args:
            graph (Graph): The graph to be updated.
            data (pd.DataFrame): The new data containing edge information to update the graph.

        Returns:
            Graph: The updated graph.
        """
        agg_data = data.groupby(['source', 'target'], as_index=False)['weight'].sum()

        # prevent adding 0 weight edges
        agg_data = agg_data[agg_data['weight'] > 0]
        if agg_data.empty:
            return graph

        # Identify existing and new nodes
        existing_nodes = set(graph.vs['name'])
        new_nodes = set(agg_data['source']).union(set(agg_data['target'])) - set(existing_nodes)

        # Add new nodes to the graph and update mappings
        if new_nodes:
            graph.add_vertices(list(new_nodes))
            self._vnames = graph.vs['name']  # Update vertex names
            # Update name to ID mappings starting from the last index
            for idx, node in enumerate(new_nodes, start=len(existing_nodes)):
                self.name_to_id[node] = idx
                self.id_to_name[idx] = node

        # Map source and target names to their respective IDs
        agg_data['source_id'] = agg_data['source'].map(self.name_to_id)
        agg_data['target_id'] = agg_data['target'].map(self.name_to_id)

        # Check if edges already exist
        edges_in_data = list(zip(agg_data['source_id'], agg_data['target_id']))
        whether_edge_exists = graph.get_eids(pairs=edges_in_data, error=False)
        agg_data['eid'] = whether_edge_exists

        # Identify new edges and existing edges to update
        new_edges = agg_data[agg_data['eid'] == -1][['source_id', 'target_id']].values.tolist()
        new_weights = agg_data[agg_data['eid'] == -1]['weight'].tolist()

        existing_edge_ids_to_update = agg_data[agg_data['eid'] != -1]['eid'].tolist()
        weight_updates = agg_data[agg_data['eid'] != -1]['weight'].tolist()

        # existing_edges = graph.get_edgelist()
        # edges_in_data = pd.DataFrame(existing_edges, columns=['source_id', 'target_id'])
        #
        # # merge to identify existing and new edges
        # df_merged = pd.merge(
        #     agg_data,
        #     edges_in_data,
        #     on=['source_id', 'target_id'],
        #     how='left',
        #     indicator=True
        # )
        #
        # df_new_edges = df_merged[df_merged['_merge'] == 'left_only']
        # df_to_update = df_merged[df_merged['_merge'] == 'both']

        # new_edges = list(zip(df_new_edges['source_id'], df_new_edges['target_id']))
        # get those with eid value of -1 for new edges
        # new_weights = df_new_edges['weight'].tolist()
        # edges_to_update = list(zip(df_to_update['source_id'], df_to_update['target_id']))
        # edges to update are those with eid value not equal to -1
        # existing_edge_ids_to_update = graph.get_eids(pairs=edges_to_update, directed=graph.is_directed())
        # weight_updates = df_to_update['weight'].tolist()

        # Add new edges in bulk
        if new_edges:
            graph.add_edges(new_edges)
            # Set weights for new edges
            new_edge_ids = graph.es[-len(new_edges):].indices
            graph.es[new_edge_ids]['weight'] = new_weights

        # Update weights of existing edges in bulk
        if existing_edge_ids_to_update:
            # Retrieve current weights
            current_weights = graph.es[existing_edge_ids_to_update]['weight']
            # Update weights by adding the new weights
            updated_weights = [cw + w for cw, w in zip(current_weights, weight_updates)]
            graph.es[existing_edge_ids_to_update]['weight'] = updated_weights

        # prevent edges with weight <= 0
        edges_to_delete = [e.index for e in graph.es if e['weight'] <= 0]
        if edges_to_delete:
            graph.delete_edges(edges_to_delete)

        return graph

    def take_interval(self, start=None, end=None):
        """
        Retrieves a subset of the data within the specified time interval.

        Args:
            start (list or tuple, optional): The starting bounds of the interval.
            end (list or tuple, optional): The ending bounds of the interval.

        Returns:
            pd.DataFrame: The filtered data within the specified interval.

        Raises:
            ValueError: If the length of `start` or `end` is out of range relative to `position`.
        """
        if start is None:
            start = [-np.inf] * len(self._position)
        else:
            if len(start) < len(self._position):
                start = list(start) + [None] * (len(self._position) - len(start))
            start = [s if s is not None else -np.inf for s in start]

        if end is None:
            end = [np.inf] * len(self._position)
        else:
            if len(end) < len(self._position):
                end = list(end) + [None] * (len(self._position) - len(end))
            end = [e if e is not None else np.inf for e in end]

        if len(self._position) > len(start) or len(self._position) > len(end):
            raise ValueError("The length of 'start/end' is out of range.")

        idx = pd.IndexSlice
        filtered_data = self.data.loc[idx[tuple(start): tuple(end)], :].copy()

        return filtered_data


