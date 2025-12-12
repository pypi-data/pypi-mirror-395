import cv2
import numpy as np

try:
    import pyrealsense2 as rs

    _HAS_RS = True
except ImportError:
    _HAS_RS = False

from .base import CameraBase


class RealSenseCamera(CameraBase):
    def __init__(self, width=640, height=480, fps=30, mode="rgb"):
        if not _HAS_RS:
            raise ImportError("pyrealsense2 is not installed")
        self.width = width
        self.height = height
        self.fps = fps
        self.mode = mode

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        if mode in ["rgb", "gray"]:
            self.config.enable_stream(
                rs.stream.color,
                width,
                height,
                rs.format.bgr8,
                fps,
                # rs.stream.color, 640, 480, rs.format.bgr8, 30
                # rs.stream.color, 1280, 720, rs.format.bgr8, 10
            )
        elif mode == "depth" or mode == "rgb":
            self.config.enable_stream(
                rs.stream.depth, width, height, rs.format.z16, fps
            )
        # print(width, height, fps)
        self.pipeline.start(self.config)

    def read(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if self.mode == "rgb":
            if not color_frame:
                return None
            return np.asanyarray(color_frame.get_data())
        elif self.mode == "gray":
            if not color_frame:
                return None
            color_image = np.asanyarray(color_frame.get_data())
            return cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        elif self.mode == "depth":
            if not depth_frame:
                return None
            return np.asanyarray(depth_frame.get_data())

    def release(self):
        self.pipeline.stop()


class USBCamera(CameraBase):
    def __init__(self, index=0, width=640, height=480, fps=30, mode="rgb"):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.mode = mode

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        if self.mode == "rgb":
            return frame
        elif self.mode == "gray":
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif self.mode == "depth":
            raise ValueError("USB camera does not support depth mode")

    def release(self):
        self.cap.release()


def get_camera_wrapper(cam_type="usb", **kwargs):
    """
    Factory function to get the appropriate camera instance.
    cam_type: 'usb' or 'realsense'
    kwargs: width, height, fps, mode, index (for USB)
    """
    if cam_type == "realsense":
        return RealSenseCamera(**kwargs)
    elif cam_type == "usb":
        return USBCamera(**kwargs)
    else:
        raise ValueError(f"Unsupported camera type: {cam_type}")


if __name__ == "__main__":
    cam = get_camera_wrapper(
        cam_type="realsense", mode="rgb", width=640, height=480, fps=30
    )
    try:
        while True:
            frame = cam.read()
            if frame is None:
                continue
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()
