
import omni.usd
import omni.kit.commands
import omni.graph.core as og

stage = omni.usd.get_context().get_stage()
keys = og.Controller.Keys
og_path = omni.usd.get_stage_next_free_path(stage, "/World/ControlGraph", True)

## Add a Franka robot to the stage if it does not already exist.
# stage.DefinePrim("/World/panda").GetReferences().AddReference("<your path to franka.usd>")

keys_CREATE_NODES = [
    ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
    ("SubscribeJointState", "isaacsim.ros2.bridge.ROS2SubscribeJointState"),
    ("ArticulationController", "isaacsim.core.nodes.IsaacArticulationController"),

]

keys_SET_VALUES =  [
    ("ArticulationController.inputs:targetPrim", "/World/panda"),
]

keys_CONNECT = [
    ("OnPlaybackTick.outputs:tick", "SubscribeJointState.inputs:execIn"),
    ("SubscribeJointState.outputs:execOut", "ArticulationController.inputs:execIn"),
    ("SubscribeJointState.outputs:effortCommand", "ArticulationController.inputs:effortCommand"),
    ("SubscribeJointState.outputs:jointNames", "ArticulationController.inputs:jointNames"),
    ("SubscribeJointState.outputs:positionCommand", "ArticulationController.inputs:positionCommand"),
    ("SubscribeJointState.outputs:velocityCommand", "ArticulationController.inputs:velocityCommand"),
    
]

(graph_handle, nodes, _, _) = og.Controller.edit(
    {"graph_path": og_path, "evaluator_name": "execution"},
    {
        keys.CREATE_NODES: keys_CREATE_NODES,
        keys.SET_VALUES: keys_SET_VALUES, 
        keys.CONNECT: keys_CONNECT
    },
)
