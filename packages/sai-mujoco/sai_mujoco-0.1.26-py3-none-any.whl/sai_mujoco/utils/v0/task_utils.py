from copy import deepcopy

import mujoco

from sai_mujoco.utils.v0.xml_utils import MujocoObject, MujocoXML
from sai_mujoco.utils.v0.mjcf_utils import (
    get_ids,
    new_body,
    new_geom,
    new_element,
    recolor_collision_geoms,
    scale_mjcf_model,
    string_to_array,
    array_to_string,
    find_elements,
    get_elements,
    ENVIRONMENT_COLLISION_COLOR,
)
from typing import List, Union
import numpy as np


def get_subtree_geom_ids_by_group(
    model: mujoco.MjModel, body_id: int, group: int
) -> list[int]:
    """Get all geoms belonging to a subtree starting at a given body, filtered by group.

    Args:
        model: MuJoCo model.
        body_id: ID of body where subtree starts.
        group: Group ID to filter geoms.

    Returns:
        A list containing all subtree geom ids in the specified group.

    Adapted from https://github.com/kevinzakka/mink/blob/main/mink/utils.py
    """

    def gather_geoms(body_id: int) -> list[int]:
        geoms: list[int] = []
        geom_start = model.body_geomadr[body_id]
        geom_end = geom_start + model.body_geomnum[body_id]
        geoms.extend(
            geom_id
            for geom_id in range(geom_start, geom_end)
            if model.geom_group[geom_id] == group
        )
        children = [i for i in range(model.nbody) if model.body_parentid[i] == body_id]
        for child_id in children:
            geoms.extend(gather_geoms(child_id))
        return geoms

    return gather_geoms(body_id)


class Arena(MujocoXML):
    """Base arena class."""

    def __init__(self, fname):
        super().__init__(fname)
        # Get references to floor and bottom
        self.bottom_pos = np.zeros(3)
        self.floor = self.worldbody.find("./geom[@name='floor']")
        self.object_scales = {}

        # Add mocap bodies to self.root for mocap control in mjviewer UI for robot control
        mocap_body_1 = new_body(name="left_eef_target", pos="0 0 -1", mocap=True)
        mocap_body_1_geom = new_geom(
            name="left_eef_target_box",
            type="box",
            size="0.05 0.05 0.05",
            rgba="0.898 0.420 0.435 0.5",
            conaffinity="0",
            contype="0",
            group="2",
        )
        mocap_body_1_sphere = new_geom(
            name="left_eef_target_sphere",
            type="sphere",
            size="0.01",
            pos="0 0 0",
            rgba="0.898 0.420 0.435 0.8",
            conaffinity="0",
            contype="0",
            group="2",
        )
        mocap_body_2 = new_body(name="right_eef_target", pos="0 0 -1", mocap=True)
        mocap_body_2_geom = new_geom(
            name="right_eef_target_box",
            type="box",
            size="0.05 0.05 0.05",
            rgba="0.208 0.314 0.439 0.5",
            conaffinity="0",
            contype="0",
            group="2",
        )
        mocap_body_2_sphere = new_geom(
            name="right_eef_target_sphere",
            type="sphere",
            size="0.01",
            pos="0 0 0",
            rgba="0.208 0.314 0.439 0.8",
            conaffinity="0",
            contype="0",
            group="2",
        )
        # Append the box and sphere geometries to their respective mocap bodies
        mocap_body_1.append(mocap_body_1_geom)
        mocap_body_1.append(mocap_body_1_sphere)
        mocap_body_2.append(mocap_body_2_geom)
        mocap_body_2.append(mocap_body_2_sphere)
        # Add the mocap bodies to the world
        self.worldbody.append(mocap_body_1)
        self.worldbody.append(mocap_body_2)

        # Run any necessary post-processing on the model
        self._postprocess_arena()

        # Recolor all geoms
        recolor_collision_geoms(
            root=self.worldbody,
            rgba=ENVIRONMENT_COLLISION_COLOR,
            exclude=lambda e: True if e.get("name", None) == "floor" else False,
        )

        self._instances_to_ids = None
        self._geom_ids_to_instances = None
        self._site_ids_to_instances = None
        self._classes_to_ids = None
        self._geom_ids_to_classes = None
        self._site_ids_to_classes = None

    def set_origin(self, offset):
        """
        Applies a constant offset to all objects.

        Args:
            offset (3-tuple): (x,y,z) offset to apply to all nodes in this XML
        """
        offset = np.array(offset)
        for node in self.worldbody.findall("./*[@pos]"):
            cur_pos = string_to_array(node.get("pos"))
            new_pos = cur_pos + offset
            node.set("pos", array_to_string(new_pos))

    def set_camera(self, camera_name, pos, quat, camera_attribs=None):
        """
        Sets a camera with @camera_name. If the camera already exists, then this overwrites its pos and quat values.

        Args:
            camera_name (str): Camera name to search for / create
            pos (3-array): (x,y,z) coordinates of camera in world frame
            quat (4-array): (w,x,y,z) quaternion of camera in world frame
            camera_attribs (dict): If specified, should be additional keyword-mapped attributes for this camera.
                See http://www.mujoco.org/book/XMLreference.html#camera for exact attribute specifications.
        """
        # Determine if camera already exists
        camera = find_elements(
            root=self.worldbody,
            tags="camera",
            attribs={"name": camera_name},
            return_first=True,
        )

        # Compose attributes
        if camera_attribs is None:
            camera_attribs = {}
        camera_attribs["pos"] = array_to_string(pos)
        camera_attribs["quat"] = array_to_string(quat)

        if camera is None:
            # If camera doesn't exist, then add a new camera with the specified attributes
            self.worldbody.append(
                new_element(tag="camera", name=camera_name, **camera_attribs)
            )
        else:
            # Otherwise, we edit all specified attributes in that camera
            for attrib, value in camera_attribs.items():
                camera.set(attrib, value)

    def _postprocess_arena(self):
        """
        Runs any necessary post-processing on the imported Arena model
        """
        pass

    def set_scale(self, scale: Union[float, List[float]], obj_name: str):
        """
        Scales each geom, mesh, site, and body under obj_name.
        Called during initialization but can also be used externally

        Args:
            scale (float or list of floats): Scale factor (1 or 3 dims)
            obj_name Name of root object to apply.
        """
        obj = self.worldbody.find(f"./body[@name='{obj_name}']")
        if obj is None:
            bodies = self.worldbody.findall("./body")
            body_names = [
                body.get("name") for body in bodies if body.get("name") is not None
            ]
            raise ValueError(
                f"Object {obj_name} not found in arena; cannot set scale. Available objects: {body_names}"
            )
        self.object_scales[obj.get("name")] = scale

        # Use the centralized scaling utility function
        scale_mjcf_model(
            obj=obj,
            asset_root=self.asset,
            worldbody=self.worldbody,
            scale=scale,
            get_elements_func=get_elements,
            scale_slide_joints=False,  # Arena doesn't handle slide joints
        )

    def merge_objects(self, mujoco_objects):
        """
        Adds object models to the MJCF model.

        Args:
            mujoco_objects (list of MujocoObject): objects to merge into this MJCF model
        """
        for mujoco_obj in mujoco_objects:
            # Make sure we actually got a MujocoObject
            assert isinstance(mujoco_obj, MujocoObject), (
                "Tried to merge non-MujocoObject! Got type: {}".format(type(mujoco_obj))
            )
            # Merge this object
            self.merge_assets(mujoco_obj)
            self.worldbody.append(mujoco_obj.get_obj())

    def generate_id_mappings(self, sim):
        """
        Generates IDs mapping class instances to set of (visual) geom IDs corresponding to that class instance

        Args:
            sim (MjSim): Current active mujoco simulation object
        """
        self._instances_to_ids = {}
        self._geom_ids_to_instances = {}
        self._site_ids_to_instances = {}
        self._classes_to_ids = {}
        self._geom_ids_to_classes = {}
        self._site_ids_to_classes = {}

        if hasattr(self, "mujoco_objects"):
            models = [model for model in self.mujoco_objects]
        else:
            models = []

        worldbody = self.root.find("worldbody")
        exclude_bodies = [
            "table",
            "left_eef_target",
            "right_eef_target",
        ]  # targets used for viz / mjgui
        top_level_bodies = [
            body.attrib.get("name")
            for body in worldbody.findall("body")
            if body.attrib.get("name") not in exclude_bodies
        ]
        models.extend(top_level_bodies)

        # Parse all mujoco models from robots and objects
        for model in models:
            if isinstance(model, str):
                body_name = model
                visual_group_number = 1
                body_id = sim.model.body_name2id(body_name)
                inst, cls = body_name, body_name
                geom_ids = get_subtree_geom_ids_by_group(
                    sim.model, body_id, visual_group_number
                )
                id_groups = [geom_ids, []]
            else:
                # Grab model class name and visual IDs
                cls = str(type(model)).split("'")[1].split(".")[-1]
                inst = model.name
                id_groups = [
                    get_ids(
                        sim=sim,
                        elements=model.visual_geoms + model.contact_geoms,
                        element_type="geom",
                    ),
                    get_ids(sim=sim, elements=model.sites, element_type="site"),
                ]
            group_types = ("geom", "site")
            ids_to_instances = (
                self._geom_ids_to_instances,
                self._site_ids_to_instances,
            )
            ids_to_classes = (self._geom_ids_to_classes, self._site_ids_to_classes)

            # Add entry to mapping dicts

            # Instances should be unique
            assert inst not in self._instances_to_ids, (
                f"Instance {inst} already registered; should be unique"
            )
            self._instances_to_ids[inst] = {}

            # Classes may not be unique
            if cls not in self._classes_to_ids:
                self._classes_to_ids[cls] = {
                    group_type: [] for group_type in group_types
                }

            for ids, group_type, ids_to_inst, ids_to_cls in zip(
                id_groups, group_types, ids_to_instances, ids_to_classes
            ):
                # Add geom, site ids
                self._instances_to_ids[inst][group_type] = ids
                self._classes_to_ids[cls][group_type] += ids

                # Add reverse mappings as well
                for idn in ids:
                    assert idn not in ids_to_inst, (
                        f"ID {idn} already registered; should be unique"
                    )
                    ids_to_inst[idn] = inst
                    ids_to_cls[idn] = cls

    @property
    def geom_ids_to_instances(self):
        """
        Returns:
            dict: Mapping from geom IDs in sim to specific class instance names
        """
        return deepcopy(self._geom_ids_to_instances)

    @property
    def site_ids_to_instances(self):
        """
        Returns:
            dict: Mapping from site IDs in sim to specific class instance names
        """
        return deepcopy(self._site_ids_to_instances)

    @property
    def instances_to_ids(self):
        """
        Returns:
            dict: Mapping from specific class instance names to {geom, site} IDs in sim
        """
        return deepcopy(self._instances_to_ids)

    @property
    def geom_ids_to_classes(self):
        """
        Returns:
            dict: Mapping from geom IDs in sim to specific classes
        """
        return deepcopy(self._geom_ids_to_classes)

    @property
    def site_ids_to_classes(self):
        """
        Returns:
            dict: Mapping from site IDs in sim to specific classes
        """
        return deepcopy(self._site_ids_to_classes)

    @property
    def classes_to_ids(self):
        """
        Returns:
            dict: Mapping from specific classes to {geom, site} IDs in sim
        """
        return deepcopy(self._classes_to_ids)
