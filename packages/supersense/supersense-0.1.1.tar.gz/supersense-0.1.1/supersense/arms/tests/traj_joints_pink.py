import numpy as np
from scipy.spatial.transform import Rotation as R

import pinocchio as pin
from pink import Configuration, Task, solve_ik
from pink.tasks import FrameTask


class RobotIK_Pink:
    def __init__(
        self,
        urdf_path: str,
        start_joint_positions=None,
        base_elements=["world"],
        end_link: str = None,
    ):

        # Load model
        self.model = pin.buildModelFromUrdf(urdf_path)
        self.data = self.model.createData()

        # Default initial joint positions
        if start_joint_positions is None:
            start_joint_positions = np.zeros(self.model.nq)
        self.start_q = np.array(start_joint_positions)

        # If user does not explicitly give end-effector link → auto-select last link
        if end_link is None:
            end_link = self.model.names[-1]

        self.end_link = end_link
        self.frame_id = self.model.getFrameId(end_link)

        # Pink requires a "task" to match a target pose
        frame_name = self.model.frames[self.frame_id].name
        self.task = FrameTask(
            frame=frame_name,  # ← string name of the frame
            position_cost=1.0,  # or [1.0, 1.0, 1.0] for isotropic
            orientation_cost=1.0,  # or [0.1, 0.1, 0.1] if you care less about orientation
            lm_damping=0.0,  # optional, default is fine
            gain=1.0,  # optional, default 1.0 = no filtering
        )

        self.configuration = Configuration(
            self.model,  # your pin.Model
            self.data,  # usually the same as model if no separate collision
            # visual_model,  # for visualization (Meshcat, Gepetto, etc.)
            q=pin.neutral(self.model),
        )

    def compute_joint_angles(
        self,
        end_effector_position,
        end_effector_orientation=None,
        initial_joint_positions=None,
        trim_base_link=False,
    ):

        if initial_joint_positions is None:
            q0 = self.start_q.copy()
        else:
            q0 = np.array(initial_joint_positions)
            if len(q0) < self.model.nq:
                q0 = np.pad(q0, (self.model.nq - len(q0), 0), "constant")
            q0 = q0[: self.model.nq]

        # Orientation handling
        if end_effector_orientation is None:
            rot = R.from_euler("xyz", [0, 0, 0]).as_matrix()
        else:
            if len(end_effector_orientation) == 3:
                rot = R.from_euler("xyz", end_effector_orientation).as_matrix()
            else:
                rot = R.from_quat(end_effector_orientation).as_matrix()

        # Compose target SE3
        target = pin.SE3(rot, np.array(end_effector_position))

        # Update IK target
        self.task.set_target(target)

        # Solve IK
        # result = solve_ik(
        #     self.model,
        #     self.task,
        #     q0,
        #     dt=1.0,  # stable optimization step
        #     max_iters=20,  # adjustable
        #     tol=1e-4,
        # )
        result = solve_ik(
            configuration=self.configuration,  # or whatever your Configuration object is called
            tasks=[self.task],  # or your list of tasks
            dt=0.001,  # pick one reasonable value, e.g. 0.005 or 0.001
            solver="osqp",  # or "quadprog" if you prefer
        )
        # print(result)
        # q_sol = result.tolist()
        q_sol = result

        if trim_base_link:
            return q_sol[1:]

        return q_sol
