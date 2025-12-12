import numpy as np
from sai_mujoco.robots.base.v1 import BaseRobot_v1, Part_v1, GripperPart_v1, ArmPart_v1
from sai_mujoco.utils.v0.rotations import make_pose


class Reachy2_v0(BaseRobot_v1):
    r"""
    Robot model for Reachy 2 mobile bi-manipulator robot.

    This class defines the kinematic structure, joint setup, and control specifications
    for the Reachy 2 robot in the Sai MuJoCo simulation framework.


    Attributes
    ----------
    name : str
        Unique identifier for this robot class ("reachy2/v0").
    base : Part
        The robot's floating base with three wheels (right, left, back).
    torso : Part
        The robot's torso with a 1-DoF joint (1 position).
    left_arm : ArmPart
        Defines the 7-DOF arm part, including:
        - `joint_names`: List of 7 joint names in the MuJoCo XML.
        - `_actuator_names`: List of 7 actuator keys corresponding to torque control.
        - `controller_config`: OSC controller gains, limits, and modes for both
          position and orientation control.
        The `gripper` sub-part is a `GripperPart` that encapsulates:
        - `joint_names`: Two gear joints for opening/closing.
        - `_actuator_names`: Single actuator for finger torque.
        - `site_name`: Name of the grasp site in the MuJoCo model.
        - `controller_config`: Grip-specific control mode.
    right_arm : ArmPart
        Defines the 7-DOF arm part, including:
        - `joint_names`: List of 7 joint names in the MuJoCo XML.
        - `_actuator_names`: List of 7 actuator keys corresponding to torque control.
        - `controller_config`: OSC controller gains, limits, and modes for both
          position and orientation control.
        The `gripper` sub-part is a `GripperPart` that encapsulates:
        - `joint_names`: Two gear joints for opening/closing.
        - `_actuator_names`: Single actuator for finger torque.
        - `site_name`: Name of the grasp site in the MuJoCo model.
        - `controller_config`: Grip-specific control mode.

    ## Observation Space

    The observation space consists of the following parts (in order):

    - *qpos (20 elements):* Joint position values of the robot's body parts. 3 for base, 1 for torso, 7 for left arm, 7 for right arm, 2 for two gripper joints.
    - *qvel (20 elements):* The velocities of these individual body parts (their derivatives). 3 for base, 1 for torso, 7 for left arm, 7 for right arm, 2 for two gripper joints.

    The order of elements in the observation space related to Reachy 2 is as follows -

    | Num | Observation                              | Min  | Max | Type (Unit)              |
    | --- | -----------------------------------------| ---- | --- | ------------------------ |
    | 0   | right_wheel position                          | -Inf | Inf | orientation (rad)        |
    | 1   | left_wheel position                          | -Inf | Inf | orientation (rad)        |
    | 2   | back_wheel position                          | -Inf | Inf | orientation (rad)        |
    | 3   | tripod_joint position                          | -Inf | Inf | orientation (rad)        |
    | 4   | l_shoulder_pitch position                          | -Inf | Inf | orientation (rad)        |
    | 5   | l_shoulder_roll position                          | -Inf | Inf | orientation (rad)        |
    | 6   | l_elbow_yaw position                          | -Inf | Inf | orientation (rad)        |
    | 7   | l_elbow_pitch position                          | -Inf | Inf | orientation (rad)        |
    | 8   | l_wrist_roll position                          | -Inf | Inf | orientation (rad)        |
    | 9   | l_wrist_pitch position                          | -Inf | Inf | orientation (rad)        |
    | 10   | l_wrist_yaw position                          | -Inf | Inf | orientation (rad)        |
    | 11   | r_shoulder_pitch position                          | -Inf | Inf | orientation (rad)        |
    | 12   | r_shoulder_roll position                          | -Inf | Inf | orientation (rad)        |
    | 13   | r_elbow_yaw position                          | -Inf | Inf | orientation (rad)        |
    | 14   | r_elbow_pitch position                          | -Inf | Inf | orientation (rad)        |
    | 15   | r_wrist_roll position                          | -Inf | Inf | orientation (rad)        |
    | 16   | r_wrist_pitch position                          | -Inf | Inf | orientation (rad)        |
    | 17   | r_wrist_yaw position                          | -Inf | Inf | orientation (rad)        |
    | 18   | l_hand_finger position                          | -Inf | Inf | orientation (rad)        |
    | 19   | r_hand_finger position                          | -Inf | Inf | orientation (rad)        |

    Same order for qvel.

    ## Action Space

    The action space is a continuous vector of shape `(18,)`. The table below describes each dimension.

    | Index | Action                                     |
    | ----- | ------------------------------------------ |
    | 0     | Base Translation X ($\Delta x$)                |
    | 1     | Base Translation Y ($\Delta y$)                |
    | 2     | Base Orientation Yaw ($\Delta \text{yaw}$)                |
    | 3     | Torso Position ($\Delta \text{pitch}$)   |
    | 4     | Left Arm End-Effector X ($\Delta \text{x}$)     |
    | 5     | Left Arm End-Effector Y ($\Delta \text{y}$)     |
    | 6     | Left Arm End-Effector Z ($\Delta \text{z}$)     |
    | 7     | Left Arm End-Effector Roll ($\Delta \text{roll}$)     |
    | 8     | Left Arm End-Effector Pitch ($\Delta \text{pitch}$)     |
    | 9     | Left Arm End-Effector Yaw ($\Delta \text{yaw}$)     |
    | 10     | Right Arm End-Effector X ($\Delta \text{x}$)     |
    | 11     | Right Arm End-Effector Y ($\Delta \text{y}$)     |
    | 12     | Right Arm End-Effector Z ($\Delta \text{z}$)     |
    | 13     | Right Arm End-Effector Roll ($\Delta \text{roll}$)     |
    | 14     | Right Arm End-Effector Pitch ($\Delta \text{pitch}$)     |
    | 15     | Right Arm End-Effector Yaw ($\Delta \text{yaw}$)     |
    | 16     | Left Arm Gripper Open/Close     |
    | 17     | Right Arm Gripper Open/Close    |

    """

    name: str = "reachy2/v0"

    is_bimanual = True

    def __init__(self, idn: int, control_freq: int, np_random, **kwargs):
        parts = {
            "base": Part_v1(
                _joint_names=[
                    "right_wheel",
                    "left_wheel",
                    "back_wheel",
                ],
                controller_config={
                    "type": "HOLONOMIC",
                    "wheel_radius": 0.105,
                    "base_radius": 0.198,
                    "input_min": -1,
                    "input_max": 1,
                    "wheel_angles": [
                        -1.0472,
                        1.0472,
                        3.14159,
                    ],  # -60°, 60°, 180° in radians
                    "interpolation": None,
                },
            ),
            "torso": Part_v1(
                _joint_names=[
                    "tripod_joint",
                ],
                _site_name="torso",
                controller_config={
                    "type": "JOINT_POSITION",
                    "input_max": 1,
                    "input_min": -1,
                    "input_type": "delta",
                    "output_max": 0.2,
                    "output_min": -0.2,
                    "kd": 550,
                    "kv": 550,
                    "kp": 1000,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                },
            ),
            "left_arm": ArmPart_v1(
                _joint_names=[
                    "l_shoulder_pitch",
                    "l_shoulder_roll",
                    "l_elbow_yaw",
                    "l_elbow_pitch",
                    "l_wrist_roll",
                    "l_wrist_pitch",
                    "l_wrist_yaw",
                ],
                controller_config={
                    "type": "OSC_POSE",
                    "input_max": 1,
                    "input_min": -1,
                    "output_max": [0.05, 0.05, 0.05, 0.5, 0.5, 0.5],
                    "output_min": [-0.05, -0.05, -0.05, -0.5, -0.5, -0.5],
                    "kp": 350,
                    "damping_ratio": 1,
                    "impedance_mode": "fixed",
                    "kp_limits": [0, 300],
                    "damping_ratio_limits": [0, 10],
                    "position_limits": None,
                    "orientation_limits": None,
                    "uncouple_pos_ori": True,
                    "input_type": "delta",
                    "input_ref_frame": "base",
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                },
                gripper=GripperPart_v1(
                    _joint_names=["l_hand_finger"],
                    _site_name="l_grip_site",
                    controller_config={"type": "GRIP"},
                    _important_geoms={
                        "left_fingerpad": [
                            "l_leftfinger_pad1",
                            "l_leftfinger_pad2",
                            "l_leftfinger_pad3",
                            "l_leftfinger_pad4",
                        ],
                        "right_fingerpad": [
                            "l_rightfinger_pad1",
                            "l_rightfinger_pad2",
                            "l_rightfinger_pad3",
                            "l_rightfinger_pad4",
                        ],
                    },
                ),
            ),
            "right_arm": ArmPart_v1(
                _joint_names=[
                    "r_shoulder_pitch",
                    "r_shoulder_roll",
                    "r_elbow_yaw",
                    "r_elbow_pitch",
                    "r_wrist_roll",
                    "r_wrist_pitch",
                    "r_wrist_yaw",
                ],
                controller_config={
                    "type": "OSC_POSE",
                    "input_max": 1,
                    "input_min": -1,
                    "output_max": [0.05, 0.05, 0.05, 0.5, 0.5, 0.5],
                    "output_min": [-0.05, -0.05, -0.05, -0.5, -0.5, -0.5],
                    "kp": 350,
                    "damping_ratio": 1,
                    "impedance_mode": "fixed",
                    "kp_limits": [0, 300],
                    "damping_ratio_limits": [0, 10],
                    "position_limits": None,
                    "orientation_limits": None,
                    "uncouple_pos_ori": True,
                    "input_type": "delta",
                    "input_ref_frame": "base",
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                },
                gripper=GripperPart_v1(
                    _joint_names=["r_hand_finger"],
                    _site_name="r_grip_site",
                    controller_config={"type": "GRIP"},
                    _important_geoms={
                        "left_fingerpad": [
                            "r_leftfinger_pad1",
                            "r_leftfinger_pad2",
                            "r_leftfinger_pad3",
                            "r_leftfinger_pad4",
                        ],
                        "right_fingerpad": [
                            "r_rightfinger_pad1",
                            "r_rightfinger_pad2",
                            "r_rightfinger_pad3",
                            "r_rightfinger_pad4",
                        ],
                    },
                ),
            ),
        }

        super().__init__(idn, parts, control_freq, np_random, **kwargs)

    def is_terminated(self):
        return self.has_fallen_from_pose()

    def has_fallen_from_pose(self, tilt_deg_thresh: float = 20.0) -> bool:
        """Determine if robot has fallen given torso pose matrix."""
        min_z, max_z = self.standing_height
        torso_pos = self.sim.data.get_site_xpos(self.parts["torso"].site_name)
        torso_z = torso_pos[2]
        torso_mat = self.sim.data.get_site_xmat(self.parts["torso"].site_name).reshape(
            3, 3
        )
        torso_pose = make_pose(torso_pos, torso_mat)
        z_world = torso_pose[:3, 2]
        cos_theta = np.clip(z_world[2], -1.0, 1.0)
        tilt = float(np.arccos(cos_theta))
        return torso_z < min_z or torso_z > max_z or tilt > np.deg2rad(tilt_deg_thresh)

    @property
    def standing_height(self):
        return 0.9, 1.3
