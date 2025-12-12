from __future__ import annotations

from typing import Dict, Optional

import mujoco
import numpy as np
from gymnasium.envs.mujoco.mujoco_rendering import WindowViewer as GymWindowViewer
from mujoco import viewer as mjviewer

OFFSCREEN_RENDER_MODES = {"rgb_array", "depth_array", "rgbd_tuple"}


def _resolve_camera_id(
    model: mujoco.MjModel,
    camera_id: Optional[int],
    camera_name: Optional[str],
    *,
    default_camera_name: str = "track",
) -> int:
    """Resolve the MuJoCo camera index from either a name or an explicit id."""
    if camera_id is not None and camera_name is not None:
        raise ValueError("Specify only one of `camera_id` or `camera_name`.")

    if camera_id is not None:
        return camera_id

    if camera_name is not None:
        resolved = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, camera_name)
        if resolved == -1:
            raise ValueError(f'Camera "{camera_name}" does not exist in the model.')
        return resolved

    if default_camera_name:
        resolved = mujoco.mj_name2id(
            model, mujoco.mjtObj.mjOBJ_CAMERA, default_camera_name
        )
        if resolved != -1:
            return resolved

    return -1


class MjViewer:
    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        default_cam_config: Optional[dict],
        camera_id: int,
        hide_menu: bool,
    ) -> None:
        self.model = model
        self.data = data
        self.default_cam_config = default_cam_config or {}
        self.camera_id = camera_id
        self.hide_menu = hide_menu

        self._viewer = mjviewer.launch_passive(
            model,
            data,
            show_left_ui=not hide_menu,
            show_right_ui=not hide_menu,
        )
        self._configure_camera(camera_id)
        self.cam = self._viewer.cam
        self.vopt = self._viewer._opt

    def render(self):
        self._viewer.sync()

    def close(self) -> None:
        if self._viewer is not None:
            self._viewer.close()

    def _configure_camera(self, camera_id: int) -> None:
        camera = self._viewer.cam
        if camera_id == -1:
            camera.type = mujoco.mjtCamera.mjCAMERA_FREE
            mujoco.mjv_defaultFreeCamera(self.model, camera)
        else:
            camera.type = mujoco.mjtCamera.mjCAMERA_FIXED
            camera.fixedcamid = camera_id

        if not self.default_cam_config:
            return

        for key, value in self.default_cam_config.items():
            if not hasattr(camera, key):
                continue
            attr = getattr(camera, key)
            if isinstance(attr, np.ndarray):
                np.copyto(attr, np.asarray(value, dtype=attr.dtype))
            else:
                setattr(camera, key, value)


class OffScreenViewer:
    """Thin wrapper around `mujoco.Renderer` with camera helpers."""

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        default_cam_config: Optional[dict],
        camera_id: int,
        width: int,
        height: int,
        max_geom: int,
        visual_options: Dict[int, bool],
    ) -> None:
        self.model = model
        self.data = data
        self.default_cam_config = default_cam_config or {}
        self.camera_id = camera_id

        self._renderer = mujoco.Renderer(
            model, height=height, width=width, max_geom=max_geom
        )
        self._camera = mujoco.MjvCamera()
        mujoco.mjv_defaultCamera(self._camera)
        self._configure_camera(camera_id)

        self._scene_option = mujoco.MjvOption()
        mujoco.mjv_defaultOption(self._scene_option)
        for flag, value in visual_options.items():
            self._scene_option.flags[flag] = int(value)

        self.cam = self._camera
        self.vopt = self._scene_option

    def render(self, render_mode: Optional[str], camera_id: Optional[int] = None):
        if render_mode not in OFFSCREEN_RENDER_MODES:
            raise ValueError(
                f"Off-screen renderer only supports {sorted(OFFSCREEN_RENDER_MODES)}."
            )

        cam_id = self.camera_id if camera_id is None else camera_id
        if cam_id != self.camera_id:
            self._configure_camera(cam_id)
            self.camera_id = cam_id

        self._renderer.update_scene(
            self.data,
            camera=self._camera,
            scene_option=self._scene_option,
        )

        if render_mode == "depth_array":
            self._renderer.enable_depth_rendering()
            depth = self._renderer.render()
            self._renderer.disable_depth_rendering()
            return np.array(depth, copy=True)

        if render_mode == "rgb_array":
            rgb = self._renderer.render()
            return np.array(rgb, copy=True)

        # rgbd_tuple
        rgb = np.array(self._renderer.render(), copy=True)
        self._renderer.enable_depth_rendering()
        depth = np.array(self._renderer.render(), copy=True)
        self._renderer.disable_depth_rendering()
        return rgb, depth

    def close(self) -> None:
        self._renderer.close()

    def _configure_camera(self, camera_id: int) -> None:
        camera = self._camera
        if camera_id == -1:
            camera.type = mujoco.mjtCamera.mjCAMERA_FREE
            mujoco.mjv_defaultFreeCamera(self.model, camera)
        else:
            camera.type = mujoco.mjtCamera.mjCAMERA_FIXED
            camera.fixedcamid = camera_id

        if not self.default_cam_config:
            return

        for key, value in self.default_cam_config.items():
            if not hasattr(camera, key):
                continue
            attr = getattr(camera, key)
            if isinstance(attr, np.ndarray):
                np.copyto(attr, np.asarray(value, dtype=attr.dtype))
            else:
                setattr(camera, key, value)


class MujocoRenderer:
    """Renderer orchestrating interactive and offscreen viewers."""

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        default_cam_config: Optional[dict] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        max_geom: int = 10000,
        camera_id: Optional[int] = None,
        camera_name: Optional[str] = None,
        visual_options: Optional[Dict[int, bool]] = None,
        visual_geom_options: Optional[Dict[int, bool]] = None,
        renderer: Optional[str] = None,
        hide_menu: bool = True,
        offscreen_height: Optional[int] = None,
        offscreen_width: Optional[int] = None,
    ) -> None:
        self.model = model
        self.data = data
        self.default_cam_config = default_cam_config or {}
        self.max_geom = max_geom
        self.visual_options = dict(visual_options) if visual_options else {}
        self.visual_geom_options = (
            dict(visual_geom_options) if visual_geom_options else {}
        )
        self.renderer = renderer
        self.hide_menu = hide_menu

        self.width = width or model.vis.global_.offwidth or 640
        self.height = height or model.vis.global_.offheight or 480
        self.offscreen_height = offscreen_height or self.height or 256
        self.offscreen_width = offscreen_width or self.width or 256
        self._ensure_offscreen_buffer_capacity()

        self.camera_id = _resolve_camera_id(model, camera_id, camera_name)
        self._viewers: Dict[str, object] = {}
        self.viewer = None

    def _ensure_offscreen_buffer_capacity(self) -> None:
        """Ensure the offscreen framebuffer can accommodate the requested resolution."""
        self.model.vis.global_.offwidth = max(
            self.model.vis.global_.offwidth, self.offscreen_width
        )
        self.model.vis.global_.offheight = max(
            self.model.vis.global_.offheight, self.offscreen_height
        )

    def render(
        self,
        render_mode: Optional[str],
        camera_id: Optional[int] = None,
    ):
        if render_mode is None:
            return None

        viewer = self._get_viewer(render_mode)

        if render_mode == "human":
            viewer.render()
            return None

        if render_mode in OFFSCREEN_RENDER_MODES:
            return viewer.render(render_mode, camera_id=camera_id)

        raise ValueError(
            f"Unsupported render mode '{render_mode}'. "
            f"Expected one of: human, {', '.join(sorted(OFFSCREEN_RENDER_MODES))}."
        )

    def _get_viewer(self, render_mode: str):
        key = "offscreen" if render_mode in OFFSCREEN_RENDER_MODES else "human"

        self.viewer = self._viewers.get(key)

        if self.viewer is None:
            if key == "human":
                if self.renderer == "mjviewer":
                    self.viewer = MjViewer(
                        self.model,
                        self.data,
                        self.default_cam_config,
                        camera_id=self.camera_id,
                        hide_menu=self.hide_menu,
                    )
                else:
                    viewer = GymWindowViewer(
                        self.model,
                        self.data,
                        self.width,
                        self.height,
                        self.max_geom,
                        self.visual_options,
                    )
                    viewer._hide_menu = self.hide_menu
                    self._configure_camera(viewer.cam, self.camera_id)
                    self.viewer = viewer
            else:
                self.viewer = OffScreenViewer(
                    self.model,
                    self.data,
                    self.default_cam_config,
                    camera_id=self.camera_id,
                    width=self.offscreen_width,
                    height=self.offscreen_height,
                    max_geom=self.max_geom,
                    visual_options=self.visual_options,
                )

            for flag, value in self.visual_geom_options.items():
                self.viewer.vopt.geomgroup[flag] = int(value)

            self._viewers[key] = self.viewer

        if len(self._viewers) > 1:
            make_current = getattr(self.viewer, "make_context_current", None)
            if callable(make_current):
                make_current()
        return self.viewer

    def close(self) -> None:
        for viewer in self._viewers.values():
            viewer.close()
        self._viewers.clear()

    def _configure_camera(self, camera: mujoco.MjvCamera, camera_id: int) -> None:
        if camera_id == -1:
            camera.type = mujoco.mjtCamera.mjCAMERA_FREE
            mujoco.mjv_defaultFreeCamera(self.model, camera)
        else:
            camera.type = mujoco.mjtCamera.mjCAMERA_FIXED
            camera.fixedcamid = camera_id

        if not self.default_cam_config:
            return

        for key, value in self.default_cam_config.items():
            if not hasattr(camera, key):
                continue
            attr = getattr(camera, key)
            if isinstance(attr, np.ndarray):
                np.copyto(attr, np.asarray(value, dtype=attr.dtype))
            else:
                setattr(camera, key, value)
