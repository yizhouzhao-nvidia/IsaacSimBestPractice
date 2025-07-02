from pxr import Gf
from isaacsim.core.utils.prims import create_prim
from isaacsim.core.utils.stage import get_next_free_path
from isaacsim.storage.native import get_assets_root_path
import isaacsim.core.api.objects as objects

import omni.kit.commands
import omni.graph.core as og

objects.GroundPlane("/World/ground_plane", visible=True)


keys = og.Controller.Keys
stage = omni.usd.get_context().get_stage()
og_path = omni.usd.get_stage_next_free_path(stage, "/World/ControlGraph", True)


keys_CREATE_NODES = [
    ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
    ("CameraInfoPublish", "isaacsim.ros2.bridge.ROS2CameraInfoHelper"),
    ("RenderProduct", "isaacsim.core.nodes.IsaacCreateRenderProduct"),
    ("RunOnce", "isaacsim.core.nodes.OgnIsaacRunOneSimulationFrame"),
    ("Context", "isaacsim.ros2.bridge.ROS2Context"),
    ("RGBPublish", "isaacsim.ros2.bridge.ROS2CameraHelper"),
]

keys_SET_VALUES =  [
    ("RenderProduct.inputs:cameraPrim", "/OmniverseKit_Persp"),

    # camera
    ("CameraInfoPublish.inputs:topicName", "camera_info"),
    ("CameraInfoPublish.inputs:frameId", "sim_camera"),
    ("CameraInfoPublish.inputs:nodeNamespace", "/isaac"),
    ("CameraInfoPublish.inputs:resetSimulationTimeOnStop", True),
    ("RGBPublish.inputs:frameId", "sim_camera"),
    ("RGBPublish.inputs:nodeNamespace", "/isaac"),
    ("RGBPublish.inputs:resetSimulationTimeOnStop", True),
]

keys_CONNECT = [
    ("OnPlaybackTick.outputs:tick", "RunOnce.inputs:execIn"),
    ("RunOnce.outputs:step", "RenderProduct.inputs:execIn"),
    ("RenderProduct.outputs:execOut", "CameraInfoPublish.inputs:execIn"),
    ("RenderProduct.outputs:execOut", "RGBPublish.inputs:execIn"),
    ("RenderProduct.outputs:renderProductPath", "CameraInfoPublish.inputs:renderProductPath"),
    ("RenderProduct.outputs:renderProductPath", "RGBPublish.inputs:renderProductPath"),
    ("Context.outputs:context", "CameraInfoPublish.inputs:context"),
    ("Context.outputs:context", "RGBPublish.inputs:context"),
]

