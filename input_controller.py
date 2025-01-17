import subprocess
import time
import pyautogui

class InputController:

    def __init__(self, pattern: list = ['r', 'd', 'l', 'u']):
        pyautogui.PAUSE = 0
        self.pattern = pattern
        self.current_index = 0
        
    def _press_key(self, key: str):
        pyautogui.keyDown(key)
        time.sleep(0.1)
        pyautogui.keyUp(key)

    def press_up(self):
        self._press_key('up')

    def press_down(self):
        self._press_key('down')

    def press_left(self):
        self._press_key('left')

    def press_right(self):
        self._press_key('right')

    def press_x(self):
        self._press_key('x')

    def press_z(self):
        self._press_key('z')

    def focus_window(self, window_name: str):
        try:
            subprocess.run(['xdotool', 'search', '--name', window_name, 'windowactivate'], check=True)
            return True
        except:
            return False
        
    def set_pattern(self, pattern: list):
        self.pattern = pattern

    def press_next_direction(self):
        direction = self.pattern[self.current_index]
        
        if direction == 'r':
            self.press_right()
        elif direction == 'l':
            self.press_left()
        elif direction == 'u':
            self.press_up()
        elif direction == 'd':
            self.press_down()
            
        self.current_index = (self.current_index + 1) % len(self.pattern)
