import numpy as np
import cv2


def imageMosaic(points, imagePath):
    image = cv2.imread(imagePath)  # 이미지 로드
    img = cv2.rectangle(image, points[0], points[1], (255, 255, 255), -1)
    cv2.imshow("image mosaic", img)
    cv2.waitKey(0)
    return
