import ciga as cg
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./BB_F4_with_speakers_listeners.csv")

def weight_func(interaction):
    return 1

position = ('Scene', 'Shot', 'Line')
interactions = cg.prepare_data(data=df,
                               position=position,
                               source='Speaker', 
                               target='Listener', 
                               interaction='transcripts')

sub_interactions = cg.segment(interactions, start=(1, 1, 1), end=(2, 1, 1))
weights = cg.calculate_weights(sub_interactions, weight_func)
agg_weights = cg.agg_weights(data=weights, 
                             position=position[:-1], 
                             agg_func=lambda x: sum(x))

tg = cg.TGraph(data=agg_weights, 
               position=position[:-1], 
               directed=False)

graph = tg.get_graph((2, 1))
fig, ax = plt.subplots()
cg.iplot(graph, target=ax)
plt.show()

res = cg.tgraph_degree(tg, weighted=True, normalized=True)

# res.to_csv('results.csv')