"""
Generic holonomic controller for triangular omni-directional mobile bases.

Reference: https://github.com/isaac-sim/IsaacSim/blob/main/source/extensions/isaacsim.robot.wheeled_robots/python/controllers/holonomic_controller.py
"""

import numpy as np
from typing import Literal
from sai_mujoco.controllers.mobile_base.v0.mobile_base_controller import (
    MobileBaseController_v0,
)
import sai_mujoco.utils.v0.rotations as T


class SlewRateLimiter:
    def __init__(self, max_rate, dt):
        self.max_rate = float(max_rate)  # units per second
        self.dt = float(dt)
        self.y = None

    def reset(self, y0=np.zeros(3)):
        self.y = np.array(y0, dtype=np.float64)

    def __call__(self, x):
        x = np.asarray(x, dtype=np.float64)
        if self.y is None:
            self.y = x.copy()
            return self.y
        delta = x - self.y
        max_step = self.max_rate * self.dt
        step = np.clip(delta, -max_step, max_step)
        self.y = self.y + step
        return self.y


class FirstOrderLPF:
    def __init__(self, dt, tau):
        self.dt = float(dt)
        self.tau = float(max(tau, 1e-6))
        self.y = None

    def reset(self, y0=np.zeros(3)):
        self.y = np.array(y0, dtype=np.float64)

    def __call__(self, x):
        x = np.asarray(x, dtype=np.float64)
        if self.y is None:
            self.y = x.copy()
            return self.y
        alpha = np.exp(-self.dt / self.tau)  # 0<alpha<1
        self.y = alpha * self.y + (1 - alpha) * x
        return self.y


class HolonomicController_v0(MobileBaseController_v0):
    """
    Holonomic velocity controller for triangular omni-wheel mobile bases.

    Inherits position-to-velocity conversion from MobileBaseJointVelocityController_v0
    and adds holonomic inverse kinematics to map body velocities to wheel velocities.

    Holonomic Kinematics (following NVIDIA Isaac Sim convention):
        For each wheel i at angle α_i from the forward axis and distance L from center:

        ω_i = (1/r) * [sin(α_i)*v_x - cos(α_i)*v_y + L*ω_z]

        where:
        - ω_i: wheel angular velocity (rad/s)
        - r: wheel radius (m)
        - v_x, v_y: linear velocities in body frame (m/s)
        - ω_z: angular velocity around vertical axis (rad/s)
        - L: distance from base center to wheel contact (m)
        - α_i: wheel heading angle (rad)

    Args:
        sim: MuJoCo simulation instance
        joint_indexes: Dictionary with 'joints', 'qpos', 'qvel' indices for the 3 wheels
        actuator_range: (min, max) velocity range for wheel actuators (rad/s)
        wheel_radius: Wheel radius in meters (required)
        base_radius: Distance from center to wheel contact in meters (required)
        wheel_angles: List of 3 wheel heading angles in radians (required)
            Convention: angle from forward (+X) axis, counter-clockwise positive
        input_max: Maximum input value (default: 1.0)
        input_min: Minimum input value (default: -1.0)
        output_max: Maximum output scaling (default: 0.1)
        output_min: Minimum output scaling (default: -0.1)
        max_linear_speed: Maximum linear velocity in m/s (default: 0.5)
        max_angular_speed: Maximum angular velocity in rad/s (default: 1.0)
        vel_tau: Time constant for velocity filter (default: 0.12)
        vel_slew: Slew rate limit for velocity (default: 2.0)
        stop_tau: Time constant for stop (default: 0.25)
        **kwargs: Additional arguments passed to parent class
    """

    def __init__(
        self,
        sim,
        joint_indexes,
        actuator_range,
        wheel_radius: float,
        base_radius: float,
        wheel_angles: list,
        input_type: Literal["delta", "absolute"] = "delta",
        input_max: float = 0.5,
        input_min: float = -0.5,
        output_max: float = 0.5,
        output_min: float = -0.5,
        max_linear_speed: float = 0.3,
        max_angular_speed: float = 1.0,
        vel_tau=0.5,
        vel_slew=2.0,
        stop_tau=0.5,
        **kwargs,
    ):
        super().__init__(
            sim=sim,
            joint_indexes=joint_indexes,
            actuator_range=actuator_range,
            naming_prefix=kwargs.get("naming_prefix", None),
        )

        assert wheel_radius > 0, "wheel_radius must be positive"
        assert base_radius > 0, "base_radius must be positive"
        assert wheel_angles is not None and len(wheel_angles) == 3, (
            "wheel_angles must be a list of 3 angles (rad)"
        )
        self.input_type = input_type
        assert self.input_type in ["delta", "absolute"], (
            f"Input type must be delta or absolute, got: {self.input_type}"
        )
        self.control_dim = 3
        self.input_max = self.nums2array(input_max, self.control_dim)
        self.input_min = self.nums2array(input_min, self.control_dim)
        self.output_max = self.nums2array(output_max, self.control_dim)
        self.output_min = self.nums2array(output_min, self.control_dim)

        self.control_dt = 0.08
        self.vel_filter = FirstOrderLPF(dt=self.control_dt, tau=vel_tau)
        self.vel_slew = SlewRateLimiter(max_rate=vel_slew, dt=self.control_dt)
        self.stop_tau = float(stop_tau)
        self._was_zero = True
        self.vel_filter.reset(np.zeros(3))
        self.vel_slew.reset(np.zeros(3))

        self.wheel_radius = float(wheel_radius)
        self.base_radius = float(base_radius)
        self.wheel_angles = np.array(wheel_angles, dtype=np.float64)

        self.max_linear_speed = float(max_linear_speed)
        self.max_angular_speed = float(max_angular_speed)

        self.smoothed_velocities = np.zeros(3)

        self._compute_holonomic_matrix()

    def _compute_holonomic_matrix(self):
        """
        Compute the holonomic inverse kinematics matrix.

        Following NVIDIA Isaac Sim HolonomicController convention:
        Maps [v_x, v_y, omega_z] -> [w_0, w_1, w_2]

        For each wheel i at angle α_i and distance L from center:
            w_i = (1/r) * [sin(α_i)*v_x - cos(α_i)*v_y + L*omega_z]

        Matrix form:
            [w_0]   [sin(α_0)  -cos(α_0)  L] [v_x    ]
            [w_1] = [sin(α_1)  -cos(α_1)  L] [v_y    ] * (1/r)
            [w_2]   [sin(α_2)  -cos(α_2)  L] [omega_z]
        """
        J = np.zeros((3, 3), dtype=np.float64)

        for i, alpha in enumerate(self.wheel_angles):
            J[i, 0] = np.sin(alpha)
            J[i, 1] = -np.cos(alpha)
            J[i, 2] = self.base_radius

        self.holonomic_matrix = J / self.wheel_radius

    def set_goal(self, action, set_qpos=None):
        if self.input_type == "delta":
            delta = action
        elif self.input_type == "absolute":
            base_pos, _ = self.get_base_pose()
            delta = action - base_pos
        else:
            raise ValueError(f"Unsupport input_type {self.input_type}")
        scaled_delta = self.scale_action(delta)
        curr_pos, curr_ori = self.get_base_pose()
        init_theta = T.mat2euler(self.init_ori)[2]
        curr_theta = T.mat2euler(curr_ori)[2]
        theta = curr_theta - init_theta
        x, y = scaled_delta[0:2]
        scaled_delta[0] = -x * np.cos(theta) + y * np.sin(theta)
        scaled_delta[1] = x * np.sin(theta) - y * np.cos(theta)
        self.goal_vel = scaled_delta / self.control_dt

    def run_controller(self):
        """
        Execute controller to compute wheel velocity commands.

        Returns:
            np.array: Wheel angular velocity commands [w_0, w_1, w_2] in rad/s
        """
        if self.goal_vel is None:
            self.set_goal(np.zeros(self.control_dim))
        self.update()

        desired_body_vel = np.array(self.goal_vel, dtype=np.float64)

        deadband_lin = 1e-3
        deadband_yaw = 1e-3
        if abs(desired_body_vel[0]) < deadband_lin:
            desired_body_vel[0] = 0.0
        if abs(desired_body_vel[1]) < deadband_lin:
            desired_body_vel[1] = 0.0
        if abs(desired_body_vel[2]) < deadband_yaw:
            desired_body_vel[2] = 0.0

        lin_norm = np.linalg.norm(desired_body_vel[:2])
        if lin_norm > self.max_linear_speed > 0.0:
            desired_body_vel[:2] *= self.max_linear_speed / lin_norm
        desired_body_vel[2] = np.clip(
            desired_body_vel[2], -self.max_angular_speed, self.max_angular_speed
        )

        if np.allclose(desired_body_vel, 0.0, atol=1e-9):
            alpha = np.exp(-self.control_dt / max(self.stop_tau, 1e-6))
            desired_body_vel = alpha * getattr(self, "smoothed_velocities", np.zeros(3))

        v_f = self.vel_filter(desired_body_vel)

        v_s = self.vel_slew(v_f)

        wheel_velocities = self.holonomic_matrix @ v_s

        max_mag = np.abs(wheel_velocities)
        for i in range(len(wheel_velocities)):
            if max_mag[i] > abs(self.actuator_max[i]):
                wheel_velocities[i] *= abs(self.actuator_max[i]) / max_mag[i]
        wheel_velocities = np.clip(
            wheel_velocities, self.actuator_min, self.actuator_max
        )

        self.vels = wheel_velocities

        return wheel_velocities

    def reset_goal(self):
        """
        Reset goal velocities to zero.
        """
        self.init_pos, self.init_ori = self.get_base_pose()
        self.goal_vel = np.zeros(self.control_dim)
        self.smoothed_velocities = np.zeros(3)

    @property
    def name(self):
        return "HOLONOMIC"
