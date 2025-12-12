from sai_mujoco.envs.kitchen.v0.kitchen import KitchenEnv_v0
from sai_mujoco.envs.kitchen.v0.models.fixtures import FixtureType
import sai_mujoco.utils.v0.object_utils as OU


class SortingCleanup_v0(KitchenEnv_v0):
    """
    Sorting Cleanup: composite task for Washing Dishes activity.

    Simulates the task of sorting and cleaning dishes.

    Steps:
        Pick the mug and place it in the sink. Pick the bowl and place it in the
        cabinet and then close the cabinet.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reward_type = kwargs.get("reward_type", "sparse")

        if self.reward_type == "sparse":
            self.reward_config = {"success_bonus": 1.0}

    def _setup_kitchen_references(self):
        super()._setup_kitchen_references()

        self.sink = self.register_fixture_ref("sink", dict(id=FixtureType.SINK))
        self.cab = self.register_fixture_ref(
            "cab", dict(id=FixtureType.CABINET_TOP, ref=self.sink)
        )
        self.counter = self.register_fixture_ref(
            "counter", dict(id=FixtureType.COUNTER, ref=self.sink, size=(0.5, 0.5))
        )

        self.init_robot_base_pos = self.sink

    def _get_task_desc(self):
        return "Pick the mug and place it in the sink. Pick the bowl and place it in the cabinet and then close the cabinet."

    def _reset_internal(self):
        super()._reset_internal()
        # not fully open since it may come in contact with eef
        self.cab.set_door_state(min=0.5, max=0.6, env=self, rng=self.np_random)

    def _get_obj_cfgs(self):
        cfgs = []

        cfgs.append(
            dict(
                name="mug",
                obj_groups=("mug"),
                graspable=True,
                washable=True,
                placement=dict(
                    fixture=self.counter,
                    sample_region_kwargs=dict(
                        ref=self.sink,
                        loc="left_right",
                    ),
                    size=(0.4, 0.4),
                    pos=("ref", -1),
                ),
            )
        )
        cfgs.append(
            dict(
                name="bowl",
                obj_groups=("bowl"),
                graspable=True,
                washable=True,
                placement=dict(
                    fixture=self.counter,
                    sample_region_kwargs=dict(
                        ref=self.sink,
                        loc="left_right",
                        # large enough region to sample the bowl
                        top_size=(0.5, 0.5),
                    ),
                    size=(0.7, 0.7),
                    pos=("ref", -1),
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
                    size=(0.50, 0.50),
                    pos=(0, 1.0),
                ),
            )
        )

        cfgs.append(
            dict(
                name="distr_cab",
                obj_groups="all",
                placement=dict(
                    fixture=self.cab,
                    size=(1.0, 0.20),
                    pos=(0.0, 1.0),
                    offset=(0.0, 0.0),
                ),
            )
        )

        return cfgs

    def _check_success(self):
        mug_in_sink = OU.obj_inside_of(self, "mug", self.sink)
        bowl_in_cab = OU.obj_inside_of(self, "bowl", self.cab)
        closed = True
        door_state = self.cab.get_door_state(env=self)

        for joint_p in door_state.values():
            if joint_p > 0.05:
                closed = False
                break

        return (
            mug_in_sink and bowl_in_cab and closed and OU.gripper_obj_far(self, "mug")
        )

    def compute_reward(self):
        return {"success_bonus": 1.0 if self._check_success() else 0.0}
