import cv2
from realsense_camera import *

rs = RealsenseCamera()

ret, bgr_frame, depth_frame = rs.get_frame_stream()

cv2.imshow("Bgr frame", bgr_frame)
key = cv2.waitKey(0)

