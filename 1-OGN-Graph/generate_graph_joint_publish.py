
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
    ("RunOnce", "isaacsim.core.nodes.OgnIsaacRunOneSimulationFrame"),
    ("Context", "isaacsim.ros2.bridge.ROS2Context"),
    ("ReadSimulationTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
    ("PublishJointState", "isaacsim.ros2.bridge.ROS2PublishJointState"),
]

keys_SET_VALUES =  [
    ("PublishJointState.inputs:targetPrim", "/World/panda"),
    ("PublishJointState.inputs:topicName", "joint_states"),
]

keys_CONNECT = [
    ("OnPlaybackTick.outputs:tick", "RunOnce.inputs:execIn"),
    ("RunOnce.outputs:step", "PublishJointState.inputs:execIn"),
    ("ReadSimulationTime.outputs:simulationTime", "PublishJointState.inputs:timeStamp"),
    ("Context.outputs:context", "PublishJointState.inputs:context"),
]

(graph_handle, nodes, _, _) = og.Controller.edit(
    {"graph_path": og_path, "evaluator_name": "execution"},
    {
        keys.CREATE_NODES: keys_CREATE_NODES,
        keys.SET_VALUES: keys_SET_VALUES, 
        keys.CONNECT: keys_CONNECT
    },
)
