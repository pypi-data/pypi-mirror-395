"""
using urdf, ikpy to inverse 3d pos to joints
"""

import ikpy.chain
import numpy as np
from scipy.spatial.transform import Rotation as R


class RobotIK:
    def __init__(
        self,
        urdf_path: str,
        start_joint_positions=None,
        base_elements=None,
        end_link_id=None,
    ):
        if base_elements is None:
            base_elements = ["link1"]
        # self.chain = ikpy.chain.Chain.from_urdf_file(urdf_path, base_elements=["world"])
        self.chain = ikpy.chain.Chain.from_urdf_file(
            urdf_path, base_elements=base_elements
        )
        if start_joint_positions is None:
            start_joint_positions = [0] * len(self.chain)
        self.start_joint_positions = start_joint_positions

        for i, link in enumerate(self.chain.links):
            print("=>", i, link.name, link.joint_type)
        print("=> active joints:", np.sum(self.chain.active_links_mask))

    def compute_joint_angles(
        self,
        end_effector_position: list,
        end_effector_orientation: list = None,
        initial_joint_positions: list = None,
        trim_base_link=False,
    ):

        if initial_joint_positions is None:
            initial_joint_positions = self.start_joint_positions

        chain_length = len(self.chain)
        # make sure init pos must same as chain length
        # chain might have a arm_base or world not exactly same as DoF
        if len(initial_joint_positions) < chain_length:
            # 不够长就用0填充
            initial_joint_positions = [0.0] * (
                chain_length - len(initial_joint_positions)
            ) + list(initial_joint_positions)
        elif len(initial_joint_positions) > chain_length:
            # 太长就截断
            # todo: this might error
            initial_joint_positions = list(initial_joint_positions)[:chain_length]

        # 默认末端姿态（Z轴朝下，单位旋转）
        if end_effector_orientation is None:
            orientation_matrix = R.from_euler("xyz", [0, 0, 0]).as_matrix()
        else:
            if len(end_effector_orientation) == 3:
                orientation_matrix = R.from_euler(
                    "xyz", end_effector_orientation
                ).as_matrix()
            elif len(end_effector_orientation) == 4:
                orientation_matrix = R.from_quat(end_effector_orientation).as_matrix()
            else:
                raise ValueError("姿态参数必须为3(欧拉角)或4(四元数)长度的数组")

        joint_angles = self.chain.inverse_kinematics(
            target_position=end_effector_position,
            target_orientation=orientation_matrix,
            orientation_mode="all",
            initial_position=initial_joint_positions,
            max_iter=400,
            # tol=1e-3
        )
        if trim_base_link:
            return joint_angles[1:]
        return joint_angles


# 使用示例
if __name__ == "__main__":
    urdf_path = "data/urdfs/robot_with_gripper.urdf"
    start_joints = [0, 0, 0, 0, 0, 0, 0]
    ik_tool = RobotIK(urdf_path, start_joints)

    # 末端位置
    ee_position = [0.5, 0.2, 0.3]

    ee_orientation_euler = [0, 0, 0]

    joints_default = ik_tool.compute_joint_angles(ee_position)
    joints_euler = ik_tool.compute_joint_angles(ee_position, ee_orientation_euler)

    print("默认末端姿态关节角:", joints_default)
    print("欧拉角姿态关节角:", joints_euler)
