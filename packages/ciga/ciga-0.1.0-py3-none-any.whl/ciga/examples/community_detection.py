import ciga as cg
import pandas as pd
from viztracer import VizTracer

df = pd.read_csv('../../m_data.csv')


# custom weight function
# input: interaction (str)
# output: weight (float)
def weight_func(interaction):
    return 1

# tracer = VizTracer()
# tracer.start()

# load data with weight
# weights = cg.prepare_data(df, ('Season', 'Episode', 'Scene', 'Line'),
#                           source='Speaker', target='Listener', interaction='Words', weight='weight')

# load data without weight
interactions = cg.prepare_data(df, ('Season', 'Episode', 'Scene', 'Line'),
                                source='Speaker', target='Listener', interaction='Words')
sub_interactions = cg.segment(interactions, start=(1, 1, 1, 1), end=(2, 1, 1, 1))

# calculate weight
weights = cg.calculate_weights(sub_interactions, weight_func=weight_func)

# adjust grain size
agg_weights = cg.agg_weights(weights, ('Season', 'Episode', 'Scene', 'Line'), agg_func=lambda x: sum(x))

# create network
tg = cg.TGraph(data=agg_weights, position=('Season', 'Episode', 'Scene', 'Line'), directed=False)

communities = cg.tgraph_community_leiden(tg, start=(1, 1, 1, 1), end=(2, 1, 1, 1), weights='weight', objective_function='CPM')

# tracer.stop()
# tracer.save()

communities.to_csv('community_test.csv', index=False)