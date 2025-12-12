import numpy as np
import pinocchio as pin
from scipy.spatial.transform import Rotation as R
from pink import Configuration, solve_ik
from pink.tasks import FrameTask


class RobotIK:
    def __init__(
        self,
        urdf_path: str,
        start_joint_positions=None,
        base_elements=["world"],
        end_link: str = None,
    ):
        # 加载 URDF 模型
        self.model = pin.buildModelFromUrdf(urdf_path)
        self.data = self.model.createData()
        self.chain_length = self.model.nq

        if end_link is None:
            end_link = self.model.names[-1]

        # 存储末端执行器 frame 名称
        self.end_link = end_link

        if start_joint_positions is None:
            start_joint_positions = np.zeros(self.model.nq)
        else:
            start_joint_positions = self._ensure_start_joint_pos_right(
                start_joint_positions
            )

        self.start_joint_positions = np.array(start_joint_positions)

    def _ensure_start_joint_pos_right(self, initial_joint_positions):
        if initial_joint_positions is not None:
            if len(initial_joint_positions) < self.chain_length:
                # 不够长就用0填充
                initial_joint_positions = [0.0] * (
                    self.chain_length - len(initial_joint_positions)
                ) + list(initial_joint_positions)
            elif len(initial_joint_positions) > self.chain_length:
                # 太长就截断
                # todo: this might error
                initial_joint_positions = list(initial_joint_positions)[
                    : self.chain_length
                ]
        return initial_joint_positions

    def compute_joint_angles(
        self,
        end_effector_position,
        end_effector_orientation=None,
        initial_joint_positions=None,
        trim_base_link=False,
        max_iter=10,
        dt=0.01,
    ):
        initial_joint_positions = self._ensure_start_joint_pos_right(
            initial_joint_positions
        )

        if initial_joint_positions is None:
            q = self.start_joint_positions.copy()
        else:
            q = np.array(initial_joint_positions)
        # print(q)

        # 创建配置
        configuration = Configuration(self.model, self.data, q)

        # 使用 __init__ 中存储的 end_link
        task = FrameTask(self.end_link, position_cost=1.0, orientation_cost=1.0)

        # 设置目标位姿
        if end_effector_orientation is None:
            orientation_matrix = np.eye(3)
        else:
            if len(end_effector_orientation) == 3:
                orientation_matrix = R.from_euler(
                    "xyz", end_effector_orientation
                ).as_matrix()
            elif len(end_effector_orientation) == 4:
                orientation_matrix = R.from_quat(end_effector_orientation).as_matrix()
            else:
                raise ValueError("姿态参数必须为3(欧拉角)或4(四元数)长度的数组")

        target_transform = pin.SE3(orientation_matrix, np.array(end_effector_position))
        task.set_target(target_transform)

        # 迭代求解
        for _ in range(max_iter):
            velocity = solve_ik(configuration, [task], dt, solver="quadprog")
            configuration.integrate_inplace(velocity, dt)

            # 检查收敛
            if np.linalg.norm(velocity) < 1e-4:
                break

        q_sol = configuration.q
        if trim_base_link:
            return q_sol[1:]
        return q_sol
