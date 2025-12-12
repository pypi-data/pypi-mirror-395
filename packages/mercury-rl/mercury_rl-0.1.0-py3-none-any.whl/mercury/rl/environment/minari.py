import pandas as pd
import numpy as np
from minari import (create_dataset_from_buffers, list_local_datasets,
                    delete_dataset)
from minari.data_collector.episode_buffer import EpisodeBuffer
from minari.dataset.step_data import StepData


def create_minari_dataset_from_df(
    df: pd.DataFrame,
    dataset_id: str,
    observation_space,
    action_space,
    env_spec: str | None = None,
    algorithm_name: str | None = None,
    author: str | None = None,
    description: str | None = None,
    overwrite: bool = True,
):
    """
    Creates a Minari dataset from a pandas DataFrame with
    per-step environment data.
    """
    if overwrite and dataset_id in list_local_datasets():
        print(f"⚠️ Dataset '{dataset_id}' already exists. Deleting it.")
        delete_dataset(dataset_id)

    episode_buffers = []
    for idx, (_, group) in enumerate(df.groupby("episode_id")):
        buffer = EpisodeBuffer(id=idx)

        for _, row in group.iterrows():
            step = StepData(
                observation=np.array(row["obs"], dtype=np.float32),
                action=row["action"],
                reward=row["reward"],
                terminated=row["terminated"],
                truncated=row["truncated"],
                info=row["info"],
            )
            buffer = buffer.add_step_data(step)

        episode_buffers.append(buffer)

    create_dataset_from_buffers(
        dataset_id=dataset_id,
        buffer=episode_buffers,
        env=env_spec,
        observation_space=observation_space,
        action_space=action_space,
        algorithm_name=algorithm_name,
        author=author,
        description=description,
    )

    print(f"✅ Dataset '{dataset_id}' created successfully.")
