import pyscreenshot as ImageGrab
import cv2
import numpy as np

class ScreenCapture:
    """
    Classe responsável por capturar e processar imagens da tela.
    
    Permite capturar a tela inteira e extrair seções específicas para processamento
    de imagem usando OpenCV.
    """

    def __init__(self):
        """
        Inicializa a classe com uma imagem vazia.
        """
        self.screen_image: ImageGrab.Image = None

    def capture_screen(self) -> None:
        """
        Captura uma imagem da tela inteira e armazena internamente.
        """
        screen_image = ImageGrab.grab()
        self.screen_image = screen_image
    
    def get_screen_section(self, bbox: tuple) -> np.ndarray:
        """
        Extrai uma seção retangular da imagem capturada.
        
        Args:
            bbox: Tupla (x1, y1, x2, y2) definindo as coordenadas do retângulo
            
        Returns:
            Array numpy contendo a imagem da seção no formato BGR
        """
        section = self.screen_image.crop(bbox)
        return cv2.cvtColor(np.array(section), cv2.COLOR_RGB2BGR)