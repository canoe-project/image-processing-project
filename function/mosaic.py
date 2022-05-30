import numpy as np
import cv2


def imageMosaic(points, image):
    return cv2.rectangle(image, points[0], points[1], (255, 255, 255), -1)
