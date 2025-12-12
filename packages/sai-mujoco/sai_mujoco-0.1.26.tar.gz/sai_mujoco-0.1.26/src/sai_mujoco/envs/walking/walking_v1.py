
# This code is built upon the following open source code https://github.com/BoosterRobotics/booster_gym

import numpy as np

from sai_mujoco.envs.base.base_v1 import BaseEnv_v1
from sai_mujoco.utils.v0.sim_utils import check_contact


class Walking_v1(BaseEnv_v1):
    """
    ## Description
    A Walking environment where a robot learns to walk and maintain stable locomotion. The robot must learn to coordinate its
    leg movements to achieve forward motion while maintaining balance and avoiding falls. The primary challenges include:
    maintaining upright posture, coordinating foot movements for stable gait, managing energy efficiency, and adapting to
    different walking speeds and terrains, all within a continuous and high-dimensional action and observation space.

    ## Observation Space
    The observation space consists of the following parts (in order):

    - *qpos:* Position values of the robot's body parts. The dimensionality depends on the robot's joint configuration.
    - *qvel:* The velocities of these individual body parts (their derivatives). The dimensionality depends on the robot's joint configuration.
    - *last_action:* The last action taken by the robot, used for action rate calculations.
    - *ang_vel:* The angular velocity of the robot's torso, used to monitor rotational
    - *projected_gravity:* The projected gravity vector in the robot's local frame, used to maintain upright posture.

    The observation space is inherited from the base environment and includes the robot's joint positions and velocities.

    ## Rewards

    The reward components include:

        1. `linear_vel_z` (weight: -0.1): Penalizes vertical linear velocity for stable motion.
        2. `ang_vel_xy` (weight: -0.15): Penalizes angular velocity in the xy-axis to encourage smooth motion.
        3. `cost_torques` (weight: -2e-4): Penalizes high actuator torques to encourage energy efficiency.
        4. `action_rate` (weight: -1.0): Penalizes rapid action changes to encourage smooth motion.
        5. `robot_energy` (weight: -2e-3): Penalizes energy consumption based on joint velocities and torques.
        6. `dof_qacc` (weight: -1e-7): Penalizes high joint accelerations.
        7. `dof_qvel` (weight: -1e-4): Penalizes high joint velocities.
        8. `linear_vel_x` (weight: 0.25): Rewards forward linear velocity to encourage walking.

    ## Episode End
    ### Termination

    The current episode should terminate based on the following criteria:
        1. If the robot has fallen (base height outside acceptable range)
        2. If the simulation data contains NaN values

    ### Truncation
    The episode will be truncated when the maximum number of timesteps is reached.
    """

    scene_name: str = "v0/base_scene"

    default_camera_config = {
        "trackbodyid": 0,
        "distance": 5,
    }

    reward_config = {
        "linear_vel_z": -0.1,
        "ang_vel_xy": -0.15,
        "cost_torques": -2e-4,
        "action_rate": -1.0,
        "robot_energy": -2e-3,
        "dof_qacc": -1e-7,
        "dof_qvel": -1e-4,
        "linear_vel_x": 0.25,
    }

    def __init__(self, *args, **kwargs):
        self.last_action = None
        self.current_action = None
        super().__init__(*args, **kwargs)

    def _pre_action(self, action, policy_step):
        self.current_action = action
        return super()._pre_action(action, policy_step)

    def compute_reward(self) -> dict:
        """
        Computes and returns individual reward components for the current simulation state.

        This function calculates various reward terms that encourage stable walking behavior:
        - Penalizes vertical motion and angular velocities to encourage forward walking
        - Rewards maintaining upright posture and target base height
        - Penalizes foot slipping during stance phase

        Returns
        -------
        raw_reward : dict
            A dictionary mapping each reward term name (str) to its corresponding scalar value (float).
            These are raw values and not yet combined into a scalar total reward.
        """
        base_height = self.sim.data.get_site_xpos(self._root_site)[2]
        [linear_vel_x, linear_vel_y, linear_vel_z] = self.robots[
            0
        ].get_sensor_measurement("torso_vel")
        linear_vel_z = np.square(linear_vel_z)
        [ang_vel_x, ang_vel_y, ang_vel_z] = self.robots[0].get_sensor_measurement(
            "torso_gyro"
        )
        ang_vel_xy = np.sum(np.square([ang_vel_x, ang_vel_y]))

        robot_energy = self.robot_energy()
        cost_torques = np.sum(np.square(self.sim.data.actuator_force))
        robot_joints_qvel = np.array(
            [self.sim.data.get_joint_qvel(j) for j in self.robots[0].robot_joints]
        )
        robot_joints_qacc = np.array(
            [self.sim.data.get_joint_qacc(j) for j in self.robots[0].robot_joints]
        )
        dof_qacc = np.sum(np.square(robot_joints_qacc))
        dof_qvel = np.sum(np.square(robot_joints_qvel))
        action_rate = np.sum(np.square(self.last_action - self.current_action))

        return {
            "linear_vel_z": linear_vel_z,
            "ang_vel_xy": ang_vel_xy,
            "cost_torques": cost_torques,
            "robot_energy": robot_energy,
            "dof_qacc": dof_qacc,
            "dof_qvel": dof_qvel,
            "linear_vel_x": linear_vel_x,
            "action_rate": action_rate,
        }

    def compute_terminated(self) -> bool:
        """
        Determines whether the current episode should terminate based on failure conditions.

        This function checks for two termination criteria in the walking environment:
            1. If the robot has fallen (base height outside acceptable range)
            2. If the simulation data contains NaN values (indicating numerical instability)

        Returns
        -------
        terminated : bool
            `True` if any of the termination conditions are met; otherwise `False`.
        """
        data_nan = (
            np.isnan(self.sim.data.qpos).any() | np.isnan(self.sim.data.qvel).any()
        )

        return bool(data_nan)

    def _setup_references(self):
        """
        Initializes and stores environment-specific reference IDs for key components in the simulation.

        This function sets up MuJoCo internal IDs (site IDs) for robot components involved in the walking
        environment. These references are necessary for accessing position, orientation, and other dynamic
        properties during simulation.

        Specifically, it retrieves:
            - Site IDs for the robot's feet (left and right)
            - Floor geometry name for contact detection
            - Root site ID for base position tracking

        These references are stored as instance attributes and used throughout the environment
        for computing observations, rewards, and termination conditions.
        """
        super()._setup_references()

        self.last_action = None
        self.current_action = None

        self.left_feet_geoms = self.robots[0].parts["left_leg"].important_geoms
        self.right_feet_geoms = self.robots[0].parts["right_leg"].important_geoms

        self.left_leg_sites = self.robots[0].parts["left_leg"].important_sites
        self.right_leg_sites = self.robots[0].parts["right_leg"].important_sites

        self._feet_site_id = np.array(
            [self.sim.model.site(site).id for site in self.left_leg_sites]
            + [self.sim.model.site(site).id for site in self.right_leg_sites]
        )

        self._floor_geom = "floor"
        self._root_site = self.robots[0].parts["torso"].site_name

    def _get_env_obs(self):
        projected_gravity = self.quat_rotate_inverse(
            self.robots[0].get_sensor_measurement("torso_quat"), np.array([0, 0, -1])
        )
        ang_vel = self.robots[0].get_sensor_measurement("torso_gyro")

        # initialize last_action if it is None, since get_obs is called inside of initialize
        if self.last_action is None:
            self.last_action = np.zeros(self.action_dim, dtype=np.float32)

        if self.current_action is None:
            self.current_action = np.zeros(self.action_dim, dtype=np.float32)

        last_action = self.last_action
        self.last_action = self.current_action

        return np.concatenate(
            [
                last_action,
                projected_gravity,
                ang_vel,
            ]
        )

    def has_robot_fallen(self, height, min_height=1.0, max_height=2.0):
        """
        Determines if the robot has fallen based on its base height.

        This function checks if the robot's base height is within an acceptable range.
        If the robot has a defined standing height range, it uses those values;
        otherwise, it uses the default minimum and maximum height thresholds.

        Parameters
        ----------
        height : float
            The current height of the robot's base from the ground.
        min_height : float, optional, default=1.0
            The minimum acceptable height for the robot base.
        max_height : float, optional, default=2.0
            The maximum acceptable height for the robot base.

        Returns
        -------
        fallen : bool
            `True` if the robot has fallen (height outside acceptable range); otherwise `False`.
        """
        if hasattr(self.robots[0], "standing_height"):
            min_height = self.robots[0].standing_height[0]
            max_height = self.robots[0].standing_height[1]
        else:
            raise ValueError("Robot does not have a defined standing height range.")

        fallen = min_height < height < max_height
        return not fallen

    def robot_energy(self):
        """
        Computes the energy consumption of the robot based on joint velocities and actuator forces.

        This function calculates the total energy consumption by multiplying joint velocities
        with actuator forces and taking the absolute sum. This encourages the robot to move
        efficiently and avoid wasteful energy consumption.

        Returns
        -------
        energy : float
            The total energy consumption of the robot (joint velocity * actuator force).
        """
        actuators_ids = [
            self.sim.model.actuator(name).id for name in self.robots[0].robot_actuators
        ]
        forces = self.sim.data.actuator_force[actuators_ids]
        vel = np.array(
            [self.sim.data.get_joint_qvel(j) for j in self.robots[0].robot_joints]
        )

        return np.sum((vel * forces).clip(min=0.0))

    def foot_clearance(self, max_foot_height: float = 0.12):
        """
        Computes a reward based on foot clearance during the swing phase of walking.

        This function calculates how well the robot's feet clear the ground during the swing
        phase. It considers the vertical distance of each foot from a maximum foot height
        threshold, weighted by the horizontal velocity of the feet. This encourages proper
        foot lifting during walking.

        Parameters
        ----------
        max_foot_height : float, optional, default=0.12
            The maximum acceptable foot height during swing phase.

        Returns
        -------
        clearance_reward : float
            A reward based on foot clearance, higher values indicate better foot lifting.
        """
        feet_vel = self.robots[0].get_sensor_measurement("global_linvel")
        vel_xy = feet_vel[..., :2]
        vel_norm = np.sqrt(np.linalg.norm(vel_xy, axis=-1))
        foot_pos = self.sim.data.site_xpos[self._feet_site_id]
        foot_z = foot_pos[..., -1]
        delta = np.abs(foot_z - max_foot_height)

        return np.sum(delta * vel_norm)

    def _feet_contact(self):
        """
        Determines which feet are in contact with the ground.

        This function checks the contact status between the robot's feet and the floor
        using MuJoCo's contact detection system. It returns a boolean array indicating
        which feet are currently in contact with the ground.

        Returns
        -------
        contact : np.ndarray
            A boolean array indicating which feet are in contact with the ground.
        """
        left_feet_contact = np.array(
            [
                check_contact(self.sim, geom, self._floor_geom)
                for geom in self.left_feet_geoms
            ]
        )
        right_feet_contact = np.array(
            [
                check_contact(self.sim, geom, self._floor_geom)
                for geom in self.right_feet_geoms
            ]
        )
        contact = np.hstack([np.any(left_feet_contact), np.any(right_feet_contact)])

        return contact

    def feet_distance(self):
        """
        Computes a penalty based on the distance between the robot's feet.

        This function calculates the distance between the left and right feet in the robot's
        local coordinate frame. It penalizes feet being too close together, which can lead
        to instability during walking. The penalty is clipped to encourage maintaining a
        reasonable stance width.

        Returns
        -------
        distance_penalty : float
            A penalty based on feet distance, higher values indicate feet are too close.
        """
        left_foot_pos = self.sim.data.site_xpos[self._feet_site_id[0]]
        right_foot_pos = self.sim.data.site_xpos[self._feet_site_id[1]]
        base_xmat = self.sim.data.get_site_xmat(self._root_site)
        base_yaw = np.arctan2(base_xmat[1], base_xmat[0])
        feet_distance = np.abs(
            np.cos(base_yaw) * (left_foot_pos[1] - right_foot_pos[1])
            - np.sin(base_yaw) * (left_foot_pos[0] - right_foot_pos[0])
        )
        return np.clip(0.2 - feet_distance, 0.0, 0.1)

    def quat_rotate_inverse(self, q, v):
        q_w = q[-1]
        q_vec = q[:3]
        a = v * (2.0 * q_w**2 - 1.0)
        b = np.cross(q_vec, v) * (q_w * 2.0)
        c = q_vec * (np.dot(q_vec, v) * 2.0)
        return a - b + c
