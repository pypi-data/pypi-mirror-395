from pathlib import Path
from typing import Dict, Optional, Union
from copy import deepcopy
from gymnasium.utils.ezpickle import EzPickle

import gymnasium as gym
import mujoco
import sai_mujoco

import sai_mujoco.utils.v0.sim_utils as SU
from sai_mujoco.utils.v0.binding_utils import MjSim_v0


class MujocoEnv_v1(gym.Env, EzPickle):
    """
    Initializes a Mujoco Environment.
    Args:

        control_freq (float): how many control signals to receive
            in every simulated second. This sets the amount of simulation time
            that passes between every action input.
        render_mode (str): Rendering mode. Defaults to None.
        width (int): Width of the rendered image. Defaults to DEFAULT_SIZE.
        height (int): Height of the rendered image. Defaults to DEFAULT_SIZE.
        camera_id (int): Camera ID. Defaults to None.
        camera_name (str): Camera name. Defaults to None.
        default_camera_config (dict): Default camera configuration. Defaults to None.
        max_geom (int): Maximum number of geometries. Defaults to 1000.
        visual_options (dict): Visual options. Defaults to {}.
    Raises:
        ValueError: [Invalid renderer selection]
    """

    scene_name = None
    env_name = None

    def __init__(
        self,
        render_mode=None,
        renderer=None,
        width: int = 1280,
        height: int = 720,
        camera_id: Optional[int] = None,
        camera_name: Optional[str] = None,
        default_camera_config: Optional[Dict[str, Union[float, int]]] = None,
        max_geom: int = 5000,
        visual_options: Dict[int, bool] = {},
        visual_geom_options: Dict[int, bool] = {},
        hide_overlay: bool = True,
        seed: Optional[int] = 0,
        offscreen_height: Optional[int] = None,
        offscreen_width: Optional[int] = None,
    ):
        self.render_mode = render_mode
        self.renderer = renderer
        self.width = width
        self.height = height
        self.camera_id = camera_id
        self.camera_name = camera_name
        self.default_camera_config = default_camera_config
        self.max_geom = max_geom
        self.visual_options = visual_options
        self.visual_geom_options = visual_geom_options
        self.hide_overlay = hide_overlay
        self.offscreen_height = offscreen_height
        self.offscreen_width = offscreen_width

        self.scene_xml_path = (
            self.get_asset_path("scene", self.scene_name)
            if self.scene_name is not None
            else None
        )

        self.env_xml_path = (
            self.get_asset_path("envs", f"{self.env_name}/env.xml")
            if self.env_name is not None
            else None
        )

        self.scene_mjcf: mujoco.MjSpec = None
        self.env_mjcf: mujoco.MjSpec = None
        self.mjcf_model: mujoco.MjSpec = None

        self.mj_model: mujoco.MjModel = None

        self.seed = seed

        # Load the model
        self._load_model()
        self.control_freq = self.robots[0].control_freq

        # Initialize the simulation
        self._initialize_sim()

        self.metadata = self.get_ep_meta()
        self.metadata["render_fps"] = self.control_freq

        # initializes the rendering
        self.initialize_renderer()

        # Run all further internal (re-)initialization required
        self._reset_internal()

        super().__init__()

    def _initialize_time(self):
        self.control_timestep = 1.0 / self.control_freq
        self.model_timestep = self.sim.model.opt.timestep

    def initialize_renderer(self):
        from sai_mujoco.utils.v0.renderer import MujocoRenderer

        default_camera_config = self.get_default_cam_config()

        self.mujoco_renderer = MujocoRenderer(
            self.sim.model._model,
            self.sim.data._data,
            default_camera_config,
            self.width,
            self.height,
            self.max_geom,
            self.camera_id,
            self.camera_name,
            self.visual_options,
            self.visual_geom_options,
            self.renderer,
            self.hide_overlay,
            self.offscreen_height,
            self.offscreen_width,
        )

    def _load_model(self):
        """Loads an xml model, puts it in self.model"""
        # Load the scene mjcf model
        self._load_scene_mjcf()

        # Load the env mjcf model
        self._load_env_mjcf()

    def _load_scene_mjcf(self):
        """
        Loads the scene mjcf model
        """
        self.scene_mjcf = mujoco.MjSpec.from_file(self.scene_xml_path)

    def _load_env_mjcf(self):
        """
        Loads the env mjcf model
        """
        if self.env_xml_path is not None:
            self.env_mjcf = mujoco.MjSpec.from_file(self.env_xml_path)
        else:
            self.env_mjcf = mujoco.MjSpec()

    def _assemble_mjcf(self):
        """
        Assembles the mjcf model
        """
        raise NotImplementedError

    def _initialize_sim(self):
        """
        Creates a MjSim object and stores it in self.sim. If @xml_string is specified, the MjSim object will be created
        from the specified xml_string. Else, it will pull from self.model to instantiate the simulation
        Args:
            xml_string (str): If specified, creates MjSim object from this filepath
        """
        # Assemble the mjcf model
        self._assemble_mjcf()

        # Compile the mjcf model
        self.mj_model = self.mjcf_model.compile()

        # Create the simulation instance
        self.sim = MjSim_v0(self.mj_model)

        # run a single step to make sure changes have propagated through sim state
        self.sim.forward()

        # Setup sim time based on control frequency
        self._initialize_time()

    def get_ep_meta(self):
        """
        Returns a dictionary containing episode metadata
        Returns:
            dict: episode metadata
        """
        return deepcopy(self.metadata)

    def set_ep_meta(self, meta):
        """
        Set episode meta data
        Args:
            meta (dict): containing episode metadata
        """
        self.metadata = meta

    def unset_ep_meta(self):
        """
        Unset episode meta data
        """
        self._ep_meta = {}

    def step(self, action):
        """
        Takes a step in simulation with control command @action.
        Args:
            action (np.array): Action to execute within the environment
        Returns:
            4-tuple:
                - (OrderedDict) observations from the environment
                - (float) reward from the environment
                - (bool) whether the current episode is completed or not
                - (dict) misc information
        Raises:
            ValueError: [Steps past episode termination]
        """
        policy_step = True
        for i in range(int(self.control_timestep / self.model_timestep)):
            self.sim.step1()
            self._pre_action(action, policy_step)
            self.sim.step2()
            policy_step = False

        reward, terminated, truncated, info = self._post_action(action)

        observations = self._get_obs()

        if self.render_mode == "human":
            self.render()

        return observations, reward, terminated, truncated, info

    def _pre_action(self, action, policy_step):
        """
        Do any preprocessing before taking an action.
        Args:
            action (np.array): Action to execute within the environment
            policy_step (bool): Whether this current loop is an actual policy step or internal sim update step
        """
        self.sim.data.ctrl[:] = action

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        deterministic: bool = False,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)

        self.sim.reset()

        self._reset_internal()

        self.sim.forward()

        obs = self._get_obs()

        info = self._get_reset_info()

        if self.render_mode == "human":
            self.render()

        return obs, info

    def _post_action(self, action):
        """
        Do any housekeeping after taking an action.
        """
        raise NotImplementedError

    def _get_obs(self):
        """
        Get the observation of the environment.
        """
        raise NotImplementedError

    def _reset_internal(self):
        """
        Reset the internal state of the environment.
        """
        self.sim_state_initial = self.sim.get_state()
        self._setup_references()

    def _setup_references(self):
        """
        Sets up references to important components. A reference is typically an
        index or a list of indices that point to the corresponding elements
        in a flatten array, which is how MuJoCo stores physical simulation data.
        """
        pass

    def _get_reset_info(self) -> Dict[str, float]:
        """Function that generates the `info` that is returned during a `reset()`."""
        return {}

    def render(self):
        """
        Render a frame from the MuJoCo simulation as specified by the render_mode.
        """
        return self.mujoco_renderer.render(self.render_mode)

    def close(self):
        """Close rendering contexts processes."""
        if self.mujoco_renderer is not None:
            self.mujoco_renderer.close()

    def get_body_com(self, body_name):
        """Return the cartesian position of a body frame."""
        return self.data.body(body_name).xpos

    def check_contact(self, geoms_1, geoms_2=None):
        """
        Finds contact between two geom groups.
        Args:
            geoms_1 (str or list of str or MujocoModel): an individual geom name or list of geom names or a model. If
                a MujocoModel is specified, the geoms checked will be its contact_geoms
            geoms_2 (str or list of str or MujocoModel or None): another individual geom name or list of geom names.
                If a MujocoModel is specified, the geoms checked will be its contact_geoms. If None, will check
                any collision with @geoms_1 to any other geom in the environment
        Returns:
            bool: True if any geom in @geoms_1 is in contact with any geom in @geoms_2.
        """
        return SU.check_contact(sim=self.sim, geoms_1=geoms_1, geoms_2=geoms_2)

    def get_contacts(self, model):
        """
        Checks for any contacts with @model (as defined by @model's contact_geoms) and returns the set of
        geom names currently in contact with that model (excluding the geoms that are part of the model itself).
        Args:
            model (MujocoModel): Model to check contacts for.
        Returns:
            set: Unique geoms that are actively in contact with this model.
        Raises:
            AssertionError: [Invalid input type]
        """
        return SU.get_contacts(sim=self.sim, model=model)

    def get_default_cam_config(self, *args, **kwargs):
        """
        Get the default camera configuration
        """
        return self.default_camera_config

    @staticmethod
    def get_asset_path(asset_type: str, asset_name: str) -> str:
        """
        Returns the path to the asset
        """
        path = Path(sai_mujoco.__file__).parent / "assets" / asset_type / asset_name
        return path.with_suffix(".xml").as_posix()

    @property
    def action_dim(self):
        """
        Size of the action space
        Returns:
            int: Action space dimension
        """
        raise NotImplementedError
