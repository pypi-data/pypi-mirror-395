import os
import glob
import cv2
import torch
import numpy as np
# import faulthandler
# faulthandler.enable() 

from depth_anything_3.api import DepthAnything3


class DepthPredictor:
    def __init__(self, model_name="depth-anything/DA3METRIC-LARGE", device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = torch.device(device)
        self.model = DepthAnything3.from_pretrained(model_name).to(self.device)

    def _infer_single(self, img_bgr: np.ndarray):
        """Infer from a single BGR numpy image."""
        prediction = self.model.inference([img_bgr])
        return prediction

    def predict_image(self, img_bgr: np.ndarray, vis=False):
        pred = self._infer_single(img_bgr)

        rgb = pred.processed_images[0]
        depth = pred.depth[0]

        if vis:
            self._visualize_pair(rgb, depth)

        return {
            "image": rgb,
            "depth": depth,
            "conf": pred.conf[0],
            "extrinsics": pred.extrinsics,
            "intrinsics": pred.intrinsics,
        }

    def predict_dir(self, image_dir, vis=False):
        images = sorted(glob.glob(os.path.join(image_dir, "*.png"))) + sorted(
            glob.glob(os.path.join(image_dir, "*.jpg"))
        )

        out_images = []
        out_depths = []
        out_conf = []

        for path in images:
            img = cv2.imread(path)
            pred = self._infer_single(img)
            rgb = pred.processed_images[0]
            depth = pred.depth[0]
            conf = pred.conf[0]

            if vis:
                self._visualize_pair(rgb, depth, wait=0)

            out_images.append(rgb)
            out_depths.append(depth)
            out_conf.append(conf)

        return {
            "images": np.stack(out_images),
            "depth": np.stack(out_depths),
            "conf": np.stack(out_conf),
            "extrinsics": pred.extrinsics,
            "intrinsics": pred.intrinsics,
        }

    def predict_video(self, video_path, vis=True):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        results = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            pred = self._infer_single(frame)
            rgb = pred.processed_images[0]
            depth = pred.depth[0]

            if vis:
                self._visualize_pair(rgb, depth, wait=1)

            results.append(
                {
                    "image": rgb,
                    "depth": depth,
                    # "conf": pred.conf[0],
                }
            )

        cap.release()
        return results

    def _visualize_pair(self, rgb, depth, wait=1):
        # Ensure BGR for OpenCV
        rgb_bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        # Normalized depth map
        depth_norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
        depth_norm = depth_norm.astype(np.uint8)
        depth_color = cv2.applyColorMap(depth_norm, cv2.COLORMAP_INFERNO)

        pair = np.hstack([rgb_bgr, depth_color])

        cv2.imshow("RGB | Depth", pair)
        cv2.waitKey(wait)


if __name__ == "__main__":
    dp = DepthPredictor()

    # From image directory
    out = dp.predict_dir("assets/examples/SOH", vis=True)
    print(out["images"].shape)
    print(out["depth"].shape)

    # From single numpy image
    # img = cv2.imread("example.png")
    # dp.predict_image(img, vis=True)

    # From video
    # dp.predict_video("test.mp4", vis=True)
