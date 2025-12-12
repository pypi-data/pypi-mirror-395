import ciga as cg
import pandas as pd
import os

# 使用更丰富的数据集 (包含 Season, Episode, Scene, Line)
data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'm_data.csv')
df = pd.read_csv(data_path)

# 准备数据 - 使用完整的四层时间索引
interactions = cg.prepare_data(df, ('Season', 'Episode', 'Scene', 'Line'),
                                source='Speaker', target='Listener', interaction='Words')
weights = cg.calculate_weights(interactions, weight_func=lambda x: 1)
agg_weights = cg.agg_weights(weights, ('Season', 'Episode', 'Scene', 'Line'), agg_func='sum')

# 创建 TGraph
tg = cg.TGraph(data=agg_weights, position=('Season', 'Episode', 'Scene', 'Line'), directed=True)
print(f"Data loaded: {len(df)} rows, {len(agg_weights)} aggregated interactions")

# 启动交互式可视化
server = cg.tgraph_viz(tg, port=8055, blocking=True)

# 保持服务器运行 (按 Ctrl+C 停止)
# import time
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("\nShutting down...")
#     server.shutdown()
#     print("Server stopped.")