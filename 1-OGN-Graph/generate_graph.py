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

lidar_count = 4

for i in range(lidar_count):

    create_prim(
        prim_path=get_next_free_path("/Lidars/" + f"microscan{i}", None),
        prim_type="Xform",
        usd_path=get_assets_root_path() + "/Isaac/Sensors/SICK/microScan3.usd",
        translation=Gf.Vec3d(1 * i, 0, 0.15),
    )

    lidar_camera_path = f"/World/Lidars/microscan{i}/SICK_microscan3_official"

    keys_CREATE_NODES.append(
        (f"HLidar{i}Product", "isaacsim.core.nodes.IsaacCreateRenderProduct")
    )
    keys_CREATE_NODES.append(
        (f"HLidar{i}Publish", "isaacsim.ros2.bridge.ROS2RtxLidarHelper")
    )
    keys_SET_VALUES.append(
        (f"HLidar{i}Product.inputs:cameraPrim", f"/World/Lidars/microscan{i}/lidar")
    )
    keys_SET_VALUES.append(
        (f"HLidar{i}Publish.inputs:topicName", f"HLidar{i}")
    )
    keys_SET_VALUES.append(
        (f"HLidar{i}Publish.inputs:frameId", f"sim_HLidar{i}")
    )
    keys_SET_VALUES.append(
        (f"HLidar{i}Publish.inputs:nodeNamespace", "/isaac")
    )
    keys_SET_VALUES.append(
        (f"HLidar{i}Publish.inputs:resetSimulationTimeOnStop", True)
    )
    keys_CONNECT.append(
        ("RunOnce.outputs:step", f"HLidar{i}Product.inputs:execIn"),
    )
    keys_CONNECT.append(
        (f"HLidar{i}Product.outputs:execOut", f"HLidar{i}Publish.inputs:execIn"),
    )
    keys_CONNECT.append(
        (f"HLidar{i}Product.outputs:renderProductPath", f"HLidar{i}Publish.inputs:renderProductPath"),
    )
    keys_CONNECT.append(
        (f"Context.outputs:context", f"HLidar{i}Publish.inputs:context"),
    )

(graph_handle, nodes, _, _) = og.Controller.edit(
    {"graph_path": og_path, "evaluator_name": "execution"},
    {
        keys.CREATE_NODES: keys_CREATE_NODES,
        keys.SET_VALUES: keys_SET_VALUES, 
        keys.CONNECT: keys_CONNECT
        },
)
