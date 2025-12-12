from re import L
import mujoco
import numpy as np
import random
from sai_mujoco.envs.base.base_v1 import BaseEnv_v1
from sai_mujoco.robots.base.v1 import GripperPart_v1
from sai_mujoco.utils.v0.rotations import mat2euler


def goal_distance(goal_a, goal_b):
    """Calculate the Euclidean distance between two goals.

    Args:
        goal_a (np.ndarray): First goal position
        goal_b (np.ndarray): Second goal position

    Returns:
        float: Euclidean distance between the two goals
    """
    assert goal_a.shape == goal_b.shape
    return np.linalg.norm(goal_a - goal_b, axis=-1)


class PickAndPlace_v1(BaseEnv_v1):
    """

        ## Description
        A Pick and place environment designed for object lifting. The task is to control the robot arm to reach, grasp, and lift a single cube from
        the table surface, and then place it accurately at a designated target position.

        ## Observation Space
        The observation space consists of the following parts (in order):

        - *qpos:* Position values of the robot's body parts. The dimensionality depends on the robot's joint configuration.
        - *qvel:* The velocities of these individual body parts (their derivatives). The dimensionality depends on the robot's joint configuration.
        - *gripper_pos (3 elements):* The end effector's position in the world frame.
        - *object_pos (3 elements):* The object's position in the world frame.
        - *pos_rel_gripper_object (3 elements):* The object's position in the end effector frame.
        - *vel_rel_gripper_object (3 elements):* The object's velocity in the end effector frame.
        - *object_rot (3 elements):* The object's rotation (euler angles) in the world frame.
        - *object_velp (3 elements):* The object's linear velocity in the world frame.
        - *object_velr (3 elements):* The object's rotational velocity in the world frame.
        - *target_pos (3 elements):* The target position in the world frame.
        - *target_rot (3 elements):* The target rotation in the world frame.

        The order of elements in the observation space related to the environment is as follows -

        | Num | Observation                        | Min  | Max | Type (Unit)              |
        | --- | -----------------------------------| ---- | --- | ------------------------ |
        | 0   | x-coordinate of gripper position   | -Inf | Inf | position (m)             |
        | 1   | y-coordinate of gripper position   | -Inf | Inf | position (m)             |
        | 2   | z-coordinate of gripper position   | -Inf | Inf | position (m)             |
        | 3   | x-coordinate of object position    | -Inf | Inf | position (m)             |
        | 4   | y-coordinate of object position    | -Inf | Inf | position (m)             |
        | 5   | z-coordinate of object position    | -Inf | Inf | position (m)             |
        | 6   | x rel pos of object in gripper     | -Inf | Inf | position (m)             |
        | 7   | y rel pos of object in gripper     | -Inf | Inf | position (m)             |
        | 8   | z rel pos of object in gripper     | -Inf | Inf | position (m)             |
        | 9   | x rel vel of object in gripper     | -Inf | Inf | linear velocity (m/s)    |
        | 10  | y rel vel of object in gripper     | -Inf | Inf | linear velocity (m/s)    |
        | 11  | z rel vel of object in gripper     | -Inf | Inf | linear velocity (m/s)    |
        | 12  | roll of object                     | -Inf | Inf | rotation (rad)           |
        | 13  | pitch of object                    | -Inf | Inf | rotation (rad)           |
        | 14  | yaw of object                      | -Inf | Inf | rotation (rad)           |
        | 15  | x velocity of object               | -Inf | Inf | linear velocity (m/s)    |
        | 16  | y velocity of object               | -Inf | Inf | linear velocity (m/s)    |
        | 17  | z velocity of object               | -Inf | Inf | linear velocity (m/s)    |
        | 18  | x angular velocity of object       | -Inf | Inf | angular velocity (rad/s) |
        | 19  | y angular velocity of object       | -Inf | Inf | angular velocity (rad/s) |
        | 20  | z angular velocity of object       | -Inf | Inf | angular velocity (rad/s) |
        | 21  | x-coordinate of target             | -Inf | Inf | position (m)             |
        | 22  | y-coordinate of target             | -Inf | Inf | position (m)             |
        | 23  | z-coordinate of target             | -Inf | Inf | position (m)             |
        | 24  | roll of target                     | -Inf | Inf | rotation (rad)           |
        | 25  | pitch of target                    | -Inf | Inf | rotation (rad)           |
        | 26  | yaw of target                      | -Inf | Inf | rotation (rad)           |

        ## Rewards

        The environment supports two reward types that can be specified during initialization:

        ### Dense Reward (default)
        The dense reward components include:

        - `reach`: Encourages the gripper to move closer to the object by assigning higher reward as the distance between the gripper and object decreases.
        - `grasp`: Rewards successful grasping of the object with a binary reward.
        - `lift`: Encourages the gripper to lift the object by assigning higher reward as the distance between the gripper and object decreases.
        - `place`: Rewards successful placement of the object at the target location with a binary reward.
        - `timestep`: Penalizes the agent for taking more timesteps to complete the task.

        ### Sparse Reward
        When `reward_type="sparse"` is specified during initialization, the reward becomes:
            - `1.0` if the object is successfully placed at the target location
            - `0.0` otherwise

        `info` contains the success parameter if the given episode succeeded.

        ## Episode End
        ### Termination

        The current episode should terminate based on termination criteria defined as follow:
            1. If the distance between object and target is less than threshold (0.05)

        ### Truncation
        The default duration of an episode is 500 timesteps.

        ## Arguments
        The environment accepts the following parameters during initialization:

        - `reward_type` (str, optional): Specifies the reward type. Options are:
            - `"dense"` (default): Provides continuous reward based on distances
            - `"sparse"`: Provides binary reward (1.0 for success, 0.0 otherwise)

        Env provides the parameter to modify the start state of the robot upon reset.
        It can be applied during `gymnasium.make` by changing deterministic_reset (bool).
    ."""

    env_name: str = "pick_place/v1"
    scene_name: str = "v0/pick_place_scene"
    single_robot = True

    default_camera_config = {
        "trackbodyid": -1,
        "lookat": [0.0, 0.0, 0.5],
        "distance": 2.5,
        "elevation": -55,
        "azimuth": 180,
    }

    reward_config = {
        "reach": 0.1,
        "grasp": 0.35,
        "lift": 0.3,
        "place": 10.0,
        "success": 50.0,
        "timestep": -0.2,
        "penalty": 5.0,
    }

    def __init__(self, *args, **kwargs):
        self.reward_type = kwargs.get("reward_type", "dense")

        robot_config = kwargs.get("robot_config", {})
        self.robot_name = list(robot_config.keys())[0]
        self.size = robot_config.get(self.robot_name, {}).get("size", 1.0)

        if self.reward_type == "sparse":
            self.reward_config = {"success_bonus": 1.0}

        super().__init__(*args, **kwargs)

    def _setup_references(self):
        super()._setup_references()

        self.ee_site_name = self.robots[0]._arms["left_arm"].gripper.site_name
        self.ee_site_id = self.sim.model.site_name2id(self.ee_site_name)
        self.gripper = self.robots[0]._arms["left_arm"].gripper
        self.object_geoms = [
            f"object{i}_geom" for i in range(5)
        ]  # Match env.xml geom names

    def _reset_internal(self):
        """
        Reset the environment to an initial state.
        """

        super()._reset_internal()

        self.object_base_names = ["cube", "cylinder", "sphere", "capsule", "rectangle"]

        self.object_names = [
            "cube_obj",
            "cylinder_obj",
            "sphere_obj",
            "capsule_obj",
            "rectangle_obj",
        ]
        self.target_names = [
            "cube_target",
            "cylinder_target",
            "sphere_target",
            "capsule_target",
            "rectangle_target",
        ]
        self.lift_success = False

        self._sample_object()
        self._sample_target()

        # Initialize prev_obj_z to the current z height of each object
        self.prev_obj_z = {}
        for obj_name in self.object_names:
            body_id = self.sim.model.body_name2id(obj_name)
            self.prev_obj_z[obj_name] = self.sim.data.xpos[body_id][2]

    def _render_callback(self):
        """Update the visualization of the target site."""
        self.sim.forward()

    def _get_env_obs(self):
        gripper_pos = self.sim.data.site_xpos[self.ee_site_id]
        gripper_vel = self.sim.data.cvel[self.ee_site_id][:3]
        obs = [gripper_pos, gripper_vel]

        for obj_name, tgt_name in zip(self.object_names, self.target_names):
            body_id = self.sim.model.body_name2id(obj_name)
            obj_pos = self.sim.data.xpos[body_id]
            obj_rot = mat2euler(self.sim.data.xmat[body_id].reshape(3, 3))
            obj_velp = self.sim.data.cvel[body_id][:3]
            obj_velr = self.sim.data.cvel[body_id][3:]

            # Relative position and velocity (object - gripper)
            rel_pos = obj_pos - gripper_pos
            rel_vel = obj_velp - gripper_vel

            # If this object's target is active, include its pose; else np.nan
            if tgt_name in self.target_site_pose:
                tgt_pos = self.target_site_pose[tgt_name]
            else:
                tgt_pos = obj_pos  # Use np.nan for inactive targets

            obs.extend(
                [
                    obj_pos,  # 3
                    rel_pos,  # 3 (relative position)
                    rel_vel,  # 3 (relative velocity)
                    obj_rot,  # 3
                    obj_velp,  # 3
                    obj_velr,  # 3
                    tgt_pos,  # 3
                ]
            )

        obs_vec = np.concatenate(obs).astype(np.float32)
        return obs_vec

    def _get_info(self):
        """
        Return info dict with per-target success, lists of active/inactive target sites,
        and incorrect bin placement info.
        """
        success_dict, incorrect_dict = self._check_bin_contacts()

        info = {
            "success": success_dict,
            "active_target_sites": list(self.active_target_sites),
            "inactive_target_sites": list(self.inactive_targets),
            "incorrect_bin": incorrect_dict,
            "check_grasp": self._check_grasp(self.gripper, self.object_geoms),
            "lift_success": self.lift_success,
        }
        return info

    def _is_success(self):
        """
        Returns a list: 1.0 if the correct object is in contact with its active target site, 0.0 otherwise.
        """
        success_dict, _ = self._check_bin_contacts()
        return success_dict

    def compute_terminated(self):
        """
        Terminate for all objects placed successfully
        """

        success_dict = self._is_success()
        success = all(success_dict.values())
        if success:
            return True

        return False

    def compute_reward(self):
        """
        Computes and returns individual reward components for the current simulation state.

        - If `reward_type` is `"sparse"`, returns a dictionary with a single key `"success_bonus"`, which is 1.0 for each object successfully placed in its correct bin, and 0.0 otherwise.
        - If `reward_type` is `"dense"`, returns a dictionary with keys:
            - `"grasp_reward"`: 1.0 if the gripper is grasping an object, else 0.0.
            - `"place_reward"`: 1.0 if any object is placed in its correct bin, else 0.0.
            - `"success_bonus"`: 1.0 if all objects are placed in their correct bins, else 0.0.
            - `"reach_reward"`: A continuous reward based on the distance between the gripper and the nearest object.
            - `"lift_reward"`: 1.0 if the object is lifted above a certain height, else 0.0.
            - `"penalty"`: -1.0 if any object is placed in an incorrect bin, else 0.0.


        Returns
        -------
        raw_reward : dict
            A dictionary mapping each reward term name (str) to its corresponding scalar value (float).
            These are raw values and not yet combined into a scalar total reward.
        """
        if self.reward_type == "sparse":
            return self._compute_sparse_reward()
        else:
            return self._compute_dense_reward()

    def _compute_sparse_reward(self):
        """
        Compute sparse reward.
        """
        num_success = sum(self._is_success())
        return {"success": 1.0 * num_success}

    def _compute_dense_reward(self):
        """
        Compute dense reward.
        """
        reward_dict = {}
        reach_object_dict = {}

        # Reach reward
        gripper_pos = self.sim.data.site_xpos[self.ee_site_id]
        for obj_name in self.object_names:
            body_id = self.sim.model.body_name2id(obj_name)
            obj_pos = self.sim.data.xpos[body_id]
            dist = np.linalg.norm(gripper_pos - obj_pos)
            reach_object_dict[obj_name] = dist
        # Get the minimum distance to any object
        min_dist = min(reach_object_dict.values())
        reward_dict["reach"] = max(0.0, 1.0 - min_dist)

        # Grasp reward
        grasp_success = self._check_grasp(self.gripper, self.object_geoms)
        reward_dict["grasp"] = 1.0 if grasp_success else 0.0

        # Lift reward
        lifted = False
        lift_threshold = 0.03  # Minimum z increase to count as a lift (tune as needed)
        for obj_name in self.object_names:
            body_id = self.sim.model.body_name2id(obj_name)
            current_z = self.sim.data.xpos[body_id][2]
            prev_z = self.prev_obj_z[obj_name]
            if current_z - prev_z > lift_threshold:
                lifted = True

        self.lift_success = lifted
        reward_dict["lift"] = 1.0 if lifted else 0.0

        # Place reward:
        success_dict = self._is_success()
        reward_dict["place"] = sum(success_dict.values())

        # Penalty for incorrect placement
        _, incorrect_dict = self._check_bin_contacts()
        incorrect_placement = sum(incorrect_dict.values())
        reward_dict["penalty"] = -1.0 * incorrect_placement
        # Success bonus
        reward_dict["success"] = 1.0 if all(success_dict.values()) else 0.0
        return reward_dict

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

    def _check_bin_contacts(self):
        """
        Check if each object body is in contact with its correct or incorrect bins
        using MuJoCo's internal contact data (not touch sensors).

        Returns:
            success_dict: {object_name: 1.0 if object is in its correct active bin, else 0.0}
            incorrect_dict: {object_name: 1.0 if placed in any incorrect or forbidden bin, 0.0 otherwise}
        """
        success_dict = {}
        incorrect = {}

        model = self.sim.model
        data = self.sim.data

        # --- Build body-to-geom mapping ---
        body_to_geoms = {}
        for geom_id, body_id in enumerate(model.geom_bodyid):
            body_name = model.body_id2name(body_id)
            if body_name is not None:
                body_to_geoms.setdefault(body_name, []).append(geom_id)

        # --- Build geom ID lists for each object and each target body ---
        object_geom_ids = {obj: body_to_geoms.get(obj, []) for obj in self.object_names}
        target_geom_ids = {tgt: body_to_geoms.get(tgt, []) for tgt in self.target_names}

        # --- Build contact pair map ---
        ncon = data.ncon
        contact_pairs = {}
        for i in range(ncon):
            c = data.contact[i]
            g1, g2 = c.geom1, c.geom2
            contact_pairs.setdefault(g1, set()).add(g2)
            contact_pairs.setdefault(g2, set()).add(g1)

        # --- Evaluate contacts for each object ---
        for obj_idx, obj_name in enumerate(self.object_names):
            correct_target = self.target_names[obj_idx]
            obj_geom_ids = object_geom_ids.get(obj_name, [])
            correct_target_ids = target_geom_ids.get(correct_target, [])

            # --- Contact with correct bin ---
            in_correct_bin = any(
                (
                    gid in contact_pairs
                    and any(tid in contact_pairs[gid] for tid in correct_target_ids)
                )
                for gid in obj_geom_ids
            )

            # --- Contact with wrong/other bins ---
            placed_in_wrong_bin = False
            for tgt_name in self.active_target_sites:
                if tgt_name == correct_target:
                    continue
                tgt_geom_ids = target_geom_ids.get(tgt_name, [])
                if any(
                    (
                        gid in contact_pairs
                        and any(tid in contact_pairs[gid] for tid in tgt_geom_ids)
                    )
                    for gid in obj_geom_ids
                ):
                    placed_in_wrong_bin = True
                    break

            if correct_target in self.active_target_sites:
                success_dict[obj_name] = float(in_correct_bin)
            incorrect[obj_name] = float(placed_in_wrong_bin)
        return success_dict, incorrect

    def _sample_target(self):
        """
        Randomly select 4 out of 5 target types, assign them to random positions, and store their pose.
        The mapping from object to target is always fixed by name.
        """
        # Randomly pick 4 out of 5 targets
        target_indices = list(range(len(self.target_names)))
        random.shuffle(target_indices)
        self.active_target_sites = [
            self.target_names[i] for i in target_indices[: self.num_targets]
        ]
        self.inactive_targets = [
            self.target_names[i] for i in target_indices[self.num_targets :]
        ]

        # Shuffle positions for the active targets
        partitions = [
            {"x": 0.015 * self.size, "y": 0.41 * self.size, "z": 0.85 * self.size},
            {"x": 0.195 * self.size, "y": 0.41 * self.size, "z": 0.85 * self.size},
            {"x": 0.015 * self.size, "y": 0.18 * self.size, "z": 0.85 * self.size},
            {"x": 0.195 * self.size, "y": 0.18 * self.size, "z": 0.85 * self.size},
        ]
        random.shuffle(partitions)

        self.target_site_pose = {}
        for i, name in enumerate(self.active_target_sites):
            joint_name = f"{name}_joint"
            joint_id = self.sim.model.joint_name2id(joint_name)
            qpos_addr = self.sim.model.jnt_qposadr[joint_id]
            geom_name = f"{name}_geom"
            geom_id = self.sim.model.geom_name2id(geom_name)

            pos = partitions[i]
            self.sim.data.qpos[qpos_addr : qpos_addr + 3] = [
                pos["x"],
                pos["y"],
                pos["z"],
            ]
            self.target_site_pose[name] = np.array([pos["x"], pos["y"], pos["z"]])

        # Set inactive targets to transparent
        for name in self.inactive_targets:
            joint_name = f"{name}_joint"
            joint_id = self.sim.model.joint_name2id(joint_name)
            qpos_addr = self.sim.model.jnt_qposadr[joint_id]
            self.sim.data.qpos[qpos_addr : qpos_addr + 3] = [10.0, 10.0, 10.0]

        self.sim.forward()

    def _sample_object(self):
        """
        Randomly modify the properties of preset objects and place active objects in a box.
        """
        # --- Scaled spawn region
        box_x_min, box_x_max = -0.05 * self.size, 0.25 * self.size
        box_y_min, box_y_max = -0.45 * self.size, -0.05 * self.size
        box_z = 0.87 * self.size

        active_positions = []
        for i, obj_name in enumerate(self.object_names):
            body_id = self.sim.model.body_name2id(obj_name)
            geom_name = f"object{i}_geom"  # Match env.xml geom names
            geom_id = self.sim.model.geom_name2id(geom_name)
            joint_id = self.sim.model.body_jntadr[body_id]
            qpos_addr = self.sim.model.jnt_qposadr[joint_id]

            # Activate all objects: Set color and enable collision

            # Sample position without overlap
            while True:
                x = self.np_random.uniform(box_x_min, box_x_max)
                y = self.np_random.uniform(box_y_min, box_y_max)
                z = box_z
                pos = np.array([x, y, z])

                # Check for overlap with previously active objects
                overlap = False
                for prev_pos in active_positions:
                    if (
                        np.linalg.norm(pos - prev_pos) < 0.15 * self.size
                    ):  # Minimum distance
                        overlap = True
                        break
                if not overlap:
                    break

            active_positions.append(pos)

            # Assign the position (set qpos for free joint)
            self.sim.data.qpos[qpos_addr : qpos_addr + 3] = pos  # Position

        # Update simulation state after setting qpos
        self.sim.forward()

    def _load_scene_mjcf(self) -> mujoco.MjSpec:
        """
        Load and prepare the MuJoCo environment model.

        Calls the parent loader and then rescales meshes and field elements
        according to the current robot size.
        """
        super()._load_scene_mjcf()
        self._rescale_geoms(self.size)
        self._rescale_bodies(self.size)
        self._rescale_camera(self.size)

    def _load_env_mjcf(self):
        super()._load_env_mjcf()
        self.num_objects = 5  # Fixed number of objects
        self.num_targets = 4

        if self.env_mjcf is not None:
            size = self.size

            # Scale env bodies
            for body in self.env_mjcf.bodies:
                body.pos = [size * p for p in body.pos]

            # Scale env geoms
            for geom in self.env_mjcf.geoms:
                geom.size = [size * s for s in geom.size]
                geom.pos = [size * p for p in geom.pos]

    def _rescale_bodies(self, size: float):
        for i in range(len(self.scene_mjcf.bodies)):
            # Change the mesh size
            pos = self.scene_mjcf.bodies[i].pos
            pos = [size * scl for scl in pos]
            self.scene_mjcf.bodies[i].pos = pos

    def _rescale_geoms(self, size: float):
        """
        Rescale the robot meshes based on the given size factor.

        Parameters:
            size (float): Scaling factor to apply to mesh dimensions.
        """
        for i in range(1, len(self.scene_mjcf.geoms)):
            # Change the mesh size
            scale = self.scene_mjcf.geoms[i].size
            scale = [size * scl for scl in scale]
            self.scene_mjcf.geoms[i].size = scale

            pos = self.scene_mjcf.geoms[i].pos
            pos = [size * scl for scl in pos]
            self.scene_mjcf.geoms[i].pos = pos

    def _rescale_camera(self, size: float):
        """
        Scales the default camera configuration based on the environment size.
        """
        if (
            hasattr(self, "default_camera_config")
            and self.default_camera_config is not None
        ):
            cam = self.default_camera_config.copy()

            # Scale lookat vector and distance
            if "lookat" in cam:
                cam["lookat"] = [size * v for v in cam["lookat"]]
            if "distance" in cam:
                cam["distance"] = size * cam["distance"]

            self.default_camera_config = cam
