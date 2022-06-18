from sys_interfaces import *
from time import sleep
import cv2 as cv
import numpy as np


class GameImage:
    window_rect = []

    def __init__(self, window_rect: list, filepath: str, confidence: float):
        self.window_rect = window_rect
        self.image = (cv.imread(filepath, cv.IMREAD_UNCHANGED), confidence)

    def find(self, screenshot: Image) -> list:
        image, confidence = self.image
        threshold = 1 - confidence
        result = cv.matchTemplate(screenshot, image, cv.TM_SQDIFF_NORMED)
        location = np.where(result <= threshold)
        location = list(zip(*location[::-1]))
        rectangle = []
        if location:
            # Gets the last time the image is found
            location = location[-1]
            rectangle = [location[0], location[1], image.shape[1], image.shape[0]]
        return rectangle
