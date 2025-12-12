import gymnasium as gym
import numpy as np

from sai_mujoco.robots.base.v1 import BaseRobot_v1
from sai_mujoco.utils.v1.mujoco_env import MujocoEnv_v1
from typing import Optional


class BaseEnv_v1(MujocoEnv_v1):
    """
    Base environment class for MuJoCo environments.

    This class provides a foundation for creating MuJoCo-based reinforcement learning
    environments. It handles robot loading, scene composition, observation and action
    space definition, and provides a standard interface for environment interactions.

    Subclasses should set:
    - env_name: str - The name of the environment (used to construct env_xml_path)
    - scene_name: str - The name of the scene (used to construct scene_xml_path)

    The metaclass automatically constructs XML paths based on these attributes.

    Attributes:
        env_name (str): The name of the environment directory
        scene_name (str): The name of the scene XML file
        env_xml_path (str): Full path to the environment XML file (auto-generated)
        scene_xml_path (str): Full path to the scene XML file (auto-generated)
        metadata (dict): Gymnasium metadata including supported render modes
        default_camera_config (dict): Default camera configuration for rendering

    Example:
        class MyEnv(BaseEnv_v1):
            env_name = "bowling"
            scene_name = "base_scene"
    """

    # Class-level configuration - subclasses should override these
    env_name: str = None
    scene_name: str = None
    single_robot: bool = True

    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
            "rgbd_tuple",
        ],
    }

    default_camera_config: dict = None

    def __init__(
        self,
        env_config: dict,
        robot_entry_points: dict = {},
        robot_config: dict = {},
        **kwargs,
    ):
        """
        Initialize the base environment.

        Args:
            env_config (dict): Environment configuration parameters
            robot_config (dict, optional): Robot configuration parameters. Defaults to {}.
            **kwargs: Additional keyword arguments including:
                - deterministic_reset (bool): Whether to use deterministic reset. Defaults to True.
                - render_mode (str): Rendering mode. Defaults to None.
                - hide_overlay (bool): Whether to hide the overlay menu. Defaults to True.
        """
        self.env_config = env_config
        self.robot_config = robot_config
        self.robot_entry_points = robot_entry_points
        self.kwargs = kwargs

        self.renderer = kwargs.get("renderer", None)
        self.deterministic_reset = kwargs.get("deterministic_reset", False)
        hide_overlay = kwargs.get("hide_overlay", True)
        render_mode = kwargs.get("render_mode", None)
        width = kwargs.get("width", 1280)
        height = kwargs.get("height", 720)
        self.use_cam_obs = kwargs.get("use_cam_obs", False)
        self.offscreen_render_mode = kwargs.get("offscreen_render_mode", "rgb_array")

        # Set obs cam names; prioritize kwargs over env_config
        self.env_obs_cam_names = kwargs.get("env_obs_cam_names")
        self.robot_obs_cam_names = kwargs.get("robot_obs_cam_names")

        if self.single_robot:
            assert len(self.robot_config) == 1, (
                f"{self.env_name} is a single robot environment, but {len(self.robot_config)} robots were provided"
            )

        self.robots: list[BaseRobot_v1] = []

        self.env_configuration = env_config.get("env_configuration", "default")
        self._check_robot_configuration(self.robot_names)

        offscreen_height = None
        offscreen_width = None
        if self.use_cam_obs:
            offscreen_height = 256
            offscreen_width = 256

        super().__init__(
            renderer=self.renderer,
            hide_overlay=hide_overlay,
            render_mode=render_mode,
            width=width,
            height=height,
            default_camera_config=self.default_camera_config,
            visual_options=kwargs.get("visual_options", {}),
            visual_geom_options=kwargs.get("visual_geom_options", {}),
            offscreen_height=offscreen_height,
            offscreen_width=offscreen_width,
        )

        self.cam_obs_names = []
        if self.env_obs_cam_names is None:
            self.env_obs_cam_names = self.env_config.get("obs_cam_names", [])
        self.cam_obs_names.extend(self.env_obs_cam_names)

        if self.robot_obs_cam_names is None:
            for robot in self.robots:
                self.cam_obs_names.extend(robot.obs_cam_names)
        else:
            self.cam_obs_names.extend(self.robot_obs_cam_names)

        if self.use_cam_obs:
            assert len(self.cam_obs_names) > 0, "No camera observations specified"

            for cam_name in self.cam_obs_names:
                if cam_name not in self.sim.model.camera_names:
                    raise ValueError(f"Camera {cam_name} not found in simulation model")

        self._setup_obs_space()
        self._setup_action_space()

    def _check_robot_configuration(self, robots):
        """
        Sanity check to make sure the inputted robots and configuration is acceptable

        Args:
            robots (str or list of str): Robots to instantiate within this env
        """
        pass

    def _setup_obs_space(self):
        obs = self._get_obs()
        if self.use_cam_obs:
            self.observation_space = gym.spaces.Dict(
                {
                    "proprio": gym.spaces.Box(
                        low=-np.inf,
                        high=np.inf,
                        shape=obs["proprio"].shape,
                        dtype=np.float32,
                    ),
                    "pixels": gym.spaces.Dict(
                        {
                            key: gym.spaces.Box(
                                low=0,
                                high=255 if "rgb" in key else 1,
                                shape=obs["pixels"][key].shape,
                                dtype=np.uint8 if "rgb" in key else np.float32,
                            )
                            for key in obs["pixels"].keys()
                        }
                    ),
                }
            )
        else:
            self.observation_space = gym.spaces.Box(
                low=-np.inf, high=np.inf, shape=obs.shape, dtype=np.float32
            )

    def _setup_action_space(self):
        low, high = self.action_spec
        self.action_space = gym.spaces.Box(low=low, high=high, dtype=np.float32)

    def _load_model(self):
        """
        Loads an xml model, puts it in self.model
        """
        super()._load_model()

        # Load robots
        self._load_robots()

    @staticmethod
    def _load_class(entry_point: str):
        """
        Load a class from its entry point string.

        Args:
            entry_point (str): The entry point string in the format 'module:ClassName'

        Returns:
            type: The loaded class
        """
        module_name, class_name = entry_point.rsplit(":", 1)
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)

    def _load_robots(self):
        """
        Instantiates robots and stores them within the self.robots attribute
        """
        idx = 0
        # Loop through robots and instantiate Robot object for each
        for name, config in self.robot_config.items():
            robot_class = self._load_class(self.robot_entry_points[name])
            if not robot_class:
                raise ValueError(f"Robot class not found for {name}")

            if isinstance(config, list):
                for robot_config in config:
                    # Extract control_freq from robot config
                    control_freq = robot_config.get("control_freq")
                    if control_freq is None:
                        raise ValueError(
                            f"control_freq must be specified for robot {name}"
                        )

                    self.robots.append(
                        robot_class(
                            idn=idx,
                            np_random=self.np_random,
                            **robot_config,
                        )
                    )
                    self.robots[idx].load_model()
                    idx += 1
            else:
                # Extract control_freq from robot config
                control_freq = config.get("control_freq")
                if control_freq is None:
                    raise ValueError(f"control_freq must be specified for robot {name}")

                self.robots.append(
                    robot_class(
                        idn=idx,
                        np_random=self.np_random,
                        **config,
                    )
                )
                self.robots[idx].load_model()
                idx += 1

    def _assemble_mjcf(self):
        attachment_frame = self.scene_mjcf.worldbody.add_frame()
        self.scene_mjcf.attach(self.env_mjcf, frame=attachment_frame)

        for robot in self.robots:
            attachment_frame = self.scene_mjcf.worldbody.add_frame()
            attachment_frame.attach_body(
                robot.mjcf_model.bodies[1], f"robot_{robot.idn}:", ""
            )

        self.mjcf_model = self.scene_mjcf

    def _setup_references(self):
        """
        Sets up references to important components. A reference is typically an
        index or a list of indices that point to the corresponding elements
        in a flatten array, which is how MuJoCo stores physical simulation data.
        """
        super()._setup_references()

        # Setup robot-specific references as well (note: requires resetting of sim for robot first)
        for robot in self.robots:
            robot.reset_sim(self.sim)

    def _render_callback(self):
        """
        Callback function called before rendering.

        This method can be overridden by subclasses to perform any
        environment-specific rendering operations before the main render call.
        """
        pass

    def render(self):
        """
        Render the environment.

        Returns:
            The rendered output (format depends on render_mode)
        """
        self._render_callback()
        return super().render()

    def compute_reward(self) -> dict:
        """
        Compute the reward for the current state.

        This method must be implemented by subclasses to define the reward function
        for the specific environment.

        Returns:
            float: The computed reward value

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError

    def compute_terminated(self) -> bool:
        """
        Compute whether the episode has terminated.

        This method must be implemented by subclasses to define the termination
        conditions for the specific environment.

        Returns:
            bool: True if the episode should terminate, False otherwise

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        deterministic: bool = False,
        options: Optional[dict] = None,
    ):
        obs, info = super().reset(
            seed=seed,
            deterministic=deterministic,
            options=options,
        )

        info = self._get_info()

        return obs, info

    def _get_env_obs(self) -> np.ndarray:
        """
        Get environment-specific observations.

        This method can be overridden by subclasses to provide additional
        environment-specific observations beyond robot state.

        Returns:
            np.ndarray: Environment-specific observation array
        """
        return np.array([], dtype=np.float32)

    def _get_obs(self) -> np.ndarray | dict[str, np.ndarray]:
        """
        Get the complete observation for the current state.

        Returns:
            np.ndarray: Proprioceptive observation or dict[str, np.ndarray] if use_cam_obs is True
        """
        obs = []
        for robot in self.robots:
            robot_pos, robot_vel = robot.get_obs()
            obs.append(robot_pos)
            obs.append(robot_vel)
        env_obs = self._get_env_obs()
        obs.append(env_obs)
        proprio_obs = np.concatenate(obs, dtype=np.float32)
        if self.use_cam_obs:
            return {"proprio": proprio_obs, "pixels": self._get_cam_obs()}
        return proprio_obs

    def _get_cam_obs(self) -> dict[str, np.ndarray]:
        """
        Get the camera observation for the current state.

        Returns:
            dict[str, np.ndarray]: Dictionary containing camera observations
        """
        cam_obs = {}
        render_mode = (
            self.offscreen_render_mode
            if self.render_mode == "human"
            else self.render_mode or self.offscreen_render_mode
        )
        for cam_name in self.cam_obs_names:
            camera_id = self.sim.model.camera_name2id(cam_name)
            if camera_id == -1:
                raise ValueError(f"Camera {cam_name} not found in simulation model")

            frame = self.mujoco_renderer.render(
                render_mode=render_mode,
                camera_id=camera_id,
            )
            if render_mode == "rgb_array":
                cam_obs[f"cam_{cam_name}_rgb"] = frame
            elif render_mode == "depth_array":
                cam_obs[f"cam_{cam_name}_depth"] = frame
            elif render_mode == "rgbd_tuple":
                cam_obs[f"cam_{cam_name}_rgb"] = frame[0]
                cam_obs[f"cam_{cam_name}_depth"] = frame[1]
            else:
                raise ValueError(f"Invalid render mode: {render_mode}")
        return cam_obs

    def _get_info(self) -> dict:
        """
        Get additional information about the current state.

        This method can be overridden by subclasses to provide additional
        information that might be useful for debugging or logging.

        Returns:
            dict: Dictionary containing additional information
        """
        return {}

    def _post_action(self, action):
        """
        Compute the reward, terminated, truncated, and info after taking an action.

        Args:
            action: The action to take (format depends on action_space)

        Returns:
            tuple: (reward, terminated, truncated, info)
                - reward: The reward received for this step
                - terminated: Whether the episode has terminated
                - truncated: Whether the episode was truncated (always False in this implementation)
                - info: Additional information about the step
        """
        raw_reward = self.compute_reward()
        reward = self._total_reward(raw_reward)
        terminated = self.compute_terminated()

        # Check if any robot has terminated
        for robot in self.robots:
            if robot.is_terminated():
                terminated = True

        truncated = False
        info = self._get_info()

        # Add reward components to info
        info.update({"reward_terms": raw_reward})

        return reward, terminated, truncated, info

    def _reset_internal(self):
        """
        Resets simulation internal configurations.
        """
        # Run superclass reset functionality
        super()._reset_internal()

        # Reset action dim
        self._action_dim = 0

        # Reset robot and update action space dimension along the way
        for robot in self.robots:
            robot.reset(deterministic=self.deterministic_reset)
            self._action_dim += robot.action_dim

    def _pre_action(self, action, policy_step):
        """
        Overrides the superclass method to control the robot(s) within this enviornment using their respective
        controllers using the passed actions and gripper control.

        Args:
            action (np.array): The control to apply to the robot(s). Note that this should be a flat 1D array that
                encompasses all actions to be distributed to each robot if there are multiple. For each section of the
                action space assigned to a single robot, the first @self.robots[i].controller.control_dim dimensions
                should be the desired controller actions and if the robot has a gripper, the next
                @self.robots[i].gripper.dof dimensions should be actuation controls for the gripper.
            policy_step (bool): Whether a new policy step (action) is being taken

        Raises:
            AssertionError: [Invalid action dimension]
        """
        # Verify that the action is the correct dimension
        assert len(action) == self.action_dim, (
            "environment got invalid action dimension -- expected {}, got {}".format(
                self.action_dim, len(action)
            )
        )

        # Update robot joints based on controller actions
        cutoff = 0
        for idx, robot in enumerate(self.robots):
            robot_action = action[cutoff : cutoff + robot.action_dim]
            robot.control(robot_action, policy_step)
            cutoff += robot.action_dim

    def _total_reward(self, raw_reward: dict) -> float:
        """
        Compute the total reward from the raw reward dictionary.

        This method applies reward weights from the reward_config to compute
        the final reward value. It multiplies each reward component by its
        corresponding weight and sums them up.

        Args:
            raw_reward (dict): Dictionary containing individual reward components

        Returns:
            float: The weighted sum of all reward components

        Raises:
            AttributeError: If reward_config is not set on the environment
        """
        assert hasattr(self, "reward_config"), "reward_config is not set"
        reward_config = self.reward_config
        total_reward = []
        for key, value in raw_reward.items():
            if key in reward_config:
                total_reward.append(reward_config[key] * value)
        return np.sum(total_reward, dtype=np.float32)

    @property
    def action_spec(self):
        """
        Action space (low, high) for this environment

        Returns:
            2-tuple:

                - (np.array) minimum (low) action values
                - (np.array) maximum (high) action values
        """
        low, high = [], []
        for robot in self.robots:
            lo, hi = robot.action_limits
            low, high = (
                np.concatenate([low, lo], dtype=np.float32),
                np.concatenate([high, hi], dtype=np.float32),
            )
        return low, high

    @property
    def action_dim(self):
        """
        Action space dimension
        """
        return self._action_dim

    @property
    def robot_names(self):
        """
        Get the names of the robots in the environment from the robot_config.
        """
        robot_names = []
        for name, config in self.robot_config.items():
            if isinstance(config, list):
                for robot_config in config:
                    robot_names.append(name)
            else:
                robot_names.append(name)
        return robot_names
