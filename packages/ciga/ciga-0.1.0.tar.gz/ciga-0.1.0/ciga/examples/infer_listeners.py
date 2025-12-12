import ciga as cg
import pandas as pd
import anthropic

df = pd.DataFrame({
    'season': [1, 1, 1, 1, 1],
    'episode': [1, 1, 1, 1, 1],
    'scene': [1, 1, 1, 2, 2],
    'line': [1, 2, 3, 1, 2],
    'source': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob'],
    'dialogue': ['Hi Bob', 'Hello Alice', 'Hey everyone', 'Good morning', 'Morning Alice'],
    'action': ['Waive hand', 'Smile', '', 'Smile', 'Waive hand'],
    'scene_description': ['In the room', 'In the room', 'In the room', 'In the room', 'In the room']
})

anthropic_client = anthropic.Anthropic(api_key="")
result = cg.infer_listeners(data=df,
                            position=('season', 'episode', 'scene', 'line'),
                            speaker='source',
                            dialogue='dialogue',
                            action='action',
                            scene_description='scene_description',
                            client=anthropic_client,
                            mode='anthropic',
                            model='claude-3-5-haiku-latest',
                            max_tokens=200,
                            gap=0.5)
print(result)
# result.to_csv('inferred_listeners.csv', index=False)