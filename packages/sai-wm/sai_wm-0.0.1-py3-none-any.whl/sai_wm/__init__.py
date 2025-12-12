from os import path
from gymnasium import register
import yaml
import logging

__version__ = "0.1.13"

def validate_robot_config(robot_config):
    if isinstance(robot_config, list):
        return all(validate_robot_config(cfg) for cfg in robot_config)
    return "control_freq" in robot_config


def register_envs_v0():
    dir_path = path.dirname(path.realpath(__file__))
    with open(f"{dir_path}/config/registry_v0.yaml", "r") as f:
        env_config = yaml.safe_load(f)

    world_model_entry_points = {r["name"]: r["entry_point"] for r in env_config["world_models"]}

    for env in env_config["environments"]:
        env_name = env["name"]
        entry_point = env["entry_point"]
        world_model = env["world_model"]
        base_env_name = env["base_env_name"]
        for world_model_entry in world_model:
            for world_model_name, world_model_config in world_model_entry.items():
                wm_env = "".join(world_model_name.title().split("_")[:])
                max_episode_steps = env.get("max_episode_steps", None)
                assert max_episode_steps is not None, (
                    f"max_episode_steps must be specified in the environment config for {env_name} "
                )
                env_id = f"{wm_env}{env_name}"
                env_config = {}
                world_config = {}
                env_config["env_name"] = env_name
                env_config["base_env_name"] = base_env_name
                env_config["use_base_env"] = world_model_config.get("use_base_env", True)
                
                world_config["wm_name"] = world_model_name
                world_config["dream"] = world_model_config.get("dream", True)
                world_config["repo_id"] = world_model_config["repo_id"]
                world_config["model_file"] = world_model_config["model_file"]

                kwargs = {
                    "env_config": env_config,
                    "world_config": world_config,
                    "world_model_entry_points": world_model_entry_points,
                }

                register(
                    id=env_id,
                    entry_point=entry_point,
                    kwargs=kwargs,
                    max_episode_steps=max_episode_steps,
                )

register_envs_v0()
