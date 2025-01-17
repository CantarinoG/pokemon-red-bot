import subprocess
import time
import pyautogui

class InputController:
    """
    Classe responsável por controlar as entradas do teclado e gerenciar o foco da janela.
    
    Permite simular pressionamentos de teclas e seguir um padrão de movimentação definido.
    """

    def __init__(self, pattern: list = ['r', 'd', 'l', 'u']):
        """
        Inicializa o controlador com um padrão de movimentação.
        
        Args:
            pattern: Lista de direções definindo o padrão de movimento ('r', 'l', 'u', 'd' para 'right', 'left', 'up' e 'down', respectivamente).
        """
        self._pattern = pattern
        self._current_index = 0
        
    def _press_key(self, key: str) -> None:
        """
        Método interno para simular o pressionamento de uma tecla.

        Se uma tecla for pressionada muito rapidamente, pode ocorrer do emulador não reconhecer. Portanto, ao invés de usar um input para apenas apertar o botão,
        é utilizado primeiro um input para apertar o botão e depois para soltar. O pyautogui adiciona um intervalo de 0.1 segundos por padrão para todos os comandos,
        dessa forma, o botão fica sendo pressionado por 0.1 segundos, que é tempo o suficiente para o emulador interpretar corretamente como uma pressionada de botão.
        
        Args:
            key: String com o nome da tecla a ser pressionada
        """
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)

    def press_up(self) -> None:
        """Simula o pressionamento da tecla para cima."""
        self._press_key('up')

    def press_down(self) -> None:
        """Simula o pressionamento da tecla para baixo."""
        self._press_key('down')

    def press_left(self) -> None:
        """Simula o pressionamento da tecla para esquerda."""
        self._press_key('left')

    def press_right(self) -> None:
        """Simula o pressionamento da tecla para direita."""
        self._press_key('right')

    def press_x(self) -> None:
        """Simula o pressionamento da tecla X."""
        self._press_key('x')

    def press_z(self) -> None:
        """Simula o pressionamento da tecla Z."""
        self._press_key('z')

    def focus_window(self, window_name: str) -> bool:
        """
        Tenta focar uma janela específica pelo nome.
        
        Args:
            window_name: Nome da janela a ser focada
            
        Returns:
            bool: True se conseguiu focar, False caso contrário
        """
        try:
            subprocess.run(['xdotool', 'search', '--name', window_name, 'windowactivate'], check=True)
            time.sleep(0.5)
            return True
        except:
            return False
        
    def set_pattern(self, pattern: list) -> None:
        """
        Define um novo padrão de movimentação.
        
        Args:
            pattern: Nova lista de direções a ser usada
        """
        self._pattern = pattern

    def press_next_direction(self) -> None:
        """
        Pressiona a próxima tecla direcional seguindo o padrão definido.
        Avança o índice do padrão ciclicamente.
        """
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
