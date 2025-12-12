import pytest
import pandas as pd
import igraph as ig

import ciga as cg
from ciga import prepare_data


@pytest.fixture
def no_weight_sample_data():
    return pd.DataFrame({
        'Season': [1, 1, 1, 1],
        'Episode': [1, 1, 1, 1],
        'Scene': [1, 1, 2, 2],
        'Line': [1, 2, 1, 2],
        'Speaker': ['Sheldon', 'Leonard', 'Penny', 'Sheldon'],
        'Listener': ['Leonard', 'Sheldon', 'Sheldon', 'Penny'],
        'Words': ['Hello', 'Hi there', 'How are you?', 'Fine, thank you']
    })

@pytest.fixture
def weight_sample_data():
    return pd.DataFrame({
        'Season': [1, 1, 1, 1],
        'Episode': [1, 1, 1, 1],
        'Scene': [1, 1, 2, 2],
        'Line': [1, 2, 1, 2],
        'Speaker': ['Sheldon', 'Leonard', 'Penny', 'Sheldon'],
        'Listener': ['Leonard', 'Sheldon', 'Sheldon', 'Penny'],
        'Words': ['Hello', 'Hi there', 'How are you?', 'Fine, thank you'],
        'Weights': [5, 8, 12, 15]
    })


def test_ciga_initialization(weight_sample_data):
    print(type(weight_sample_data))
    df = cg.prepare_data(data=weight_sample_data,
                                   position=('Season', 'Episode', 'Scene', 'Line'),
                                   source='Speaker',
                                   target='Listener',
                                   interaction='Words',
                                   weight='Weights')
    tg = cg.TGraph(data = df,
                    position = ('Season', 'Episode', 'Scene', 'Line'),
                    directed = False)
    assert tg.data is not None
    assert len(tg._position) == 4
    assert tg._position == ('Season', 'Episode', 'Scene', 'Line')


def test_get_weights(no_weight_sample_data):
    df = prepare_data(data = no_weight_sample_data,
                        position = ('Season', 'Episode', 'Scene', 'Line'),
                        source = 'Speaker',
                        target = 'Listener',
                        interaction = 'Words')
    weighted_df = cg.calculate_weights(df, lambda x: len(x))
    tg = cg.TGraph(data = weighted_df,
                   position = ('Season', 'Episode', 'Scene', 'Line'))
    assert 'weight' in tg.data.columns
    assert tg.data['weight'].tolist() == [5, 8, 12, 15]


def test_get_interval(weight_sample_data):
    df = cg.prepare_data(data=weight_sample_data,
                         position=('Season', 'Episode', 'Scene', 'Line'),
                         source='Speaker',
                         target='Listener',
                         interaction='Words',
                         weight='Weights')
    tg = cg.TGraph(data = df,
                   position = ('Season', 'Episode', 'Scene', 'Line'),
                   directed = False)
    subset = tg.take_interval((1, 1, 1, 1), (1, 1, 2, 1))
    assert len(subset) == 3


def test_agg_weights(weight_sample_data):
    df = cg.prepare_data(data=weight_sample_data,
                         position=('Season', 'Episode', 'Scene', 'Line'),
                         source='Speaker',
                         target='Listener',
                         interaction='Words',
                         weight='Weights')
    agg_df = cg.agg_weights(data=df,
                   position=('Season', 'Episode', 'Scene'),
                   agg_func=lambda x: sum(x))
    tg = cg.TGraph(data = agg_df,
                   position = ('Season', 'Episode', 'Scene'),
                   directed = False)
    print(tg.data.columns)
    assert len(tg.data) == 4
    assert tg._position == ('Season', 'Episode', 'Scene')


def test_get_graph(weight_sample_data):
    df = cg.prepare_data(data=weight_sample_data,
                         position=('Season', 'Episode', 'Scene', 'Line'),
                         source='Speaker',
                         target='Listener',
                         interaction='Words',
                         weight='Weights')
    tg = cg.TGraph(data = df,
                   position = ('Season', 'Episode', 'Scene', 'Line'),
                   directed = True)
    graph = tg.get_graph()
    assert isinstance(graph, ig.Graph)
    assert graph.vcount() == 3
    assert graph.ecount() == 4

