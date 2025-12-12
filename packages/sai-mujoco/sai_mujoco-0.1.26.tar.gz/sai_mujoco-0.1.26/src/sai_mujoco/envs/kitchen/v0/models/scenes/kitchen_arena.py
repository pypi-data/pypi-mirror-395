from sai_mujoco.utils.v0.task_utils import Arena
from sai_mujoco.utils.v1.mujoco_env import MujocoEnv_v1
from sai_mujoco.envs.kitchen.v0.models.scenes.scene_builder import create_fixtures


# base class for kitchens
class KitchenArena(Arena):
    """
    Kitchen arena class holding all of the fixtures

    Args:
        layout_id (int or LayoutType): layout of the kitchen to load

        style_id (int or StyleType): style of the kitchen to load

        rng (np.random.Generator): random number generator used for initializing
            fixture state in the KitchenArena
    """

    def __init__(self, layout_id, style_id, mujoco_objects=[], rng=None):
        scene_xml_path = MujocoEnv_v1.get_asset_path("scene", "v0/kitchen")
        super().__init__(scene_xml_path)
        self.fixtures = create_fixtures(
            layout_id=layout_id,
            style_id=style_id,
            rng=rng,
        )
        self.mujoco_objects = mujoco_objects

    def get_fixture_cfgs(self):
        """
        Returns config data for all fixtures in the arena

        Returns:
            list: list of fixture configurations
        """
        fixture_cfgs = []
        for name, fxtr in self.fixtures.items():
            cfg = {}
            cfg["name"] = name
            cfg["model"] = fxtr
            cfg["type"] = "fixture"
            if hasattr(fxtr, "_placement"):
                cfg["placement"] = fxtr._placement

            fixture_cfgs.append(cfg)

        return fixture_cfgs
