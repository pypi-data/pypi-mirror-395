#!/usr/bin/env python3
import os
import sys
import time
import math
import tempfile
import argparse
import csv
import requests
import numpy as np
from ikpy.chain import Chain
from ikpy.utils import geometry
import matplotlib.pyplot as plt


# ---------- helpers ----------
def download_urdf_try(urls, out_path):
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200 and "<robot" in r.text:
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(r.text)
                print("Downloaded URDF from:", url)
                return out_path
        except Exception:
            pass
    return None


def make_transform_matrix(x, y, z, roll=0.0, pitch=0.0, yaw=0.0):
    r = geometry.rpy_matrix([roll, pitch, yaw])
    T = np.eye(4)
    T[0:3, 0:3] = r[0:3, 0:3]
    T[0:3, 3] = [x, y, z]
    return T


def smooth_trajectory(traj, upsample=5):
    out = []
    for i in range(len(traj) - 1):
        a = traj[i]
        b = traj[i + 1]
        for t in np.linspace(0, 1, upsample, endpoint=False):
            out.append(a * (1 - t) + b * t)
    out.append(traj[-1])
    return out


# ---------- generate a safe trajectory inside typical PiPER workspace ----------
def generate_helix_trajectory(
    center=(0.25, 0.0, 0.20), radius=0.08, height=0.05, turns=1.5, points=80
):
    cx, cy, cz = center
    t = np.linspace(0, 2 * math.pi * turns, points)
    traj = []
    for i, ti in enumerate(t):
        x = cx + radius * math.cos(ti)
        y = cy + radius * math.sin(ti)
        z = cz + (height * (ti / (2 * math.pi * turns))) - height / 2
        traj.append(np.array([x, y, z], dtype=float))
    return traj


# ---------- main pipeline ----------
def run(urdf_path=None, ros_mode=False, save_csv="joint_trajectory.csv"):
    # find or download URDF
    if urdf_path is None or not os.path.exists(urdf_path):
        print(
            "No local URDF provided or not found. Trying to download common PiPER URDF from GitHub..."
        )
        tmp = tempfile.gettempdir()
        dst = os.path.join(tmp, "piper_description.urdf")
        candidate_urls = [
            "https://raw.githubusercontent.com/agilexrobotics/piper_ros/noetic/piper_description/urdf/piper_description.urdf",
            "https://raw.githubusercontent.com/agilexrobotics/piper_ros/noetic/piper_description/urdf/piper_description_old.urdf",
            "https://raw.githubusercontent.com/agilexrobotics/piper_ros/master/piper_description/urdf/piper_description.urdf",
        ]
        got = download_urdf_try(candidate_urls, dst)
        if got is None:
            print(
                "Couldn't download URDF automatically. Please clone https://github.com/agilexrobotics/piper_ros and pass the path to piper_description.urdf via --urdf."
            )
            print("See repository: https://github.com/agilexrobotics/piper_ros")
            sys.exit(1)
        urdf_path = got
    print("Using URDF:", urdf_path)

    # build ikpy chain
    chain = Chain.from_urdf_file(urdf_path)
    print("Chain built. Number of links:", len(chain.links))
    # active joints mask is often needed if ikpy treats links differently.
    # We'll rely on chain.inverse_kinematics_frame which returns full vector (including fixed joints).

    # generate target trajectory and upsample for smooth joint motion
    cart_traj = generate_helix_trajectory(
        center=(0.25, 0.0, 0.20), radius=0.08, height=0.06, turns=1.2, points=50
    )
    cart_traj = smooth_trajectory(cart_traj, upsample=4)
    print("Cartesian trajectory waypoints:", len(cart_traj))

    # initial joint guess: zeros or chain.resting_position
    q_curr = np.array(
        chain.inverse_kinematics_frame(make_transform_matrix(*cart_traj[0])),
        dtype=float,
    )
    joint_trajectory = []

    # solve IK for each waypoint
    for p in cart_traj:
        target = make_transform_matrix(p[0], p[1], p[2])
        q_sol = chain.inverse_kinematics_frame(target, initial_position=q_curr)
        # ikpy returns an array length = n_links (including fixed). We keep it as-is; the actuated joints are the non-fixed ones.
        joint_trajectory.append(np.array(q_sol))
        q_curr = q_sol

    joint_trajectory = np.array(joint_trajectory)  # (N_waypoints, n_links)
    print("Computed joint trajectory shape:", joint_trajectory.shape)

    # save CSV (each row = waypoint, columns = joint values)
    header = [f"joint_{i}" for i in range(joint_trajectory.shape[1])]
    with open(save_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for row in joint_trajectory:
            w.writerow(row.tolist())
    print("Saved joint trajectory to:", save_csv)

    # quick plot of end-effector path (cartesian)
    cart = np.array(cart_traj)
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(cart[:, 0], cart[:, 1], cart[:, 2], label="EE path")
    ax.scatter(cart[0, 0], cart[0, 1], cart[0, 2], color="green", label="start")
    ax.scatter(cart[-1, 0], cart[-1, 1], cart[-1, 2], color="red", label="end")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.legend()
    plt.tight_layout()
    plt.show()

    # ---------- playback options ----------
    # 1) Dry-run printed playback (safe)
    print("\n--- Dry-run: printing first 8 joint waypoints ---")
    for i, row in enumerate(joint_trajectory[:8]):
        print(f"{i:03d}:", np.round(row, 4))
        time.sleep(0.05)

    # 2) If ROS environment present: publish joint_states to /joint_states (works with piper_ros node)
    if ros_mode:
        try:
            import rospy
            from sensor_msgs.msg import JointState

            rospy.init_node("piper_ikpy_player", anonymous=True)
            pub = rospy.Publisher("/joint_states", JointState, queue_size=1)
            js = JointState()
            # set joint names if known by your system; adjust names to match piper's joints if needed.
            js.name = [
                "joint_1",
                "joint_2",
                "joint_3",
                "joint_4",
                "joint_5",
                "joint_6",
                "joint_7",
            ][: joint_trajectory.shape[1]]
            rate_hz = 20
            rate = rospy.Rate(rate_hz)
            print(
                "Publishing joint_states to /joint_states. Make sure piper_ctrl_single_node.py is running and enabled."
            )
            for q in joint_trajectory:
                js.header.stamp = rospy.Time.now()
                js.position = q.tolist()
                pub.publish(js)
                rate.sleep()
            print("ROS playback done.")
        except Exception as e:
            print("ROS mode requested but failed:", e)
            print("Make sure you run this in a ROS-enabled Python environment (rospy).")

    # 3) Placeholder: direct piper_sdk send (you can adapt to your installed SDK)
    # The piper_sdk repo and demos show how to enable and send position commands; for safety, I leave this as a clearly marked area to adapt.
    print(
        "\nIf you want to send joint targets via piper_sdk, adapt the snippet below to your SDK version."
    )
    print(
        "See piper_sdk README and the piper_ros repo for examples and URDF. If using piper_ctrl_single_node (ROS), prefer ROS playback. "
    )
    # Example conceptual pseudocode (do NOT run as-is):
    print(
        """
# from piper_sdk import C_PiperInterface
# piper = C_PiperInterface(...)
# piper.ConnectPort()
# for q in joint_trajectory:
#     piper.send_joint_position_cmd(q)   # adapt to the exact method in your piper_sdk/demo
# piper.Disconnect()
    """
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--urdf",
        type=str,
        default=None,
        help="path to piper_description.urdf (optional)",
    )
    ap.add_argument(
        "--ros",
        action="store_true",
        help="publish to ROS /joint_states (requires rospy and running piper ROS node)",
    )
    ap.add_argument(
        "--out", type=str, default="joint_trajectory.csv", help="csv output path"
    )
    args = ap.parse_args()
    run(urdf_path=args.urdf, ros_mode=args.ros, save_csv=args.out)
