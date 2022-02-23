import pybullet as bullet
from liba1 import A1

# Initialisation
physics_server_id = bullet.connect(bullet.GUI)
bullet.setRealTimeSimulation(enableRealTimeSimulation=True, physicsClientId=physics_server_id)
bullet.setGravity(0, 0, -9.8, physics_server_id)
import pybullet_data; bullet.setAdditionalSearchPath(pybullet_data.getDataPath());
bullet.loadURDF("plane.urdf")
a1 = A1(physics_server_id)
bullet.resetDebugVisualizerCamera(
    physicsClientId = physics_server_id,
    cameraTargetPosition = [0, 0, 0.4],
    cameraDistance = 1.5,
    cameraYaw = 40,
    cameraPitch = -15)

motor_debug = a1.motor_info.applymap(
    lambda info: (index := info[0], bullet.addUserDebugParameter(
                                        physicsClientId = physics_server_id,
                                        paramName = info[1].decode("UTF-8"),
                                        rangeMin = info[8],
                                        rangeMax = info[9],
                                        startValue = 0.7 if index in a1.motor_indices.loc["hip flexion/extension", :].to_numpy()
                                               else -0.7*2 if index in a1.motor_indices.loc["knee", :].to_numpy()
                                               else  0,))
).to_numpy().flatten()

while True:
    bullet.setJointMotorControlArray(
        physicsClientId = physics_server_id,
        bodyUniqueId = a1.id,
        jointIndices = [index for index, _ in motor_debug],
        controlMode = bullet.POSITION_CONTROL,
        targetPositions = [bullet.readUserDebugParameter(param) for _, param in motor_debug],)
