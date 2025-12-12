from sai_mujoco.robots.base.v1 import BaseRobot_v1, Part_v1, ArmPart_v1


class T1_v1(BaseRobot_v1):
    name: str = "t1/v1"

    standing_height: list = [0.3, 0.7]

    def __init__(self, idn: int, control_freq: int, np_random, **kwargs):
        parts = {
            "head": Part_v1(
                _joint_names=["AAHead_yaw", "Head_pitch"],
                _actuator_names=["AAHead_yaw", "Head_pitch"],
                controller_config={
                    "type": "JOINT_POSITION",
                    "input_max": 1,
                    "input_min": -1,
                    "output_max": 0.5,
                    "output_min": -0.5,
                    "kd": 5,
                    "kv": 5,
                    "kp": 75,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                    "damping_ratio": 0.7,
                },
            ),
            "left_arm": ArmPart_v1(
                _joint_names=[
                    "Left_Shoulder_Pitch",
                    "Left_Shoulder_Roll",
                    "Left_Elbow_Pitch",
                    "Left_Elbow_Yaw",
                ],
                _actuator_names=[
                    "Left_Shoulder_Pitch",
                    "Left_Shoulder_Roll",
                    "Left_Elbow_Pitch",
                    "Left_Elbow_Yaw",
                ],
                controller_config={
                    "type": "JOINT_POSITION",
                    "input_max": 1,
                    "input_min": -1,
                    "output_max": 0.5,
                    "output_min": -0.5,
                    "kd": 5,
                    "kv": 5,
                    "kp": 75,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                    "damping_ratio": 0.7,
                },
            ),
            "right_arm": ArmPart_v1(
                _joint_names=[
                    "Right_Shoulder_Pitch",
                    "Right_Shoulder_Roll",
                    "Right_Elbow_Pitch",
                    "Right_Elbow_Yaw",
                ],
                _actuator_names=[
                    "Right_Shoulder_Pitch",
                    "Right_Shoulder_Roll",
                    "Right_Elbow_Pitch",
                    "Right_Elbow_Yaw",
                ],
                controller_config={
                    "type": "JOINT_POSITION",
                    "input_max": 1,
                    "input_min": -1,
                    "output_max": 0.5,
                    "output_min": -0.5,
                    "kd": 5,
                    "kv": 5,
                    "kp": 75,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                    "damping_ratio": 0.7,
                },
            ),
            "left_leg": Part_v1(
                _joint_names=[
                    "Left_Hip_Pitch",
                    "Left_Hip_Roll",
                    "Left_Hip_Yaw",
                    "Left_Knee_Pitch",
                    "Left_Ankle_Pitch",
                    "Left_Ankle_Roll",
                ],
                _actuator_names=[
                    "Left_Hip_Pitch",
                    "Left_Hip_Roll",
                    "Left_Hip_Yaw",
                    "Left_Knee_Pitch",
                    "Left_Ankle_Pitch",
                    "Left_Ankle_Roll",
                ],
                controller_config={
                    "type": "JOINT_POSITION",
                    "input_max": 1,
                    "input_min": -1,
                    "output_max": 0.5,
                    "output_min": -0.5,
                    "kd": 5,
                    "kv": 5,
                    "kp": 75,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                    "damping_ratio": 0.7,
                },
                _important_sites=["left_foot"],
            ),
            "right_leg": Part_v1(
                _joint_names=[
                    "Right_Hip_Pitch",
                    "Right_Hip_Roll",
                    "Right_Hip_Yaw",
                    "Right_Knee_Pitch",
                    "Right_Ankle_Pitch",
                    "Right_Ankle_Roll",
                ],
                _actuator_names=[
                    "Right_Hip_Pitch",
                    "Right_Hip_Roll",
                    "Right_Hip_Yaw",
                    "Right_Knee_Pitch",
                    "Right_Ankle_Pitch",
                    "Right_Ankle_Roll",
                ],
                controller_config={
                    "type": "JOINT_POSITION",
                    "input_max": 1,
                    "input_min": -1,
                    "output_max": 0.5,
                    "output_min": -0.5,
                    "kd": 5,
                    "kv": 5,
                    "kp": 75,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                    "damping_ratio": 0.7,
                },
                _important_sites=["right_foot"],
            ),
            "torso": Part_v1(
                _site_name="imu",
                _joint_names=[
                    "Waist",
                ],
                _actuator_names=["Waist"],
                controller_config={
                    "type": "JOINT_POSITION",
                    "input_max": 1,
                    "input_min": -1,
                    "output_max": 0.5,
                    "output_min": -0.5,
                    "kd": 5,
                    "kv": 5,
                    "kp": 75,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                    "damping_ratio": 0.7,
                },
            ),
        }

        super().__init__(idn, parts, control_freq, np_random, **kwargs)

    def is_terminated(self):
        # Check if the robot has fallen
        height = self.sim.data.get_site_xpos(self.parts["torso"].site_name)[2]
        min_height, _ = self.standing_height
        return not (min_height < height)


class LowerT1_v1(BaseRobot_v1):
    name: str = "t1/v1"
    xml_path: str = "t1/v1/robot_lower.xml"
    standing_height: list = [0.4, 0.7]

    def __init__(self, idn: int, control_freq: int, np_random, **kwargs):
        parts = {
            "torso": Part_v1(_site_name="imu", _joint_names=[]),
            "left_leg": Part_v1(
                _joint_names=[
                    "Left_Hip_Pitch",
                    "Left_Hip_Roll",
                    "Left_Hip_Yaw",
                    "Left_Knee_Pitch",
                    "Left_Ankle_Pitch",
                    "Left_Ankle_Roll",
                ],
                _actuator_names=[
                    "Left_Hip_Pitch",
                    "Left_Hip_Roll",
                    "Left_Hip_Yaw",
                    "Left_Knee_Pitch",
                    "Left_Ankle_Pitch",
                    "Left_Ankle_Roll",
                ],
                controller_config={
                    "type": "JOINT_TORQUE",
                    "input_max": [45.0, 45.0, 30.0, 65.0, 24.0, 15.0],
                    "input_min": [-45.0, -45.0, -30.0, -65.0, -24.0, -15.0],
                    "output_max": [45.0, 45.0, 30.0, 65.0, 24.0, 15.0],
                    "output_min": [-45.0, -45.0, -30.0, -65.0, -24.0, -15.0],
                    "kd": 5,
                    "kv": 5,
                    "kp": 75,
                    "use_torque_compensation": False,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                    "damping_ratio": 0.7,
                },
                _important_sites=["left_foot"],
            ),
            "right_leg": Part_v1(
                _joint_names=[
                    "Right_Hip_Pitch",
                    "Right_Hip_Roll",
                    "Right_Hip_Yaw",
                    "Right_Knee_Pitch",
                    "Right_Ankle_Pitch",
                    "Right_Ankle_Roll",
                ],
                _actuator_names=[
                    "Right_Hip_Pitch",
                    "Right_Hip_Roll",
                    "Right_Hip_Yaw",
                    "Right_Knee_Pitch",
                    "Right_Ankle_Pitch",
                    "Right_Ankle_Roll",
                ],
                controller_config={
                    "type": "JOINT_TORQUE",
                    "input_max": [45.0, 45.0, 30.0, 65.0, 24.0, 15.0],
                    "input_min": [-45.0, -45.0, -30.0, -65.0, -24.0, -15.0],
                    "output_max": [45.0, 45.0, 30.0, 65.0, 24.0, 15.0],
                    "output_min": [-45.0, -45.0, -30.0, -65.0, -24.0, -15.0],
                    "kd": 5,
                    "kv": 5,
                    "kp": 75,
                    "use_torque_compensation": False,
                    "velocity_limits": [-1, 1],
                    "kp_limits": [0, 1000],
                    "interpolation": None,
                    "ramp_ratio": 0.2,
                    "damping_ratio": 0.7,
                },
                _important_sites=["right_foot"],
            ),
        }

        super().__init__(idn, parts, control_freq, np_random, **kwargs)
    
    def is_terminated(self):
        # Check if the robot has fallen
        height = self.sim.data.get_site_xpos(self.parts["torso"].site_name)[2]
        min_height, _ = self.standing_height
        return not (min_height < height)
