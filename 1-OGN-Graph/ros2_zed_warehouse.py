from pxr import Usd, UsdGeom, Sdf, Gf
from isaacsim.core.utils.prims import create_prim
from isaacsim.core.utils.stage import get_next_free_path
from isaacsim.storage.native import get_assets_root_path
import isaacsim.core.api.objects as objects

import omni.kit.commands
import omni.graph.core as og

# # enable extension
# ext_manager = omni.kit.app.get_app().get_extension_manager()
# if not ext_manager.is_extension_enabled("sl.sensor.camera.bridge"):
#     ext_manager.set_extension_enabled_immediate("sl.sensor.camera.bridge", True)
#     ext_manager.set_extension_enabled_immediate("sl.sensor.camera", True)


# stage = omni.usd.get_context().get_stage()
objects.GroundPlane("/World/ground_plane", visible=True)

create_prim(
    prim_path=get_next_free_path("/World/scene", None),
    prim_type="Xform",
    usd_path="https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Buildings/Warehouse/Warehouse01.usd",
    translation=Gf.Vec3d(0, 0, 0),
)

create_prim(
    prim_path=get_next_free_path("/World/ZED_X", None),
    prim_type="Xform",
    usd_path="https://github.com/stereolabs/zed-isaac-sim/raw/refs/heads/main/usd/ZED_X.usdc",
    translation=Gf.Vec3d(0, 0, 0),
)


keys = og.Controller.Keys
stage = omni.usd.get_context().get_stage()
og_path = omni.usd.get_stage_next_free_path(stage, "/World/ControlGraph", True)


keys_CREATE_NODES = [
    ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
    ("RunOnce", "isaacsim.core.nodes.OgnIsaacRunOneSimulationFrame"),
    ("Context", "isaacsim.ros2.bridge.ROS2Context"),

    ("RenderProduct1", "isaacsim.core.nodes.IsaacCreateRenderProduct"),
    ("RGBPublish1", "isaacsim.ros2.bridge.ROS2CameraHelper"),
    ("CameraInfoPublish1", "isaacsim.ros2.bridge.ROS2CameraInfoHelper"),

    ("RenderProduct2", "isaacsim.core.nodes.IsaacCreateRenderProduct"),
    ("RGBPublish2", "isaacsim.ros2.bridge.ROS2CameraHelper"),
    ("CameraInfoPublish2", "isaacsim.ros2.bridge.ROS2CameraInfoHelper"),

]

keys_SET_VALUES =  [
    ("RenderProduct1.inputs:cameraPrim", "/World/ZED_X/base_link/ZED_X/CameraLeft"),
    ("RenderProduct1.inputs:height", 1200),
    ("RenderProduct1.inputs:width", 1920),
    

    # camera
    ("CameraInfoPublish1.inputs:topicName", "camera_info_left"),
    ("CameraInfoPublish1.inputs:frameId", "sim_camera"),

    ("CameraInfoPublish1.inputs:resetSimulationTimeOnStop", True),
    ("RGBPublish1.inputs:frameId", "sim_camera"),
    ("RGBPublish1.inputs:nodeNamespace", "/isaac"),
    ("RGBPublish1.inputs:resetSimulationTimeOnStop", True),
    ("RGBPublish1.inputs:topicName", "rgb_left"),

    ("RenderProduct2.inputs:cameraPrim", "/World/ZED_X/base_link/ZED_X/CameraRight"),
    ("RenderProduct2.inputs:height", 1200),
    ("RenderProduct2.inputs:width", 1920),
    
    # camera
    ("CameraInfoPublish2.inputs:topicName", "camera_info_right"),
    ("CameraInfoPublish2.inputs:frameId", "sim_camera"),

    ("CameraInfoPublish2.inputs:resetSimulationTimeOnStop", True),
    ("RGBPublish2.inputs:frameId", "sim_camera"),
    ("RGBPublish2.inputs:nodeNamespace", "/isaac"),
    ("RGBPublish2.inputs:resetSimulationTimeOnStop", True),
    ("RGBPublish2.inputs:topicName", "rgb_right"),
]

keys_CONNECT = [
    ("OnPlaybackTick.outputs:tick", "RunOnce.inputs:execIn"),
    ("RunOnce.outputs:step", "RenderProduct1.inputs:execIn"),
    ("RenderProduct1.outputs:execOut", "CameraInfoPublish1.inputs:execIn"),
    ("RenderProduct1.outputs:execOut", "RGBPublish1.inputs:execIn"),
    ("RenderProduct1.outputs:renderProductPath", "CameraInfoPublish1.inputs:renderProductPath"),
    ("RenderProduct1.outputs:renderProductPath", "RGBPublish1.inputs:renderProductPath"),
    ("Context.outputs:context", "CameraInfoPublish1.inputs:context"),
    ("Context.outputs:context", "RGBPublish1.inputs:context"),

    ("RunOnce.outputs:step", "RenderProduct2.inputs:execIn"),
    ("RenderProduct2.outputs:execOut", "CameraInfoPublish2.inputs:execIn"),
    ("RenderProduct2.outputs:execOut", "RGBPublish2.inputs:execIn"),
    ("RenderProduct2.outputs:renderProductPath", "CameraInfoPublish2.inputs:renderProductPath"),
    ("RenderProduct2.outputs:renderProductPath", "RGBPublish2.inputs:renderProductPath"),
    ("Context.outputs:context", "CameraInfoPublish2.inputs:context"),
    ("Context.outputs:context", "RGBPublish2.inputs:context"),

]

(graph_handle, nodes, _, _) = og.Controller.edit(
    {"graph_path": og_path, "evaluator_name": "execution"},
    {
        keys.CREATE_NODES: keys_CREATE_NODES,
        keys.SET_VALUES: keys_SET_VALUES, 
        keys.CONNECT: keys_CONNECT
    },
)
