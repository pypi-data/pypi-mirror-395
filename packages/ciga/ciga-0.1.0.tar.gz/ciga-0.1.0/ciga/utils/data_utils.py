import json
import time
from typing import Tuple, Optional, Union, Callable, List
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.signal import lfilter


def _validate_columns(df: pd.DataFrame, columns: List[str]):
    """检查列是否存在"""
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def prepare_data(
        data: pd.DataFrame,
        position: Tuple[str, ...],
        source: str = 'source',
        target: str = 'target',
        interaction: str = 'interaction',
        weight: Optional[str] = None,
):
    """
    Prepare the input data for analysis by validating, sorting, and renaming columns.

    Args:
        data (pd.DataFrame): The input dataframe containing interaction data.
        position (Tuple[str, ...]): Column names used for positional indexing.
        source (str, optional): Name of the source column. Defaults to 'source'.
        target (str, optional): Name of the target column. Defaults to 'target'.
        interaction (str, optional): Name of the interaction column. Defaults to 'interaction'.
        weight (Optional[str], optional): Name of the weight column, if any. Defaults to None.

    Returns:
        pd.DataFrame: The processed dataframe ready for analysis.

    Raises:
        ValueError: If required columns are missing or position columns are not numeric.
    """
    # make a copy, keep original data safe
    df = data.copy().reset_index(drop=True)
    # check required columns
    required_columns = list(position) + [source, target]
    if weight: required_columns.append(weight)
    _validate_columns(df, required_columns)
    # examine data
    _check_numeric_position(df, position)

    # rename columns
    rename_map = {source: 'source', target: 'target'}
    if interaction: rename_map[interaction] = 'interaction'
    if weight: rename_map[weight] = 'weight'
    df = df.rename(columns=rename_map)

    # Process 'source', 'target', 'observer' columns to ensure lists
    df['source'] = _process_column(df['source'])
    df['target'] = _process_column(df['target'])

    if weight:
        df['weight'] = df['weight'].astype(float)
    df = _flatten_weights(df)

    df = df.sort_values(by=list(position)).reset_index(drop=True)

    return df

def segment(data,
            start=None,
            end=None,
            position=None):
    """
    Extract a subset of interactions based on a specified interval.

    Args:
        data (pd.DataFrame): The dataframe containing interaction data.
        start (tuple, optional): The starting position of the interval. Defaults to None.
        end (tuple, optional): The ending position of the interval. Defaults to None.
        position (tuple, optional): Column names used for positional indexing. Required if multi-indexing is needed. Defaults to None.

    Returns:
        pd.DataFrame: A dataframe containing interactions within the specified interval.

    Raises:
        ValueError: If multi-level time steps are required but position columns are not provided.
    """
    if position is None:
        raise ValueError("Must provide 'position' column names for segmentation.")
    _validate_columns(data, list(position))
    df_temp = data.copy().set_index(list(position)).sort_index()
    idx = pd.IndexSlice
    try:
        return df_temp.loc[idx[start:end], :].reset_index()
    except KeyError:
        raise KeyError(f"Interval {start}-{end} not found. Ensure data is sorted.")


def calculate_weights(data,
                      weight_func=lambda x: len(x)):
    """
    Calculate weights for each interaction based on a provided weight function.

    Args:
        data (pd.DataFrame): The dataframe containing interaction data.
        weight_func (Callable, optional): A function that takes an interaction entry and returns a numerical weight. Defaults to lambda x: len(x).

    Returns:
        pd.DataFrame: The dataframe with an added 'weight' column and flattened weights.
    """
    _validate_columns(data, ['interaction'])
    df = data.copy()
    # work on interactions
    unique_interactions = df['interaction'].unique()
    weight_map = {text: weight_func(text) for text in unique_interactions}
    df['weight'] = df['interaction'].map(weight_map)
    return df

def _flatten_weights(df):
    """
    Expand the dataframe so that each source-target pair has its own row.

    This is useful when the 'source' and 'target' columns contain lists,
    ensuring that each interaction is represented as a single row.

    Args:
        df (pd.DataFrame): The dataframe with potential list-like 'source' and 'target' columns.

    Returns:
        pd.DataFrame: The exploded dataframe with individual source-target pairs.
    """
    return df.explode('source').explode('target')


def agg_weights(data,
                position,
                agg_func: Union[str, Callable] = 'sum'):
    """
    Aggregate weights by grouping interactions based on positional columns and source-target pairs.

    Args:
        data (pd.DataFrame): The dataframe containing interaction data with weights.
        position (Tuple[str, ...]): Column names used for positional indexing (excluding the line identifier).
        agg_func (Union[str, Callable], optional): The aggregation function to apply to the weights.
            Can be a string like 'sum', 'mean', 'max', 'min', or a callable. Defaults to 'sum'.

    Returns:
        pd.DataFrame: The aggregated dataframe with summed weights for each group.

    Raises:
        ValueError: If the 'weight' column is missing from the dataframe.
    """
    cols = list(position) + ['source', 'target', 'weight']
    _validate_columns(data, cols)
    grouped = data.groupby(list(position) + ['source', 'target'])['weight'].agg(agg_func)
    return grouped.reset_index()

def _process_column(series):
    """
    Process a dataframe column to ensure each cell contains a list of unique, stripped string items.

    Args:
        series (pd.Series): The column to process.

    Returns:
        pd.Series: The processed column with each cell as a list of unique, stripped strings.
    """
    def clean_cell(cell):
        if isinstance(cell, list):
            items = cell
        elif isinstance(cell, str):
            items = [item.strip() for item in cell.strip('[]').split(',')]
        else:
            items = [str(cell).strip()]
        # return np.unique([str(item).strip() for item in items])
        return np.unique([str(item).strip() for item in items if str(item).strip()])
    return series.apply(clean_cell)

# get accumulate data
def accumulate_weights(
        data: pd.DataFrame,
        decay: float = 0.0,
        decay_mode: str = 'exponential',  # 'exponential' | 'power_law' | 'linear'
        accum_mode: str = 'auto',  # 'auto' | 'recursive' | 'convolution'
        ltm_rate: float = 1.0,
        time: Optional[str] = None,
        position: Optional[Tuple[str, ...]] = None
) -> pd.DataFrame:
    """
    权重累积函数。

    支持两种计算内核 (accum_mode)：
    1. 滚雪球模式 (recursive): 递归计算 S_t = S_{t-1} * (1-decay) + X_t
       - 特点：拥有“状态记忆”，计算效率高 O(N)。
       - 适用：Exponential 衰减。

    2. 直接叠加模式 (convolution): 卷积计算 S_t = Sum(X_{t-k} * Kernel(k))
       - 特点：事件独立衰减后叠加，计算复杂度较高 O(N*Window)。
       - 适用：Power Law, Linear 等非马尔可夫衰减，或需要回溯修改历史的场景。

    参数:
        data: 输入 DataFrame
        decay: 衰减率 (0~1)
        mode: 衰减函数形状 ('exponential', 'power_law', 'linear')
        accum_mode: 指定累计模式 ('recursive', 'convolution', 'auto')
                    'auto' 下会自动根据 decay mode 选择最优算法。
        ltm_rate: 长期记忆保留率 (Long Term Memory)，即由 cumsum 贡献的比例
        time: 时间列名 (Time 模式)
        position: 定义位置/场次的列名列表 (Position 模式)
    """
    # --- 1. 基础校验 ---
    if position is None:
        raise ValueError("Must provide 'position' columns.")

    pos_cols = list(position)
    required = pos_cols + ['source', 'target', 'weight']
    if time:
        if time not in data.columns:
            raise ValueError(f"Time column '{time}' not found in data.")
        required.append(time)

    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if decay_mode == 'exponential' and not (0 <= decay < 1):
        raise ValueError("Exponential decay must be in [0, 1).")
    if ltm_rate < 0:
        raise ValueError("ltm_rate must be >= 0.")

    if accum_mode == 'auto':
        accum_mode = 'recursive' if decay_mode == 'exponential' else 'convolution'

    # --- 2. 统一构建“计算轴” ---
    df = data.copy().reset_index(drop=True)
    temp_axis_col = '_calc_axis_'

    # 保存原始的时间/位置映射关系
    axis_metadata_map = None

    if time:
        # === Time 模式 ===
        if not pd.api.types.is_integer_dtype(df[time]):
            df[temp_axis_col] = df[time].astype(int)
        else:
            df[temp_axis_col] = df[time]
        axis_metadata_map = df[[temp_axis_col] + pos_cols].drop_duplicates(subset=[temp_axis_col])
    else:
        # === Position 模式 ===
        unique_pos = df[pos_cols].drop_duplicates().sort_values(by=pos_cols)
        unique_pos['_rank'] = np.arange(len(unique_pos))

        df = df.merge(unique_pos, on=pos_cols, how='left')
        df[temp_axis_col] = df['_rank']
        axis_metadata_map = unique_pos.rename(columns={'_rank': temp_axis_col})

    # --- 3. 预聚合 ---
    group_keys = ['source', 'target', temp_axis_col]
    df_agg = df.groupby(group_keys)['weight'].sum().reset_index()

    # --- 4. 构建全量骨架 ---
    min_t, max_t = df_agg[temp_axis_col].min(), df_agg[temp_axis_col].max()
    full_axis_index = np.arange(min_t, max_t + 1)

    # --- 5. 定义计算内核 ---
    def process_pair(group):
        s_series = group.set_index(temp_axis_col)['weight']
        s_expanded = s_series.reindex(full_axis_index, fill_value=0.0)
        vals = s_expanded.values

        stm = np.zeros_like(vals, dtype=float)

        if decay == 0:
            stm = np.cumsum(vals)
        elif accum_mode == 'recursive':
            if decay_mode != 'exponential':
                raise ValueError(f"Conflict: 'recursive' supports only 'exponential'. Got '{decay_mode}'.")
            stm = lfilter([1.0], [1.0, -(1.0 - decay)], vals)
        elif accum_mode == 'convolution':
            lags = np.arange(len(vals))
            kernel = np.zeros_like(vals, dtype=float)
            if decay_mode == 'exponential':
                kernel = (1.0 - decay) ** lags
            elif decay_mode == 'power_law':
                kernel = (lags + 1.0) ** (-decay)
            elif decay_mode == 'linear':
                kernel = np.maximum(0.0, 1.0 - decay * lags)
            stm = np.convolve(vals, kernel, mode='full')[:len(vals)]

        final_weights = stm
        if ltm_rate > 0:
            final_weights += (np.cumsum(vals) * ltm_rate)

        # 把计算结果填回 Series
        s_expanded[:] = final_weights
        return s_expanded

    # --- 6. 并行应用 ---
    desc_str = f"Accumulating [Mode: {decay_mode} | Algo: {accum_mode}]"
    tqdm.pandas(desc=desc_str)

    # 这里的 result_obj 可能是 Series (Long) 也可能是 DataFrame (Wide)
    result_obj = df_agg.groupby(['source', 'target'])[group_keys + ['weight']].progress_apply(process_pair)

    # --- 7. 重组与合并 (关键修复！) ---

    # 检测：如果 Pandas 自动把它变成了宽表 (DataFrame)，我们需要把它折叠 (Stack) 回去
    if isinstance(result_obj, pd.DataFrame):
        # 此时 columns 是 0, 1, 2... (时间步)，Index 是 (source, target)
        # stack() 后变成 MultiIndex Series: (source, target, time)
        result_obj = result_obj.stack()

    # 现在 result_obj 肯定是一个 Series 了
    result_df = result_obj.reset_index()

    # 强制重命名列，确保万无一失
    # 此时列顺序必然是: [source, target, time_axis, value]
    # 有时候 index 会多出 level_n，但在 stack+reset 后通常很干净
    if len(result_df.columns) == 4:
        result_df.columns = ['source', 'target', temp_axis_col, 'weight']
    else:
        raise KeyError(f"Unexpected columns structure after stack/reset: {result_df.columns}")

    # --- 8. 恢复元数据 ---
    if axis_metadata_map is not None:
        df_final = result_df.merge(axis_metadata_map, on=temp_axis_col, how='left')
    else:
        df_final = result_df

    df_final = df_final.drop(columns=[temp_axis_col, '_rank'], errors='ignore')

    final_cols = ['source', 'target', 'weight'] + pos_cols
    if time and time in df_final.columns and time not in final_cols:
        final_cols.append(time)

    valid_cols = [c for c in final_cols if c in df_final.columns]

    return df_final[valid_cols].sort_values(by=pos_cols).reset_index(drop=True)

def _check_numeric_position(data, position):
    """
    Validate that all position columns contain numeric data types.

    Args:
        data (pd.DataFrame): The dataframe containing position columns.
        position (Tuple[str, ...]): Column names used for positional indexing.

    Raises:
        ValueError: If any position column does not have a numeric data type.
    """
    # check required columns
    for col in position:
        if not pd.api.types.is_numeric_dtype(data[col]):
            raise ValueError(f"Position column '{col}' must be numeric.")

# Infer listener LLM

def generate_prompt(scene_data):
    """
    Generate a formatted prompt for the language model to identify listeners in dialogue lines.

    Args:
        scene_data (Dict[str, Any]): A dictionary containing scene descriptions and dialogue lines.

    Returns:
        str: A formatted prompt string to be sent to the language model.
    """
    prompt = f"""
    Scene Description: {scene_data['Scene_Description']}

    Dialogue Lines:
    """
    for line in scene_data['Lines']:
        prompt += f"Line {line['Line_ID']} - {line['Speaker']}: \"{line['Line']}\"\n"

    prompt += """
    For each line, identify the listeners from the characters present. Provide the results in JSON format only, following this exact structure:

    {
      "listeners": {
        "1": ["Listener1", "Listener2"],
        "2": ["Listener3"],
        ...
      }
    }
    """

    # print(">> prompt:\n", prompt)

    return prompt


def infer_scene_listeners(client, model_name, prompt, *, mode="openai", max_tokens=200):
    """
    Use a language model to infer listeners for each dialogue line in a scene.

    Args:
        client: The API client for interacting with the language model.
        model_name (str): The name of the language model to use.
        prompt (str): The prompt string generated for the language model.
        mode (str, optional): The service provider ("openai" or "anthropic"). Defaults to "openai".
        max_tokens (int, optional): The maximum number of tokens for the response. Defaults to 200.

    Returns:
        Dict[str, List[str]]: A dictionary mapping line IDs to lists of listeners.

    Notes:
        - Ensures the response is valid JSON and adheres to the expected structure.
        - Implements error handling for JSON decoding and other exceptions.
    """
    listeners_json = ""
    listeners_data = {}
    try:
        if mode == "openai":
            import openai
            response = client.chat.completions.create(
                # model="gpt-4o-mini",
                model=model_name,
                messages=[
                    {"role": "system",
                     "content": "You are an assistant that identifies listeners for each line in a conversation. Respond only with JSON following the specified format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0.3
            )
            # print(">> response:\n", response)
            # print(">> response.choices[0].message.content:\n", response.choices[0].message.content)
            listeners_json = response.choices[0].message.content

            # Validate that the response is proper JSON and matches the expected structure
            listeners_data = json.loads(listeners_json)
        elif mode == "anthropic":
            import anthropic
            response = client.messages.create(
                model=model_name,
                messages=[
                    {"role": "user",
                     "content": "You are an assistant that identifies listeners for each line in a conversation. Respond only with JSON following the specified format.\n" + prompt}
                ],
                max_tokens=max_tokens
            )
            # print(">> response:\n", response)
            # print(">> response.choices[0].message.content:\n", response.content[0].text)
            listeners_data = json.loads(response.content[0].text)
        if "listeners" in listeners_data and isinstance(listeners_data["listeners"], dict):
            return listeners_data["listeners"]
        else:
            print("JSON response does not match the expected format.")
            return {}
    except json.JSONDecodeError:
        print("Failed to decode JSON. Response was:", listeners_json)
        return {}
    except Exception as e:
        print(f"Error inferring listeners for scene: {e}")
        return {}

def infer_listeners(data: pd.DataFrame,
                    position: Tuple[str, ...],
                    speaker: str = 'speaker',
                    dialogue: str = 'dialogue',
                    action: Optional[str] = None,
                    scene_description: Optional[str] = None,
                    client: Optional = None,
                    model: Optional[str] = None,
                    mode: str = "openai",
                    max_tokens: int = 200,
                    gap: float = 1.0
                    ) -> pd.DataFrame:
    """
    Infer listeners for each dialogue line across different scenes using a language model.

    Args:
        data (pd.DataFrame): The dataframe containing interaction data.
        position (Tuple[str, ...]): Column names used for positional indexing.
        speaker (str, optional): Name of the speaker column. Defaults to 'speaker'.
        dialogue (str, optional): Name of the dialogue column. Defaults to 'dialogue'.
        action (Optional[str], optional): Name of the action notes column. Defaults to None.
        scene_description (Optional[str], optional): Name of the scene description column. Defaults to None.
        client (Optional, optional): The API client for interacting with the language model. Defaults to None.
        model (Optional[str], optional): The name of the language model to use. Defaults to None.
        mode (str, optional): The service provider ("openai" or "anthropic"). Defaults to "openai".
        max_tokens (int, optional): The maximum number of tokens for the response. Defaults to 200.
        gap (float, optional): Delay between API requests to prevent rate limiting. Defaults to 1.0.

    Returns:
        pd.DataFrame: The dataframe with an added 'listener' column containing inferred listeners.

    Raises:
        ValueError: If required columns are missing or position columns are not numeric.
    """
    required_columns = list(position) + [speaker, dialogue]
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"""Missing required columns.\nExpected: {required_columns}\nFound: {data.columns.tolist()}""")

    _check_numeric_position(data, position)
    df = data.sort_values(by=list(position)).reset_index(drop=True)

    df = df.rename(columns={speaker: 'speaker'})
    if dialogue:
        df = df.rename(columns={dialogue: 'dialogue'})
    else:
        df['dialogue'] = None
    if action:
        df = df.rename(columns={action: 'action'})
    else:
        df['action'] = None
    if scene_description:
        df = df.rename(columns={scene_description: 'scene_description'})
    else:
        df['scene_description'] = None

    # Process 'source', 'target', 'observer' columns to ensure lists
    df['speaker'] = _process_column(df['speaker'])

    # print(df)
    # check data type of speaker column elements
    # print(df.iloc[0]['speaker'])
    # print(type(df.iloc[0]['speaker']))

    # return

    grouped = df.groupby(list(position[:-1]))
    scene_json = []
    df['listener'] = None
    # use tqdm for progress bar
    # for scene_number, group in grouped
    for scene_number, group in tqdm(grouped, desc='Processing scenes', unit='scene'):
        # print(">> scene_number:", scene_number)
        # print(">> group:\n", group)
        scene_data = {
            "Scene_Description": group['scene_description'].iloc[0],
            "Lines": [
                {
                    "Line_ID": int(row[position[-1]]),
                    "Speaker": list(row['speaker']),
                    "Line": row['dialogue'],
                    "Action_Notes": row['action']
                }
                for _, row in group.iterrows()
            ]
        }
        # print(">> scene_data before inference:\n", json.dumps(scene_data, indent=4))

        # Infer listeners for the entire scene
        prompt = generate_prompt(scene_data)
        listeners = infer_scene_listeners(client, model, prompt, mode=mode, max_tokens=max_tokens)

        # Assign listeners to each line
        for line in scene_data["Lines"]:
            line_id = line["Line_ID"]
            line["Listeners"] = listeners.get(str(line_id), [])
            # for row with column position[-1] == line_id, assign listeners
            df.loc[(df[list(position[:-1])].eq(scene_number)).all(axis=1) &
                   (df[position[-1]] == line_id), 'listener'] = str(line["Listeners"])

        # print(">> scene_data after inference:\n", json.dumps(scene_data, indent=4))
        scene_json.append(scene_data)
        time.sleep(gap)  # Adjust delay as needed
    return df

