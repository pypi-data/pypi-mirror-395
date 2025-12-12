from sai_mujoco.envs.kitchen.v0.kitchen import KitchenEnv_v0
from sai_mujoco.envs.kitchen.v0.models.fixtures import FixtureType
import sai_mujoco.utils.v0.object_utils as OU


class PreSoakPan_v0(KitchenEnv_v0):
    """
    Pre Soak Pan: composite task for Washing Dishes activity.

    Simulates the task of pre-soaking a pan.

    Steps:
        Pick the pan and sponge and place them into the sink. Then turn on the sink.
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
            "counter", dict(id=FixtureType.COUNTER, ref=self.sink, size=(0.6, 0.4))
        )
        self.init_robot_base_pos = self.sink

    def _reset_internal(self):
        super()._reset_internal()
        self.sink.set_handle_state(mode="off", env=self, rng=self.np_random)

    def _get_obj_cfgs(self):
        cfgs = []
        cfgs.append(
            dict(
                name="obj1",
                obj_groups=("pan"),
                graspable=True,
                washable=True,
                placement=dict(
                    fixture=self.counter,
                    sample_region_kwargs=dict(
                        ref=self.sink,
                        loc="left_right",
                        # make sure sampled counter region is large enough to place the pan
                        top_size=(0.6, 0.4),
                    ),
                    size=(0.35, 0.55),
                    pos=("ref", -1.0),
                ),
                # make sure the sampled pan would fit in the sink basin
                max_size=(0.35, 0.45, None),
            )
        )

        cfgs.append(
            dict(
                name="obj2",
                obj_groups=("sponge"),
                placement=dict(
                    fixture=self.counter,
                    sample_region_kwargs=dict(ref=self.sink, loc="left_right"),
                    size=(0.3, 0.3),
                    pos=("ref", -1.0),
                ),
            )
        )

        return cfgs

    def _check_success(self):
        handle_state = self.sink.get_handle_state(env=self)
        water_on = handle_state["water_on"]
        pan_in_sink = OU.obj_inside_of(self, "obj1", self.sink)
        sponge_in_sink = OU.obj_inside_of(self, "obj2", self.sink)
        return (
            water_on
            and pan_in_sink
            and sponge_in_sink
            and OU.gripper_obj_far(self, "obj1")
        )

    def _get_task_desc(self):
        return "Pick the pan and sponge and place them into the sink. Then turn on the water."

    def compute_reward(self):
        return {"success_bonus": 1.0 if self._check_success() else 0.0}

