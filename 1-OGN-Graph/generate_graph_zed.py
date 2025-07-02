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
    prim_path=get_next_free_path("/World/camera1", None),
    prim_type="Xform",
    usd_path="https://github.com/stereolabs/zed-isaac-sim/raw/refs/heads/main/usd/ZED_X.usdc",
    translation=Gf.Vec3d(0, 0, 0),
)

create_prim(
    prim_path=get_next_free_path("/World/camera2", None),
    prim_type="Xform",
    usd_path="https://github.com/stereolabs/zed-isaac-sim/raw/refs/heads/main/usd/ZED_X.usdc",
    translation=Gf.Vec3d(1, 0, 0),
)

keys = og.Controller.Keys
stage = omni.usd.get_context().get_stage()
og_path = omni.usd.get_stage_next_free_path(stage, "/World/ControlGraph", True)


keys_CREATE_NODES = [
    ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
    ("RunOnce", "isaacsim.core.nodes.OgnIsaacRunOneSimulationFrame"),
    ("ZedCamera1", "sl.sensor.camera.ZED_Camera"),
    ("ZedCamera2", "sl.sensor.camera.ZED_Camera"),
]

keys_SET_VALUES =  [
    ("ZedCamera1.inputs:camera_prim", "/World/camera1/base_link/ZED_X"),
    ("ZedCamera1.inputs:streaming_port", 30001),
    ("ZedCamera2.inputs:camera_prim", "/World/camera2/base_link/ZED_X"),
    ("ZedCamera2.inputs:streaming_port", 30002),
]


keys_CONNECT = [
    ("OnPlaybackTick.outputs:tick", "RunOnce.inputs:execIn"),
    ("RunOnce.outputs:step", "ZedCamera1.inputs:exec_in"),
    ("RunOnce.outputs:step", "ZedCamera2.inputs:exec_in"),
]


(graph_handle, nodes, _, _) = og.Controller.edit(
    {"graph_path": og_path, "evaluator_name": "execution"},
    {
        keys.CREATE_NODES: keys_CREATE_NODES,
        keys.SET_VALUES: keys_SET_VALUES, 
        keys.CONNECT: keys_CONNECT
    },
)



