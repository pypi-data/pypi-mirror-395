import yaml
import mujoco
import numpy as np
import sai_mujoco
from pathlib import Path
from typing import Tuple, List
from sai_mujoco.envs.base.base_v1 import BaseEnv_v1

class FootballEnv_v0(BaseEnv_v1):
    r"""
    Base class for football (soccer) simulation environments in sai_mujoco.

    This class provides the core tools, structure, and MuJoCo integration needed
    to create different football environments involving robots, a ball, and a field.
    It handles physics setup, observation construction, episode termination checks,
    and in-game logic (e.g., goal detection, ball position checks).

    A key feature is its scaling mechanism, which automatically adjusts robot
    dimensions, field size, goal size, and mesh scaling based on the selected
    robot type. This allows the same environment logic to be reused for robots
    of different sizes without rewriting geometry or parameters.
    """

    env_name: str = "football/v0"
    scene_name: str = "v0/base_scene"
    default_camera_config = {
        "distance": 2.8,
        "azimuth": -130,
        "elevation": -45.0,
        "lookat": np.array([0.2, 0.0, 0.35]),
    }

    def __init__(self, *args, **kwargs):
        """
        Initialize the FootballEnv instance.

        This constructor reads the robot configuration, team assignment, and texture
        settings from keyword arguments, determines the scaling factor for the robot
        and field based on the robot type, and loads environment parameters from the
        YAML configuration file. The parameters are automatically scaled and flattened
        for convenient access during simulation.
        """
        robot_config = kwargs.get("robot_config", {})
        self.textures = kwargs.get("textures", -1)
        self.team = kwargs.get("team", 0)

        self.robot_name = list(robot_config.keys())[0]
        self.size = robot_config.get(self.robot_name, {}).get("size", 1.0)
        self.parameters_dict = self._flatten_robot_keys(
            self._scale_parameters(self.load_yaml())
        )

        super().__init__(*args, **kwargs)

    def _scale_parameters(self, d, inside_robot=False):
        """
        Scale numeric values inside the "robot" part of the config by self.size.

        Recursively goes through the input dict or list. If inside a "robot" key,
        multiplies numbers by the size to adjust for robot scale.

        Parameters:
            d: dict, list, int, or float - input data to scale
            inside_robot: bool - whether currently inside a "robot" key

        Returns:
            The scaled data with the same structure as input.
        """
        if isinstance(d, dict):
            # Check if we're entering a 'robot' key
            return {
                k: self._scale_parameters(
                    v, inside_robot=(inside_robot or k == "robot")
                )
                for k, v in d.items()
            }
        elif isinstance(d, list):
            return [self._scale_parameters(v, inside_robot=inside_robot) for v in d]
        elif isinstance(d, (int, float)):
            return d * self.size if inside_robot else d
        else:
            return d

    def _flatten_robot_keys(self, d):
        """
        Remove the "robot" nesting in the config by merging its contents up.

        Recursively processes dicts and lists. When a "robot" key is found, its
        content is merged directly into the parent dict.

        Parameters:
            d: dict, list, or other - input data to flatten

        Returns:
            The data with "robot" keys flattened out.
        """
        if isinstance(d, dict):
            new_dict = {}
            for k, v in d.items():
                # If key is "robot", we inline its contents (assuming it's a dict)
                if k == "robot" and isinstance(v, dict):
                    # Recursively flatten its children
                    flattened = self._flatten_robot_keys(v)
                    new_dict.update(flattened)
                else:
                    new_dict[k] = self._flatten_robot_keys(v)
            return new_dict
        elif isinstance(d, list):
            return [self._flatten_robot_keys(v) for v in d]
        else:
            return d

    def _setup_references(self):
        """
        Set up references to important MuJoCo model parts for easy access.

        Finds and stores IDs of robot geoms, the floor geom, the robot torso geom,
        the soccer ball body, and the robot's root site. This allows quick access
        to these elements during simulation and observation.
        """

        super()._setup_references()

        body_names = [
            body
            for body in self.sim.model.body_names
            if self.robots[0].name_prefix in body
        ]

        self.robot_geom_ids = []
        for body_name in body_names:
            body_id = self.sim.model.body_name2id(body_name)

            for geom_id in range(self.sim.model.ngeom):
                if self.sim.model.geom_bodyid[geom_id] == body_id:
                    self.robot_geom_ids.append(geom_id)

        self._floor_geom = "floor"
        self._torso_id = self.sim.model.geom_name2id(
            f"{self.robots[0].name_prefix}Trunk"
        )
        self.ball_id = self.sim.model.body_name2id("soccer_ball")
        self._root_site = self.robots[0].parts["torso"].site_name
        self.target_name = self._root_site

    def build_obs(self):

        self.complete_space = {}
        self.complete_space = self._get_field_obs(self.complete_space)
        self.complete_space = self._get_ball_goal_obs(self.complete_space)
        self.complete_space = self._get_robot_obs(self.complete_space)
        self.complete_space = self._get_goalkeeper_obs(self.complete_space)
        self.complete_space = self._get_target_obs(self.complete_space)
        self.complete_space = self._get_defender_obs(self.complete_space)

    def _get_ball_goal_obs(self, obs_dict):

        ball_xpos = self.sim.data.get_site_xpos("ball")
        ball_velp = self.sim.data.get_site_xvelp("ball")
        ball_velr = self.sim.data.get_site_xvelr("ball")

        robot_xpos = self.sim.data.get_site_xpos(self._root_site)
        robot_velp = self.sim.data.get_site_xvelp(self._root_site)
        robot_velr = self.sim.data.get_site_xvelr(self._root_site)

        goal_xpos_team_0 = self.sim.data.get_site_xpos("goal_post_south")
        goal_xpos_team_1 = self.sim.data.get_site_xpos("goal_post_north")

        obs_dict["goal_team_0_rel_robot"] = goal_xpos_team_0 - robot_xpos
        obs_dict["goal_team_1_rel_robot"] = goal_xpos_team_1 - robot_xpos

        obs_dict["goal_team_0_rel_ball"] = goal_xpos_team_0 - ball_xpos
        obs_dict["goal_team_1_rel_ball"] = goal_xpos_team_1 - ball_xpos

        obs_dict["ball_xpos_rel_robot"] = ball_xpos - robot_xpos
        obs_dict["ball_velp_rel_robot"] = ball_velp - robot_velp
        obs_dict["ball_velr_rel_robot"] = ball_velr - robot_velr

        obs_dict["player_team"] = np.array([1, 0]) if self.current_team == 0 else np.array([0, 1])

        return obs_dict

    def _get_field_obs(self, obs_dict):

        obs_dict["length"] = self.parameters_dict["env_parameters"]["field"]["length"]
        obs_dict["width"] = self.parameters_dict["env_parameters"]["field"]["width"]
        obs_dict["goal_width"] = self.parameters_dict["env_parameters"]["goal"]["width"]
        obs_dict["goal_height"] = self.parameters_dict["env_parameters"]["goal"]["height"]
        obs_dict["goal_depth"] = self.parameters_dict["env_parameters"]["goal"]["depth"]

        return obs_dict

    def _get_robot_obs(self, obs_dict):

        obs_dict["robot_accelerometer"] = self.sim.data._data.sensor(f"{self.robots[0].name_prefix}accelerometer").data.astype(np.float32)
        obs_dict["robot_gyro"] = self.sim.data._data.sensor(f"{self.robots[0].name_prefix}torso_gyro").data.astype(np.float32)
        obs_dict["robot_velocimeter"] = self.sim.data._data.sensor(f"{self.robots[0].name_prefix}torso_vel").data.astype(np.float32)
        obs_dict["robot_quat"] = self.sim.data._data.sensor(f"{self.robots[0].name_prefix}torso_quat").data[[1, 2, 3, 0]].astype(np.float32)

        return obs_dict

    def _get_goalkeeper_obs(self, obs_dict):

        try:
            goalkeeper_team_0_xpos = self.sim.data.get_site_xpos("goalkeeper_team_0_site")
            goalkeeper_team_0_xvelp = self.sim.data.get_site_xvelp("goalkeeper_team_0_site")
            goalkeeper_team_1_xpos = self.sim.data.get_site_xpos("goalkeeper_team_1_site")
            goalkeeper_team_1_xvelp = self.sim.data.get_site_xvelp("goalkeeper_team_1_site")
        except:
            goalkeeper_team_0_xpos = self.sim.data.get_site_xpos(self._root_site)
            goalkeeper_team_0_xvelp = self.sim.data.get_site_xvelp(self._root_site)
            goalkeeper_team_1_xpos = self.sim.data.get_site_xpos(self._root_site)
            goalkeeper_team_1_xvelp = self.sim.data.get_site_xvelp(self._root_site)

        robot_xpos = self.sim.data.get_site_xpos(self._root_site)
        robot_velp = self.sim.data.get_site_xvelp(self._root_site)
        obs_dict["goalkeeper_team_0_xpos_rel_robot"] = goalkeeper_team_0_xpos - robot_xpos
        obs_dict["goalkeeper_team_0_velp_rel_robot"] = goalkeeper_team_0_xvelp - robot_velp
        obs_dict["goalkeeper_team_1_xpos_rel_robot"] = goalkeeper_team_1_xpos - robot_xpos
        obs_dict["goalkeeper_team_1_velp_rel_robot"] = goalkeeper_team_1_xvelp - robot_velp

        return obs_dict

    def _get_target_obs(self, obs_dict):

        ## Target can be goal, player, target
        robot_xpos = self.sim.data.get_site_xpos(self._root_site)
        robot_velp = self.sim.data.get_site_xvelp(self._root_site)
        try:
            target_xpos = self.sim.data.get_site_xpos(self.target_name)
            target_xvelp = self.sim.data.get_site_xvelp(self.target_name)
        except:
            target_xpos = self.sim.data.get_site_xpos(self._root_site)
            target_xvelp = self.sim.data.get_site_xvelp(self._root_site)

        obs_dict["target_xpos_rel_robot"] = target_xpos - robot_xpos
        obs_dict["target_velp_rel_robot"] = target_xvelp - robot_velp
        return obs_dict

    def _get_defender_obs(self, obs_dict):

        obs = []
        try:
            for i in range(3):
                obstacle_xpos = self.sim.data.get_geom_xpos(f"defender_geom{i}")
                obs.append(obstacle_xpos)
        except:
            for i in range(3):
                obstacle_xpos = self.sim.data.get_site_xpos(self._root_site)
                obs.append(obstacle_xpos)
        obs_dict["defender_xpos"] = np.concatenate(obs)
        return obs_dict

    def compute_terminated(self):
        """
        Check if the episode should terminate.

        The episode ends if the robot has fallen or if any simulation data
        (positions or velocities) contain NaNs.

        Returns:
            bool: True if terminated, False otherwise.
        """

        data_nan = (
            np.isnan(self.sim.data.qpos).any() | np.isnan(self.sim.data.qvel).any()
        )
        return bool(data_nan)

    def has_robot_fallen(
        self, height: float, min_height: float = 1.0, max_height: float = 2.0
    ) -> bool:
        """
        Determine if the robot has fallen based on its torso height.

        Uses custom standing height bounds if available; otherwise defaults.

        Parameters:
            height (float): Current height of the robot's torso.
            min_height (float): Minimum allowed height before considered fallen.
            max_height (float): Maximum height threshold (unused here).

        Returns:
            bool: True if robot is standing, False if fallen.
        """
        if hasattr(self.robots[0], "standing_height"):
            min_height = self.robots[0].standing_height[0]
            max_height = self.robots[0].standing_height[1]

        fallen = min_height < height
        return not fallen

    def is_outside_field(self, ball_xpos: np.ndarray, inside_goal: np.ndarray) -> bool:
        """
        Check if the ball is outside the field boundaries (excluding goals).

        Parameters:
            ball_xpos (array-like): Ball position [x, y, z].
            inside_goal (bool): Whether the ball is inside a goal.

        Returns:
            bool: True if ball is outside the field and not inside a goal.
        """

        outside_field = (
            ball_xpos[0] < -self.parameters_dict["env_parameters"]["field"]["length"]
            or ball_xpos[0] > self.parameters_dict["env_parameters"]["field"]["length"]
            or ball_xpos[1] < -self.parameters_dict["env_parameters"]["field"]["width"]
            or ball_xpos[1] > self.parameters_dict["env_parameters"]["field"]["width"]
        )
        return not inside_goal and outside_field

    def ball_inside_goal(self, ball_xpos: np.ndarray) -> bool:
        """
        Check if the ball is inside the current team's goal area.

        Parameters:
            ball_xpos (np.ndarray): The (x, y, z) position of the ball.

        Returns:
            bool: True if the ball is within the goal boundaries, False otherwise.
        """

        # Check if the ball is in goal
        goal_centre = self.sim.data.get_site_xpos(
            self.parameters_dict["team_parameters"][self.current_team]["goal"]["name"]
        )

        x = goal_centre[0]
        x_max = (
            x + self.parameters_dict["env_parameters"]["goal"]["depth"]
            if x >= 0
            else x - self.parameters_dict["env_parameters"]["goal"]["depth"]
        )

        if x > x_max:
            x, x_max = x_max, x

        is_ball_inside = (
            (x <= ball_xpos[0] <= x_max)
            and (
                goal_centre[1] - self.parameters_dict["env_parameters"]["goal"]["width"]
                <= ball_xpos[1]
                < goal_centre[1]
                + self.parameters_dict["env_parameters"]["goal"]["width"]
            )
            and (
                ball_xpos[2]
                < goal_centre[2]
                + self.parameters_dict["env_parameters"]["goal"]["height"]
            )
        )

        return bool(is_ball_inside)

    def _load_env_mjcf(self) -> mujoco.MjSpec:
        """
        Load and prepare the MuJoCo environment model.

        Calls the parent loader and then rescales meshes and field elements
        according to the current robot size.
        """

        super()._load_env_mjcf()
        self._rescale_meshes(self.size)
        self._rescale_field(self.size)

    def _reset_internal(self):
        """
        Reset internal state of the environment.

        Calls the parent reset, then updates textures, team states, and
        sets direction and rotation for the current team.
        """

        super()._reset_internal()
        self._change_model_texture(self.textures)
        self._change_team_state(self.team)

        self.direction = self.parameters_dict["team_parameters"][self.current_team][
            "direction"
        ][0]
        self.rotation = self.parameters_dict["team_parameters"][self.current_team][
            "rotation"
        ]

        self.build_obs()

    def _rescale_meshes(self, size: float):
        """
        Rescale the robot meshes based on the given size factor.

        Parameters:
            size (float): Scaling factor to apply to mesh dimensions.
        """
        for i in range(0, 1):
            # Change the mesh size
            scale = self.env_mjcf.meshes[i].scale
            scale = [size * scl for scl in scale]
            self.env_mjcf.meshes[i].scale = scale

    def _rescale_field(self, size: float):
        """
        Rescale field geometries, goals, boundary walls, and logos.

        Parameters:
            size (float): Scaling factor to apply to field components.
        """

        scale = self.env_mjcf.geoms[0].size
        scale[:2] = [size * scl for scl in scale[:2]]
        self.env_mjcf.geoms[0].size = scale

        # SOUTH GOAL
        for i in range(2, 4):
            pos = self.env_mjcf.bodies[i].pos
            pos[0:2] = [ps * size for ps in pos[:2]]
            self.env_mjcf.bodies[i].pos = pos

        # Change the boundary walls and SAI logo size
        geom_list = list(range(1, 3)) + list(range(20, 24))
        for i in geom_list:
            scale = self.env_mjcf.geoms[i].size
            scale[0:2] = [scl * size for scl in scale[:2]]
            self.env_mjcf.geoms[i].size = scale

            pos = self.env_mjcf.geoms[i].pos
            pos[:2] = [ps * size for ps in pos[:2]]

        for i in range(4, 20):
            scale = self.env_mjcf.geoms[i].size
            scale[0:2] = [scl * size for scl in scale[:2]]
            self.env_mjcf.geoms[i].size = scale

            pos = self.env_mjcf.geoms[i].pos
            pos[:3] = [ps * size for ps in pos[:3]]
            self.env_mjcf.geoms[i].pos = pos

    def _change_model_texture(self, texture: float):
        """
        Update ground texture properties based on the given texture index or value.

        Adjusts friction and color accordingly.
        """

        friction, rgba = self.get_friction_rgba(texture)

        self.sim.model.geom_rgba[1] = rgba
        self.sim.model.geom_friction[1] = friction

    def _change_team_state(self, team: int):
        """
        Set the current team and update the robot's jersey color.

        Parameters:
            team (int): Team index (0 or 1).
        """
        self.current_team, jersey_colour = self._choose_teams(team)
        self.sim.model.geom_rgba[self._torso_id] = jersey_colour

    def get_friction_rgba(self, texture) -> Tuple[List[float], List[float]]:
        """
        Compute friction and color values interpolated by the texture parameter.

        Parameters:
            texture (float or int): Texture index or random value for interpolation.

        Returns:
            tuple: (friction, rgba color) lists.
        """
        if texture == -1:
            texture = self.np_random.random()

        friction = self.parameters_dict["env_parameters"]["friction"]
        color = self.parameters_dict["env_parameters"]["color"]

        fric = [
            (1 - texture) * friction[0][i] + texture * friction[1][i]
            for i in range(len(friction[0]))
        ]
        rgba = [
            (1 - texture) * color[0][i] + texture * color[1][i]
            for i in range(len(color[0]))
        ]

        return fric, rgba

    def _choose_teams(self, team: int) -> Tuple[int, List[int]]:
        """
        Choose a team index and corresponding jersey color.

        If team == -1, randomly select between team 0 or 1.

        Parameters:
            team (int): Team index or -1 for random choice.

        Returns:
            tuple: (team index, jersey RGBA color list)
        """
        if team == -1:
            team = self.np_random.choice([0, 1])
        jersey_colour = [1, 0, 0, 1] if team else [0, 0, 1, 1]

        return team, jersey_colour

    def _setup_obs_space(self):

        self.build_obs()
        super()._setup_obs_space()

    def _get_info(self):

        self.complete_space = self._get_field_obs(self.complete_space)
        self.complete_space = self._get_ball_goal_obs(self.complete_space)
        self.complete_space = self._get_robot_obs(self.complete_space)
        self.complete_space = self._get_goalkeeper_obs(self.complete_space)
        self.complete_space = self._get_target_obs(self.complete_space)
        self.complete_space = self._get_defender_obs(self.complete_space)

        return self.complete_space

    def load_yaml(self) -> dict:
        """
        Load the football environment configuration from a YAML file.

        Returns:
            dict: Parsed configuration data.
        """
        file_path = (
            Path(sai_mujoco.__file__).parent
            / "envs"
            / "football"
            / "v0"
            / "config.yaml"
        )
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        return data
