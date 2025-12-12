import mujoco
import numpy as np

from sai_mujoco.envs.football.v0 import FootballEnv_v0
import sai_mujoco.utils.v0.rotations as R


class KickToTarget_v0(FootballEnv_v0):
    env_name: str = "football/v0"
    scene_name: str = "v0/base_scene"
    default_camera_config = {
        "distance": 7.8,
        "azimuth": 90,
        "elevation": -90.0,
        "lookat": np.array([0.0, 0.0, 0.35]),
    }

    reward_config = {"offside": -10.0, "success": 20.0, "distance": 5.0}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_target = kwargs.get("move_target", False)

    def _setup_references(self):
        super()._setup_references()       
        self.target_name = "target0"

    def _get_env_obs(self):

        return np.concatenate([
            self.complete_space["ball_xpos_rel_robot"],
            self.complete_space["ball_velp_rel_robot"],
            self.complete_space["ball_velr_rel_robot"],
            self.complete_space["target_xpos_rel_robot"],
            self.complete_space["target_velp_rel_robot"]
        ],dtype=np.float32)

    def compute_reward(self):
        ball_xpos = self.sim.data.get_site_xpos("ball")
        outside_field = self.is_outside_field(ball_xpos, False)
        distance_reward, inside_target = self._is_success(ball_xpos, self.goal_pos)

        raw_reward = {
            "offside": outside_field,
            "success": inside_target,
            "distance": distance_reward,
        }

        return raw_reward

    def compute_terminated(self):
        terminated = super().compute_terminated()

        ball_xpos = self.sim.data.get_site_xpos("ball")
        outside_field = self.is_outside_field(ball_xpos, False)
        _, inside_target = self._is_success(ball_xpos, self.goal_pos)

        return bool(terminated or outside_field or inside_target)

    def _is_success(self, ball_xpos, target_xpos, distance_threshold=0.4):
        """Check if the achieved goal is close enough to the desired goal.

        Args:
            achieved_goal (np.ndarray): The achieved goal position
            desired_goal (np.ndarray): The desired goal position

        Returns:
            float: 1.0 if successful, 0.0 otherwise
        """

        distance = np.linalg.norm(ball_xpos - target_xpos, axis=-1)
        return np.exp(-distance), bool(distance < distance_threshold)

    def _reset_internal(self):
        """
        Reset the environment to an initial state.
        """
        super()._reset_internal()
        self._set_camera()
        self._sample_robot()
        self.goal_pos = self._sample_target()

    def _sample_robot(self):
        robot_qpos = self.sim.data.get_joint_qpos(f"{self.robots[0].name_prefix}root")
        ball_qpos = self.sim.data.get_joint_qpos("env:ball")
        robot_pose, robot_z = self.sample_robot_pose()
        ball_pose = self.sample_ball_position(robot_pose, robot_z)
        ball_qpos[:2] = ball_pose
        robot_quat = R.euler2quat([0.0, 0.0, robot_z])

        robot_qpos[:2] = robot_pose
        robot_qpos[3:] = robot_quat
        self.sim.data.set_joint_qpos(f"{self.robots[0].name_prefix}root", robot_qpos)
        self.sim.data.set_joint_qpos("env:ball", ball_qpos)
        self.sim.forward()

    def sample_robot_pose(self, offset=0.5):
        x = self.np_random.uniform(
            -self.parameters_dict["env_parameters"]["field"]["length"] + offset,
            self.parameters_dict["env_parameters"]["field"]["length"] - offset,
        )
        y = self.np_random.uniform(
            -self.parameters_dict["env_parameters"]["field"]["width"] + offset,
            self.parameters_dict["env_parameters"]["field"]["width"] - offset,
        )

        dx = -x
        dy = -y
        theta = np.arctan2(dy, dx)
        return np.array([x, y]), theta

    def sample_ball_position(
        self, robot_xy, angle, min_dist=0.5, max_dist=2.0, bord_offset=0.5
    ):
        while True:  # Try up to 100 times to sample a valid point
            dist = self.np_random.uniform(min_dist, max_dist)
            offset = np.array([dist * np.cos(angle), dist * np.sin(angle)])
            ball_xy = robot_xy + offset
            if (
                -self.parameters_dict["env_parameters"]["field"]["length"] + bord_offset
                <= ball_xy[0]
                <= self.parameters_dict["env_parameters"]["field"]["length"]
                - bord_offset
                and -self.parameters_dict["env_parameters"]["field"]["width"]
                + bord_offset
                <= ball_xy[1]
                <= self.parameters_dict["env_parameters"]["field"]["width"]
                - bord_offset
            ):
                return ball_xy

    def _sample_target(self, min_offset=2.0, max_offset=3.5, offset=0.5):
        robot_qpos = self.sim.data.get_joint_qpos(f"{self.robots[0].name_prefix}root")
        goal_pos = self.sim.data.get_site_xpos("target0")

        while True:
            y_offset = self.np_random.uniform(min_offset, max_offset)
            if self.np_random.uniform() > 0.5:
                y_offset = -y_offset  # Flip direction randomly
            goal_pos[1] = robot_qpos[1] + y_offset
            goal_pos[0] = self.np_random.uniform(
                -self.parameters_dict["env_parameters"]["field"]["length"] + offset,
                self.parameters_dict["env_parameters"]["field"]["length"] - offset,
            )
            if (
                -self.parameters_dict["env_parameters"]["field"]["width"] + offset
                <= goal_pos[1]
                <= self.parameters_dict["env_parameters"]["field"]["width"] - offset
            ):
                return goal_pos.copy()
            
    def _set_camera(self, 
                    margin = 1.15):

        ball_qpos = self.sim.data.get_joint_qpos("env:ball")[:3]
        robot_pos = self.sim.data.get_joint_qpos(f"{self.robots[0].name_prefix}root")[:3]
        goal_pos = self.sim.data.get_site_xpos("target0")

        if np.linalg.norm((ball_qpos - robot_pos)[:2]) > np.linalg.norm((ball_qpos - goal_pos)[:2]):
            entity_pos = robot_pos
        else:
            entity_pos = ball_qpos

        center = 0.6 * entity_pos + 0.4 * goal_pos

        # Distance: use vertical FOV to fit the horizontal span conservatively
        # Treat the XY distance as the "span" to keep within view.
        span_xy = float(np.linalg.norm((entity_pos - goal_pos)[:2]))
        z_min, z_max = float(min(entity_pos[2], goal_pos[2])), float(max(entity_pos[2], goal_pos[2]))
        span_z = z_max - z_min

        # Choose distance using vertical FOV so both spans fit with margin
        fovy = 45.0
        d_h = (0.5 * span_xy) / np.tan(np.radians(0.5 * fovy)) if span_xy > 1e-6 else 0.6
        d_v = (0.5 * span_z)  / np.tan(np.radians(0.5 * fovy)) if span_z > 1e-6 else 0.6
        dist = float(np.clip(margin * max(d_h, d_v), 8.0, 15))

        # Apply camera
        if self.mujoco_renderer.viewer is None:
            self.default_camera_config = {
                "distance": dist,
                "azimuth": 90,
                "elevation": -90.0,
                "lookat": center,
            }
            if hasattr(self.mujoco_renderer, "default_cam_config"):
                self.mujoco_renderer.default_cam_config.update(self.default_camera_config)
            elif hasattr(self.mujoco_renderer, "camera_config"):
                self.mujoco_renderer.camera_config.update(self.default_camera_config)                

        if self.mujoco_renderer.viewer is not None:
            self.mujoco_renderer.viewer.cam.lookat[:] = center
            self.mujoco_renderer.viewer.cam.azimuth = 90
            self.mujoco_renderer.viewer.cam.elevation = -90
            self.mujoco_renderer.viewer.cam.distance = dist

    def _render_callback(self):
        """Update the visualization of the target site."""
        sites_offset = (self.sim.data.site_xpos - self.sim.model._model.site_pos).copy()
        site_id = mujoco.mj_name2id(
            self.sim.model._model, mujoco.mjtObj.mjOBJ_SITE, "target0"
        )
        self.sim.model._model.site_pos[site_id] = self.goal_pos - sites_offset[site_id]
        self.sim.forward()
        self._set_camera()

    def _load_env_mjcf(self) -> mujoco.MjSpec:
        super()._load_env_mjcf()
        self._add_target()

    def _add_target(self):
        red_body = self.env_mjcf.worldbody.add_body(
            name="target0",
            pos=[0, 0, 0.0],  # adjust z to place it above the ground
        )

        red_body.add_site(
            type=mujoco.mjtGeom.mjGEOM_CYLINDER,
            name="target0",
            pos=[0, 0, 0.001],  # optional, can center it
            size=[self.parameters_dict["kick_to_target"]["target_size"], 0.01, 0.0],
            rgba=[1, 0, 0, 0.4],
        )

    def _get_info(self):
        """Get additional information about the environment state.

        Returns:
            dict: Additional information dictionary
        """

        robot_info = super()._get_info()
        robot_info.update({"success": self._is_success(self.sim.data.get_site_xpos("ball"), self.goal_pos)[1]})
        return robot_info

class DefenderKickToTarget_v0(KickToTarget_v0):
    env_name: str = "football/v0"
    scene_name: str = "v0/base_scene"
    default_camera_config = {
        "distance": 7.8,
        "azimuth": -160,
        "elevation": -20.0,
        "lookat": np.array([0.0, 0.0, 0.35]),
    }

    reward_config = {
        "test": -10.0,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_target = kwargs.get("move_target", False)

    def compute_reward(self):
        raw_reward = {
            "test": np.float64(0),
        }

        return raw_reward

    def compute_terminated(self):
        return False

    def _reset_internal(self):
        """
        Reset the environment to an initial state.
        """
        super()._reset_internal()
        self._sample_robot()
        self.goal_pos = self._sample_n_targets(20)

    def _sample_n_targets(
        self, n, min_offset=2.0, max_offset=3.5, offset=0.5, min_dist=0.9
    ):
        robot_qpos = self.sim.data.get_joint_qpos(f"{self.robots[0].name_prefix}root")
        field_length = self.parameters_dict["env_parameters"]["field"]["length"]
        field_width = self.parameters_dict["env_parameters"]["field"]["width"]

        targets = []

        def is_far_enough(new_pos, existing):
            for e in existing:
                if np.linalg.norm(new_pos[:2] - e[:2]) < min_dist:
                    return False
            return True

        while len(targets) < n:
            y_offset = self.np_random.uniform(min_offset, max_offset)
            if self.np_random.uniform() > 0.5:
                y_offset = -y_offset
            new_y = self.np_random.uniform(-field_width + offset, field_width - offset)
            new_x = self.np_random.uniform(
                -field_length + offset, field_length - offset
            )

            if -field_width + offset <= new_y <= field_width - offset:
                candidate = np.array([new_x, new_y, 0.01])
                if is_far_enough(candidate, targets):
                    targets.append(candidate)

        return targets

    def _render_callback(self):
        """Update the visualization of the target site."""

        for i in range(10):
            sites_offset = (
                self.sim.data.site_xpos - self.sim.model._model.site_pos
            ).copy()
            site_id = mujoco.mj_name2id(
                self.sim.model._model, mujoco.mjtObj.mjOBJ_SITE, f"target{i}"
            )
            self.sim.model._model.site_pos[site_id] = (
                self.goal_pos[i] - sites_offset[site_id]
            )

        for i in range(10, 20):
            sites_offset = (
                self.sim.data.site_xpos - self.sim.model._model.site_pos
            ).copy()
            body_id = self.sim.model.body_name2id(f"goalkeeper_body{i - 10}")
            # site_id = mujoco.mj_name2id(
            #     self.sim.model._model, mujoco.mjtObj.mjOBJ_SITE, f"goalkeeper_site{i-10}"
            # )
            pose = self.goal_pos[i]
            pose[-1] = 0.5
            self.sim.model.body_pos[body_id] = self.goal_pos[i] - sites_offset[site_id]
            # self.sim.model._model.site_pos[site_id] = self.goal_pos[i] - sites_offset[site_id]
        self.sim.forward()

    def _add_target(self):
        for i in range(10):
            red_body = self.env_mjcf.worldbody.add_body(
                name=f"target{i}",
                pos=[0, 0, 0.0],  # adjust z to place it above the ground
            )

            red_body.add_site(
                type=mujoco.mjtGeom.mjGEOM_CYLINDER,
                name=f"target{i}",
                pos=[0, 0, 0.001],  # optional, can center it
                size=[self.parameters_dict["kick_to_target"]["target_size"], 0.01, 0.0],
                rgba=[1, 0, 0, 0.4],
            )

        for i in range(10):
            goalkeeper_body = self.env_mjcf.worldbody.add_body(
                name=f"goalkeeper_body{i}",
                pos=[0, 0, 0.3],  # adjust z to place it above the ground
            )
            goalkeeper_body.add_geom(
                name=f"goalkeeper_geom{i}",
                type=mujoco.mjtGeom.mjGEOM_MESH,
                meshname="defender",
                pos=[0, 0, 0.3],  # half height to sit above the joint
                quat=[0.5, 0.5, 0.5, 0.5],
                rgba=[1, 1, 0, 1],
                mass=1.0,
            )

            goalkeeper_body.add_site(
                name=f"goalkeeper_site{i}",
                pos=[0, 0, 0.001],  # optional, can center it
            )

    def _get_info(self):
        """Get additional information about the environment state.

        Returns:
            dict: Additional information dictionary
        """
        return {}