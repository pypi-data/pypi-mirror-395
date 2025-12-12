import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_string("""
<mujoco>
    <worldbody>
        <body name="mocap" mocap="true">
            <geom type="sphere" size="0.1"/>
        </body>
    </worldbody>
</mujoco>
""")
data = mujoco.MjData(model)
mocap_id = model.body("mocap").mocapid

def on_key(viewer, keycode):
    print("KEY:", keycode)
    if keycode == ord('a'):
        with viewer.lock():
            data.mocap_pos[mocap_id][2] += 0.1

with mujoco.viewer.launch(model, data) as viewer:
    viewer.user_key_callback = on_key
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
