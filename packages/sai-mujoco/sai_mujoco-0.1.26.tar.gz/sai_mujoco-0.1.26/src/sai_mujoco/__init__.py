from os import path
from gymnasium import register
import yaml
import logging

__version__ = "0.1.13"

def validate_robot_config(robot_config):
    if isinstance(robot_config, list):
        return all(validate_robot_config(cfg) for cfg in robot_config)
    return "control_freq" in robot_config

register(
    id="InvertedPendulumWheel-v0",
    entry_point="sai_mujoco.envs.wheeled_inverted_pendulum.wheeled_inverted_pendulum_v0:InvertedPendulumWheelEnv_v0",
    kwargs={},
)


def register_envs_v0(registry_name: str):
    dir_path = path.dirname(path.realpath(__file__))
    with open(f"{dir_path}/config/{registry_name}.yaml", "r") as f:
        env_config = yaml.safe_load(f)

    robots_entry_points = {r["name"]: r["entry_point"] for r in env_config["robots"]}

    for env in env_config["environments"]:
        env_name = env["name"]
        entry_point = env["entry_point"]
        robots = env["robots"]

        # Normalize to list of dicts
        if isinstance(robots, dict):  # single robot dict
            robots = [robots]

        for robot_entry in robots:
            for robot_name, robot_config in robot_entry.items():
                robot_env = "".join(robot_name.title().split("_")[:-1])
                max_episode_steps = env.get("max_episode_steps", None)
                assert max_episode_steps is not None, (
                    f"max_episode_steps must be specified in the environment config for {env_name} "
                )
                env_id = f"{robot_env}{env_name}"
                env_config = {}
                env_config["robot_pos"] = robot_config.pop("position")
                env_config["robot_quat"] = robot_config.pop("orientation")
                robot_config["name"] = robot_name
                robot_config["reset_noise"] = "default"
                kwargs = {
                    "env_config": env_config,
                    "robot_entry_points": robots_entry_points,
                    "robot_config": robot_config,
                    "deterministic_reset": False,
                }

                register(
                    id=env_id,
                    entry_point=entry_point,
                    kwargs=kwargs,
                    max_episode_steps=max_episode_steps,
                )


def register_envs_v1(registry_name: str):
    dir_path = path.dirname(path.realpath(__file__))
    with open(f"{dir_path}/config/{registry_name}.yaml", "r") as f:
        env_config = yaml.safe_load(f)

    robots_entry_points = {r["name"]: r["entry_point"] for r in env_config["robots"]}

    for env in env_config["environments"]:
        env_name = env["name"]
        entry_point = env["entry_point"]
        max_episode_steps = env.get("max_episode_steps", None)
        assert max_episode_steps is not None, (
            f"max_episode_steps must be specified in the environment config for {env_name} "
        )

        for robot_entry in env["robot_configs"]:
            try:
                robot_name = robot_entry["name"]
                robot_env = "".join(robot_name.title().split("_"))
                env_id = f"{robot_env}{env_name}"
                env_cfg = env.copy()
                env_cfg.pop("robot_configs")

                # Validate that each robot has control_freq specified
                for robot_config_name, robot_configs in robot_entry["robots"].items():
                    if not validate_robot_config(robot_configs):
                        raise ValueError(
                            f"control_freq must be specified for robot {robot_config_name} in environment {env_name}"
                        )

                kwargs = {
                    "env_config": env_cfg,
                    "robot_entry_points": robots_entry_points,
                    "robot_config": robot_entry["robots"],
                    "deterministic_reset": False,
                }

                register(
                    id=env_id,
                    entry_point=entry_point,
                    kwargs=kwargs,
                    max_episode_steps=max_episode_steps,
                )
            except Exception as e:
                logging.warning(f"Error registering environment {env_name}: {e}")


# Registry is Split Base off of the Base Env Version (due to differing kwargs)
register_envs_v0("registry_v0")
register_envs_v1("registry_v1")


try:
    register_envs_v1("_future_registry")
except Exception:
    pass
