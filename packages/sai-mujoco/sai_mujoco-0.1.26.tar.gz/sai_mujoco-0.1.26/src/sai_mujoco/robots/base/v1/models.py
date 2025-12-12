from dataclasses import dataclass, field
import numpy as np


@dataclass
class Part_v1:
    _joint_names: list[str] = field(default_factory=list)
    controller_config: dict = None
    _actuator_names: list[str] = None
    _init_qpos: np.ndarray | dict[str, np.ndarray] = None
    _init_qvel: np.ndarray = None
    _important_bodies: dict[str, str] = field(default_factory=dict)
    _important_geoms: dict[str, str] = field(default_factory=dict)
    _important_sites: list[str] = field(default_factory=list)
    _site_name: str = None
    naming_prefix: str = ""

    def set_prefix(self, prefix: str):
        """Set the naming prefix for this part."""
        self.naming_prefix = prefix

    @property
    def joint_names(self) -> list[str]:
        """Get joint names with prefix if available."""
        if self.naming_prefix:
            return [f"{self.naming_prefix}{name}" for name in self._joint_names]
        return self._joint_names

    @property
    def actuator_names(self):
        """Get actuator names with prefix if available."""
        base_names = (
            self._actuator_names
            if self._actuator_names is not None
            else self._joint_names
        )
        if self.naming_prefix:
            return [f"{self.naming_prefix}{name}" for name in base_names]
        return base_names

    @property
    def dof(self):
        """
        Defines the number of DOF of the gripper

        Returns:
            int: gripper DOF
        """
        return len(self.actuator_names)

    @property
    def init_qpos(self):
        if self._init_qpos is None:
            return np.zeros(len(self._joint_names))

        if isinstance(self._init_qpos, dict):
            # Add prefix to keys if prefix is set
            if self.naming_prefix:
                return {
                    f"{self.naming_prefix}{key}": value
                    for key, value in self._init_qpos.items()
                }
            return self._init_qpos

        return self._init_qpos

    @property
    def init_qvel(self):
        if self._init_qvel is None:
            return np.zeros(len(self._joint_names))

        if isinstance(self._init_qvel, dict):
            # Add prefix to keys if prefix is set
            if self.naming_prefix:
                return {
                    f"{self.naming_prefix}{key}": value
                    for key, value in self._init_qvel.items()
                }
            return self._init_qvel

        return self._init_qvel

    @property
    def important_bodies(self):
        if self.naming_prefix:
            return {
                f"{key}": f"{self.naming_prefix}{value}"
                for key, value in self._important_bodies.items()
            }
        return self._important_bodies

    @property
    def important_geoms(self):
        if self.naming_prefix:
            imp_geoms = {}
            for key, value in self._important_geoms.items():
                if isinstance(value, list):
                    imp_geoms[key] = [f"{self.naming_prefix}{v}" for v in value]
                else:
                    imp_geoms[key] = [f"{self.naming_prefix}{value}"]
            return imp_geoms
        return self._important_geoms

    @property
    def important_sites(self):
        if self.naming_prefix:
            return [f"{self.naming_prefix}{site}" for site in self._important_sites]
        return self._important_sites

    @property
    def site_name(self):
        if self.naming_prefix:
            return f"{self.naming_prefix}{self._site_name}"
        return self._site_name


@dataclass
class GripperPart_v1(Part_v1):
    @property
    def speed(self):
        """
        How quickly the gripper opens / closes

        Returns:
            float: Speed of the gripper
        """
        return 0.3

    def format_action(self, action):
        return action


@dataclass
class ArmPart_v1(Part_v1):
    gripper: GripperPart_v1 = None
