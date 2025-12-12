import os
import mujoco
import mujoco.viewer
from pynput import keyboard
import time
import numpy as np


class DragBallDemo:
    def __init__(self, xml_path):
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)
        self.mocap_id = self.model.body("ball_mocap").mocapid[0]
        self.running = True
        self.key_pressed = set()
        self.delta = 0.01  # 每帧移动量

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                # 方向键
                if key in [
                    keyboard.Key.up,
                    keyboard.Key.down,
                    keyboard.Key.left,
                    keyboard.Key.right,
                ]:
                    self.key_pressed.add(key)
                # z/x 控制 Z 轴
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

    def run(self):
        self.start_keyboard_listener()
        with mujoco.viewer.launch_passive(self.model, self.data) as viewer:
            while viewer.is_running() and self.running:
                move = np.array([0.0, 0.0, 0.0])

                # XY 平移
                if keyboard.Key.up in self.key_pressed:
                    move[1] += self.delta
                if keyboard.Key.down in self.key_pressed:
                    move[1] -= self.delta
                if keyboard.Key.left in self.key_pressed:
                    move[0] -= self.delta
                if keyboard.Key.right in self.key_pressed:
                    move[0] += self.delta

                # Z 轴
                if "z" in self.key_pressed:
                    move[2] += self.delta
                if "x" in self.key_pressed:
                    move[2] -= self.delta

                if np.any(move != 0.0):
                    with viewer.lock():
                        self.data.mocap_pos[self.mocap_id, :] += move
                        mujoco.mj_forward(self.model, self.data)
                        print(f"update pos: {self.data.mocap_pos[self.mocap_id]}")

                mujoco.mj_step(self.model, self.data)
                viewer.sync()
                time.sleep(0.01)


if __name__ == "__main__":
    xml_path = os.path.join(os.path.dirname(__file__), "scene_ball3.xml")
    sim = DragBallDemo(xml_path)
    sim.run()
