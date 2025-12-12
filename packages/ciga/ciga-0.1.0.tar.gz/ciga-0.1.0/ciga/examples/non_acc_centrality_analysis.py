import ciga as cg
import pandas as pd
import matplotlib.pyplot as plt

from viztracer import VizTracer

df = pd.read_csv('../../m_data.csv')

# custom weight function
# input: interaction (str)
# output: weight (float)
def weight_func(interaction):
    # return sid.polarity_scores(interaction)['neg']
    return 1

# tracer = VizTracer()
# tracer.start()

# load data
interactions = cg.prepare_data(df, ('Season', 'Episode', 'Scene', 'Line'),
                                source='Speaker', target='Listener', interaction='Words')
sub_interactions = cg.segment(interactions, start=(1, 1, 1, 1), end=(2, 1, 1, 1))

weights = cg.calculate_weights(sub_interactions, weight_func=weight_func)

agg_weights = cg.agg_weights(weights, ('Season', 'Episode', 'Scene', 'Line'), agg_func=lambda x: sum(x))

# create network
tg = cg.TGraph(data=agg_weights, position=('Season', 'Episode', 'Scene', 'Line'), directed=False)

# centrality analysis
# res = cg.tgraph_eigenvector_centrality(tg, weighted=True, scale=True, return_eigenvalue=False)
res = cg.tgraph_degree(tg, accumulate=False, weighted=True, normalized=True)
# res = cg.tgraph_betweenness(tg, weighted=True, normalized=True)
# res = cg.tgraph_closeness(tg, weighted=True, normalized=True)
res.head()

# tracer.stop()
# tracer.save()

g = tg.get_graph((2, 1, 1, 1))
fig, ax = plt.subplots()
cg.iplot(g, target=ax)
plt.show()
print(g.vcount(), g.ecount())

res.to_csv('non_acc_centrality_res.csv', index=False)