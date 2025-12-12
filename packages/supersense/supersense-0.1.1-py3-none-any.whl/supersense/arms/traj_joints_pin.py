"""
using vanilla pinchino for inverse ik
"""

import numpy as np
import pinocchio as pin
from numpy.linalg import norm, solve
from scipy.spatial.transform import Rotation as R
from loguru import logger


class RobotIK:
    def __init__(
        self,
        urdf_path,
        start_joint_positions=None,
        base_elements=None,
        end_link_id=None,
    ):
        """
        pinocchio can not using original urdf model
        it will confused the end effector
        the urdf were modified
        and you should not make the DoF exactly same as you want control
        it will ignore arm_base and multiple end effector DoFs.
        """
        self.model = pin.buildModelFromUrdf(urdf_path)
        self.data = self.model.createData()

        if end_link_id is not None:
            self.end_link_id = end_link_id
        else:
            self.end_link_id = self.model.nq

        logger.info(f"end_link_id: {self.end_link_id}")

        self.chain_length = self.model.nq
        if start_joint_positions is None:
            start_joint_positions = np.zeros(self.model.nq)
        else:
            start_joint_positions = self._ensure_start_joint_pos_right(
                start_joint_positions
            )
        assert (
            len(start_joint_positions) == self.chain_length
        ), f"start_joint_pos not same as chain length {len(start_joint_positions)} vs {self.chain_length}"
        self.start_q = np.array(start_joint_positions, dtype=float)
        logger.info(f"chain length: {self.chain_length}")

    def _ensure_start_joint_pos_right(self, initial_joint_positions):
        if initial_joint_positions is None:
            return self.start_q.copy()

        initial_joint_positions = list(initial_joint_positions)
        if len(initial_joint_positions) < self.chain_length:
            initial_joint_positions = [0.0] * (
                self.chain_length - len(initial_joint_positions)
            ) + initial_joint_positions
        elif len(initial_joint_positions) > self.chain_length:
            initial_joint_positions = initial_joint_positions[: self.chain_length]

        return np.array(initial_joint_positions, dtype=float)

    def compute_joint_angles(
        self,
        end_effector_position,
        end_effector_orientation=None,
        initial_joint_positions=None,
        trim_base_link=False,
        max_iter=530,
        dt=1e-2,
        fixed_joint_indices=[0],
    ):
        q = self._ensure_start_joint_pos_right(initial_joint_positions)
        pos = np.array(end_effector_position, dtype=float)
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
                raise ValueError(
                    "end_effector_orientation must be length 3 (euler) or 4 (quat)"
                )

        oMdes = pin.SE3(orientation_matrix, np.array(end_effector_position))

        eps = 1e-4
        IT_MAX = max_iter
        DT = dt
        damp = 1e-6

        i = 0
        while True:
            pin.forwardKinematics(self.model, self.data, q)
            iMd = self.data.oMi[self.end_link_id].actInv(oMdes)

            err = pin.log(iMd).vector

            if norm(err) < eps:
                success = True
                break
            if i >= IT_MAX:
                success = False
                break

            J = pin.computeJointJacobian(self.model, self.data, q, self.end_link_id)
            J = -np.dot(pin.Jlog6(iMd.inverse()), J)

            v = -J.T.dot(solve(J.dot(J.T) + damp * np.eye(6), err))

            q = pin.integrate(self.model, q, v * DT)

            if not i % 80:
                print(f"{i}: err = {[round(x, 6) for x in err.T.tolist()]}")
            i += 1

        if success:
            logger.success("Convergence achieved!")
        else:
            logger.warning(
                "\n"
                "Warning: the iterative algorithm has not reached convergence "
                "to the desired precision"
            )

        # print(f"\nresult: {q}")
        # print(f"\nfinal error: {err.T}")
        # 返回最终的关节角度向量（以列表形式）
        return np.array(q.flatten())
