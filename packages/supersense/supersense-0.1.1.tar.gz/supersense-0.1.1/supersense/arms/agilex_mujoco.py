import asyncio
import json
import mujoco
import mujoco.viewer
import websockets
from loguru import logger


class PiperSim:
    def __init__(self, xml_path, actuator_names=[], host="0.0.0.0", port=8765):
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)
        self.joint_ids = [self.model.actuator(name).id for name in actuator_names]
        self.host = host
        self.port = port
        self.cmd_qpos = [0.0] * len(self.joint_ids)
        self.lock = asyncio.Lock()

    async def set_joint_positions(self, qpos_list):
        if len(qpos_list) != len(self.joint_ids):
            logger.error(
                f"qpos list not same as joint_ids: {len(qpos_list)} vs {len(self.joint_ids)}"
            )
            return
        async with self.lock:
            self.cmd_qpos = qpos_list

    async def ws_handler(self, websocket):
        async for msg in websocket:
            try:
                arr = json.loads(msg)
                print(f"Got control: {arr}")
                if isinstance(arr, list) and len(arr) == len(self.joint_ids):
                    await self.set_joint_positions(arr)
            except Exception as e:
                print("WS handler error:", e)

    async def ws_server(self):
        async with websockets.serve(self.ws_handler, self.host, self.port):
            await asyncio.Future()

    async def sim_loop(self, attach_gui_ctrl=False):
        with mujoco.viewer.launch_passive(self.model, self.data) as viewer:
            while viewer.is_running():
                if not attach_gui_ctrl:
                    async with self.lock:
                        for jid, val in zip(self.joint_ids, self.cmd_qpos):
                            self.data.qpos[jid] = val
                mujoco.mj_step(self.model, self.data)
                viewer.sync()
                await asyncio.sleep(0)

    async def run(self):
        await asyncio.gather(self.sim_loop(), self.ws_server())


if __name__ == "__main__":
    joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7"]
    sim = PiperSim("data/mujoco_menagerie-main/agilex_piper/scene.xml", joint_names)
    asyncio.run(sim.run())
