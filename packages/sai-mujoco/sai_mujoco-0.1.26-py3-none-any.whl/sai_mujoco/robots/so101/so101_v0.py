import numpy as np
from sai_mujoco.robots.base.v1 import BaseRobot_v1, ArmPart_v1, GripperPart_v1

class SO101Gripper_v0(GripperPart_v1):
    @property
    def dof(self):
        return 1

    def format_action(self, action):
        """
        Maps continuous action to a single scalar command for the hinge gripper.

        Args:
            action (np.array): gripper-specific action of shape (1,)

        Raises:
            AssertionError: [Invalid action dimension size]
        """
        assert len(action) == self.dof
        return np.clip(action, -1.0, 1.0)

class SO101_v0(BaseRobot_v1):
    r"""
    Robot model for the LeRobot SO-101 arm consisting of 5 DOFs and a gripper.

    This class defines the robot kinematics, default joint configuration, and controller parameters for a generic collaborative manipulator in the Sai MuJoCo framework.

    Attributes
    ----------
    default_pose : list of float
        A 6-element list specifying the default joint positions (radians) for
        [shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll, gripper] on reset.
    name : str
        Unique identifier for this robot class (“lerobot”).
    metadata : dict
        Rendering configuration, including available modes (“human”, “rgb_array”, “depth_array”) and frames per second (“render_fps”: 12).
    left_arm : ArmPart
        Defines the 5-DOF arm part, including:
          - `joint_names`: List of 5 joint names in the MuJoCo XML.
          - `_actuator_names`: List of 5 actuator keys corresponding to position control
          - `controller_config`: Joint-position controller gains and limits.
        The `gripper` sub-part is a `GripperPart` that encapsulates:
          - `joint_names`: Single hinge joint (“gripper”).
          - `_actuator_names`: Single position actuator (“gripper”).
          - `site_name`: Name of the grasp / end-effector site in the MuJoCo model (“gripperframe”).
          - `controller_config`: Grip-specific control mode (“GRIP”).

    ## Observation Space

    The observation space consists of the following parts (in order):

    - *qpos (6 elements):* Position values of the robot's body parts. 5 elements for the arm and 1 for the gripper.
    - *qvel (6 elements):* The velocities of these individual body parts. 5 for the arm, 1 for the gripper.

    The order of elements in the observation space related to LeRobot is as follows -

    | Num | Observation                | Min  | Max | Type (Unit)              |
    | --- | -------------------------- | ---- | --- | ------------------------ |
    | 0   | shoulder_pan position      | -Inf | Inf | orientation (rad)        |
    | 1   | shoulder_lift position     | -Inf | Inf | orientation (rad)        |
    | 2   | elbow_flex position        | -Inf | Inf | orientation (rad)        |
    | 3   | wrist_flex position        | -Inf | Inf | orientation (rad)        |
    | 4   | wrist_roll position        | -Inf | Inf | orientation (rad)        |
    | 5   | gripper position           | -Inf | Inf | orientation (rad)        |
    | 6   | shoulder_pan velocity      | -Inf | Inf | angular velocity (rad/s) |
    | 7   | shoulder_lift velocity     | -Inf | Inf | angular velocity (rad/s) |
    | 8   | elbow_flex velocity        | -Inf | Inf | angular velocity (rad/s) |
    | 9   | wrist_flex velocity        | -Inf | Inf | angular velocity (rad/s) |
    | 10  | wrist_roll velocity        | -Inf | Inf | angular velocity (rad/s) |
    | 11  | gripper velocity           | -Inf | Inf | angular velocity (rad/s) |

    ## Action Space

    The action space is a continuous vector of shape `(6,)`, where each dimension directly
    commands a joint-position target (per-step delta / setpoint, depending on your controller layer).

    | Index | Action                                     |
    | ----- | ------------------------------------------ |
    | 0     | shoulder_pan position                      |
    | 1     | shoulder_lift position                     |
    | 2     | elbow_flex position                        |
    | 3     | wrist_flex position                        |
    | 4     | wrist_roll position                        |
    | 5     | Gripper Open/Close (continuous scalar)     |

    All six joints are position actuated in the XML, with actuator names equal to joint names.
    """

    name: str = "so101/v0"

    def __init__(self, idn: int, control_freq: int, np_random, **kwargs):
        parts = {
            "left_arm": ArmPart_v1(
                _joint_names=[
                    "shoulder_pan",
                    "shoulder_lift",
                    "elbow_flex",
                    "wrist_flex",
                    "wrist_roll",
                ],
                _actuator_names=[
                    "shoulder_pan",
                    "shoulder_lift",
                    "elbow_flex",
                    "wrist_flex",
                    "wrist_roll",
                ],
                controller_config={
                    "type": "OSC_POSE",
                    "input_max": 1,
                    "input_min": -1,
                    "kp": 500,
                    "damping_ratio": 1.5,
                    "impedance_mode": "fixed",
                    "kp_limits": [0, 600],
                    "damping_ratio_limits": [0, 10],
                    "position_limits": None,
                    "orientation_limits": None,
                    "uncouple_pos_ori": True,
                    "input_type": "delta",
                    "input_ref_frame": "base",
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                },
                gripper=SO101Gripper_v0(
                    _joint_names=["gripper"],
                    _actuator_names=["gripper"],
                    _site_name="gripperframe",
                    _important_geoms={
                        "left_fingerpad": [
                            "l_fingerpad1",
                            "l_fingerpad2",
                            "l_fingerpad3",
                            "l_fingerpad4",
                        ],
                        "right_fingerpad": [
                            "r_fingerpad1",
                            "r_fingerpad2",
                            "r_fingerpad3",
                        ],
                    },
                    controller_config={"type": "GRIP"},
                ),
            )
        }

        super().__init__(
            idn=idn,
            parts=parts,
            control_freq=control_freq,
            np_random=np_random,
            **kwargs,
        )
