from PIL import Image, ImageDraw, ImageFont
import minari
import os
import numpy as np


DIRECTION_NAMES = {
    0: "right",
    1: "down",
    2: "left",
    3: "up"
}

def compress_state(observation: dict) -> tuple:
    image_key = tuple(observation["image"].flatten().tolist())  # avoid NumPy comparison issues
    mission_key = observation["mission"]
    direction_key = observation["direction"]

    if isinstance(mission_key, bytes):  # decode byte strings if needed
        mission_key = mission_key.decode("utf-8")
    if isinstance(direction_key, np.integer):
        direction_key = int(direction_key)

    return (image_key, mission_key, direction_key)


def annotate_frame(frame, direction, mission, action=None, font=None):
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)
    direction_name = DIRECTION_NAMES.get(direction, str(direction))
    draw.text((8, 8), f"Mission: {mission}", font=font, fill="white")
    draw.text((8, 40), f"Direction: {direction_name}", font=font, fill="white")
    if action:
        draw.text((8, 72), f"Action: {action}", font=font, fill="white")
    return img


def generate_extreme_value_state_image(
    dataset_id,
    output_path,
    value_fn_generator,
    highest
):
    """
    Generate an image of the state with the highest (or lowest) value according to a given value function generator.

    Parameters
    ----------
    dataset_id : str
        The Minari dataset ID.

    output_path : str
        Path to save the annotated image.

    value_fn_generator : callable
        A function that takes a dataset_id and returns (V, state_locations):
            - V: dict mapping state keys to estimated value
            - state_locations: dict mapping state keys to (episode_idx, time_step)

    highest : bool
        If True, pick the highest-valued state. If False, pick the lowest.
    """
    dataset = minari.load_dataset(dataset_id)
    V, state_locations = value_fn_generator(dataset_id)

    # Select the most extreme state
    if highest:
        selected_state_key, _ = max(V.items(), key=lambda item: item[1])
    else:
        selected_state_key, _ = min(V.items(), key=lambda item: item[1])

    if selected_state_key not in state_locations:
        raise ValueError("State key not found in recorded state locations.")

    episode_idx, step_idx = state_locations[selected_state_key]
    episode = list(dataset.iterate_episodes())[episode_idx]
    metadata = next(dataset.storage.get_episode_metadata([episode_idx])) # type: ignore

    env = dataset.recover_environment(render_mode="rgb_array")
    env.reset(seed=metadata.get("seed"), options=metadata.get("options"))

    for i in range(step_idx):
        env.step(episode.actions[i])

    frame = env.render()
    obs = {
        "image": episode.observations["image"][step_idx],
        "mission": episode.observations["mission"][step_idx],
        "direction": episode.observations["direction"][step_idx],
    }

    font = ImageFont.load_default(size=38)

    mission = obs["mission"]
    if isinstance(mission, bytes):
        mission = mission.decode("utf-8")

    img = annotate_frame(frame, direction=obs["direction"], mission=mission, font=font)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)


def generate_extreme_value_state_image_from_q_table(
    dataset_id,
    output_path,
    q_fn_generator,
    highest=True
):
    """
    Generate an image of the state with the highest (or lowest) value from a Q-table.

    Parameters
    ----------
    dataset_id : str
        The Minari dataset ID.

    output_path : str
        Path to save the annotated image.

    q_fn_generator : callable
        A function that takes a dataset_id and returns:
            - Q: dict mapping (state_key, action) to Q-value
            - state_locations: dict mapping state_key to (episode_idx, time_step)

    highest : bool
        If True, select the state with the highest max Q-value. If False, select the lowest.
    """
    
    dataset = minari.load_dataset(dataset_id)
    Q, state_locations = q_fn_generator(dataset_id)

    # Convert Q(s, a) into V(s) = max_a Q(s, a), and track best action
    V = {} # Maps state_key to max Q-value
    best_actions = {} # Maps state_key to best action (policy)
    for (s, a), q in Q.items():
        if s not in V or q > V[s]:
            V[s] = q
            best_actions[s] = a

    # Select state with extreme value -> s = argmax_s V(s) or argmin_s V(s)
    selected_state_key = max(V.items(), key=lambda item: item[1])[0] if highest else min(V.items(), key=lambda item: item[1])[0] #item[1] = V[s]
    best_action = best_actions[selected_state_key]
    print(f"Selected state: {selected_state_key}, Best action: {best_action}")

    if selected_state_key not in state_locations:
        raise ValueError("State key not found in recorded state locations.")

    # Get the episode index and step index for the selected state
    episode_idx, step_idx = state_locations[selected_state_key]
    episode = list(dataset.iterate_episodes())[episode_idx]
    metadata = next(dataset.storage.get_episode_metadata([episode_idx]))  # type: ignore

    env = dataset.recover_environment(render_mode="rgb_array")
    env.reset(seed=metadata.get("seed"), options=metadata.get("options"))

    for i in range(step_idx):
        env.step(episode.actions[i])

    frame = env.render()
    obs = {
        "image": episode.observations["image"][step_idx],
        "mission": episode.observations["mission"][step_idx],
        "direction": episode.observations["direction"][step_idx],
    }

    font = ImageFont.load_default(size=38)

    mission = obs["mission"]
    if isinstance(mission, bytes):
        mission = mission.decode("utf-8")

    # Updated annotate_frame to show the selected action
    img = annotate_frame(
        frame,
        direction=obs["direction"],
        mission=mission,
        action=best_action,
        font=font,
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
