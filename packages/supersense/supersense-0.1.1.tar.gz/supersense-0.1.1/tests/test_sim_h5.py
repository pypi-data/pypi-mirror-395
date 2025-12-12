import os
import mujoco
import mujoco.viewer
import threading
from pynput import keyboard
import asyncio
import time
import numpy as np
from loguru import logger


class PiperSim:
    def __init__(self, xml_path, actuator_names, ik_tool, host="0.0.0.0", port=8765):
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)

        # 机械臂
        self.joint_ids = [self.model.actuator(n).id for n in actuator_names]
        self.ik_tool = ik_tool
        self.cmd_qpos = [0.0] * len(self.joint_ids)

        # 小球
        self.mocap_id = self.model.body("target").mocapid[0]
        self.key_pressed = set()
        self.delta = 0.01
        self.dragging = False
        self.lock = asyncio.Lock()

        # 目标位置延迟更新
        self.latest_target = self.data.mocap_pos[self.mocap_id].copy()
        self.target_to_use = self.latest_target.copy()
        self.last_update_time = time.time()
        self.update_delay = 1.0  # 秒

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                if key in [
                    keyboard.Key.up,
                    keyboard.Key.down,
                    keyboard.Key.left,
                    keyboard.Key.right,
                ]:
                    self.key_pressed.add(key)
                elif hasattr(key, "char") and key.char in ["z", "x"]:
                    self.key_pressed.add(key.char)
            except AttributeError:
                pass

        def on_release(key):
            try:
                if key in self.key_pressed:
                    self.key_pressed.remove(key)
                elif hasattr(key, "char") and key.char in self.key_pressed:
                    self.key_pressed.remove(key.char)
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.daemon = True
        listener.start()

    async def update_ball_position(self, viewer):
        """独立线程/协程，处理键盘移动小球"""
        while viewer.is_running():
            move = np.array([0.0, 0.0, 0.0])
            if keyboard.Key.up in self.key_pressed:
                move[1] += self.delta
            if keyboard.Key.down in self.key_pressed:
                move[1] -= self.delta
            if keyboard.Key.left in self.key_pressed:
                move[0] -= self.delta
            if keyboard.Key.right in self.key_pressed:
                move[0] += self.delta
            if "z" in self.key_pressed:
                move[2] += self.delta
            if "x" in self.key_pressed:
                move[2] -= self.delta

            if np.any(move != 0.0):
                with viewer.lock():
                    self.data.mocap_pos[self.mocap_id, :] += move
                    mujoco.mj_forward(self.model, self.data)
                    # 更新时间戳
                    self.latest_target = self.data.mocap_pos[self.mocap_id].copy()
            await asyncio.sleep(0.01)

    async def sim_loop(self):
        self.start_keyboard_listener()
        with mujoco.viewer.launch_passive(self.model, self.data) as viewer:
            # 启动小球控制协程
            ball_task = asyncio.create_task(self.update_ball_position(viewer))

            while viewer.is_running():
                # 延迟更新目标点
                if time.time() - self.last_update_time > self.update_delay:
                    self.target_to_use = self.latest_target.copy()
                    self.last_update_time = time.time()

                # IK 计算机械臂到 target_to_use
                joints = self.ik_tool.compute_joint_angles(
                    self.target_to_use,
                    [0, 0, 0],
                    initial_joint_positions=self.cmd_qpos,
                    trim_base_link=True,
                    max_iter=200,
                )
                async with self.lock:
                    self.cmd_qpos = joints
                    for jid, val in zip(self.joint_ids, self.cmd_qpos):
                        self.data.qpos[jid] = val

                mujoco.mj_step(self.model, self.data)
                viewer.sync()
                await asyncio.sleep(0)

            ball_task.cancel()

    async def run(self):
        await self.sim_loop()


if __name__ == "__main__":
    from supersense.arms.traj_joints_pink import RobotIK

    joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "gripper"]

    ik_tool = RobotIK(
        "assets/piper_description_v100_test2.urdf",
        [0] * 7,
        base_elements=["arm_base"],
        end_link_id="link7",
    )

    sim = PiperSim(
        "data/mujoco_menagerie-main/agilex_piper/scene_ball.xml", joint_names, ik_tool
    )
    asyncio.run(sim.sim_loop())
