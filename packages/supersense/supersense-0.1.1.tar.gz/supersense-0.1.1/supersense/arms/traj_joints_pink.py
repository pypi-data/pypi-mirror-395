import numpy as np
import pinocchio as pin
import qpsolvers
import pink
from pink.tasks import FrameTask
from scipy.spatial.transform import Rotation as R
from loguru import logger
from robot_descriptions.loaders.pinocchio import load_robot_description


"""
using robot_description for piper, ur5, etc
"""


class RobotIK:
    def __init__(
        self,
        urdf_path_or_type="piper_description",
        start_joint_positions=None,
        base_elements=None,
        end_link_name=None,
    ):
        try:
            self.robot = load_robot_description(urdf_path_or_type)
            self.model = self.robot.model
            self.data = self.robot.data
        except Exception as e:
            logger.warning(
                f"failed to load robot description {urdf_path_or_type}: {e}, try loading as urdf_file"
            )

            self.model = pin.buildModelFromUrdf(urdf_path_or_type)
            self.data = pin.Data(self.model)

        self.lower = self.model.lowerPositionLimit
        self.upper = self.model.upperPositionLimit
        self.q0 = (
            start_joint_positions
            if start_joint_positions is not None
            else pin.neutral(self.model)
        )
        self.end_link_name = (
            end_link_name if end_link_name is not None else self.model.names[-1]
        )
        self.end_joint_id = self.model.getJointId(self.end_link_name)
        self.end_frame_id = self.model.getFrameId(self.end_link_name)
        self.frame_task = FrameTask(
            self.end_link_name, [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]
        )
        self.default_random_start_pos = self._random_q().tolist()

    def remap_traj_to_base(self, traj_ee):
        """
        note, return traj format exactly same as input: x,y,z,qx,qy,qz,qw
        """
        return self._convert_traj_ee_to_base(
            self.model, self.data, self.q0, self.end_link_name, traj_ee
        )

    def _convert_traj_ee_to_base(self, model, data, q0, framename, traj_ee0):
        """
        q0 can be 0, but sometimes it has some default angle for most arms.
        if so, just send it in, otherwise use 0.

        return traj quaternion order is qx, qy, qz, qw
        """
        fid = model.getFrameId(framename)
        pin.forwardKinematics(model, data, q0)
        pin.updateFramePlacement(model, data, fid)
        # ee0 real zero point to base
        base_T_ee0 = data.oMf[fid]

        traj_base = []
        for pq in traj_ee0:
            p = pq[0:3]  # xyz
            q = pq[3:7]  # qx,qy,qz,qw
            # mapping each traj to relative to base
            quat = pin.Quaternion(q[3], q[0], q[1], q[2])
            T_ee0 = pin.SE3(quat.toRotationMatrix(), np.array(p))
            T_base = base_T_ee0 * T_ee0
            pos = T_base.translation
            q = pin.Quaternion(T_base.rotation)
            traj_base.append([pos[0], pos[1], pos[2], q.x, q.y, q.z, q.w])
        return np.array(traj_base)

    def _random_q(self):
        return np.array(
            [
                np.random.uniform(self.lower[i], self.upper[i])
                for i in range(self.model.nq)
            ]
        )

    def compute_joint_angles(
        self,
        end_effector_position,
        end_effector_orientation=None,
        initial_joint_positions=None,
        trim_base_link=False,
        max_iter=530,
        dt=1e-2,
        fixed_joint_indices=[0],
        verbose=False,
        convert_ee_to_base=False,
    ):
        if initial_joint_positions is None:
            q_init = self._random_q()
            pin.forwardKinematics(self.model, self.data, q_init)
        else:
            q_init = np.array(initial_joint_positions)

        target = pin.SE3.Identity()
        target.translation = np.array(end_effector_position)

        if end_effector_orientation is not None:
            if len(end_effector_orientation) == 3:
                logger.warning(
                    f"euler angle not supported well, better using quaternion!"
                )
                orientation_matrix = R.from_euler(
                    "xyz", end_effector_orientation
                ).as_matrix()
            elif len(end_effector_orientation) == 4:
                orientation_matrix = R.from_quat(end_effector_orientation).as_matrix()
            else:
                raise ValueError(
                    "end_effector_orientation must be length 3 (euler) or 4 (quat)"
                )
            target.rotation = orientation_matrix

        configuration = pink.Configuration(self.model, self.data, q_init)
        self.frame_task.set_target(target)

        solver = (
            "daqp"
            if "daqp" in qpsolvers.available_solvers
            else qpsolvers.available_solvers[0]
        )
        solver = "clarabel"

        for i in range(max_iter):
            error_norm = np.linalg.norm(self.frame_task.compute_error(configuration))
            if verbose and i % 80 == 0:
                logger.info(f"error={i}: {error_norm}")
            if error_norm < 1e-4:
                if verbose:
                    logger.success(f"converged with: {error_norm} at: {i} step.")
                break

            dv = pink.solve_ik(
                configuration,
                tasks=[self.frame_task],
                dt=dt,
                damping=1e-8,
                solver=solver,
            )

            q_next = pin.integrate(self.model, configuration.q, dv * dt)
            q_next = np.clip(q_next, self.lower, self.upper)
            configuration = pink.Configuration(self.model, self.data, q_next)
            pin.updateFramePlacements(self.model, self.data)

        return configuration.q.tolist()
