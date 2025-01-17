import pyscreenshot as ImageGrab
import cv2
import numpy as np

class ScreenCapture:

    def __init__(self):
        self.screen_image: ImageGrab.Image = None

    def capture_screen(self) -> None:
        screen_image = ImageGrab.grab()
        self.screen_image = screen_image
    
    def get_screen_section(self, bbox: tuple) -> np.ndarray:
        section = self.screen_image.crop(bbox)
        return cv2.cvtColor(np.array(section), cv2.COLOR_RGB2BGR)