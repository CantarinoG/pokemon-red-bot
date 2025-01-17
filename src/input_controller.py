import subprocess
import time
import pyautogui

class InputController:

    def __init__(self, pattern: list = ['r', 'd', 'l', 'u']):
        self._pattern = pattern
        self._current_index = 0
        
    def _press_key(self, key: str) -> None:
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)

    def press_up(self) -> None:
        self._press_key('up')

    def press_down(self) -> None:
        self._press_key('down')

    def press_left(self) -> None:
        self._press_key('left')

    def press_right(self) -> None:
        self._press_key('right')

    def press_x(self) -> None:
        self._press_key('x')

    def press_z(self) -> None:
        self._press_key('z')

    def focus_window(self, window_name: str) -> bool:
        try:
            subprocess.run(['xdotool', 'search', '--name', window_name, 'windowactivate'], check=True)
            time.sleep(0.5)
            return True
        except:
            return False
        
    def set_pattern(self, pattern: list) -> None:
        self._pattern = pattern

    def press_next_direction(self) -> None:
        direction = self._pattern[self._current_index]
        
        if direction == 'r':
            self.press_right()
        elif direction == 'l':
            self.press_left()
        elif direction == 'u':
            self.press_up()
        elif direction == 'd':
            self.press_down()
            
        self._current_index = (self._current_index + 1) % len(self._pattern)
