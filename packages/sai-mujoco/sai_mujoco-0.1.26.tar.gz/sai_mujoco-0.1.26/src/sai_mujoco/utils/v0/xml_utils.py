import io
import os
import xml.dom.minidom
import xml.etree.ElementTree as ET
from copy import deepcopy

import numpy as np

from sai_mujoco.utils.v0.mjcf_utils import (
    get_size,
    _element_filter,
    add_prefix,
    find_elements,
    recolor_collision_geoms,
    sort_elements,
    string_to_array,
    OBJECT_COLLISION_COLOR,
    array_to_string,
    get_elements,
    new_joint,
    scale_mjcf_model,
    new_body,
    new_site,
    new_geom,
    CustomMaterial,
)


class MujocoXML(object):
    """
    Base class of Mujoco xml file
    Wraps around ElementTree and provides additional functionality for merging different models.
    Specially, we keep track of <worldbody/>, <actuator/> and <asset/>

    When initialized, loads a mujoco xml from file.

    Args:
        fname (str): path to the MJCF xml file.
    """

    def __init__(self, fname):
        self.file = fname
        self.folder = os.path.dirname(fname)
        self.tree = ET.parse(fname)
        self.root = self.tree.getroot()
        self.worldbody = self.create_default_element("worldbody")
        self.actuator = self.create_default_element("actuator")
        self.sensor = self.create_default_element("sensor")
        self.asset = self.create_default_element("asset")
        self.tendon = self.create_default_element("tendon")
        self.equality = self.create_default_element("equality")
        self.contact = self.create_default_element("contact")

        # Parse any default classes and replace them inline
        default = self.create_default_element("default")
        default_classes = self._get_default_classes(default)
        self._replace_defaults_inline(default_dic=default_classes)

        # Remove original default classes
        self.root.remove(default)

        self.resolve_asset_dependency()

    def resolve_asset_dependency(self):
        """
        Converts every file dependency into absolute path so when we merge we don't break things.
        """

        for node in self.asset.findall("./*[@file]"):
            file = node.get("file")
            abs_path = os.path.abspath(self.folder)
            abs_path = os.path.join(abs_path, file)
            node.set("file", abs_path)

    def create_default_element(self, name):
        """
        Creates a <@name/> tag under root if there is none.

        Args:
            name (str): Name to generate default element

        Returns:
            ET.Element: Node that was created
        """

        found = self.root.find(name)
        if found is not None:
            return found
        ele = ET.Element(name)
        self.root.append(ele)
        return ele

    def merge(self, others, merge_body="default"):
        """
        Default merge method.

        Args:
            others (MujocoXML or list of MujocoXML): other xmls to merge into this one
                raises XML error if @others is not a MujocoXML instance.
                merges <worldbody/>, <actuator/> and <asset/> of @others into @self
            merge_body (None or str): If set, will merge child bodies of @others. Default is "default", which
                corresponds to the root worldbody for this XML. Otherwise, should be an existing body name
                that exists in this XML. None results in no merging of @other's bodies in its worldbody.

        Raises:
            XMLError: [Invalid XML instance]
        """
        if type(others) is not list:
            others = [others]
        for idx, other in enumerate(others):
            if not isinstance(other, MujocoXML):
                raise ValueError("{} is not a MujocoXML instance.".format(type(other)))
            if merge_body is not None:
                root = (
                    self.worldbody
                    if merge_body == "default"
                    else find_elements(
                        root=self.worldbody,
                        tags="body",
                        attribs={"name": merge_body},
                        return_first=True,
                    )
                )
                for body in other.worldbody:
                    root.append(body)
            self.merge_assets(other)
            for one_actuator in other.actuator:
                self.actuator.append(one_actuator)
            for one_sensor in other.sensor:
                self.sensor.append(one_sensor)
            for one_tendon in other.tendon:
                self.tendon.append(one_tendon)
            for one_equality in other.equality:
                self.equality.append(one_equality)
            for one_contact in other.contact:
                self.contact.append(one_contact)

    def get_model(self, mode="mujoco"):
        """
        Generates a MjModel instance from the current xml tree.

        Args:
            mode (str): Mode with which to interpret xml tree

        Returns:
            MjModel: generated model from xml

        Raises:
            ValueError: [Invalid mode]
        """

        available_modes = ["mujoco"]
        with io.StringIO() as string:
            string.write(ET.tostring(self.root, encoding="unicode"))
            if mode == "mujoco":
                import mujoco

                model = mujoco.MjModel.from_xml_string(string.getvalue())
                return model
            raise ValueError(
                "Unkown model mode: {}. Available options are: {}".format(
                    mode, ",".join(available_modes)
                )
            )

    def get_xml(self):
        """
        Reads a string of the MJCF XML file.

        Returns:
            str: XML tree read in from file
        """
        with io.StringIO() as string:
            string.write(ET.tostring(self.root, encoding="unicode"))
            return string.getvalue()

    def save_model(self, fname, pretty=False):
        """
        Saves the xml to file.

        Args:
            fname (str): output file location
            pretty (bool): If True, (attempts!! to) pretty print the output
        """
        with open(fname, "w") as f:
            xml_str = ET.tostring(self.root, encoding="unicode")
            if pretty:
                parsed_xml = xml.dom.minidom.parseString(xml_str)
                xml_str = parsed_xml.toprettyxml(newl="")
            f.write(xml_str)

    def merge_assets(self, other):
        """
        Merges @other's assets in a custom logic.

        Args:
            other (MujocoXML or MujocoObject): other xml file whose assets will be merged into this one
        """
        for asset in other.asset:
            if (
                find_elements(
                    root=self.asset,
                    tags=asset.tag,
                    attribs={"name": asset.get("name")},
                    return_first=True,
                )
                is None
            ):
                self.asset.append(asset)

    def get_element_names(self, root, element_type):
        """
        Searches recursively through the @root and returns a list of names of the specified @element_type

        Args:
            root (ET.Element): Root of the xml element tree to start recursively searching through
                (e.g.: `self.worldbody`)
            element_type (str): Name of element to return names of. (e.g.: "site", "geom", etc.)

        Returns:
            list: names that correspond to the specified @element_type
        """
        names = []
        for child in root:
            if child.tag == element_type:
                names.append(child.get("name"))
            names += self.get_element_names(child, element_type)
        return names

    @staticmethod
    def _get_default_classes(default):
        """
        Utility method to convert all default tags into a nested dictionary of values -- this will be used to replace
        all elements' class tags inline with the appropriate defaults if not specified.

        Args:
            default (ET.Element): Nested default tag XML root.

        Returns:
            dict: Nested dictionary, where each default class name is mapped to its own dict mapping element tag names
                (e.g.: geom, site, etc.) to the set of default attributes for that tag type
        """
        # Create nested dict to return
        default_dic = {}
        # Parse the default tag accordingly
        for cls in default:
            default_dic[cls.get("class")] = {child.tag: child for child in cls}
        return default_dic

    def _replace_defaults_inline(self, default_dic, root=None):
        """
        Utility method to replace all default class attributes recursively in the XML tree starting from @root
        with the corresponding defaults in @default_dic if they are not explicitly specified for ta given element.

        Args:
            root (ET.Element): Root of the xml element tree to start recursively replacing defaults. Only is used by
                recursive calls
            default_dic (dict): Nested dictionary, where each default class name is mapped to its own dict mapping
                element tag names (e.g.: geom, site, etc.) to the set of default attributes for that tag type
        """
        # If root is None, this is the top level call -- replace root with self.root
        if root is None:
            root = self.root
        # Check this current element if it contains any class elements
        cls_name = root.attrib.pop("class", None)
        if cls_name is not None:
            # If the tag for this element is contained in our default dic, we add any defaults that are not
            # explicitly specified in this
            tag_attrs = default_dic[cls_name].get(root.tag, None)
            if tag_attrs is not None:
                for k, v in tag_attrs.items():
                    if root.get(k, None) is None:
                        root.set(k, v)
        # Loop through all child elements
        for child in root:
            self._replace_defaults_inline(default_dic=default_dic, root=child)

    @property
    def name(self):
        """
        Returns name of this MujocoXML

        Returns:
            str: Name of this MujocoXML
        """
        return self.root.get("model")


class MujocoModel(object):
    """
    Base class for all simulation models used in mujoco.

    Standardizes core API for accessing models' relevant geoms, names, etc.
    """

    def correct_naming(self, names):
        """
        Corrects all strings in @names by adding the naming prefix to it and returns the name-corrected values

        Args:
            names (str, list, or dict): Name(s) to be corrected

        Raises:
            TypeError: [Invalid input type]
        """
        if type(names) is str:
            return (
                self.naming_prefix + names
                if not self.exclude_from_prefixing(names)
                else names
            )
        elif type(names) is list:
            return [
                self.naming_prefix + name
                if not self.exclude_from_prefixing(name)
                else name
                for name in names
            ]
        elif type(names) is dict:
            names = names.copy()
            for key, val in names.items():
                names[key] = self.correct_naming(val)
            return names
        else:
            # Assumed to be type error
            raise TypeError("Error: type of 'names' must be str, list, or dict!")

    def set_sites_visibility(self, sim, visible):
        """
        Set all site visual states for this model.

        Args:
            sim (MjSim): Current active mujoco simulation instance
            visible (bool): If True, will visualize model sites. Else, will hide the sites.
        """
        # Loop through all visualization geoms and set their alpha values appropriately
        for vis_g in self.sites:
            vis_g_id = sim.model.site_name2id(vis_g)
            if (visible and sim.model.site_rgba[vis_g_id][3] < 0) or (
                not visible and sim.model.site_rgba[vis_g_id][3] > 0
            ):
                # We toggle the alpha value
                sim.model.site_rgba[vis_g_id][3] = -sim.model.site_rgba[vis_g_id][3]

    def exclude_from_prefixing(self, inp):
        """
        A function that should take in an arbitrary input and return either True or False, determining whether the
        corresponding name to @inp should have naming_prefix added to it. Must be defined by subclass.

        Args:
            inp (any): Arbitrary input, depending on subclass. Can be str, ET.Element, etc.

        Returns:
            bool: True if we should exclude the associated name(s) with @inp from being prefixed with naming_prefix
        """
        raise NotImplementedError

    @property
    def name(self):
        """
        Name for this model. Should be unique.

        Returns:
            str: Unique name for this model.
        """
        raise NotImplementedError

    @property
    def naming_prefix(self):
        """
        Generates a standardized prefix to prevent naming collisions

        Returns:
            str: Prefix unique to this model.
        """
        raise NotImplementedError

    @property
    def root_body(self):
        """
        Root body name for this model. This should correspond to the top-level body element in the equivalent mujoco xml
        tree for this object.
        """
        raise NotImplementedError

    @property
    def bodies(self):
        """
        Returns:
            list: Body names for this model
        """
        raise NotImplementedError

    @property
    def joints(self):
        """
        Returns:
            list: Joint names for this model
        """
        raise NotImplementedError

    @property
    def actuators(self):
        """
        Returns:
            list: Actuator names for this model
        """
        raise NotImplementedError

    @property
    def sites(self):
        """
        Returns:
             list: Site names for this model
        """
        raise NotImplementedError

    @property
    def sensors(self):
        """
        Returns:
             list: Sensor names for this model
        """
        raise NotImplementedError

    @property
    def contact_geoms(self):
        """
        List of names corresponding to the geoms used to determine contact with this model.

        Returns:
            list: relevant contact geoms for this model
        """
        raise NotImplementedError

    @property
    def visual_geoms(self):
        """
        List of names corresponding to the geoms used for visual rendering of this model.

        Returns:
            list: relevant visual geoms for this model
        """
        raise NotImplementedError

    @property
    def important_geoms(self):
        """
        Geoms corresponding to important components of this model. String keywords should be mapped to lists of geoms.

        Returns:
            dict of list: Important set of geoms, where each set of geoms are grouped as a list and are
            organized by keyword string entries into a dict
        """
        raise NotImplementedError

    @property
    def important_sites(self):
        """
        Dict of sites corresponding to the important site geoms (e.g.: used to aid visualization during sim).

        Returns:
            dict: Important site geoms, where each specific geom name is mapped from keyword string entries
                in the dict
        """
        raise NotImplementedError

    @property
    def important_sensors(self):
        """
        Dict of important sensors enabled for this model.

        Returns:
            dict: Important sensors for this model, where each specific sensor name is mapped from keyword string
                entries in the dict
        """
        raise NotImplementedError

    @property
    def bottom_offset(self):
        """
        Returns vector from model root body to model bottom.
        Useful for, e.g. placing models on a surface.
        Must be defined by subclass.

        Returns:
            np.array: (dx, dy, dz) offset vector
        """
        raise NotImplementedError

    @property
    def top_offset(self):
        """
        Returns vector from model root body to model top.
        Useful for, e.g. placing models on a surface.
        Must be defined by subclass.

        Returns:
            np.array: (dx, dy, dz) offset vector
        """
        raise NotImplementedError

    @property
    def horizontal_radius(self):
        """
        Returns maximum distance from model root body to any radial point of the model.

        Helps us put models programmatically without them flying away due to a huge initial contact force.
        Must be defined by subclass.

        Returns:
            float: radius
        """
        raise NotImplementedError


class MujocoXMLModel(MujocoXML, MujocoModel):
    """
    Base class for all MujocoModels that are based on a raw XML file.

    Args:
        fname (str): Path to relevant xml file from which to create this robot instance
        idn (int or str): Number or some other unique identification string for this model instance
    """

    def __init__(self, fname, idn=0):
        super().__init__(fname)

        # Set id and add prefixes to all body names to prevent naming clashes
        self.idn = idn

        # Define other variables that get filled later
        self.mount = None

        # Define filter method to automatically add a default name to visual / collision geoms if encountered
        group_mapping = {
            None: "col",
            "0": "col",
            "1": "vis",
        }
        ctr_mapping = {
            "col": 0,
            "vis": 0,
        }

        def _add_default_name_filter(element, parent):
            # Run default filter
            filter_key = _element_filter(element=element, parent=parent)
            # Also additionally modify element if it is (a) a geom and (b) has no name
            if element.tag == "geom" and element.get("name") is None:
                group = group_mapping[element.get("group")]
                element.set("name", f"g{ctr_mapping[group]}_{group}")
                ctr_mapping[group] += 1
            # Return default filter key
            return filter_key

        # Parse element tree to get all relevant bodies, joints, actuators, and geom groups
        self._elements = sort_elements(
            root=self.root, element_filter=_add_default_name_filter
        )
        assert len(self._elements["root_body"]) == 1, (
            "Invalid number of root bodies found for robot model. Expected 1,"
            "got {}".format(len(self._elements["root_body"]))
        )
        self._elements["root_body"] = self._elements["root_body"][0]
        self._elements["bodies"] = (
            [self._elements["root_body"]] + self._elements["bodies"]
            if "bodies" in self._elements
            else [self._elements["root_body"]]
        )
        self._root_body = self._elements["root_body"].get("name")
        self._bodies = [e.get("name") for e in self._elements.get("bodies", [])]
        self._joints = [e.get("name") for e in self._elements.get("joints", [])]
        self._actuators = [e.get("name") for e in self._elements.get("actuators", [])]
        self._sites = [e.get("name") for e in self._elements.get("sites", [])]
        self._sensors = [e.get("name") for e in self._elements.get("sensors", [])]
        self._contact_geoms = [
            e.get("name") for e in self._elements.get("contact_geoms", [])
        ]
        self._visual_geoms = [
            e.get("name") for e in self._elements.get("visual_geoms", [])
        ]
        self._base_offset = string_to_array(
            self._elements["root_body"].get("pos", "0 0 0")
        )

        # Update all xml element prefixes
        add_prefix(
            root=self.root,
            prefix=self.naming_prefix,
            exclude=self.exclude_from_prefixing,
        )

        # Recolor all collision geoms appropriately
        recolor_collision_geoms(root=self.worldbody, rgba=self.contact_geom_rgba)

    def exclude_from_prefixing(self, inp):
        """
        By default, don't exclude any from being prefixed
        """
        return False

    @property
    def base_offset(self):
        """
        Provides position offset of root body.

        Returns:
            3-array: (x,y,z) pos value of root_body body element. If no pos in element, returns all zeros.
        """
        return self._base_offset

    @property
    def name(self):
        return "{}{}".format(type(self).__name__, self.idn)

    @property
    def naming_prefix(self):
        return "{}_".format(self.idn)

    @property
    def root_body(self):
        return self.correct_naming(self._root_body)

    @property
    def bodies(self):
        return self.correct_naming(self._bodies)

    @property
    def joints(self):
        return self.correct_naming(self._joints)

    @property
    def actuators(self):
        return self.correct_naming(self._actuators)

    @property
    def sites(self):
        return self.correct_naming(self._sites)

    @property
    def sensors(self):
        return self.correct_naming(self._sensors)

    @property
    def contact_geoms(self):
        return self.correct_naming(self._contact_geoms)

    @property
    def visual_geoms(self):
        return self.correct_naming(self._visual_geoms)

    @property
    def important_sites(self):
        return self.correct_naming(self._important_sites)

    @property
    def important_geoms(self):
        return self.correct_naming(self._important_geoms)

    @property
    def important_sensors(self):
        return self.correct_naming(self._important_sensors)

    @property
    def _important_sites(self):
        """
        Dict of sites corresponding to the important site geoms (e.g.: used to aid visualization during sim).

        Returns:
            dict: Important site geoms, where each specific geom name is mapped from keyword string entries
                in the dict. Note that the mapped sites should be the RAW site names found directly in the XML file --
                the naming prefix will be automatically added in the public method call
        """
        raise NotImplementedError

    @property
    def _important_geoms(self):
        """
        Geoms corresponding to important components of this model. String keywords should be mapped to lists of geoms.

        Returns:
            dict of list: Important set of geoms, where each set of geoms are grouped as a list and are
                organized by keyword string entries into a dict. Note that the mapped geoms should be the RAW geom
                names found directly in the XML file -- the naming prefix will be automatically added in the
                public method call
        """
        raise NotImplementedError

    @property
    def _important_sensors(self):
        """
        Dict of important sensors enabled for this model.

        Returns:
            dict: Important sensors for this model, where each specific sensor name is mapped from keyword string
                entries in the dict. Note that the mapped geoms should be the RAW sensor names found directly in the
                XML file -- the naming prefix will be automatically added in the public method call
        """
        raise NotImplementedError

    @property
    def contact_geom_rgba(self):
        """
        RGBA color to assign to all contact geoms for this model

        Returns:
            4-array: (r,g,b,a) values from 0 to 1 for this model's set of contact geoms
        """
        raise NotImplementedError

    @property
    def bottom_offset(self):
        """
        Returns vector from model root body to model bottom.
        Useful for, e.g. placing models on a surface.
        By default, this corresponds to the root_body's base offset.

        Returns:
            np.array: (dx, dy, dz) offset vector
        """
        return self.base_offset

    @property
    def top_offset(self):
        raise NotImplementedError

    @property
    def horizontal_radius(self):
        raise NotImplementedError


# Dict mapping geom type string keywords to group number
GEOMTYPE2GROUP = {
    "collision": {0},  # If we want to use a geom for physics, but NOT visualize
    "visual": {1},  # If we want to use a geom for visualization, but NOT physics
    "all": {0, 1},  # If we want to use a geom for BOTH physics + visualization
}

GEOM_GROUPS = GEOMTYPE2GROUP.keys()


class MujocoObject(MujocoModel):
    """
    Base class for all objects.

    We use Mujoco Objects to implement all objects that:

        1) may appear for multiple times in a task
        2) can be swapped between different tasks

    Typical methods return copy so the caller can all joints/attributes as wanted

    Args:
        obj_type (str): Geom elements to generate / extract for this object. Must be one of:

            :`'collision'`: Only collision geoms are returned (this corresponds to group 0 geoms)
            :`'visual'`: Only visual geoms are returned (this corresponds to group 1 geoms)
            :`'all'`: All geoms are returned

        duplicate_collision_geoms (bool): If set, will guarantee that each collision geom has a
            visual geom copy

    """

    def __init__(self, obj_type="all", duplicate_collision_geoms=True, scale=None):
        super().__init__()
        self.asset = ET.Element("asset")
        assert obj_type in GEOM_GROUPS, (
            "object type must be one in {}, got: {} instead.".format(
                GEOM_GROUPS, obj_type
            )
        )
        self.obj_type = obj_type
        self.duplicate_collision_geoms = duplicate_collision_geoms
        self._scale = scale
        # Attributes that should be filled in within the subclass
        self._name = None
        self._obj = None

        # Attributes that are auto-filled by _get_object_properties call
        self._root_body = None
        self._bodies = None
        self._joints = None
        self._actuators = None
        self._sites = None
        self._contact_geoms = None
        self._visual_geoms = None

        if self._scale is not None:
            self.set_scale(self._scale)

    def set_scale(self, scale, obj=None):
        """
        Scales each geom, mesh, site, and body.
        Called during initialization but can also be used externally

        Args:
            scale (float or list of floats): Scale factor (1 or 3 dims)
            obj (ET.Element) Root object to apply. Defaults to root object of model
        """
        if obj is None:
            obj = self._obj

        self._scale = scale

        # Use the centralized scaling utility function
        scale_mjcf_model(
            obj=obj,
            asset_root=self.asset,
            worldbody=None,  # because we don't have a worldbody in MujocoObject
            scale=scale,
            get_elements_func=get_elements,
            scale_slide_joints=False,  # MujocoObject doesn't handle slide joints
        )

    def merge_assets(self, other):
        """
        Merges @other's assets in a custom logic.

        Args:
            other (MujocoXML or MujocoObject): other xml file whose assets will be merged into this one
        """
        for asset in other.asset:
            if (
                find_elements(
                    root=self.asset,
                    tags=asset.tag,
                    attribs={"name": asset.get("name")},
                    return_first=True,
                )
                is None
            ):
                self.asset.append(asset)

    def get_obj(self):
        """
        Returns the generated / extracted object, in XML ElementTree form.

        Returns:
            ET.Element: Object in XML form.
        """
        assert self._obj is not None, "Object XML tree has not been generated yet!"
        return self._obj

    def exclude_from_prefixing(self, inp):
        """
        A function that should take in either an ET.Element or its attribute (str) and return either True or False,
        determining whether the corresponding name / str to @inp should have naming_prefix added to it.
        Must be defined by subclass.

        Args:
            inp (ET.Element or str): Element or its attribute to check for prefixing.

        Returns:
            bool: True if we should exclude the associated name(s) with @inp from being prefixed with naming_prefix
        """
        raise NotImplementedError

    def _get_object_subtree(self):
        """
        Returns a ET.Element
        It is a <body/> subtree that defines all collision and / or visualization related fields
        of this object.
        Return should be a copy.
        Must be defined by subclass.

        Returns:
            ET.Element: body
        """
        raise NotImplementedError

    def _get_object_properties(self):
        """
        Helper function to extract relevant object properties (bodies, joints, contact/visual geoms, etc...) from this
        object's XML tree. Assumes the self._obj attribute has already been filled.
        """
        # Parse element tree to get all relevant bodies, joints, actuators, and geom groups
        _elements = sort_elements(root=self.get_obj())
        assert len(_elements["root_body"]) == 1, (
            "Invalid number of root bodies found for robot model. Expected 1,"
            "got {}".format(len(_elements["root_body"]))
        )
        _elements["root_body"] = _elements["root_body"][0]
        _elements["bodies"] = (
            [_elements["root_body"]] + _elements["bodies"]
            if "bodies" in _elements
            else [_elements["root_body"]]
        )
        self._root_body = _elements["root_body"].get("name")
        self._bodies = [e.get("name") for e in _elements.get("bodies", [])]
        self._joints = [e.get("name") for e in _elements.get("joints", [])]
        self._actuators = [e.get("name") for e in _elements.get("actuators", [])]
        self._sites = [e.get("name") for e in _elements.get("sites", [])]
        self._sensors = [e.get("name") for e in _elements.get("sensors", [])]
        self._contact_geoms = [
            e.get("name") for e in _elements.get("contact_geoms", [])
        ]
        self._visual_geoms = [e.get("name") for e in _elements.get("visual_geoms", [])]

        # Add prefix to all elements
        add_prefix(
            root=self.get_obj(),
            prefix=self.naming_prefix,
            exclude=self.exclude_from_prefixing,
        )

    @property
    def name(self):
        return self._name

    @property
    def naming_prefix(self):
        return "{}_".format(self.name)

    @property
    def root_body(self):
        return self.correct_naming(self._root_body)

    @property
    def bodies(self):
        return self.correct_naming(self._bodies)

    @property
    def joints(self):
        return self.correct_naming(self._joints)

    @property
    def actuators(self):
        return self.correct_naming(self._actuators)

    @property
    def sites(self):
        return self.correct_naming(self._sites)

    @property
    def sensors(self):
        return self.correct_naming(self._sensors)

    @property
    def contact_geoms(self):
        return self.correct_naming(self._contact_geoms)

    @property
    def visual_geoms(self):
        return self.correct_naming(self._visual_geoms)

    @property
    def important_geoms(self):
        """
        Returns:
             dict: (Default is no important geoms; i.e.: empty dict)
        """
        return {}

    @property
    def important_sites(self):
        """
        Returns:
            dict:

                :`obj`: Object default site
        """
        return {"obj": self.naming_prefix + "default_site"}

    @property
    def important_sensors(self):
        """
        Returns:
            dict: (Default is no sensors; i.e.: empty dict)
        """
        return {}

    @property
    def bottom_offset(self):
        """
        Returns vector from model root body to model bottom.
        Useful for, e.g. placing models on a surface.
        Must be defined by subclass.

        Returns:
            np.array: (dx, dy, dz) offset vector
        """
        raise NotImplementedError

    @property
    def top_offset(self):
        """
        Returns vector from model root body to model top.
        Useful for, e.g. placing models on a surface.
        Must be defined by subclass.

        Returns:
            np.array: (dx, dy, dz) offset vector
        """
        raise NotImplementedError

    @property
    def horizontal_radius(self):
        """
        Returns maximum distance from model root body to any radial point of the model.

        Helps us put models programmatically without them flying away due to a huge initial contact force.
        Must be defined by subclass.

        Returns:
            float: radius
        """
        raise NotImplementedError

    @staticmethod
    def get_site_attrib_template():
        """
        Returns attribs of spherical site used to mark body origin

        Returns:
            dict: Dictionary of default site attributes
        """
        return {
            "pos": "0 0 0",
            "size": "0.002 0.002 0.002",
            "rgba": "1 0 0 1",
            "type": "sphere",
            "group": "0",
        }

    @staticmethod
    def get_joint_attrib_template():
        """
        Returns attribs of free joint

        Returns:
            dict: Dictionary of default joint attributes
        """
        return {
            "type": "free",
        }

    def get_bounding_box_half_size(self):
        raise NotImplementedError

    def get_bounding_box_size(self):
        """
        Returns numpy array with dimensions of a bounding box around this object.
        """
        return 2.0 * self.get_bounding_box_half_size()


class MujocoXMLObject(MujocoObject, MujocoXML):
    """
    MujocoObjects that are loaded from xml files (by default, inherit all properties (e.g.: name)
    from MujocoObject class first!)

    Args:
        fname (str): XML File path

        name (str): Name of this MujocoXMLObject

        joints (None or str or list of dict): each dictionary corresponds to a joint that will be created for this
            object. The dictionary should specify the joint attributes (type, pos, etc.) according to the MuJoCo xml
            specification. If "default", a single free-joint will be automatically generated. If None, no joints will
            be created.

        obj_type (str): Geom elements to generate / extract for this object. Must be one of:

            :`'collision'`: Only collision geoms are returned (this corresponds to group 0 geoms)
            :`'visual'`: Only visual geoms are returned (this corresponds to group 1 geoms)
            :`'all'`: All geoms are returned

        duplicate_collision_geoms (bool): If set, will guarantee that each collision geom has a
            visual geom copy

        scale (float or list of floats): 3D scale factor
    """

    def __init__(
        self,
        fname,
        name,
        joints="default",
        obj_type="all",
        duplicate_collision_geoms=True,
        scale=None,
    ):
        MujocoXML.__init__(self, fname)
        # Set obj type and duplicate args
        assert obj_type in GEOM_GROUPS, (
            "object type must be one in {}, got: {} instead.".format(
                GEOM_GROUPS, obj_type
            )
        )
        self.obj_type = obj_type
        self.duplicate_collision_geoms = duplicate_collision_geoms

        # Set name
        self._name = name

        # set scale
        self._scale = scale

        # joints for this object
        if joints == "default":
            self.joint_specs = [self.get_joint_attrib_template()]  # default free joint
        elif joints is None:
            self.joint_specs = []
        else:
            self.joint_specs = joints

        # Make sure all joints have names!
        for i, joint_spec in enumerate(self.joint_specs):
            if "name" not in joint_spec:
                joint_spec["name"] = "joint{}".format(i)

        # Lastly, parse XML tree appropriately
        self._obj = self._get_object_subtree()

        # scale
        if self._scale is not None:
            self.set_scale(self._scale)

        # Extract the appropriate private attributes for this
        self._get_object_properties()

    def _get_object_subtree(self):
        # Parse object
        # this line used to be wrapped in deepcopy.
        # removed this deepcopy line, as it creates discrepancies between obj and self.worldbody!
        obj = self.worldbody.find("./body/body[@name='object']")
        # Rename this top level object body (will have self.naming_prefix added later)
        obj.attrib["name"] = "main"
        # Get all geom_pairs in this tree
        geom_pairs = get_elements(obj, "geom")

        # Define a temp function so we don't duplicate so much code
        obj_type = self.obj_type

        def _should_keep(el):
            return int(el.get("group")) in GEOMTYPE2GROUP[obj_type]

        # Loop through each of these pairs and modify them according to @elements arg
        for i, (parent, element) in enumerate(geom_pairs):
            # Delete non-relevant geoms and rename remaining ones
            if not _should_keep(element):
                parent.remove(element)
            else:
                g_name = element.get("name")
                g_name = g_name if g_name is not None else f"g{i}"
                element.set("name", g_name)
                # Also optionally duplicate collision geoms if requested (and this is a collision geom)
                if self.duplicate_collision_geoms and element.get("group") in {
                    None,
                    "0",
                }:
                    parent.append(self._duplicate_visual_from_collision(element))
                    # Also manually set the visual appearances to the original collision model
                    element.set("rgba", array_to_string(OBJECT_COLLISION_COLOR))
                    if element.get("material") is not None:
                        del element.attrib["material"]
        # add joint(s)
        for joint_spec in self.joint_specs:
            obj.append(new_joint(**joint_spec))
        # Lastly, add a site for this object
        template = self.get_site_attrib_template()
        template["rgba"] = "1 0 0 0"
        template["name"] = "default_site"
        obj.append(ET.Element("site", attrib=template))

        return obj

    def exclude_from_prefixing(self, inp):
        """
        By default, don't exclude any from being prefixed
        """
        return False

    def _get_object_properties(self):
        """
        Extends the base class method to also add prefixes to all bodies in this object
        """
        super()._get_object_properties()
        add_prefix(
            root=self.root,
            prefix=self.naming_prefix,
            exclude=self.exclude_from_prefixing,
        )

    @staticmethod
    def _duplicate_visual_from_collision(element):
        """
        Helper function to duplicate a geom element to be a visual element. Namely, this corresponds to the
        following attribute requirements: group=1, conaffinity/contype=0, no mass, name appended with "_visual"

        Args:
            element (ET.Element): element to duplicate as a visual geom

        Returns:
            element (ET.Element): duplicated element
        """
        # Copy element
        vis_element = deepcopy(element)
        # Modify for visual-specific attributes (group=1, conaffinity/contype=0, no mass, update name)
        vis_element.set("group", "1")
        vis_element.set("conaffinity", "0")
        vis_element.set("contype", "0")
        vis_element.set("mass", "1e-8")
        vis_element.set("name", vis_element.get("name") + "_visual")
        return vis_element

    def set_pos(self, pos):
        """
        Set position of object position is defined as center of bounding box

        Args:
            pos (list of floats): 3D position to set object (should be 3 dims)
        """
        self._obj.set("pos", array_to_string(pos))

    def set_euler(self, euler):
        """
        Set Euler value object position

        Args:
            euler (list of floats): 3D Euler values (should be 3 dims)
        """
        self._obj.set("euler", array_to_string(euler))

    @property
    def rot(self):
        rot = string_to_array(self._obj.get("euler", "0.0 0.0 0.0"))
        return rot[2]

    def set_scale(self, scale, obj=None):
        """
        Scales each geom, mesh, site, and body.
        Called during initialization but can also be used externally

        Args:
            scale (float or list of floats): Scale factor (1 or 3 dims)
            obj (ET.Element) Root object to apply. Defaults to root object of model
        """
        if obj is None:
            obj = self._obj

        self._scale = scale

        # Use the centralized scaling utility function
        scale_mjcf_model(
            obj=obj,
            asset_root=self.asset,
            worldbody=self.worldbody,
            scale=scale,
            get_elements_func=get_elements,
            scale_slide_joints=False,  # MujocoXMLObject doesn't handle slide joints
        )

    @property
    def bottom_offset(self):
        bottom_site = self.worldbody.find(
            "./body/site[@name='{}bottom_site']".format(self.naming_prefix)
        )
        return string_to_array(bottom_site.get("pos"))

    @property
    def top_offset(self):
        top_site = self.worldbody.find(
            "./body/site[@name='{}top_site']".format(self.naming_prefix)
        )
        return string_to_array(top_site.get("pos"))

    @property
    def horizontal_radius(self):
        horizontal_radius_site = self.worldbody.find(
            "./body/site[@name='{}horizontal_radius_site']".format(self.naming_prefix)
        )
        return string_to_array(horizontal_radius_site.get("pos"))[0]

    def get_bounding_box_half_size(self):
        horizontal_radius_site = self.worldbody.find(
            "./body/site[@name='{}horizontal_radius_site']".format(self.naming_prefix)
        )
        return string_to_array(horizontal_radius_site.get("pos")) - self.bottom_offset

    def _get_elements_by_name(self, geom_names, body_names=None, joint_names=None):
        """
        seaches for returns all geoms, bodies, and joints used for cabinet
        called by _get_cab_components, as implemented in subclasses

        for geoms, include both collision and visual geoms
        """

        # names of every geom
        geoms = {geom_name: list() for geom_name in geom_names}
        for geom_name in geoms.keys():
            for postfix in ["", "_visual"]:
                g = find_elements(
                    root=self._obj,
                    tags="geom",
                    attribs={"name": self.name + "_" + geom_name + postfix},
                    return_first=True,
                )
                geoms[geom_name].append(g)

        # get bodies
        bodies = dict()
        if body_names is not None:
            for body_name in body_names:
                bodies[body_name] = find_elements(
                    root=self._obj,
                    tags="body",
                    attribs={"name": self.name + "_" + body_name},
                    return_first=True,
                )

        # get joints
        joints = dict()
        if joint_names is not None:
            for joint_name in joint_names:
                joints[joint_name] = find_elements(
                    root=self._obj,
                    tags="joint",
                    attribs={"name": self.name + "_" + joint_name},
                    return_first=True,
                )
        return geoms, bodies, joints


class MujocoGeneratedObject(MujocoObject):
    """
    Base class for all procedurally generated objects.

    Args:
        obj_type (str): Geom elements to generate / extract for this object. Must be one of:

            :`'collision'`: Only collision geoms are returned (this corresponds to group 0 geoms)
            :`'visual'`: Only visual geoms are returned (this corresponds to group 1 geoms)
            :`'all'`: All geoms are returned

        duplicate_collision_geoms (bool): If set, will guarantee that each collision geom has a
            visual geom copy
    """

    def __init__(self, obj_type="all", duplicate_collision_geoms=True):
        super().__init__(
            obj_type=obj_type, duplicate_collision_geoms=duplicate_collision_geoms
        )

        # Store common material names so we don't add prefixes to them
        self.shared_materials = set()
        self.shared_textures = set()

    def sanity_check(self):
        """
        Checks if data provided makes sense.
        Called in __init__()
        For subclasses to inherit from
        """
        pass

    @staticmethod
    def get_collision_attrib_template():
        """
        Generates template with collision attributes for a given geom

        Returns:
            dict: Initial template with `'pos'` and `'group'` already specified
        """
        return {"group": "0", "rgba": array_to_string(OBJECT_COLLISION_COLOR)}

    @staticmethod
    def get_visual_attrib_template():
        """
        Generates template with visual attributes for a given geom

        Returns:
            dict: Initial template with `'conaffinity'`, `'contype'`, and `'group'` already specified
        """
        return {"conaffinity": "0", "contype": "0", "mass": "1e-8", "group": "1"}

    def append_material(self, material):
        """
        Adds a new texture / material combination to the assets subtree of this XML
        Input is expected to be a CustomMaterial object

        See http://www.mujoco.org/book/XMLreference.html#asset for specific details on attributes expected for
        Mujoco texture / material tags, respectively

        Note that the "file" attribute for the "texture" tag should be specified relative to the textures directory
        located in sai_mujoco/assets

        Args:
            material (CustomMaterial): Material to add to this object
        """
        # First check if asset attribute exists; if not, define the asset attribute
        if not hasattr(self, "asset"):
            self.asset = ET.Element("asset")
        # If the material name is not in shared materials, add this to our assets
        if material.name not in self.shared_materials:
            self.asset.append(ET.Element("texture", attrib=material.tex_attrib))
            self.asset.append(ET.Element("material", attrib=material.mat_attrib))
        # Add this material name to shared materials if it should be shared
        if material.shared:
            self.shared_materials.add(material.name)
            self.shared_textures.add(material.tex_attrib["name"])
        # Update prefix for assets
        add_prefix(
            root=self.asset,
            prefix=self.naming_prefix,
            exclude=self.exclude_from_prefixing,
        )

    def exclude_from_prefixing(self, inp):
        """
        Exclude all shared materials and their associated names from being prefixed.

        Args:
            inp (ET.Element or str): Element or its attribute to check for prefixing.

        Returns:
            bool: True if we should exclude the associated name(s) with @inp from being prefixed with naming_prefix
        """
        # Automatically return False if this is not of type "str"
        if type(inp) is not str:
            return False
        # Only return True if the string matches the name of a common material
        return (
            True
            if inp in self.shared_materials or inp in self.shared_textures
            else False
        )

    # Methods that still need to be defined by subclass
    def _get_object_subtree(self):
        raise NotImplementedError

    def bottom_offset(self):
        raise NotImplementedError

    def top_offset(self):
        raise NotImplementedError

    def horizontal_radius(self):
        raise NotImplementedError

    def get_bounding_box_half_size(self):
        return (
            np.array([self.horizontal_radius, self.horizontal_radius, 0.0])
            - self.bottom_offset
        )


class CompositeBodyObject(MujocoGeneratedObject):
    """
    An object constructed out of multiple bodies to make more complex shapes.

    Args:
        name (str): Name of overall object

        objects (MujocoObject or list of MujocoObjects): object(s) to combine to form the composite body object.
            Note that these objects will be added sequentially, so if an object is required to be nested relative to
            another object, that nested object should be listed after the parent object. Note that all top-level joints
            for any inputted objects are automatically stripped

        object_locations (list): list of body locations in the composite. Each
            location should be a list or tuple of 3 elements and all
            locations are taken relative to that object's parent body. Giving None for a location results in (0,0,0)
            for that object.

        object_quats (None or list): list of (w, x, y, z) quaternions for each body. None results in (1,0,0,0) for
            that object.

        object_parents (None or list): Parent bodies to append each object to. Note that specifying "None" will
            automatically append all objects to the root body ("root")

        joints (None or list): Joints to use for the top-level composite body object. If None, no joints will be used
            for this top-level object. If "default", a single free joint will be added to the top-level body of this
            object. Otherwise, should be a list of dictionaries, where each dictionary should specify the specific
            joint attributes necessary. See http://www.mujoco.org/book/XMLreference.html#joint for reference.

        body_joints (None or dict): If specified, maps body names to joint specifications to append to that
            body. If None, no extra joints will be used. If mapped value is "default", a single free joint will be
            added to the specified body. Otherwise, should be a list of dictionaries, where each dictionary should
            specify the specific joint attributes necessary. See http://www.mujoco.org/book/XMLreference.html#joint
            for reference.

        sites (None or list): list of sites to add to top-level composite body object. If None, only the default
            top-level object site will be used. Otherwise, should be a list of dictionaries, where each dictionary
            should specify the appropriate attributes for the given site.
            See http://www.mujoco.org/book/XMLreference.html#site for reference.

        total_size (None or np.array): if provided, use this to describe the bounding box for this composite body
            object. Can also be used to specify @object_locations relative to the lower left corner of the bounding
            box defined by @total_size, instead of the center of this body, with @locations_relative_to_corner.

        locations_relative_to_corner (bool): if True, must supply @total_size. All object locations will be
            relative to the lower left corner of the bounding box.
    """

    def __init__(
        self,
        name,
        objects,
        object_locations,
        object_quats=None,
        object_parents=None,
        joints="default",
        body_joints=None,
        sites=None,
        total_size=None,
        locations_relative_to_corner=False,
    ):
        # Always call superclass first
        super().__init__()

        self._name = name

        # Set internal variable geometric properties which will be modified later
        self._object_absolute_positions = {
            "root": np.zeros(3)
        }  # maps body names to abs positions (rel to root)
        self._top = 0
        self._bottom = 0
        self._horizontal = 0

        # Standardize inputs
        if isinstance(objects, MujocoObject):
            self.objects = [objects]
        elif type(objects) in {list, tuple}:
            self.objects = list(objects)
        else:
            # Invalid objects received
            raise ValueError(
                "Invalid objects received, got type: {}".format(type(objects))
            )

        n_objects = len(self.objects)
        self.object_locations = np.array(object_locations)
        self.object_quats = (
            deepcopy(object_quats) if object_quats is not None else [None] * n_objects
        )
        self.object_parents = (
            deepcopy(object_parents)
            if object_parents is not None
            else ["root"] * n_objects
        )

        # Set joints
        if joints == "default":
            self.joint_specs = [self.get_joint_attrib_template()]  # default free joint
        elif joints is None:
            self.joint_specs = []
        else:
            self.joint_specs = joints

        # Set body joints
        if body_joints is None:
            body_joints = {}
        self.body_joint_specs = body_joints

        # Make sure all joints are named appropriately
        j_num = 0
        for joint_spec in self.joint_specs:
            if "name" not in joint_spec:
                joint_spec["name"] = "joint{}".format(j_num)
                j_num += 1

        # Set sites
        self.site_specs = deepcopy(sites) if sites is not None else []
        # Add default site
        site_element_attr = self.get_site_attrib_template()
        site_element_attr["rgba"] = "1 0 0 0"
        site_element_attr["name"] = "default_site"
        self.site_specs.append(site_element_attr)

        # Make sure all sites are named appropriately
        s_num = 0
        for site_spec in self.site_specs:
            if "name" not in site_spec:
                site_spec["name"] = "site{}".format(s_num)
                s_num += 1

        self.total_size = np.array(total_size) if total_size is not None else None
        self.locations_relative_to_corner = locations_relative_to_corner
        if self.locations_relative_to_corner:
            assert self.total_size is not None

        # Always run sanity check
        self.sanity_check()

        # Lastly, parse XML tree appropriately
        self._obj = self._get_object_subtree()

        # Extract the appropriate private attributes for this
        self._get_object_properties()

    def _get_object_subtree(self):
        # Initialize top-level body
        obj = new_body(name="root")

        # Add all joints and sites
        for joint_spec in self.joint_specs:
            obj.append(new_joint(**joint_spec))
        for site_spec in self.site_specs:
            obj.append(new_site(**site_spec))

        # Loop through all objects and associated args and append them appropriately
        for o, o_parent, o_pos, o_quat in zip(
            self.objects, self.object_parents, self.object_locations, self.object_quats
        ):
            self._append_object(
                root=obj, obj=o, parent_name=o_parent, pos=o_pos, quat=o_quat
            )

        # Loop through all joints and append them appropriately
        for body_name, joint_specs in self.body_joint_specs.items():
            self._append_joints(root=obj, body_name=body_name, joint_specs=joint_specs)

        # Return final object
        return obj

    def _get_object_properties(self):
        """
        Extends the superclass method to add prefixes to all assets
        """
        super()._get_object_properties()
        # Add prefix to all assets
        add_prefix(
            root=self.asset,
            prefix=self.naming_prefix,
            exclude=self.exclude_from_prefixing,
        )

    def _append_object(self, root, obj, parent_name=None, pos=None, quat=None):
        """
        Helper function to add pre-generated object @obj to the body with name @parent_name

        Args:
            root (ET.Element): Top-level element to iteratively search through for @parent_name to add @obj to
            obj (MujocoObject): Object to append to the body specified by @parent_name
            parent_name (None or str): Body name to search for in @root to append @obj to.
                None defaults to "root" (top-level body)
            pos (None or 3-array): (x,y,z) relative offset from parent body when appending @obj.
                None defaults to (0,0,0)
            quat (None or 4-array) (w,x,y,z) relative quaternion rotation from parent body when appending @obj.
                None defaults to (1,0,0,0)
        """
        # Set defaults if any are None
        if parent_name is None:
            parent_name = "root"
        if pos is None:
            pos = np.zeros(3)
        if quat is None:
            quat = np.array([1, 0, 0, 0])
        # First, find parent body
        parent = find_elements(
            root=root, tags="body", attribs={"name": parent_name}, return_first=True
        )
        assert parent is not None, "Could not find parent body with name: {}".format(
            parent_name
        )
        # Get the object xml element tree, remove its top-level joints, and modify its top-level pos / quat
        child = obj.get_obj()
        self._remove_joints(child)

        if self.locations_relative_to_corner:
            # use object location to convert to position coordinate (the origin is the
            # center of the composite object)
            cartesian_size = obj.get_bounding_box_half_size()
            pos = [
                (-self.total_size[0] + cartesian_size[0]) + pos[0],
                (-self.total_size[1] + cartesian_size[1]) + pos[1],
                (-self.total_size[2] + cartesian_size[2]) + pos[2],
            ]

        child.set("pos", array_to_string(pos))
        child.set("quat", array_to_string(quat))
        # Add this object and its assets to this composite object
        self.merge_assets(other=obj)
        parent.append(child)
        # Update geometric properties for this composite object
        obj_abs_pos = self._object_absolute_positions[parent_name] + np.array(pos)
        self._object_absolute_positions[obj.root_body] = obj_abs_pos
        self._top = max(self._top, obj_abs_pos[2] + obj.top_offset[2])
        self._bottom = min(self._bottom, obj_abs_pos[2] + obj.bottom_offset[2])
        self._horizontal = max(
            self._horizontal, max(obj_abs_pos[:2]) + obj.horizontal_radius
        )

    def _append_joints(self, root, body_name=None, joint_specs="default"):
        """
        Appends all joints as specified by @joint_specs to @body.

        Args:
            root (ET.Element): Top-level element to iteratively search through for @body_name
            body_name (None or str): Name of the body to append the joints to.
                None defaults to "root" (top-level body)
            joint_specs (str or list): List of joint specifications to add to the specified body, or
                "default", which results in a single free joint
        """
        # Standardize inputs
        if body_name is None:
            body_name = "root"
        if joint_specs == "default":
            joint_specs = [self.get_joint_attrib_template()]
        for i, joint_spec in enumerate(joint_specs):
            if "name" not in joint_spec:
                joint_spec["name"] = f"{body_name}_joint{i}"
        # Search for body and make sure it exists
        body = find_elements(
            root=root, tags="body", attribs={"name": body_name}, return_first=True
        )
        assert body is not None, "Could not find body with name: {}".format(body_name)
        # Add joint(s) to this body
        for joint_spec in joint_specs:
            body.append(new_joint(**joint_spec))

    @staticmethod
    def _remove_joints(body):
        """
        Helper function to strip all joints directly appended to the specified @body.

        Args:
            body (ET.Element): Body to strip joints from
        """
        children_to_remove = []
        for child in body:
            if child.tag == "joint":
                children_to_remove.append(child)
        for child in children_to_remove:
            body.remove(child)

    @property
    def bottom_offset(self):
        return np.array([0.0, 0.0, self._bottom])

    @property
    def top_offset(self):
        return np.array([0.0, 0.0, self._top])

    @property
    def horizontal_radius(self):
        return self._horizontal

    def get_bounding_box_half_size(self):
        if self.total_size is not None:
            return np.array(self.total_size)
        return super().get_bounding_box_half_size()


class CompositeObject(MujocoGeneratedObject):
    """
    An object constructed out of basic geoms to make more intricate shapes.

    Note that by default, specifying None for a specific geom element will usually set a value to the mujoco defaults.

    Args:
        name (str): Name of overall object

        total_size (list): (x, y, z) half-size in each dimension for the bounding box for
            this Composite object

        geom_types (list): list of geom types in the composite. Must correspond
            to MuJoCo geom primitives, such as "box" or "capsule".

        geom_locations (list): list of geom locations in the composite. Each
            location should be a list or tuple of 3 elements and all
            locations are relative to the lower left corner of the total box
            (e.g. (0, 0, 0) corresponds to this corner).

        geom_sizes (list): list of geom sizes ordered the same as @geom_locations

        geom_quats (None or list): list of (w, x, y, z) quaternions for each geom.

        geom_names (None or list): list of geom names ordered the same as @geom_locations. The
            names will get appended with an underscore to the passed name in @get_collision
            and @get_visual

        geom_rgbas (None or list): list of geom colors ordered the same as @geom_locations. If
            passed as an argument, @rgba is ignored.

        geom_materials (None or list of CustomTexture): list of custom textures to use for this object material

        geom_frictions (None or list): list of geom frictions to use for each geom.

        rgba (None or list): (r, g, b, a) default values to use if geom-specific @geom_rgbas isn't specified for a given element

        density (float or list of float): either single value to use for all geom densities or geom-specific values

        solref (list or list of list): parameters used for the mujoco contact solver. Can be single set of values or
            element-specific values. See http://www.mujoco.org/book/modeling.html#CSolver for details.

        solimp (list or list of list): parameters used for the mujoco contact solver. Can be single set of values or
            element-specific values. See http://www.mujoco.org/book/modeling.html#CSolver for details.

        locations_relative_to_center (bool): If true, @geom_locations will be considered relative to the center of the
            overall object bounding box defined by @total_size. Else, the corner of this bounding box is considered the
            origin.

        joints (None or list): Joints to use for this composite object. If None, no joints will be used
            for this top-level object. If "default", a single free joint will be added to this object.
            Otherwise, should be a list of dictionaries, where each dictionary should specify the specific
            joint attributes necessary. See http://www.mujoco.org/book/XMLreference.html#joint for reference.

        sites (None or list): list of sites to add to this composite object. If None, only the default
             object site will be used. Otherwise, should be a list of dictionaries, where each dictionary
            should specify the appropriate attributes for the given site.
            See http://www.mujoco.org/book/XMLreference.html#site for reference.

        obj_types (str or list of str): either single obj_type for all geoms or geom-specific type. Choices are
            {"collision", "visual", "all"}
    """

    def __init__(
        self,
        name,
        total_size,
        geom_types,
        geom_sizes,
        geom_locations,
        geom_quats=None,
        geom_names=None,
        geom_rgbas=None,
        geom_materials=None,
        geom_frictions=None,
        geom_condims=None,
        rgba=None,
        density=100.0,
        solref=(0.02, 1.0),
        solimp=(0.9, 0.95, 0.001),
        locations_relative_to_center=False,
        joints="default",
        sites=None,
        obj_types="all",
        duplicate_collision_geoms=True,
    ):
        # Always call superclass first
        super().__init__(duplicate_collision_geoms=duplicate_collision_geoms)

        self._name = name

        # Set joints
        if joints == "default":
            self.joint_specs = [self.get_joint_attrib_template()]  # default free joint
        elif joints is None:
            self.joint_specs = []
        else:
            self.joint_specs = joints

        # Make sure all joints are named appropriately
        j_num = 0
        for joint_spec in self.joint_specs:
            if "name" not in joint_spec:
                joint_spec["name"] = "joint{}".format(j_num)
                j_num += 1

        # Set sites
        self.site_specs = deepcopy(sites) if sites is not None else []
        # Add default site
        site_element_attr = self.get_site_attrib_template()
        site_element_attr["rgba"] = "1 0 0 0"
        site_element_attr["name"] = "default_site"
        self.site_specs.append(site_element_attr)

        # Make sure all sites are named appropriately
        s_num = 0
        for site_spec in self.site_specs:
            if "name" not in site_spec:
                site_spec["name"] = "site{}".format(s_num)
                s_num += 1

        n_geoms = len(geom_types)
        self.total_size = np.array(total_size)
        self.geom_types = np.array(geom_types)
        self.geom_sizes = deepcopy(geom_sizes)
        self.geom_locations = np.array(geom_locations)
        self.geom_quats = (
            deepcopy(geom_quats) if geom_quats is not None else [None] * n_geoms
        )
        self.geom_names = (
            list(geom_names) if geom_names is not None else [None] * n_geoms
        )
        self.geom_rgbas = (
            list(geom_rgbas) if geom_rgbas is not None else [None] * n_geoms
        )
        self.geom_materials = (
            list(geom_materials) if geom_materials is not None else [None] * n_geoms
        )
        self.geom_frictions = (
            list(geom_frictions) if geom_frictions is not None else [None] * n_geoms
        )
        self.geom_condims = (
            list(geom_condims) if geom_condims is not None else [None] * n_geoms
        )
        self.density = (
            [density] * n_geoms
            if density is None or type(density) in {float, int}
            else list(density)
        )
        self.solref = (
            [solref] * n_geoms
            if solref is None or type(solref[0]) in {float, int}
            else list(solref)
        )
        self.solimp = (
            [solimp] * n_geoms
            if obj_types is None or type(solimp[0]) in {float, int}
            else list(solimp)
        )
        self.rgba = rgba  # override superclass setting of this variable
        self.locations_relative_to_center = locations_relative_to_center
        self.obj_types = (
            [obj_types] * n_geoms
            if obj_types is None or type(obj_types) is str
            else list(obj_types)
        )

        # Always run sanity check
        self.sanity_check()

        # Lastly, parse XML tree appropriately
        self._obj = self._get_object_subtree()

        # Extract the appropriate private attributes for this
        self._get_object_properties()

    def get_bounding_box_half_size(self):
        return np.array(self.total_size)

    def in_box(self, position, object_position):
        """
        Checks whether the object is contained within this CompositeObject.
        Useful for when the CompositeObject has holes and the object should
        be within one of the holes. Makes an approximation by treating the
        object as a point, and the CompositeBoxObject as an axis-aligned grid.
        Args:
            position: 3D body position of CompositeObject
            object_position: 3D position of object to test for insertion
        """
        ub = position + self.total_size
        lb = position - self.total_size

        # fudge factor for the z-check, since after insertion the object falls to table
        lb[2] -= 0.01

        return np.all(object_position > lb) and np.all(object_position < ub)

    def _get_object_subtree(self):
        # Initialize top-level body
        obj = new_body(name="root")

        # Add all joints and sites
        for joint_spec in self.joint_specs:
            obj.append(new_joint(**joint_spec))
        for site_spec in self.site_specs:
            obj.append(new_site(**site_spec))

        # Loop through all geoms and generate the composite object
        for i, (
            obj_type,
            g_type,
            g_size,
            g_loc,
            g_name,
            g_rgba,
            g_friction,
            g_condim,
            g_quat,
            g_material,
            g_density,
            g_solref,
            g_solimp,
        ) in enumerate(
            zip(
                self.obj_types,
                self.geom_types,
                self.geom_sizes,
                self.geom_locations,
                self.geom_names,
                self.geom_rgbas,
                self.geom_frictions,
                self.geom_condims,
                self.geom_quats,
                self.geom_materials,
                self.density,
                self.solref,
                self.solimp,
            )
        ):
            # geom type
            geom_type = g_type
            # get cartesian size from size spec
            size = g_size
            cartesian_size = self._size_to_cartesian_half_lengths(geom_type, size)
            if self.locations_relative_to_center:
                # no need to convert
                pos = g_loc
            else:
                # use geom location to convert to position coordinate (the origin is the
                # center of the composite object)
                pos = [
                    (-self.total_size[0] + cartesian_size[0]) + g_loc[0],
                    (-self.total_size[1] + cartesian_size[1]) + g_loc[1],
                    (-self.total_size[2] + cartesian_size[2]) + g_loc[2],
                ]

            # geom name
            geom_name = g_name if g_name is not None else f"g{i}"

            # geom rgba
            geom_rgba = g_rgba if g_rgba is not None else self.rgba

            # geom friction
            geom_friction = (
                array_to_string(g_friction)
                if g_friction is not None
                else array_to_string(np.array([1.0, 0.005, 0.0001]))
            )  # mujoco default

            # Define base geom attributes
            geom_attr = {
                "size": size,
                "pos": pos,
                "name": geom_name,
                "type": geom_type,
            }

            # Optionally define quat if specified
            if g_quat is not None:
                geom_attr["quat"] = array_to_string(g_quat)

            # Add collision geom if necessary
            if obj_type in {"collision", "all"}:
                col_geom_attr = deepcopy(geom_attr)
                col_geom_attr.update(self.get_collision_attrib_template())
                if g_density is not None:
                    col_geom_attr["density"] = str(g_density)
                col_geom_attr["friction"] = geom_friction
                col_geom_attr["solref"] = array_to_string(g_solref)
                col_geom_attr["solimp"] = array_to_string(g_solimp)
                col_geom_attr["rgba"] = OBJECT_COLLISION_COLOR
                if g_condim is not None:
                    col_geom_attr["condim"] = str(g_condim)
                obj.append(new_geom(**col_geom_attr))

            # Add visual geom if necessary
            if obj_type in {"visual", "all"}:
                vis_geom_attr = deepcopy(geom_attr)
                vis_geom_attr.update(self.get_visual_attrib_template())
                vis_geom_attr["name"] += "_vis"
                if g_material is not None:
                    vis_geom_attr["material"] = g_material
                vis_geom_attr["rgba"] = geom_rgba
                obj.append(new_geom(**vis_geom_attr))

        return obj

    @staticmethod
    def _size_to_cartesian_half_lengths(geom_type, geom_size):
        """
        converts from geom size specification to x, y, and z half-length bounding box
        """
        if geom_type in ["box", "ellipsoid"]:
            return geom_size
        if geom_type == "sphere":
            # size is radius
            return [geom_size[0], geom_size[0], geom_size[0]]
        if geom_type == "capsule":
            # size is radius, half-length of cylinder part
            return [geom_size[0], geom_size[0], geom_size[0] + geom_size[1]]
        if geom_type == "cylinder":
            # size is radius, half-length
            return [geom_size[0], geom_size[0], geom_size[1]]
        raise Exception("unsupported geom type!")

    @property
    def bottom_offset(self):
        return np.array([0.0, 0.0, -self.total_size[2]])

    @property
    def top_offset(self):
        return np.array([0.0, 0.0, self.total_size[2]])

    @property
    def horizontal_radius(self):
        return np.linalg.norm(self.total_size[:2], 2)


class PrimitiveObject(MujocoGeneratedObject):
    """
    Base class for all programmatically generated mujoco object
    i.e., every MujocoObject that does not have an corresponding xml file

    Args:
        name (str): (unique) name to identify this generated object

        size (n-tuple of float): relevant size parameters for the object, should be of size 1 - 3

        rgba (4-tuple of float): Color

        density (float): Density

        friction (3-tuple of float): (sliding friction, torsional friction, and rolling friction).
            A single float can also be specified, in order to set the sliding friction (the other values) will
            be set to the MuJoCo default. See http://www.mujoco.org/book/modeling.html#geom for details.

        solref (2-tuple of float): MuJoCo solver parameters that handle contact.
            See http://www.mujoco.org/book/XMLreference.html for more details.

        solimp (3-tuple of float): MuJoCo solver parameters that handle contact.
            See http://www.mujoco.org/book/XMLreference.html for more details.

        material (CustomMaterial or `'default'` or None): if "default", add a template material and texture for this
            object that is used to color the geom(s).
            Otherwise, input is expected to be a CustomMaterial object

            See http://www.mujoco.org/book/XMLreference.html#asset for specific details on attributes expected for
            Mujoco texture / material tags, respectively

            Note that specifying a custom texture in this way automatically overrides any rgba values set

        joints (None or str or list of dict): Joints for this object. If None, no joint will be created. If "default",
            a single (free) joint will be crated. Else, should be a list of dict, where each dictionary corresponds to
            a joint that will be created for this object. The dictionary should specify the joint attributes
            (type, pos, etc.) according to the MuJoCo xml specification.

        obj_type (str): Geom elements to generate / extract for this object. Must be one of:

            :`'collision'`: Only collision geoms are returned (this corresponds to group 0 geoms)
            :`'visual'`: Only visual geoms are returned (this corresponds to group 1 geoms)
            :`'all'`: All geoms are returned

        duplicate_collision_geoms (bool): If set, will guarantee that each collision geom has a
            visual geom copy
    """

    def __init__(
        self,
        name,
        size=None,
        rgba=None,
        density=None,
        friction=None,
        solref=None,
        solimp=None,
        material=None,
        joints="default",
        obj_type="all",
        duplicate_collision_geoms=True,
    ):
        # Always call superclass first
        super().__init__(
            obj_type=obj_type, duplicate_collision_geoms=duplicate_collision_geoms
        )

        # Set name
        self._name = name

        if size is None:
            size = [0.05, 0.05, 0.05]
        self.size = list(size)

        if rgba is None:
            rgba = [1, 0, 0, 1]
        assert len(rgba) == 4, "rgba must be a length 4 array"
        self.rgba = list(rgba)

        if density is None:
            density = 1000  # water
        self.density = density

        if friction is None:
            friction = [1, 0.005, 0.0001]  # MuJoCo default
        elif isinstance(friction, float) or isinstance(friction, int):
            friction = [friction, 0.005, 0.0001]
        assert len(friction) == 3, (
            "friction must be a length 3 array or a single number"
        )
        self.friction = list(friction)

        if solref is None:
            self.solref = [0.02, 1.0]  # MuJoCo default
        else:
            self.solref = solref

        if solimp is None:
            self.solimp = [0.9, 0.95, 0.001]  # MuJoCo default
        else:
            self.solimp = solimp

        self.material = material
        if material == "default":
            # add in default texture and material for this object (for domain randomization)
            default_tex = CustomMaterial(
                texture=self.rgba,
                tex_name="tex",
                mat_name="mat",
            )
            self.append_material(default_tex)
        elif material is not None:
            # add in custom texture and material
            self.append_material(material)

        # joints for this object
        if joints == "default":
            self.joint_specs = [self.get_joint_attrib_template()]  # default free joint
        elif joints is None:
            self.joint_specs = []
        else:
            self.joint_specs = joints

        # Make sure all joints have names!
        for i, joint_spec in enumerate(self.joint_specs):
            if "name" not in joint_spec:
                joint_spec["name"] = "joint{}".format(i)

        # Always run sanity check
        self.sanity_check()

        # Lastly, parse XML tree appropriately
        self._obj = self._get_object_subtree()

        # Extract the appropriate private attributes for this
        self._get_object_properties()

    def _get_object_subtree_(self, ob_type="box"):
        # Create element tree
        obj = new_body(name="main")

        # Get base element attributes
        element_attr = {
            "name": "g0",
            "type": ob_type,
            "size": array_to_string(self.size),
        }

        # Add collision geom if necessary
        if self.obj_type in {"collision", "all"}:
            col_element_attr = deepcopy(element_attr)
            col_element_attr.update(self.get_collision_attrib_template())
            col_element_attr["density"] = str(self.density)
            col_element_attr["friction"] = array_to_string(self.friction)
            col_element_attr["solref"] = array_to_string(self.solref)
            col_element_attr["solimp"] = array_to_string(self.solimp)
            obj.append(new_geom(**col_element_attr))
        # Add visual geom if necessary
        if self.obj_type in {"visual", "all"}:
            vis_element_attr = deepcopy(element_attr)
            vis_element_attr.update(self.get_visual_attrib_template())
            vis_element_attr["name"] += "_vis"
            if self.material == "default":
                vis_element_attr["rgba"] = "0.5 0.5 0.5 1"  # mujoco default
                vis_element_attr["material"] = "mat"
            elif self.material is not None:
                vis_element_attr["material"] = self.material.mat_attrib["name"]
            else:
                vis_element_attr["rgba"] = array_to_string(self.rgba)
            obj.append(new_geom(**vis_element_attr))
        # add joint(s)
        for joint_spec in self.joint_specs:
            obj.append(new_joint(**joint_spec))
        # add a site as well
        site_element_attr = self.get_site_attrib_template()
        site_element_attr["name"] = "default_site"
        obj.append(new_site(**site_element_attr))
        return obj

    # Methods that still need to be defined by subclass
    def _get_object_subtree(self):
        raise NotImplementedError

    def bottom_offset(self):
        raise NotImplementedError

    def top_offset(self):
        raise NotImplementedError

    def horizontal_radius(self):
        raise NotImplementedError


class BoxObject(PrimitiveObject):
    """
    A box object.

    Args:
        size (3-tuple of float): (half-x, half-y, half-z) size parameters for this box object
    """

    def __init__(
        self,
        name,
        size=None,
        size_max=None,
        size_min=None,
        density=None,
        friction=None,
        rgba=None,
        solref=None,
        solimp=None,
        material=None,
        joints="default",
        obj_type="all",
        duplicate_collision_geoms=True,
        rng=None,
    ):
        size = get_size(
            size, size_max, size_min, [0.07, 0.07, 0.07], [0.03, 0.03, 0.03], rng=rng
        )
        super().__init__(
            name=name,
            size=size,
            rgba=rgba,
            density=density,
            friction=friction,
            solref=solref,
            solimp=solimp,
            material=material,
            joints=joints,
            obj_type=obj_type,
            duplicate_collision_geoms=duplicate_collision_geoms,
        )

    def sanity_check(self):
        """
        Checks to make sure inputted size is of correct length

        Raises:
            AssertionError: [Invalid size length]
        """
        assert len(self.size) == 3, "box size should have length 3"

    def _get_object_subtree(self):
        return self._get_object_subtree_(ob_type="box")

    @property
    def bottom_offset(self):
        return np.array([0, 0, -1 * self.size[2]])

    @property
    def top_offset(self):
        return np.array([0, 0, self.size[2]])

    @property
    def horizontal_radius(self):
        return np.linalg.norm(self.size[0:2], 2)

    def get_bounding_box_half_size(self):
        return np.array([self.size[0], self.size[1], self.size[2]])
