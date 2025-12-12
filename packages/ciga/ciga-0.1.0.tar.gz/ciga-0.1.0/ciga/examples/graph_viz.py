"""
Example: Single Graph Visualization

This example demonstrates how to create and visualize a single graph
using the graph_viz function with clean black-and-white style.
"""
import ciga as cg
import pandas as pd
import os

# Load data
data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'm_data.csv')
df = pd.read_csv(data_path)

# Prepare data
interactions = cg.prepare_data(df, ('Season', 'Episode', 'Scene', 'Line'),
                               source='Speaker', target='Listener', interaction='Words')

# Segment to a specific time range
sub_interactions = cg.segment(interactions, start=(1, 1, 1, 1), end=(2, 1, 1, 1))

# Calculate weights (1 per interaction)
weights = cg.calculate_weights(sub_interactions, weight_func=lambda x: 1)

# Aggregate weights
agg_weights = cg.agg_weights(weights, ('Season', 'Episode', 'Scene', 'Line'), agg_func='sum')

# Create TGraph and extract a single graph
tg = cg.TGraph(data=agg_weights, position=('Season', 'Episode', 'Scene', 'Line'), directed=True)
graph = tg.get_graph((2, 1, 1, 1), accumulate=True)

print(f"Graph: {graph.vcount()} nodes, {graph.ecount()} edges")

# Visualize with graph_viz (saves HTML file)
cg.graph_viz(graph, output_file='graph.html')
print("Graph saved to graph.html")
