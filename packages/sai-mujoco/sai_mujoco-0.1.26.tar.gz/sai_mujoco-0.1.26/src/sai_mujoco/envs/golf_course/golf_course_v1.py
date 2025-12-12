import numpy as np

from sai_mujoco.envs.base.base_v1 import BaseEnv_v1
from sai_mujoco.robots.base.v1 import GripperPart_v1


class GolfCourse_v1(BaseEnv_v1):
    r"""
    ## Description
    A Golf Course environment with playing a simplified golf game by grasping a golf club, striking a golf ball, and maneuvering it toward a designated hole.
    The robot must precisely control its end-effector to approach the club, align and close its gripper to secure it, lift the club, and swing to hit the
    ball, ultimately guiding the ball closer to the hole. The primary challenges are: precise manipulation for grasping, dynamic control for hitting the ball,
    and spatial reasoning to approach the hole, all within a continuous and high-dimensional action and observation space.

    ## Observation Space
    The observation space consists of the following parts (in order):

    - *qpos:* Position values of the robot's body parts. The dimensionality depends on the robot's joint configuration.
    - *qvel:* The velocities of these individual body parts (their derivatives). The dimensionality depends on the robot's joint configuration.
    - *ball_xpos (3 elements):* The golf ball's position in the world frame.
    - *golf_club_xpos (3 elements):* The golf club's position in the world frame.
    - *golf_club_quat (4 elements):* The quaternion orientation of the golf club in the world frame.
    - *hole_xpos (3 elements):* The golf hole's position in the world frame.

    The order of elements in the observation space related to the environment is as follows -

    | Num | Observation                        | Min  | Max | Type (Unit)              |
    | --- | -----------------------------------| ---- | --- | ------------------------ |
    | 0   | x-coordinate of the golf ball      | -Inf | Inf | position (m)             |
    | 1   | y-coordinate of the golf ball      | -Inf | Inf | position (m)             |
    | 2   | z-coordinate of the golf ball      | -Inf | Inf | position (m)             |
    | 3   | x-coordinate of the golf club      | -Inf | Inf | position (m)             |
    | 4   | y-coordinate of the golf club      | -Inf | Inf | position (m)             |
    | 5   | z-coordinate of the golf club      | -Inf | Inf | position (m)             |
    | 6   | w quaternion of the golf club      | -Inf | Inf | orientation (q)          |
    | 7   | x quaternion of the golf club      | -Inf | Inf | orientation (q)          |
    | 8   | y quaternion of the golf club      | -Inf | Inf | orientation (q)          |
    | 9   | z quaternion of the golf club      | -Inf | Inf | orientation (q)          |
    | 10  | x-coordinate of the hole           | -Inf | Inf | position (m)             |
    | 11  | y-coordinate of the hole           | -Inf | Inf | position (m)             |
    | 12  | z-coordinate of the hole           | -Inf | Inf | position (m)             |

    ## Rewards

    The reward components include:

        1. `ee_club_dist` (weight: 0.1): Encourages the end-effector to move closer to the club grip.
        2. `grasp_club` (weight: 0.2): Rewards proper grasping of the club grip with the fingers.
        3. `ball_hole_dist` (weight: 0.4): Encourages minimizing the distance between the golf ball and the hole.
        4. `ball_in_hole` (weight: 200.0): Rewards when the ball enters the hole.
        5. `club_dropped` (weight: -100.0): Penalizes dropping the club prematurely.
        6. `ball_passed_hole` (weight: -50.0): Penalizes overshooting the ball past the hole.
        7. `joint_vel` (weight: -0.0001): Penalizes high joint velocities to encourage smooth motions.
        8. `timestep` (weight: -0.2): Penalizes the agent for taking more timesteps to complete the task.

    `info` contains the success parameter if the given episode succeeded.

    ## Episode End
    ### Termination

    The current episode should terminate based on three termination criteria defined as follow:
        1. If the golf ball has entered the hole
        2. If the ball has passed beyond the hole without entering
        3. If the golf club has been dropped

    ### Truncation
    The default duration of an episode is 650 timesteps.

    ## Arguments
    Env provides the parameter to modify the start state of the robot upon reset.
    It can be applied during `gymnasium.make` by changing deterministic_reset (bool).
    """

    env_name: str = "golf_course/v0"
    scene_name: str = "v0/base_scene"
    default_camera_config = {
        "distance": 2.8,
        "azimuth": -130,
        "elevation": -45.0,
        "lookat": np.array([0.2, 0.0, 0.35]),
    }

    reward_config = {
        "ee_club_dist": 0.1,
        "grasp_club": 0.2,
        "ball_hole_dist": 0.3,
        "ball_in_hole": 200.0,
        "club_dropped": -100.0,
        "ball_passed_hole": -50.0,
        "joint_vel": -0.0001,
        "timestep": -0.6,
    }

    single_robot = True

    def _get_env_obs(self):
        """
        Collects and returns the current environment observation.

        This function gathers the relevant physical states of the main entities
        in the golf simulation environment—namely, the golf ball, the golf club,
        and the hole—and concatenates their positions and orientation into a single
        observation vector.

        Specifically, it retrieves:
            - The 3D position of the golf ball (`ball_xpos`)
            - The 3D position of the golf club (`golf_club_xpos`)
            - The orientation of the golf club as a quaternion (`golf_club_quat`)
            - The 3D position of the hole (`hole_xpos`)

        The final observation is a 13-dimensional float32 NumPy array:
            [ball_x, ball_y, ball_z,
            club_x, club_y, club_z,
            club_qw, club_qx, club_qy, club_qz,
            hole_x, hole_y, hole_z]

        Returns
        -------
        obs : np.ndarray of shape (13,), dtype np.float32
            The concatenated observation vector representing the positions and
            orientation of key environment elements.
        """
        ball_xpos = self.sim.data.xpos[self.golf_ball_id]
        hole_xpos = self.sim.data.xpos[self.golf_hole_id]
        golf_club_xpos = self.sim.data.xpos[self.golf_club_id]
        golf_club_quat = self.sim.data.xquat[self.golf_club_id]

        obs = np.concatenate(
            [ball_xpos, golf_club_xpos, golf_club_quat, hole_xpos],
            dtype=np.float32,
        )

        return obs

    def compute_terminated(self):
        """
        Determines whether the current episode should terminate based on task conditions.

        This function checks for three termination criteria in the golf environment:
            1. If the golf ball has entered the hole (`_ball_in_hole`)
            2. If the ball has passed beyond the hole without entering (`_ball_passed_hole`)
            3. If the golf club has been dropped (`_club_dropped`)

        Returns
        -------
        terminated : bool
            `True` if any of the termination conditions are met; otherwise `False`.
        """
        ball_pos = self.sim.data.xpos[self.golf_ball_id]
        hole_pos = self.sim.data.xpos[self.golf_hole_id]
        club_grip_pos = self.sim.data.xpos[self.golf_club_id]

        is_ball_in_hole = self._ball_in_hole(ball_pos, hole_pos)
        is_ball_passed_hole = self._ball_passed_hole(ball_pos, hole_pos)
        is_club_dropped = self._club_dropped(club_grip_pos)
        return bool(is_ball_in_hole or is_ball_passed_hole or is_club_dropped)

    def _setup_references(self):
        """
        Initializes and stores environment-specific reference IDs for key entities in the simulation.

        This function sets up MuJoCo internal IDs (body and site IDs) for objects and components
        involved in the golf environment. These references are necessary for accessing
        position, orientation, and other dynamic properties during simulation.

        Specifically, it retrieves:
            - Body IDs for the golf ball, hole (flag assembly), golf club grip, and club head
            - Site ID for the left arm end-effector
            - Body names and IDs for the left and right gripper fingers of the left arm

        These references are stored as instance attributes and used throughout the environment
        for computing observations, rewards, and termination conditions.
        """

        super()._setup_references()

        # Set body IDs for various objects like golf ball, golf hole, and the golf club.
        self.golf_ball_id = self.sim.model.body_name2id("golf_ball")
        self.golf_hole_id = self.sim.model.body_name2id("flag_assembly")
        self.golf_club_id = self.sim.model.body_name2id("grip_link")
        self.club_head_id = self.sim.model.body_name2id("head_link")

        self.golf_club_geom = "grip_collision"

        self.ee_site_name = self.robots[0]._arms["left_arm"].gripper.site_name

        self.left_finger_body_name = (
            self.robots[0]._arms["left_arm"].gripper.important_bodies["left_finger"]
        )
        self.left_finger_body_id = self.sim.model.body_name2id(
            self.left_finger_body_name
        )

        self.right_finger_body_name = (
            self.robots[0]._arms["left_arm"].gripper.important_bodies["right_finger"]
        )
        self.right_finger_body_id = self.sim.model.body_name2id(
            self.right_finger_body_name
        )

    def compute_reward(self):
        """
        Computes and returns individual reward components for the current simulation state.

        The reward components include:

        1. `ee_club_dist`: Encourages the end-effector to move closer to the club grip.
        2. `grasp_club`: Rewards proper grasping of the club grip with the fingers.
        3. `ball_hole_dist`: Encourages minimizing the distance between the golf ball and the hole.
        4. `joint_vel`: Penalizes high joint velocities to encourage smooth motions.
        5. `club_dropped`: Penalizes dropping the club prematurely.
        6. `ball_passed_hole`: Penalizes overshooting the ball past the hole.
        7. `ball_in_hole`: Rewards when the ball enters the hole.
        8. `timestep`: Penalizes the agent for taking more timesteps to complete the task.

        Returns
        -------
        raw_reward : dict
            A dictionary mapping each reward term name (str) to its corresponding scalar value (float).
            These are raw values and not yet combined into a scalar total reward.
        """
        # Get positions and orientations
        ee_pos = self.sim.data.get_site_xpos(self.ee_site_name)

        # Get club grip position and orientation
        club_grip_pos = self.sim.data.xpos[self.golf_club_id]

        # Get ball and hole positions
        ball_pos = self.sim.data.xpos[self.golf_ball_id]
        hole_pos = self.sim.data.xpos[self.golf_hole_id]

        # 1. Approach the club grip
        approach_ee_club_grip = self._ee_club_dist(ee_pos, club_grip_pos)

        # 2. Grasp the club
        grasp_club = (
            1.0
            if self._check_grasp(
                self.robots[0]._arms["left_arm"].gripper, self.golf_club_geom
            )
            else 0.0
        )

        # 3. Approach ball to the hole
        approach_ball_hole = self._ball_hole_dist(ball_pos, hole_pos)

        # 4. Penalize joint velocities
        joint_vel = self._joint_vel_l2()

        # 5. Penalize if the club is dropped
        club_dropped = self._club_dropped(club_grip_pos)

        # 6. Penalize if the ball passed the hole
        ball_passed_hole = self._ball_passed_hole(ball_pos, hole_pos)

        # 7. Reward if the ball is in the hole
        ball_in_hole = self._ball_in_hole(ball_pos, hole_pos)

        raw_reward = {
            "ee_club_dist": approach_ee_club_grip,
            "grasp_club": grasp_club,
            "ball_hole_dist": approach_ball_hole,
            "ball_in_hole": ball_in_hole,
            "club_dropped": club_dropped,
            "ball_passed_hole": ball_passed_hole,
            "joint_vel": joint_vel,
            "timestep": 1.0,
        }
        return raw_reward

    def _ee_club_dist(self, ee_pos, club_grip_pos):
        """
        Computes a reward based on the distance between the end-effector and the club grip.

        This function calculates how close the end-effector is to the target position
        above the club grip. A vertical offset of 0.12 meters is added to the club grip
        position to encourage approaching from above, which is typically better for grasping.

        The reward is computed using a hyperbolic tangent function based on the Euclidean distance:
            reward = 1 - tanh(10 * distance)

        Parameters
        ----------
        ee_pos : np.ndarray of shape (3,)
            The 3D position of the robot end-effector.
        club_grip_pos : np.ndarray of shape (3,)
            The 3D position of the golf club grip.

        Returns
        -------
        rew : float
            A reward scalar with higher values indicating closer proximity
            to the target approach point above the club grip.
        """
        target_pos = club_grip_pos.copy()
        target_pos[2] += 0.12  # Add offset for z axis
        dist = np.linalg.norm(ee_pos - target_pos)
        rew = 1 - np.tanh(10 * dist, dtype=np.float32)
        return rew

    def _ball_hole_dist(self, ball_pos, hole_pos):
        """
        Computes a reward based on the distance between the ball and the hole.

        This function calculates the Euclidean distance between the golf ball and the hole,
        then returns a reward based on a hyperbolic tangent function of this distance. The reward
        is highest when the ball is close to the hole and decreases as the distance increases.

        Parameters
        ----------
        ball_pos : np.ndarray of shape (3,)
            The 3D position of the golf ball.
        hole_pos : np.ndarray of shape (3,)
            The 3D position of the hole.

        Returns
        -------
        reward : float
            A scalar reward based on the distance between the ball and the hole.
            The reward is higher for closer proximity and decays exponentially with distance.
        """
        distance = np.linalg.norm(ball_pos - hole_pos)
        reward = 1 - np.tanh(10 * distance, dtype=np.float32)
        return reward

    def _joint_vel_l2(self):
        """
        Computes the penalty for joint velocities in the system.

        This function calculates the L2 norm (sum of squares) of the joint velocities,
        which acts as a penalty term. The penalty encourages the robot to move smoothly,
        avoiding rapid or jerky movements that could result from high joint velocities.

        Returns
        -------
        penalty : float
            The total L2 penalty for all robot joint velocities. Higher values indicate
            faster and more abrupt movements, which are penalized more heavily.
        """
        joint_vel = []
        for robot in self.robots:
            for joint in robot.robot_joints:
                joint_vel.append(self.sim.data.get_joint_qvel(joint))
        joint_vel = np.array(joint_vel)
        return np.sum(joint_vel**2, dtype=np.float32)

    def _club_dropped(self, club_grip_pos, minimum_height=0.06):
        """
        Penalizes if the golf club is dropped below a specified minimum height.

        This function checks if the grip of the golf club falls below a certain height threshold
        (default is 0.06 meters), which signifies that the club has been dropped. A penalty is
        returned when the club's grip position violates this condition.

        Parameters
        ----------
        club_grip_pos : np.ndarray of shape (3,)
            The 3D position of the golf club grip.
        minimum_height : float, optional, default=0.06
            The minimum height threshold to determine if the club has been dropped.

        Returns
        -------
        penalty : float
            A scalar penalty of 1.0 if the club has dropped (i.e., its z-position is below the threshold),
            otherwise 0.0.
        """
        return float(club_grip_pos[2] < minimum_height)

    def _ball_passed_hole(self, ball_pos, hole_pos):
        """
        Penalizes if the ball has passed beyond the hole in the x-direction.

        This function checks if the golf ball has moved past the hole in the x-axis direction,
        indicating that the ball has overshot the hole. A penalty is applied when this condition is met.

        Parameters
        ----------
        ball_pos : np.ndarray of shape (3,)
            The 3D position of the golf ball.
        hole_pos : np.ndarray of shape (3,)
            The 3D position of the hole.

        Returns
        -------
        penalty : float
            A scalar penalty of 1.0 if the ball has passed the hole in the x-direction (with an offset),
            otherwise 0.0.
        """
        # Check if the ball has passed the hole in the x direction
        return float(ball_pos[0] < hole_pos[0] - 0.08)

    def _ball_in_hole(self, ball_pos, hole_pos):
        """
        Checks if the ball is within the hole.

        This function computes the Euclidean distance between the golf ball and the hole.
        If the distance is below a specified threshold (0.06 meters), it considers the ball to be in the hole.

        Parameters
        ----------
        ball_pos : np.ndarray of shape (3,)
            The 3D position of the golf ball.
        hole_pos : np.ndarray of shape (3,)
            The 3D position of the hole.

        Returns
        -------
        is_in_hole : float
            A scalar value of 1.0 if the ball is within the hole (distance is below the threshold),
            otherwise 0.0.
        """
        return (np.linalg.norm(ball_pos - hole_pos) < 0.06).astype(np.float32)

    def _get_info(self) -> dict:
        return {
            "success": bool(
                self._ball_in_hole(
                    self.sim.data.xpos[self.golf_ball_id],
                    self.sim.data.xpos[self.golf_hole_id],
                )
            )
        }

    def _check_grasp(self, gripper, object_geoms):
        """
        Checks whether the specified gripper as defined by @gripper is grasping the specified object in the environment.
        If multiple grippers are specified, will return True if at least one gripper is grasping the object.

        By default, this will return True if at least one geom in both the "left_fingerpad" and "right_fingerpad" geom
        groups are in contact with any geom specified by @object_geoms. Custom gripper geom groups can be
        specified with @gripper as well.

        Args:
            gripper (GripperModel or str or list of str or list of list of str or dict): If a MujocoModel, this is specific
                gripper to check for grasping (as defined by "left_fingerpad" and "right_fingerpad" geom groups). Otherwise,
                this sets custom gripper geom groups which together define a grasp. This can be a string
                (one group of single gripper geom), a list of string (multiple groups of single gripper geoms) or a
                list of list of string (multiple groups of multiple gripper geoms), or a dictionary in the case
                where the robot has multiple arms/grippers. At least one geom from each group must be in contact
                with any geom in @object_geoms for this method to return True.
            object_geoms (str or list of str or MujocoModel): If a MujocoModel is inputted, will check for any
                collisions with the model's contact_geoms. Otherwise, this should be specific geom name(s) composing
                the object to check for contact.

        Returns:
            bool: True if the gripper is grasping the given object
        """
        # Convert object, gripper geoms into standardized form
        o_geoms = [object_geoms] if type(object_geoms) is str else object_geoms

        if isinstance(gripper, GripperPart_v1):
            g_geoms = [
                gripper.important_geoms["left_fingerpad"],
                gripper.important_geoms["right_fingerpad"],
            ]
        elif type(gripper) is str:
            g_geoms = [[gripper]]
        elif isinstance(gripper, dict):
            assert all([isinstance(gripper[arm], GripperPart_v1) for arm in gripper]), (
                "Invalid gripper dict format!"
            )
            return any(
                [self._check_grasp(gripper[arm], object_geoms) for arm in gripper]
            )
        else:
            # Parse each element in the gripper_geoms list accordingly
            g_geoms = [
                [g_group] if type(g_group) is str else g_group for g_group in gripper
            ]

        # Search for collisions between each gripper geom group and the object geoms group
        for g_group in g_geoms:
            if not self.check_contact(g_group, o_geoms):
                return False
        return True
