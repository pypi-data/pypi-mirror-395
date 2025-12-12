from cams.cam import get_camera_wrapper
import cv2

cam = get_camera_wrapper(cam_type='realsense')
while True:
    a = cam.read()
    cv2.imshow('aa', a)
    cv2.waitKey(1)