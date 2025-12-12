from pathlib import Path
import numpy as np
import mujoco

import sai_mujoco
from sai_mujoco.controllers.composite.v0 import composite_controller_factory
from sai_mujoco.utils.v0.binding_utils import MjSim_v0

from .models import Part_v1, ArmPart_v1, GripperPart_v1

BASE_ATTACH_FRAME_NAME = {"v0/omron_mobile_base": "support"}


class BaseRobotMeta_v1(type):
    """Metaclass to automatically construct XML path from robot name."""

    def __new__(mcs, name, bases, namespace):
        # Get the robot name
        robot_name = namespace.get("name")

        # Construct XML path if robot_name is provided
        xml_path = namespace.get("xml_path")
        if xml_path is None:
            assert robot_name is not None, (
                "Robot name is required to construct XML path"
            )
            namespace["xml_path"] = (
                Path(
                    Path(sai_mujoco.__file__).parent
                    / "assets"
                    / "robots"
                    / robot_name
                    / "robot.xml"
                )
                .with_suffix(".xml")
                .as_posix()
            )
        else:
            namespace["xml_path"] = (
                Path(Path(sai_mujoco.__file__).parent / "assets" / "robots" / xml_path)
                .with_suffix(".xml")
                .as_posix()
            )

        return super().__new__(mcs, name, bases, namespace)


class BaseRobot_v1(metaclass=BaseRobotMeta_v1):
    """
    Base robot class for MuJoCo robots.

    The BaseRobotMeta metaclass automatically constructs the xml_path from the robot name:
    - xml_path: assets/robots/{name}/robot.xml

    Parts initialization happens in __init__ where:
    - All parts get their robot_idn and naming_prefix set
    - Parts are categorized into _arms, _legs, and _grippers dictionaries
    - All joint and actuator names are automatically prefixed with "robot_{idn}:"

    Subclasses should set:
    - name: str - The name of the robot (used to construct xml_path)
    - Robot parts (base, torso, head, left_arm, right_arm, left_leg, right_leg)

    Example:
        class FrankaRobot(BaseRobot):
            name = "franka"
            # xml_path will be automatically set to: assets/robots/franka/robot.xml
    """

    # Class-level configuration - subclasses should override this
    name: str = "base_robot"

    is_bimanual: bool = False

    # XML path is automatically constructed by the metaclass
    xml_path: str = None

    def __init__(
        self,
        idn: int,
        parts: dict[str, Part_v1 | ArmPart_v1 | GripperPart_v1],
        control_freq: int,
        np_random: np.random.Generator,
        composite_controller_config: dict | None = None,
        **kwargs,
    ):
        self.idn = idn
        self.name_prefix = f"robot_{idn}:"
        self.parts = parts
        self.composite_controller_config = (
            composite_controller_config
            if composite_controller_config
            else {"type": "BASIC"}
        )
        self.control_freq = control_freq
        self.np_random = np_random
        self.kwargs = kwargs

        self._init_parts()

        self.base_pos = kwargs.get("position")
        self.base_quat = kwargs.get("orientation")

        self.base_type = kwargs.get("base_type", None)

        self.reset_noise = kwargs.get("reset_noise")

        self._obs_cam_names = kwargs.get("obs_cam_names", [])

        if self.reset_noise is None:
            self.reset_noise = {
                "magnitude": 0.0,
                "type": "gaussian",
            }  # no noise conditions
        elif self.reset_noise == "default":
            self.reset_noise = {"magnitude": 0.02, "type": "gaussian"}
        self.reset_noise["magnitude"] = (
            self.reset_noise["magnitude"] if self.reset_noise["magnitude"] else 0.0
        )

        self.sim: MjSim_v0 = None

        self.composite_controller = None

        self.part_controller_config = {}
        self._ref_actuators_indexes_dict = {}
        self._robot_init_qpos = {}

        self._default_init_qpos()

        if kwargs.get("init_qpos") is not None:
            assert isinstance(kwargs.get("init_qpos"), dict), (
                "init_qpos must be a dict of joint names and values! Instead, got type: {}".format(
                    type(kwargs.get("init_qpos"))
                )
            )
            for joint_name, init_q in kwargs.get("init_qpos").items():
                self._robot_init_qpos[f"{self.name_prefix}{joint_name}"] = init_q

        self._load_controller_config()

    def _init_parts(self):
        self._arms = {}
        self._legs = {}
        self._grippers = {}
        self.gripper_joints = []

        # Add arms to the list of arms
        for name in ["left_arm", "right_arm"]:
            if name in self.parts:
                self._arms[name] = self.parts[name]
                if self.parts[name].gripper is not None:
                    gripper_name = f"{name}_gripper"
                    self.parts[gripper_name] = self.parts[name].gripper
                    self._grippers[gripper_name] = self.parts[name].gripper

        # Add legs to the list of legs
        for name in ["left_leg", "right_leg"]:
            if name in self.parts:
                self._legs[name] = self.parts[name]

        # Set the naming prefix for all parts
        for name, part in self.parts.items():
            part.set_prefix(self.name_prefix)

        # Add gripper joints to the list of gripper joints
        for name, gripper in self._grippers.items():
            self.gripper_joints.extend(gripper.joint_names)

    def reset_sim(self, sim: MjSim_v0):
        self.sim = sim

    def _postprocess_part_controller_config(self):
        """
        Update part_controller_config with values from composite_controller_config for each body part.
        Remove unused parts that are not in the controller.
        Called by _load_controller() function
        """
        for part_name, controller_config in self.composite_controller_config.get(
            "body_parts", {}
        ).items():
            if part_name in self.part_controller_config:
                self.part_controller_config[part_name].update(controller_config)

    def _load_controller(self):
        """
        Loads controller to be used for dynamic trajectories
        """

        # Flag for loading urdf once (only applicable for IK controllers)
        self.composite_controller = composite_controller_factory(
            type=self.composite_controller_config.get("type", "BASIC"),
            sim=self.sim,
            arms=self._arms,
            grippers=self._grippers,
        )

        self._load_arm_controllers()
        self._load_base_controller()
        self._load_leg_controllers()
        self._load_head_controller()
        self._load_torso_controller()

        self._postprocess_part_controller_config()

        self.composite_controller.load_controller_config(
            self.part_controller_config, self.composite_controller_config
        )

    def _load_controller_config(self):
        assert hasattr(self, "composite_controller_config"), (
            "composite_controller_config is not set"
        )

        for part_name, part in self.parts.items():
            if part.controller_config is not None:
                self.part_controller_config[part_name] = part.controller_config

        self.composite_controller_config["body_parts"] = {}
        for name, config in self.part_controller_config.items():
            self.composite_controller_config["body_parts"][name] = config

    def control(self, action, policy_step):
        """
        Actuate the robot with the
        passed joint velocities and gripper control.

        Args:
            action (np.array): The control to apply to the robot. The first @self.robot_model.dof dimensions should
                be the desired normalized joint velocities and if the robot has a gripper, the next @self.gripper.dof
                dimensions should be actuation controls for the gripper.

                :NOTE: Assumes inputted actions are of form:
                    [right_arm_control, right_gripper_control, left_arm_control, left_gripper_control]
            policy_step (bool): Whether this current loop is an actual policy step or internal sim update step

        Raises:
            AssertionError: [Invalid action dimension]
        """
        # clip actions into valid range
        assert len(action) == self.action_dim, (
            "environment got invalid action dimension -- expected {}, got {}".format(
                self.action_dim, len(action)
            )
        )

        if policy_step:
            self.composite_controller.set_goal(action)

        applied_action_dict = self.composite_controller.run_controller()
        for part_name, applied_action in applied_action_dict.items():
            actuator_indexes = self._ref_actuators_indexes_dict[part_name]
            applied_action_low = self.sim.model.actuator_ctrlrange[actuator_indexes, 0]
            applied_action_high = self.sim.model.actuator_ctrlrange[actuator_indexes, 1]
            applied_action = np.clip(
                applied_action, applied_action_low, applied_action_high
            )
            self.sim.data.ctrl[actuator_indexes] = applied_action

    def reset(self, deterministic: bool = False, **kwargs):
        self._reset_robot_joints(deterministic)

        self._load_controller()

        self.composite_controller.update_state()
        self.composite_controller.reset()

    def _reset_robot_joints(self, deterministic: bool = False):
        if not deterministic:
            # Determine noise
            if self.reset_noise["type"] == "gaussian":
                noise = (
                    self.np_random.normal(size=len(self._robot_init_qpos))
                    * self.reset_noise["magnitude"]
                )
            elif self.reset_noise["type"] == "uniform":
                noise = (
                    self.np_random.uniform(-1.0, 1.0, len(self._robot_init_qpos))
                    * self.reset_noise["magnitude"]
                )
            else:
                raise ValueError(
                    "Error: Invalid noise type specified. Options are 'gaussian' or 'uniform'."
                )
        else:
            noise = np.zeros(len(self._robot_init_qpos))

        for i, (joint_name, init_q) in enumerate(self._robot_init_qpos.items()):
            # Don't add noise to the gripper joints
            if joint_name in self.gripper_joints:
                noise[i] = 0
            self.sim.data.set_joint_qpos(joint_name, init_q + noise[i])
        self.sim.forward()

    def _default_init_qpos(self):
        """Initialize robot joint positions from part configurations."""
        for part_name, part in self.parts.items():
            init_qpos = part.init_qpos

            if isinstance(init_qpos, dict):
                # The init_qpos property already handles prefixed keys
                self._robot_init_qpos.update(init_qpos)
            elif isinstance(init_qpos, (list, np.ndarray)):
                # For list/array format, use joint_names property (already prefixed)
                for i, joint_name in enumerate(part.joint_names):
                    self._robot_init_qpos[joint_name] = init_qpos[i]
            else:
                raise ValueError(
                    f"Invalid init_qpos type: {type(init_qpos)} for part {part_name}. "
                    f"Expected dict, list, or numpy array."
                )

    def get_obs(self) -> tuple[np.ndarray, np.ndarray]:
        """Returns the joint positions and velocities of the robot."""
        robot_qpos = [
            self.sim.data.get_joint_qpos(joint_name) for joint_name in self.robot_joints
        ]
        robot_qvel = [
            self.sim.data.get_joint_qvel(joint_name) for joint_name in self.robot_joints
        ]
        return robot_qpos, robot_qvel

    def _load_leg_controllers(self):
        for leg_name, leg in self._legs.items():
            if leg.controller_config is None:
                continue

            self.part_controller_config[leg_name]["ramp_ratio"] = 1.0
            self.part_controller_config[leg_name]["robot_name"] = self.name

            self.part_controller_config[leg_name]["sim"] = self.sim
            self.part_controller_config[leg_name]["part_name"] = leg_name
            self.part_controller_config[leg_name]["naming_prefix"] = leg.naming_prefix
            self.part_controller_config[leg_name]["ndim"] = leg.dof
            self.part_controller_config[leg_name]["policy_freq"] = self.control_freq

            ref_legs_joint_indexes = [
                self.sim.model.joint_name2id(x) for x in leg.joint_names
            ]
            ref_legs_joint_pos_indexes = [
                self.sim.model.get_joint_qpos_addr(x) for x in leg.joint_names
            ]
            ref_legs_joint_vel_indexes = [
                self.sim.model.get_joint_qvel_addr(x) for x in leg.joint_names
            ]
            self.part_controller_config[leg_name]["joint_indexes"] = {
                "joints": ref_legs_joint_indexes,
                "qpos": ref_legs_joint_pos_indexes,
                "qvel": ref_legs_joint_vel_indexes,
            }

            self._ref_actuators_indexes_dict[leg_name] = [
                self.sim.model.actuator_name2id(actuator)
                for actuator in leg.actuator_names
            ]

            low = self.sim.model.actuator_ctrlrange[
                self._ref_actuators_indexes_dict[leg_name], 0
            ]
            high = self.sim.model.actuator_ctrlrange[
                self._ref_actuators_indexes_dict[leg_name], 1
            ]

            self.part_controller_config[leg_name]["actuator_range"] = (low, high)

    def _load_arm_controllers(self):
        # Load composite controller configs for both left and right arm
        for arm_name, arm in self._arms.items():
            if arm.controller_config is None:
                continue

            # Assert that the controller config is a dict file:
            #             NOTE: "type" must be one of: {JOINT_POSITION, JOINT_TORQUE, JOINT_VELOCITY,
            #                                           OSC_POSITION, OSC_POSE, IK_POSE}
            assert isinstance(self.part_controller_config[arm_name], dict), (
                "Inputted controller config must be a dict! Instead, got type: {}".format(
                    type(self.part_controller_config[arm_name])
                )
            )

            # Add to the controller dict additional relevant params:
            #   the robot name, mujoco sim, eef_name, actuator_range, joint_indexes, timestep (model) freq,
            #   policy (control) freq, and ndim (# joints)
            self.part_controller_config[arm_name]["robot_name"] = self.name
            self.part_controller_config[arm_name]["sim"] = self.sim
            self.part_controller_config[arm_name]["ref_name"] = (
                arm.gripper.site_name if arm.gripper is not None else None
            )
            self.part_controller_config[arm_name]["part_name"] = arm_name
            self.part_controller_config[arm_name]["naming_prefix"] = arm.naming_prefix

            self.part_controller_config[arm_name]["eef_rot_offset"] = np.array(
                [0, 0, 0, 1]
            )
            self.part_controller_config[arm_name]["ndim"] = arm.dof
            self.part_controller_config[arm_name]["policy_freq"] = self.control_freq
            self.part_controller_config[arm_name]["lite_physics"] = True

            self.part_controller_config[arm_name]["joint_indexes"] = {
                "joints": [
                    self.sim.model.joint_name2id(joint) for joint in arm.joint_names
                ],
                "qpos": [
                    self.sim.model.get_joint_qpos_addr(joint)
                    for joint in arm.joint_names
                ],
                "qvel": [
                    self.sim.model.get_joint_qvel_addr(joint)
                    for joint in arm.joint_names
                ],
            }
            self.part_controller_config[arm_name]["actuator_range"] = (
                self.sim.model.actuator_ctrlrange[
                    [
                        self.sim.model.actuator_name2id(actuator)
                        for actuator in arm.actuator_names
                    ],
                    0,
                ],
                self.sim.model.actuator_ctrlrange[
                    [
                        self.sim.model.actuator_name2id(actuator)
                        for actuator in arm.actuator_names
                    ],
                    1,
                ],
            )

            # Only load urdf the first time this controller gets called
            self.part_controller_config[arm_name]["load_urdf"] = False

            self._ref_actuators_indexes_dict[arm_name] = [
                self.sim.model.actuator_name2id(actuator)
                for actuator in arm.actuator_names
            ]

            if arm.gripper is not None:
                # Load gripper controllers
                gripper_name = f"{arm_name}_gripper"
                self.part_controller_config[gripper_name]["part_name"] = gripper_name
                self.part_controller_config[gripper_name]["robot_name"] = self.name
                self.part_controller_config[gripper_name]["sim"] = self.sim
                self.part_controller_config[gripper_name]["eef_name"] = (
                    arm.gripper.site_name
                )
                self.part_controller_config[gripper_name]["naming_prefix"] = (
                    arm.gripper.naming_prefix
                )
                self.part_controller_config[gripper_name]["ndim"] = arm.gripper.dof
                self.part_controller_config[gripper_name]["policy_freq"] = (
                    self.control_freq
                )
                self.part_controller_config[gripper_name]["joint_indexes"] = {
                    "joints": [
                        self.sim.model.joint_name2id(joint)
                        for joint in arm.gripper.joint_names
                    ],
                    "actuators": [
                        self.sim.model.actuator_name2id(actuator)
                        for actuator in arm.gripper.actuator_names
                    ],
                    "qpos": [
                        self.sim.model.get_joint_qpos_addr(joint)
                        for joint in arm.gripper.joint_names
                    ],
                    "qvel": [
                        self.sim.model.get_joint_qvel_addr(joint)
                        for joint in arm.gripper.joint_names
                    ],
                }
                low = self.sim.model.actuator_ctrlrange[
                    [
                        self.sim.model.actuator_name2id(actuator)
                        for actuator in arm.gripper.actuator_names
                    ],
                    0,
                ]
                high = self.sim.model.actuator_ctrlrange[
                    [
                        self.sim.model.actuator_name2id(actuator)
                        for actuator in arm.gripper.actuator_names
                    ],
                    1,
                ]

                self.part_controller_config[gripper_name]["actuator_range"] = (
                    low,
                    high,
                )

                self._ref_actuators_indexes_dict[gripper_name] = [
                    self.sim.model.actuator_name2id(actuator)
                    for actuator in arm.gripper.actuator_names
                ]

    def _load_base_controller(self):
        """
        Load base controller
        """
        base = self.parts.get("base")
        if base is None or base.controller_config is None:
            return

        self.part_controller_config["base"]["ramp_ratio"] = 1.0
        self.part_controller_config["base"]["robot_name"] = self.name

        self.part_controller_config["base"]["sim"] = self.sim
        self.part_controller_config["base"]["part_name"] = "base"
        self.part_controller_config["base"]["naming_prefix"] = base.naming_prefix
        self.part_controller_config["base"]["ndim"] = base.dof
        self.part_controller_config["base"]["policy_freq"] = self.control_freq
        self.part_controller_config["base"]["lite_physics"] = True

        ref_base_joint_indexes = [
            self.sim.model.joint_name2id(x) for x in base.joint_names
        ]
        ref_base_joint_pos_indexes = [
            self.sim.model.get_joint_qpos_addr(x) for x in base.joint_names
        ]
        ref_base_joint_vel_indexes = [
            self.sim.model.get_joint_qvel_addr(x) for x in base.joint_names
        ]
        ref_base_actuator_indexes = [
            self.sim.model.actuator_name2id(x) for x in base.actuator_names
        ]
        self.part_controller_config["base"]["joint_indexes"] = {
            "joints": ref_base_joint_indexes,
            "qpos": ref_base_joint_pos_indexes,
            "qvel": ref_base_joint_vel_indexes,
            "actuators": ref_base_actuator_indexes,
        }

        low = self.sim.model.actuator_ctrlrange[
            [
                self.sim.model.actuator_name2id(actuator)
                for actuator in base.actuator_names
            ],
            0,
        ]
        high = self.sim.model.actuator_ctrlrange[
            [
                self.sim.model.actuator_name2id(actuator)
                for actuator in base.actuator_names
            ],
            1,
        ]

        self.part_controller_config["base"]["actuator_range"] = (low, high)

        self._ref_actuators_indexes_dict["base"] = [
            self.sim.model.actuator_name2id(actuator)
            for actuator in base.actuator_names
        ]

    def _load_torso_controller(self):
        """
        Load torso controller
        """
        torso = self.parts.get("torso")
        if torso is None or torso.controller_config is None:
            return

        self.part_controller_config["torso"]["robot_name"] = self.name
        self.part_controller_config["torso"]["sim"] = self.sim
        self.part_controller_config["torso"]["part_name"] = "torso"
        self.part_controller_config["torso"]["naming_prefix"] = torso.naming_prefix
        self.part_controller_config["torso"]["policy_freq"] = self.control_freq
        self.part_controller_config["torso"]["lite_physics"] = True

        ref_torso_joint_indexes = [
            self.sim.model.joint_name2id(x) for x in torso.joint_names
        ]
        ref_torso_joint_pos_indexes = [
            self.sim.model.get_joint_qpos_addr(x) for x in torso.joint_names
        ]
        ref_torso_joint_vel_indexes = [
            self.sim.model.get_joint_qvel_addr(x) for x in torso.joint_names
        ]
        self.part_controller_config["torso"]["joint_indexes"] = {
            "joints": ref_torso_joint_indexes,
            "qpos": ref_torso_joint_pos_indexes,
            "qvel": ref_torso_joint_vel_indexes,
        }

        low = self.sim.model.actuator_ctrlrange[
            [
                self.sim.model.actuator_name2id(actuator)
                for actuator in torso.actuator_names
            ],
            0,
        ]
        high = self.sim.model.actuator_ctrlrange[
            [
                self.sim.model.actuator_name2id(actuator)
                for actuator in torso.actuator_names
            ],
            1,
        ]
        self.part_controller_config["torso"]["actuator_range"] = (low, high)

        self._ref_actuators_indexes_dict["torso"] = [
            self.sim.model.actuator_name2id(actuator)
            for actuator in torso.actuator_names
        ]

    def _load_head_controller(self):
        """
        Load head controller
        """
        head = self.parts.get("head")
        if head is None or head.controller_config is None:
            return

        self.part_controller_config["head"]["robot_name"] = self.name
        self.part_controller_config["head"]["sim"] = self.sim

        self.part_controller_config["head"]["part_name"] = "head"
        self.part_controller_config["head"]["naming_prefix"] = head.naming_prefix
        self.part_controller_config["head"]["ndim"] = head.dof
        self.part_controller_config["head"]["policy_freq"] = self.control_freq
        self.part_controller_config["head"]["lite_physics"] = True

        ref_head_joint_indexes = [
            self.sim.model.joint_name2id(x) for x in head.joint_names
        ]
        ref_head_joint_pos_indexes = [
            self.sim.model.get_joint_qpos_addr(x) for x in head.joint_names
        ]
        ref_head_joint_vel_indexes = [
            self.sim.model.get_joint_qvel_addr(x) for x in head.joint_names
        ]
        self.part_controller_config["head"]["joint_indexes"] = {
            "joints": ref_head_joint_indexes,
            "qpos": ref_head_joint_pos_indexes,
            "qvel": ref_head_joint_vel_indexes,
        }

        low = self.sim.model.actuator_ctrlrange[
            [
                self.sim.model.actuator_name2id(actuator)
                for actuator in head.actuator_names
            ],
            0,
        ]
        high = self.sim.model.actuator_ctrlrange[
            [
                self.sim.model.actuator_name2id(actuator)
                for actuator in head.actuator_names
            ],
            1,
        ]

        self.part_controller_config["head"]["actuator_range"] = (low, high)

        self._ref_actuators_indexes_dict["head"] = [
            self.sim.model.actuator_name2id(actuator)
            for actuator in head.actuator_names
        ]

    def get_sensor_measurement(self, sensor_name):
        """
        Grabs relevant sensor data from the sim object

        Args:
            sensor_name (str): name of the sensor

        Returns:
            np.array: sensor values
        """
        sensor_name = f"{self.name_prefix}{sensor_name}"
        sensor_idx = np.sum(
            self.sim.model.sensor_dim[: self.sim.model.sensor_name2id(sensor_name)]
        )
        sensor_dim = self.sim.model.sensor_dim[
            self.sim.model.sensor_name2id(sensor_name)
        ]
        return np.array(self.sim.data.sensordata[sensor_idx : sensor_idx + sensor_dim])

    def load_model(self):
        self.mjcf_model = mujoco.MjSpec.from_file(self.xml_path)

        if self.base_type is not None:
            base_xml_path = (
                Path(sai_mujoco.__file__).parent / "assets" / "bases" / self.base_type
            ).with_suffix(".xml")
            base_mjcf = mujoco.MjSpec.from_file(base_xml_path.as_posix())

            # Add base controllers
            self.add_base_controllers(base_mjcf)

            # Attach base to robot
            base_body_name = BASE_ATTACH_FRAME_NAME.get(self.base_type, "base")
            base_body = base_mjcf.body(base_body_name)
            assert base_body is not None, (
                f"Base body not found in the {self.base_type} XML file"
            )

            # Fix conflict with robot "base" body name
            robot_base_body = self.mjcf_model.body("base")
            if robot_base_body is not None:
                robot_base_body.name = f"{self.name_prefix}base"

            attach_frame = base_body.add_frame()
            attach_frame.attach_body(self.mjcf_model.bodies[1], "", "")

            self.mjcf_model = base_mjcf

        self.base_body_name = f"{self.name_prefix}{self.mjcf_model.bodies[1].name}"

        if self.base_pos is not None:
            self.set_base_xpos(self.base_pos - self.mjcf_model.bodies[1].pos)
        if self.base_quat is not None:
            self.set_base_quat(self.base_quat)

    def add_base_controllers(self, base_mjcf):
        base_joints = base_mjcf.joints
        mobile_joints = []
        torso_joints = []
        mobile_actuators = []
        torso_actuators = []
        for joint in base_joints:
            if "torso" in joint.name:
                torso_joints.append(joint.name)
            elif "mobile" in joint.name:
                mobile_joints.append(joint.name)

        for actuator in base_mjcf.actuators:
            if actuator.target in mobile_joints:
                mobile_actuators.append(actuator.name)
            elif actuator.target in torso_joints:
                torso_actuators.append(actuator.name)

        if len(mobile_joints) > 0:
            self._add_part(
                "base",
                Part_v1(
                    _joint_names=mobile_joints,
                    _actuator_names=mobile_actuators,
                    controller_config={
                        "type": "JOINT_VELOCITY",
                        "interpolation": None,
                    },
                ),
            )
        if len(torso_joints) > 0:
            self._add_part(
                "torso",
                Part_v1(
                    _joint_names=torso_joints,
                    _actuator_names=torso_actuators,
                    controller_config={
                        "type": "JOINT_POSITION",
                        "interpolation": None,
                        "kp": 2000,
                    },
                ),
            )

    def _add_part(self, part_name, part):
        part.set_prefix(self.name_prefix)
        self.parts[part_name] = part
        self.part_controller_config[part_name] = part.controller_config
        self.composite_controller_config["body_parts"][part_name] = (
            part.controller_config
        )

    def set_base_xpos(self, xpos):
        self.mjcf_model.bodies[1].pos = xpos

    def set_base_quat(self, quat):
        self.mjcf_model.bodies[1].quat = quat

    def _remove_joint_actuation(self, part_name):
        assert hasattr(self, "mjcf_model"), "Mjcf model not found"
        assert self.mjcf_model is not None, "Mjcf model not found"
        assert part_name in self.parts, f"Part {part_name} not found"

        mujoco_version = mujoco.__version__

        if mujoco_version >= "3.3.4":
            for joint in self.parts[part_name]._joint_names:
                self.mjcf_model.delete(self.mjcf_model.joint(joint))
            for actuator in self.parts[part_name]._actuator_names:
                self.mjcf_model.delete(self.mjcf_model.actuator(actuator))
        else:
            for joint in self.parts[part_name]._joint_names:
                self.mjcf_model.joint(joint).delete()
            for actuator in self.parts[part_name]._actuator_names:
                self.mjcf_model.actuator(actuator).delete()

        for joint in self.parts[part_name].joint_names:
            self._robot_init_qpos.pop(joint)

        self.parts.pop(part_name, None)
        self._arms.pop(part_name, None)
        self._legs.pop(part_name, None)
        self._grippers.pop(part_name, None)
        self.part_controller_config.pop(part_name, None)
        self._ref_actuators_indexes_dict.pop(part_name, None)

    def create_action_vector(self, action_dict):
        """
        A helper function that creates the action vector given a dictionary
        """
        # check if there's a composite controller and if the controller has a create_action_vector method
        if self.composite_controller is not None and hasattr(
            self.composite_controller, "create_action_vector"
        ):
            return self.composite_controller.create_action_vector(action_dict)
        else:
            full_action_vector = np.zeros(self.action_dim)
            for part_name, action_vector in action_dict.items():
                if part_name not in self.composite_controller._action_split_indexes:
                    continue
                start_idx, end_idx = self.composite_controller._action_split_indexes[
                    part_name
                ]
                if end_idx - start_idx == 0:
                    # skipping not controlling actions
                    continue
                assert len(action_vector) == (end_idx - start_idx), (
                    f"Action vector for {part_name} is not the correct size. Expected {end_idx - start_idx} for {part_name}, got {len(action_vector)}"
                )
                full_action_vector[start_idx:end_idx] = action_vector
            return full_action_vector

    def is_terminated(self):
        return False

    @property
    def base_xpos(self):
        return self.mjcf_model.bodies[1].pos

    @property
    def action_limits(self):
        return self.composite_controller.action_limits

    @property
    def action_dim(self):
        return self.action_limits[0].shape[0]

    @property
    def robot_joints(self):
        _joints = []
        for _, part in self.parts.items():
            _joints.extend(part.joint_names)
        return _joints

    @property
    def robot_actuators(self):
        _actuators = []
        for part_name, part in self.parts.items():
            _actuators.extend(part.actuator_names)
        return _actuators

    @property
    def obs_cam_names(self):
        return [f"{self.name_prefix}{cam_name}" for cam_name in self._obs_cam_names]
