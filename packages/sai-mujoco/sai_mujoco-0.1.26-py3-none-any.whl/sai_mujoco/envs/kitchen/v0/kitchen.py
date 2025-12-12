import os
from copy import deepcopy
import logging
from pathlib import Path
import numpy as np
import mujoco
import sai_mujoco.utils.v0.rotations as T
import sai_mujoco
import sai_mujoco.utils.v0.object_utils as OU
from sai_mujoco.envs.kitchen.v0.models.fixtures import (
    Fixture,
    FixtureType,
    Counter,
    Stove,
    Stovetop,
    HousingCabinet,
    Fridge,
    fixture_is_type,
)
from sai_mujoco.envs.kitchen.v0.models.objects.kitchen_objects import (
    OBJ_CATEGORIES,
    init_obj_categories,
    init_obj_groups,
)
from sai_mujoco.envs.kitchen.v0.models.objects.kitchen_object_utils import (
    ObjCat,
    sample_kitchen_object,
)
from sai_mujoco.envs.kitchen.v0.models.objects.objects import MJCFObject
from sai_mujoco.utils.v0.placement_samplers import (
    SequentialCompositeSampler,
    UniformRandomSampler,
)
from sai_mujoco.envs.base.base_v1 import BaseEnv_v1
from sai_mujoco.envs.kitchen.v0.models.scenes.kitchen_arena import KitchenArena
from sai_mujoco.utils.v0.download_assets import (
    check_assets_exist,
    prompt_user_confirmation,
    download_file,
    extract_zip,
    fetch_manifest,
    load_local_manifest,
    save_local_manifest,
    compare_manifests,
)


ASSETS_URL = "https://storage.googleapis.com/sai-mujoco-assets/kitchen/v0/assets.zip"
MANIFEST_URL = (
    "https://storage.googleapis.com/sai-mujoco-assets/kitchen/v0/manifest.json"
)

# default free cameras for different kitchen layouts
LAYOUT_CAMS = {
    0: dict(
        lookat=[2.26593463, -1.00037131, 1.38769295],
        distance=3.0505089839567323,
        azimuth=90.71563812375285,
        elevation=-12.63948837207208,
    ),
    1: dict(
        lookat=[2.66147999, -1.00162429, 1.2425155],
        distance=3.7958766287746255,
        azimuth=89.75784013699234,
        elevation=-15.177406642875091,
    ),
    2: dict(
        lookat=[3.02344359, -1.48874618, 1.2412914],
        distance=3.6684844368165512,
        azimuth=51.67880851867874,
        elevation=-13.302619131542388,
    ),
    3: dict(
        lookat=[11.44842548, -11.47664723, 11.24115989],
        distance=43.923271794728187,
        azimuth=227.12928449329333,
        elevation=-16.495686334624907,
    ),
    4: dict(
        lookat=[1.6, -1.0, 1.0],
        distance=5,
        azimuth=89.70301806083651,
        elevation=-18.02177994296577,
    ),
}

DEFAULT_LAYOUT_CAM = {
    "lookat": [2.25, -1, 1.05312667],
    "distance": 3,
    "azimuth": 89.70301806083651,
    "elevation": -25,
}

_ROBOT_POS_OFFSETS: dict[str, list[float]] = {
    "reachy2/v0": [0.1, 0.0, 0.0],
}


class KitchenEnv_v0(BaseEnv_v1):
    """
    Base class for Kitchen environments.

    Args:

        env_config (dict): environment configuration

        robot_entry_points (dict): robot entry points

        robot_config (dict): robot configuration

    # Observation Space
    The observation space consists of the robot state and the environment state. The kitchen environment state includes the robot gripper position and orientation, the object positions and orientations, and the relative positions and orientations of the object and the gripper.

    # Rewards
    The rewards are sparse rewards. The reward is 1.0 if the task is successful, otherwise 0.0.

    # Episode End
    The episode ends when the task is successful.

    # Truncation
    The default duration of an episode is 5000 timesteps.

    """

    scene_name = "v0/kitchen"
    single_robot = True
    default_camera_config = {
        "lookat": [2.25, -1, 1.05312667],
        "distance": 5,
        "azimuth": 89.70301806083651,
        "elevation": -30,
    }

    def __init__(
        self,
        env_config,
        robot_entry_points,
        robot_config,
        **kwargs,
    ):
        self.layout_id = int(env_config.get("layout_id", 6))
        self.style_id = int(env_config.get("style_id", 3))

        self.init_robot_base_pos = env_config.get("init_robot_base_pos", None)

        self.default_camera_config = LAYOUT_CAMS.get(self.layout_id, DEFAULT_LAYOUT_CAM)

        self._ensure_assets_available()

        self._create_obj_instances()

        kwargs.update(
            {
                "visual_geom_options": {
                    0: 0,
                },
            }
        )

        super().__init__(
            env_config=env_config,
            robot_entry_points=robot_entry_points,
            robot_config=robot_config,
            **kwargs,
        )
        assert len(self.robots) == 1, "KitchenEnv only supports one robot"

    def _ensure_assets_available(self):
        base_dir = Path(os.path.dirname(sai_mujoco.__file__)) / "assets" / "envs"
        ver = self.__class__.__name__.split("_")[-1]
        assets_dir = base_dir / "kitchen" / ver
        manifest_path = assets_dir / "manifest.json"
        required_dirs = ["fixtures", "objects", "textures"]

        assets_exist, missing_dirs = check_assets_exist(str(assets_dir), required_dirs)

        remote_manifest = fetch_manifest(MANIFEST_URL)
        if remote_manifest is None:
            if not assets_exist:
                raise RuntimeError(
                    f"Cannot fetch remote manifest and local assets missing: {', '.join(missing_dirs)}"
                )
            return

        local_manifest = load_local_manifest(str(manifest_path))

        if not assets_exist:
            needs_download = True
            reason = f"Assets missing: {', '.join(missing_dirs)}"
        else:
            needs_download, reason = compare_manifests(local_manifest, remote_manifest)

        if not needs_download:
            return

        message = f"{reason}\nDownload location: {assets_dir}\nSource: {ASSETS_URL}\n"

        if not prompt_user_confirmation(message):
            raise RuntimeError("Asset download declined.")

        print(f"Downloading assets to {assets_dir}...")
        zip_path = assets_dir / "assets.zip"

        try:
            os.makedirs(assets_dir, exist_ok=True)
            download_file(ASSETS_URL, str(zip_path))
            extract_zip(str(zip_path), str(assets_dir))

            assets_exist, missing_dirs = check_assets_exist(
                str(assets_dir), required_dirs
            )
            if not assets_exist:
                raise RuntimeError(
                    f"Asset extraction incomplete. Missing: {', '.join(missing_dirs)}"
                )

            save_local_manifest(remote_manifest, str(manifest_path))
            print(f"✓ Assets downloaded (version {remote_manifest.get('version')})")
        except Exception as e:
            raise RuntimeError(f"Download failed: {e}") from e
        finally:
            if zip_path.exists():
                zip_path.unlink()

    def _create_obj_instances(self):
        """
        Creates instances of the ObjCat class for each object category.
        Maps name to the different registries it can belong to and then maps the registry to the ObjCat instance
        """
        init_obj_categories()
        init_obj_groups()
        for name, kwargs in OBJ_CATEGORIES.items():
            # get the properties that are common to both registries
            common_properties = deepcopy(kwargs)
            for k in common_properties.keys():
                assert k in [
                    "graspable",
                    "washable",
                    "microwavable",
                    "cookable",
                    "freezable",
                    "types",
                    "aigen",
                    "objaverse",
                ]
            objaverse_kwargs = common_properties.pop("objaverse", None)
            aigen_kwargs = common_properties.pop("aigen", None)
            assert "scale" not in kwargs
            OBJ_CATEGORIES[name] = {}

            # create instances
            if objaverse_kwargs is not None:
                objaverse_kwargs.update(common_properties)
                OBJ_CATEGORIES[name]["objaverse"] = ObjCat(
                    name=name, **objaverse_kwargs
                )
            if aigen_kwargs is not None:
                aigen_kwargs.update(common_properties)
                OBJ_CATEGORIES[name]["aigen"] = ObjCat(
                    name=name, aigen_cat=True, **aigen_kwargs
                )

    def _load_scene_mjcf(self):
        """
        Loads the scene mjcf model
        """
        self.scene_mjcf = mujoco.MjSpec.from_string(self.model.get_xml())

    def _load_model(self):
        """
        Loads an xml model, puts it in self.model
        """
        # setup scene
        self.model = KitchenArena(
            layout_id=self.layout_id,
            style_id=self.style_id,
            rng=self.np_random,
        )

        # Arena always gets set to zero origin
        self.model.set_origin([0, 0, 0])

        # setup fixtures
        self.fixture_cfgs = self.model.get_fixture_cfgs()
        self.fixtures = {cfg["name"]: cfg["model"] for cfg in self.fixture_cfgs}

        self.model.merge_objects(list(self.fixtures.values()))

        # setup fixture locations
        fxtr_placement_initializer = self._get_placement_initializer(
            self.fixture_cfgs, z_offset=0.0
        )
        fxtr_placements = None
        for i in range(10):
            try:
                fxtr_placements = fxtr_placement_initializer.sample()
            except Exception as e:
                logging.debug(
                    "Ranomization error in initial placement. Try #{}: {}".format(i, e)
                )
                continue
            break
        if fxtr_placements is None:
            logging.debug(
                "Could not place fixtures. Trying again with self._load_model()"
            )
            self._load_model()
            return
        self.fxtr_placements = fxtr_placements
        # Loop through all objects and reset their positions
        for obj_pos, obj_quat, obj in fxtr_placements.values():
            assert isinstance(obj, Fixture)
            obj.set_pos(obj_pos)

            # hacky code to set orientation
            obj.set_euler(T.mat2euler(T.quat2mat(T.convert_quat(obj_quat, "xyzw"))))

        # setup internal references related to fixtures
        self._setup_kitchen_references()

        # set robot position
        if self.init_robot_base_pos is not None:
            ref_fixture = self.get_fixture(self.init_robot_base_pos)
        else:
            fixtures = list(self.fixtures.values())
            valid_src_fixture_classes = [
                "CoffeeMachine",
                "Toaster",
                "Stove",
                "Stovetop",
                "SingleCabinet",
                "HingeCabinet",
                "OpenCabinet",
                "Drawer",
                "Microwave",
                "Sink",
                "Hood",
                "Oven",
                "Fridge",
                "Dishwasher",
            ]
            while True:
                ref_fixture = self.np_random.choice(fixtures)
                fxtr_class = type(ref_fixture).__name__
                if fxtr_class not in valid_src_fixture_classes:
                    continue
                break

        # create and place objects
        self._create_objects()

        # setup object locations
        self.placement_initializer = self._get_placement_initializer(self.object_cfgs)
        object_placements = None
        for i in range(1):
            try:
                object_placements = self.placement_initializer.sample(
                    placed_objects=self.fxtr_placements
                )
            except Exception as e:
                logging.debug(
                    "Randomization error in initial placement. Try #{}".format(i)
                )
                continue
            break
        if object_placements is None:
            logging.debug(
                "Could not place objects. Trying again with self._load_model()"
            )
            self._load_model()
            return
        self.object_placements = object_placements

        super()._load_model()

        robot_base_pos, robot_base_ori = self.compute_robot_base_placement_pose(
            ref_fixture=ref_fixture
        )

        self.robots[0].set_base_xpos(robot_base_pos.tolist())
        quat = T.euler2quat(robot_base_ori.tolist())
        self.robots[0].set_base_quat(quat.tolist())

    def get_default_cam_config(self):
        robot_base_pos = self.sim.data.body_xpos[
            self.sim.model.body_name2id(self.robots[0].base_body_name)
        ]
        robot_base_mat = self.sim.data.body_xmat[
            self.sim.model.body_name2id(self.robots[0].base_body_name)
        ].reshape(3, 3)
        robot_base_ori = T.mat2euler(robot_base_mat)

        # Set default camera config
        lookat = robot_base_pos.copy()
        lookat[2] += 1.4
        distance = 1.3
        elevation = -55.0
        azimuth = robot_base_ori[2] * 180 / np.pi

        cam_config = {
            "lookat": lookat,
            "distance": distance,
            "azimuth": azimuth,
            "elevation": elevation,
        }
        return cam_config

    def _create_objects(self):
        """
        Creates and places objects in the kitchen environment.
        Helper function called by _create_objects()
        """
        # add objects
        self.objects = {}
        if "object_cfgs" in self.env_config:
            self.object_cfgs = self.env_config["object_cfgs"]
            for obj_num, cfg in enumerate(self.object_cfgs):
                if "name" not in cfg:
                    cfg["name"] = "obj_{}".format(obj_num + 1)
                model, info = self._create_obj(cfg)
                cfg["info"] = info
                self.objects[model.name] = model
                self.model.merge_objects([model])
        else:
            self.object_cfgs = self._get_obj_cfgs()
            addl_obj_cfgs = []
            for obj_num, cfg in enumerate(self.object_cfgs):
                cfg["type"] = "object"
                if "name" not in cfg:
                    cfg["name"] = "obj_{}".format(obj_num + 1)
                model, info = self._create_obj(cfg)
                cfg["info"] = info
                self.objects[model.name] = model
                self.model.merge_objects([model])

                try_to_place_in = cfg["placement"].get("try_to_place_in", None)

                # place object in a container and add container as an object to the scene
                if try_to_place_in and (
                    "in_container" in cfg["info"]["groups_containing_sampled_obj"]
                ):
                    container_cfg = {
                        "name": cfg["name"] + "_container",
                        "obj_groups": cfg["placement"].get("try_to_place_in"),
                        "placement": deepcopy(cfg["placement"]),
                        "type": "object",
                    }

                    container_kwargs = cfg["placement"].get("container_kwargs", None)
                    if container_kwargs is not None:
                        for k, v in container_kwargs.items():
                            container_cfg[k] = v

                    # add in the new object to the model
                    addl_obj_cfgs.append(container_cfg)
                    model, info = self._create_obj(container_cfg)
                    container_cfg["info"] = info
                    self.objects[model.name] = model
                    self.model.merge_objects([model])

                    # modify object config to lie inside of container
                    cfg["placement"] = dict(
                        size=(0.01, 0.01),
                        ensure_object_boundary_in_range=False,
                        sample_args=dict(
                            reference=container_cfg["name"],
                        ),
                    )

            # prepend the new object configs in
            self.object_cfgs = addl_obj_cfgs + self.object_cfgs

            # # remove objects that didn't get created
            # self.object_cfgs = [cfg for cfg in self.object_cfgs if "model" in cfg]

    def _create_obj(self, cfg):
        """
        Helper function for creating objects.
        Called by _create_objects()
        """
        if "info" in cfg:
            """
            if cfg has "info" key in it, that means it is storing meta data already
            that indicates which object we should be using.
            set the obj_groups to this path to do deterministic playback
            """
            mjcf_path = cfg["info"]["mjcf_path"]
            # replace with correct base path
            new_base_path = os.path.join(
                os.path.dirname(sai_mujoco.__path__),
                "assets",
                "envs",
                "kitchen",
                "v0",
                "objects",
            )
            new_path = os.path.join(new_base_path, mjcf_path.split("/objects/")[-1])
            obj_groups = new_path
            exclude_obj_groups = None
        else:
            obj_groups = cfg.get("obj_groups", "all")
            exclude_obj_groups = cfg.get("exclude_obj_groups", None)
        object_kwargs, object_info = self.sample_object(
            obj_groups,
            exclude_groups=exclude_obj_groups,
            graspable=cfg.get("graspable", None),
            washable=cfg.get("washable", None),
            microwavable=cfg.get("microwavable", None),
            cookable=cfg.get("cookable", None),
            freezable=cfg.get("freezable", None),
            max_size=cfg.get("max_size", (None, None, None)),
            object_scale=cfg.get("object_scale", None),
        )
        info = object_info

        object = MJCFObject(name=cfg["name"], **object_kwargs)

        return object, info

    def _setup_kitchen_references(self):
        """
        setup fixtures (and their references). this function is called within load_model function for kitchens
        """
        serialized_refs = self.env_config.get("fixture_refs", {})
        # unserialize refs
        self.fixture_refs = {
            k: self.get_fixture(v) for (k, v) in serialized_refs.items()
        }

    def compute_robot_base_placement_pose(self, ref_fixture, offset=None):
        """
        steps:
        1. find the nearest counter to this fixture
        2. compute offset relative to this counter
        3. transform offset to global coordinates

        Args:
            ref_fixture (Fixture): reference fixture to place th robot near

            offset (list): offset to add to the base position

        """
        # step 1: find vase fixture closest to robot
        base_fixture = None

        # get all base fixtures in the environment
        base_fixtures = [
            fxtr
            for fxtr in self.fixtures.values()
            if isinstance(fxtr, Counter)
            or isinstance(fxtr, Stove)
            or isinstance(fxtr, Stovetop)
            or isinstance(fxtr, HousingCabinet)
            or isinstance(fxtr, Fridge)
        ]

        for fxtr in base_fixtures:
            # get bounds of fixture
            point = ref_fixture.pos
            if not OU.point_in_fixture(point=point, fixture=fxtr, only_2d=True):
                continue
            base_fixture = fxtr
            break

        # set the base fixture as the ref fixture itself if cannot find fixture containing ref
        if base_fixture is None:
            base_fixture = ref_fixture
        # assert base_fixture is not None

        # step 2: compute offset relative to this counter
        base_to_ref, _ = OU.get_rel_transform(base_fixture, ref_fixture)
        cntr_y = base_fixture.get_ext_sites(relative=True)[0][1]
        base_to_edge = [
            base_to_ref[0],
            cntr_y - 0.20,
            0,
        ]
        if offset is not None:
            base_to_edge[0] += offset[0]
            base_to_edge[1] += offset[1]

        if (
            isinstance(base_fixture, HousingCabinet)
            or isinstance(base_fixture, Fridge)
            or "stack" in base_fixture.name
        ):
            base_to_edge[1] -= 0.10

        # apply robot-specific offset relative to the base fixture for x,y dims
        robot_name = self.robots[0].name
        if robot_name in _ROBOT_POS_OFFSETS:
            relative_rot = np.pi / 2
            cos_rot = np.cos(-relative_rot)
            sin_rot = np.sin(-relative_rot)
            rotation_matrix = np.array([[cos_rot, -sin_rot], [sin_rot, cos_rot]])

            robot_offset_xy = np.array(_ROBOT_POS_OFFSETS[robot_name][:2])
            fixture_offset_xy = rotation_matrix @ robot_offset_xy
            base_to_edge[0] += fixture_offset_xy[0]
            base_to_edge[1] += fixture_offset_xy[1]

        # step 3: transform offset to global coordinates
        robot_base_pos = np.zeros(3)
        robot_base_pos[0:2] = OU.get_pos_after_rel_offset(base_fixture, base_to_edge)[
            0:2
        ]

        # apply robot-specific absolutely for z dim
        if robot_name in _ROBOT_POS_OFFSETS:
            robot_base_pos[2] += _ROBOT_POS_OFFSETS[robot_name][2]
        robot_base_ori = np.array([0, 0, base_fixture.rot + np.pi / 2])

        return robot_base_pos, robot_base_ori

    def _get_placement_initializer(self, cfg_list, z_offset=0.01):
        """
        Creates a placement initializer for the objects/fixtures based on the specifications in the configurations list

        Args:
            cfg_list (list): list of object configurations

            z_offset (float): offset in z direction

        Returns:
            SequentialCompositeSampler: placement initializer

        """

        placement_initializer = SequentialCompositeSampler(
            name="SceneSampler", rng=self.np_random
        )

        for obj_i, cfg in enumerate(cfg_list):
            # determine which object is being placed
            if cfg["type"] == "fixture":
                mj_obj = self.fixtures[cfg["name"]]
            elif cfg["type"] == "object":
                mj_obj = self.objects[cfg["name"]]
            else:
                raise ValueError

            placement = cfg.get("placement", None)
            if placement is None:
                continue
            fixture_id = placement.get("fixture", None)
            if fixture_id is not None:
                # get fixture to place object on
                fixture = self.get_fixture(
                    id=fixture_id,
                    ref=placement.get("ref", None),
                )

                # calculate the total available space where object could be placed
                sample_region_kwargs = placement.get("sample_region_kwargs", {})
                reset_region = fixture.sample_reset_region(
                    env=self, **sample_region_kwargs
                )
                outer_size = reset_region["size"]
                margin = placement.get("margin", 0.04)
                outer_size = (outer_size[0] - margin, outer_size[1] - margin)

                # calculate the size of the inner region where object will actually be placed
                target_size = placement.get("size", None)
                if target_size is not None:
                    target_size = deepcopy(list(target_size))
                    for size_dim in [0, 1]:
                        if target_size[size_dim] == "obj":
                            target_size[size_dim] = mj_obj.size[size_dim] + 0.005
                        if target_size[size_dim] == "obj.x":
                            target_size[size_dim] = mj_obj.size[0] + 0.005
                        if target_size[size_dim] == "obj.y":
                            target_size[size_dim] = mj_obj.size[1] + 0.005
                    inner_size = np.min((outer_size, target_size), axis=0)
                else:
                    inner_size = outer_size

                inner_xpos, inner_ypos = placement.get("pos", (None, None))
                offset = placement.get("offset", (0.0, 0.0))

                # center inner region within outer region
                if inner_xpos == "ref":
                    # compute optimal placement of inner region to match up with the reference fixture
                    x_halfsize = outer_size[0] / 2 - inner_size[0] / 2
                    if x_halfsize == 0.0:
                        inner_xpos = 0.0
                    else:
                        ref_fixture = self.get_fixture(
                            placement["sample_region_kwargs"]["ref"]
                        )
                        ref_pos = ref_fixture.pos
                        fixture_to_ref = OU.get_rel_transform(fixture, ref_fixture)[0]
                        outer_to_ref = fixture_to_ref - reset_region["offset"]
                        inner_xpos = outer_to_ref[0] / x_halfsize
                        inner_xpos = np.clip(inner_xpos, a_min=-1.0, a_max=1.0)
                elif inner_xpos is None:
                    inner_xpos = 0.0

                if inner_ypos is None:
                    inner_ypos = 0.0
                # offset for inner region
                intra_offset = (
                    (outer_size[0] / 2 - inner_size[0] / 2) * inner_xpos + offset[0],
                    (outer_size[1] / 2 - inner_size[1] / 2) * inner_ypos + offset[1],
                )

                # center surface point of entire region
                ref_pos = fixture.pos + [0, 0, reset_region["offset"][2]]
                ref_rot = fixture.rot

                # x, y, and rotational ranges for randomization
                x_range = (
                    np.array([-inner_size[0] / 2, inner_size[0] / 2])
                    + reset_region["offset"][0]
                    + intra_offset[0]
                )
                y_range = (
                    np.array([-inner_size[1] / 2, inner_size[1] / 2])
                    + reset_region["offset"][1]
                    + intra_offset[1]
                )
                rotation = placement.get("rotation", np.array([-np.pi / 4, np.pi / 4]))
            else:
                target_size = placement.get("size", None)
                x_range = np.array([-target_size[0] / 2, target_size[0] / 2])
                y_range = np.array([-target_size[1] / 2, target_size[1] / 2])
                rotation = placement.get("rotation", np.array([-np.pi / 4, np.pi / 4]))
                ref_pos = [0, 0, 0]
                ref_rot = 0.0

            placement_initializer.append_sampler(
                sampler=UniformRandomSampler(
                    name="{}_Sampler".format(cfg["name"]),
                    mujoco_objects=mj_obj,
                    x_range=x_range,
                    y_range=y_range,
                    rotation=rotation,
                    ensure_object_boundary_in_range=placement.get(
                        "ensure_object_boundary_in_range", True
                    ),
                    ensure_valid_placement=placement.get(
                        "ensure_valid_placement", True
                    ),
                    reference_pos=ref_pos,
                    reference_rot=ref_rot,
                    z_offset=z_offset,
                    rng=self.np_random,
                    rotation_axis=placement.get("rotation_axis", "z"),
                ),
                sample_args=placement.get("sample_args", None),
            )

        return placement_initializer

    def _reset_internal(self):
        """
        Resets simulation internal configurations.
        """
        super()._reset_internal()

        # Reset all object positions using initializer sampler if we're not directly loading from an xml
        if not self.deterministic_reset and self.placement_initializer is not None:
            # use pre-computed object placements
            object_placements = self.object_placements

            # Loop through all objects and reset their positions
            for obj_pos, obj_quat, obj in object_placements.values():
                self.sim.data.set_joint_qpos(
                    obj.joints[0],
                    np.concatenate([np.array(obj_pos), np.array(obj_quat)]),
                )

        # step through a few timesteps to settle objects
        action = np.zeros(self.action_spec[0].shape)  # apply empty action

        # Loop through the simulation at the model timestep rate until we're ready to take the next policy step
        # (as defined by the control frequency specified at the environment level)
        policy_step = True
        for i in range(10 * int(self.control_timestep / self.model_timestep)):
            self.sim.step1()
            self._pre_action(action, policy_step)
            self.sim.step2()
            policy_step = False

    def _get_obj_cfgs(self):
        """
        Returns a list of object configurations to use in the environment.
        The object configurations are usually environment-specific and should
        be implemented in the subclass.

        Returns:
            list: list of object configurations
        """

        return []

    def find_object_cfg_by_name(self, name):
        """
        Finds and returns the object configuration with the given name.

        Args:
            name (str): name of the object configuration to find

        Returns:
            dict: object configuration with the given name
        """
        for cfg in self.object_cfgs:
            if cfg["name"] == name:
                return cfg
        raise ValueError

    def _setup_references(self):
        """
        Sets up references to important components. A reference is typically an
        index or a list of indices that point to the corresponding elements
        in a flatten array, which is how MuJoCo stores physical simulation data.
        """
        super()._setup_references()

        self.obj_body_id = {}
        for name, model in self.objects.items():
            self.obj_body_id[name] = self.sim.model.body_name2id(model.root_body)

    def _get_env_obs(self):
        obs = []
        eef_world_poses = []

        # Gripper(s) positions and orientations
        if self.robots[0].is_bimanual:
            l_eef_pose = self.sim.data.get_site_xpos(
                self.robots[0]._grippers["left_arm_gripper"].site_name
            )
            l_eef_quat = T.mat2quat(
                self.sim.data.get_site_xmat(
                    self.robots[0]._grippers["left_arm_gripper"].site_name
                )
            )

            obs.append(l_eef_pose)
            obs.append(l_eef_quat)

            l_world_pose_in_gripper = self.world_pose_in_gripper(l_eef_pose, l_eef_quat)

            r_eef_pose = self.sim.data.get_site_xpos(
                self.robots[0]._grippers["right_arm_gripper"].site_name
            )
            r_eef_quat = T.mat2quat(
                self.sim.data.get_site_xmat(
                    self.robots[0]._grippers["right_arm_gripper"].site_name
                )
            )

            obs.append(r_eef_pose)
            obs.append(r_eef_quat)

            r_world_pose_in_gripper = self.world_pose_in_gripper(r_eef_pose, r_eef_quat)

            eef_world_poses.append(l_world_pose_in_gripper)
            eef_world_poses.append(r_world_pose_in_gripper)
        else:
            eef_pose = self.sim.data.get_site_xpos(
                self.robots[0]._grippers["left_arm_gripper"].site_name
            )
            eef_quat = T.mat2quat(
                self.sim.data.get_site_xmat(
                    self.robots[0]._grippers["left_arm_gripper"].site_name
                )
            )
            obs.append(eef_pose)
            obs.append(eef_quat)

            world_pose_in_gripper = self.world_pose_in_gripper(eef_pose, eef_quat)
            eef_world_poses.append(world_pose_in_gripper)

        for obj_name in self.obj_body_id:
            obj_pose = self.sim.data.body_xpos[self.obj_body_id[obj_name]]
            obj_quat = self.sim.data.body_xquat[self.obj_body_id[obj_name]]

            obs.append(obj_pose)
            obs.append(obj_quat)

            for eef_world_pose in eef_world_poses:
                obj_eef_pose, obj_eef_quat = self.obj_to_eef_pos(
                    obj_pose, obj_quat, eef_world_pose
                )
                obs.append(obj_eef_pose)
                obs.append(obj_eef_quat)
        return np.concatenate(obs, dtype=np.float32)

    def obj_to_eef_pos(self, obj_pos, obj_quat, world_pose_in_gripper):
        obj_pose = T.pose2mat((obj_pos, obj_quat))
        rel_pose = T.pose_in_A_to_pose_in_B(obj_pose, world_pose_in_gripper)
        rel_pos, rel_quat = T.mat2pose(rel_pose)
        return rel_pos, rel_quat

    def world_pose_in_gripper(self, eef_pos, eef_quat):
        return T.pose_inv(T.pose2mat((eef_pos, eef_quat)))

    def _post_action(self, action):
        """
        Do any housekeeping after taking an action.

        Args:
            action (np.array): Action to execute within the environment

        Returns:
            3-tuple:
                - (float) reward from the environment
                - (bool) whether the current episode is terminated or not
                - (bool) whether the current episode is truncated or not
                - (dict) information about the current state of the environment
        """
        reward, terminated, truncated, info = super()._post_action(action)

        # Check if stove is turned on or not
        self.update_state()
        return reward, terminated, truncated, info

    def _get_info(self):
        info = super()._get_info()
        info.update({"success": self._check_success()})
        task_desc = self._get_task_desc()
        info.update({"task_desc": task_desc})
        return info

    def _get_task_desc(self) -> str:
        """
        Get the task description for the environment.
        """
        return ""

    def update_state(self):
        """
        Updates the state of the environment.
        This involves updating the state of all fixtures in the environment.
        """
        for fixtr in self.fixtures.values():
            fixtr.update_state(self)

    def _check_success(self):
        """
        Checks if the task has been successfully completed.
        Success condition is based on the task and to be implemented in the
        subclasses. Returns False by default.

        Returns:
            bool: True if the task is successfully completed, False otherwise
        """
        return False

    def sample_object(
        self,
        groups,
        exclude_groups=None,
        graspable=None,
        microwavable=None,
        washable=None,
        cookable=None,
        freezable=None,
        max_size=(None, None, None),
        object_scale=None,
    ):
        """
        Sample a kitchen object from the specified groups and within max_size bounds.

        Args:
            groups (list or str): groups to sample from or the exact xml path of the object to spawn

            exclude_groups (str or list): groups to exclude

            graspable (bool): whether the sampled object must be graspable

            washable (bool): whether the sampled object must be washable

            microwavable (bool): whether the sampled object must be microwavable

            cookable (bool): whether whether the sampled object must be cookable

            freezable (bool): whether whether the sampled object must be freezable

            max_size (tuple): max size of the object. If the sampled object is not within bounds of max size,
                            function will resample

            object_scale (float): scale of the object. If set will multiply the scale of the sampled object by this value


        Returns:
            dict: kwargs to apply to the MJCF model for the sampled object

            dict: info about the sampled object - the path of the mjcf, groups which the object's category belongs to,
            the category of the object the sampling split the object came from, and the groups the object was sampled from
        """
        return sample_kitchen_object(
            groups,
            exclude_groups=exclude_groups,
            graspable=graspable,
            washable=washable,
            microwavable=microwavable,
            cookable=cookable,
            freezable=freezable,
            rng=self.np_random,
            max_size=max_size,
            object_scale=object_scale,
        )

    def _is_fxtr_valid(self, fxtr, size):
        """
        checks if counter is valid for object placement by making sure it is large enough

        Args:
            fxtr (Fixture): fixture to check
            size (tuple): minimum size (x,y) that the counter region must be to be valid

        Returns:
            bool: True if fixture is valid, False otherwise
        """
        for region in fxtr.get_reset_regions(self).values():
            if region["size"][0] >= size[0] and region["size"][1] >= size[1]:
                return True
        return False

    def get_fixture(self, id, ref=None, size=(0.2, 0.2)):
        """
        search fixture by id (name, object, or type)

        Args:
            id (str, Fixture, FixtureType): id of fixture to search for

            ref (str, Fixture, FixtureType): if specified, will search for fixture close to ref (within 0.10m)

            size (tuple): if sampling counter, minimum size (x,y) that the counter region must be

        Returns:
            Fixture: fixture object
        """
        # case 1: id refers to fixture object directly
        if isinstance(id, Fixture):
            return id
        # case 2: id refers to exact name of fixture
        elif id in self.fixtures.keys():
            return self.fixtures[id]

        if ref is None:
            # find all fixtures with names containing given name
            if isinstance(id, FixtureType) or isinstance(id, int):
                matches = [
                    name
                    for (name, fxtr) in self.fixtures.items()
                    if fixture_is_type(fxtr, id)
                ]
            else:
                matches = [name for name in self.fixtures.keys() if id in name]
            if id == FixtureType.COUNTER or id == FixtureType.COUNTER_NON_CORNER:
                matches = [
                    name
                    for name in matches
                    if self._is_fxtr_valid(self.fixtures[name], size)
                ]
            assert len(matches) > 0
            # sample random key
            key = self.np_random.choice(matches)
            return self.fixtures[key]
        else:
            ref_fixture = self.get_fixture(ref)

            assert isinstance(id, FixtureType)
            cand_fixtures = []
            for fxtr in self.fixtures.values():
                if not fixture_is_type(fxtr, id):
                    continue
                if fxtr is ref_fixture:
                    continue
                if id == FixtureType.COUNTER:
                    fxtr_is_valid = self._is_fxtr_valid(fxtr, size)
                    if not fxtr_is_valid:
                        continue
                cand_fixtures.append(fxtr)

            # first, try to find fixture "containing" the reference fixture
            for fxtr in cand_fixtures:
                if OU.point_in_fixture(ref_fixture.pos, fxtr, only_2d=True):
                    return fxtr
            # if no fixture contains reference fixture, sample all close fixtures
            dists = [
                OU.fixture_pairwise_dist(ref_fixture, fxtr) for fxtr in cand_fixtures
            ]
            min_dist = np.min(dists)
            close_fixtures = [
                fxtr for (fxtr, d) in zip(cand_fixtures, dists) if d - min_dist < 0.10
            ]
            return self.np_random.choice(close_fixtures)

    def register_fixture_ref(self, ref_name, fn_kwargs):
        """
        Registers a fixture reference for later use. Initializes the fixture
        if it has not been initialized yet.

        Args:
            ref_name (str): name of the reference

            fn_kwargs (dict): keyword arguments to pass to get_fixture

        Returns:
            Fixture: fixture object
        """
        if ref_name not in self.fixture_refs:
            self.fixture_refs[ref_name] = self.get_fixture(**fn_kwargs)
        return self.fixture_refs[ref_name]

    def get_obj_lang(self, obj_name="obj", get_preposition=False):
        """
        gets a formatted language string for the object (replaces underscores with spaces)

        Args:
            obj_name (str): name of object
            get_preposition (bool): if True, also returns preposition for object

        Returns:
            str: language string for object
        """
        obj_cfg = None
        for cfg in self.object_cfgs:
            if cfg["name"] == obj_name:
                obj_cfg = cfg
                break
        lang = obj_cfg["info"]["cat"].replace("_", " ")

        if not get_preposition:
            return lang

        if lang in ["bowl", "pot", "pan"]:
            preposition = "in"
        elif lang in ["plate"]:
            preposition = "on"
        else:
            raise ValueError

        return lang, preposition

    def compute_terminated(self) -> bool:
        return self._check_success()
