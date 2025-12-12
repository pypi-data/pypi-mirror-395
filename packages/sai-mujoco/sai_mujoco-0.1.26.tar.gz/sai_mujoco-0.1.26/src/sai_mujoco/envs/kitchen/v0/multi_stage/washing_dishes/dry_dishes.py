from sai_mujoco.envs.kitchen.v0.kitchen import KitchenEnv_v0
from sai_mujoco.envs.kitchen.v0.models.fixtures import FixtureType
import sai_mujoco.utils.v0.object_utils as OU


class DryDishes_v0(KitchenEnv_v0):
    """
    Dry Dishes: composite task for Washing Dishes activity.

    Simulates the task of drying dishes.

    Steps:
        Pick the cup and bowl from the sink and place them on the counter for drying.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reward_type = kwargs.get("reward_type", "sparse")

        if self.reward_type == "sparse":
            self.reward_config = {"success_bonus": 1.0}

    def _setup_kitchen_references(self):
        super()._setup_kitchen_references()

        self.sink = self.register_fixture_ref("sink", dict(id=FixtureType.SINK))
        self.counter = self.register_fixture_ref(
            "counter",
            dict(
                id=FixtureType.COUNTER,
                ref=self.sink,
            ),
        )
        self.init_robot_base_pos = self.sink

    def _get_task_desc(self):
        return "Pick the cup and bowl from the sink and place them on the counter for drying."

    def _get_obj_cfgs(self):
        cfgs = []

        # sample a random back corner for the cup to be placed on
        cup_pos = self.np_random.choice([(1.0, 1.0), (-1.0, 1.0)])
        cfgs.append(
            dict(
                name="obj1",
                obj_groups=("cup"),
                graspable=True,
                washable=True,
                placement=dict(
                    fixture=self.sink,
                    # hard code the cup to be in corners so that the cup and bowl fit in the sink
                    size=(0.1, 0.1),
                    # offset=(0.25, 0.25)
                    pos=cup_pos,
                ),
            )
        )
        cfgs.append(
            dict(
                name="obj2",
                obj_groups=("bowl"),
                graspable=True,
                washable=True,
                placement=dict(
                    fixture=self.sink,
                    # place the bowl in the middle of the sink and turn of ensure_object_boundary_in_range
                    # otherwise it becomes difficult to initialize since the bowl is so big
                    size=(0.05, 0.05),
                    ensure_object_boundary_in_range=False,
                ),
            )
        )

        cfgs.append(
            dict(
                name="distr_counter",
                obj_groups="all",
                placement=dict(
                    fixture=self.counter,
                    sample_region_kwargs=dict(
                        ref=self.sink,
                        loc="left_right",
                    ),
                    size=(0.30, 0.30),
                    pos=("ref", -1.0),
                    offset=(0.0, 0.30),
                ),
            )
        )

        return cfgs

    def _check_success(self):
        objs_on_counter = self.check_contact(
            self.objects["obj1"].contact_geoms, self.counter.contact_geoms
        ) and self.check_contact(
            self.objects["obj2"].contact_geoms, self.counter.contact_geoms
        )
        gripper_objs_far = OU.gripper_obj_far(self, "obj1") and OU.gripper_obj_far(
            self, "obj2"
        )
        return objs_on_counter and gripper_objs_far

    def compute_reward(self):
        return {"success_bonus": 1.0 if self._check_success() else 0.0}

