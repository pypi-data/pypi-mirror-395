"""

supersense/data/robotwin_data/adjust_bottle/demo_randomized/data/episode0.hdf5

"""

import sys, json
import h5py
from alfred.io.h5_wrapper import load_h5
import numpy as np


def test(h5_f):
    a = load_h5(h5_f)
    print(a.keys())

    ee = a["endpose"]
    print(ee.keys())
    obs = a["observation"]
    # print(f'ee: {ee['left_endpose']}')
    # print(f'ee: {ee['left_gripper']}')
    print(f"ee: {ee['right_endpose']}")
    print(f"ee: {ee['right_gripper']}")
    print(a["observation"].keys())
    print(a["joint_action"]["right_arm"])
    print(a["joint_action"]["right_gripper"])

    right_arm = a['joint_action']['right_arm']        # [140, 6]
    right_gripper = a['joint_action']['right_gripper']  # [6]
    
    g = np.array(right_gripper)[0]        # 取一个值
    g = np.full((right_arm.shape[0], 1), g)

    joint_all = np.hstack([right_arm, g])

    print(joint_all)
    # print(f'obs: {obs}')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        path = 'data/robotwin_data/blocks_ranking_rgb/demo_randomized_piper/data/episode0.hdf5'
    else:
        path = sys.argv[1]
    info = test(path)
    print(json.dumps(info, indent=2))
