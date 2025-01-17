import numpy as np
import os
import cv2

class TemplateMatcher:
    """
    Classe responsável por fazer correspondência de templates em imagens.
    
    Permite encontrar a melhor correspondência de uma imagem template em uma imagem maior,
    bem como encontrar múltiplas correspondências ordenadas por similaridade ou posição.
    """

    def get_best_match_from_folder(self, path: str, image: np.ndarray) -> dict:
        """
        Encontra a melhor correspondência entre uma imagem e os templates em uma pasta.
        
        Args:
            path: Caminho para a pasta contendo os templates em formato PNG
            image: Array numpy contendo a imagem onde buscar correspondências
            
        Returns:
            Dicionário contendo o nome do template com melhor correspondência e sua diferença
        """
        best_match = {"name": None, "difference": float("inf")}
        image_files = [f for f in os.listdir(path) if f.endswith(".png")]
        
        for image_file in image_files:
            template = cv2.imread(os.path.join(path, image_file))
            gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray_template, 254, 255, cv2.THRESH_BINARY_INV)
            result = cv2.matchTemplate(
                image,
                template,
                cv2.TM_SQDIFF_NORMED,
                mask=mask
            )
            min_val, _, _, _ = cv2.minMaxLoc(result)
            
            if min_val < best_match["difference"]:
                name = os.path.splitext(image_file)[0]
                best_match = {"name": name, "difference": min_val}
        
        return best_match
    
    def get_n_best_matches_from_folder(self, n: int, path: str, image: np.ndarray) -> list:
        """
        Encontra as N melhores correspondências entre uma imagem e os templates em uma pasta.
        
        Args:
            n: Número de melhores correspondências a retornar
            path: Caminho para a pasta contendo os templates em formato PNG
            image: Array numpy contendo a imagem onde buscar correspondências
            
        Returns:
            Lista com os N templates de melhor correspondência, ordenados por posição vertical,
            cada um contendo nome, diferença e posição Y
        """
        matches = []
        image_files = [f for f in os.listdir(path) if f.endswith(".png")]
        
        for image_file in image_files:
            template = cv2.imread(os.path.join(path, image_file))
            gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray_template, 254, 255, cv2.THRESH_BINARY_INV)
            result = cv2.matchTemplate(
                image,
                template,
                cv2.TM_SQDIFF_NORMED,
                mask=mask
            )
            min_val, _, min_loc, _ = cv2.minMaxLoc(result)
            name = os.path.splitext(image_file)[0]
            matches.append({"name": name, "difference": min_val, "y_pos": min_loc[1]})
        
        matches.sort(key=lambda x: x["difference"])
        top_matches = matches[:n]
        
        return sorted(top_matches, key=lambda x: x["y_pos"])

    def get_match_value(self, template_path: str, image: np.ndarray) -> dict:
        """
        Calcula o valor de correspondência entre uma imagem template e uma imagem maior.
        
        Args:
            template_path: Caminho para o arquivo de template
            image: Array numpy contendo a imagem onde buscar correspondência
            
        Returns:
            Dicionário contendo o nome do template e o valor de diferença encontrado
        """
        template_img = cv2.imread(template_path)
        result = cv2.matchTemplate(
            image,
            template_img,
            cv2.TM_SQDIFF_NORMED
        )
        min_val, _, _, _ = cv2.minMaxLoc(result)
        name = os.path.splitext(os.path.basename(template_path))[0]
        return {"name": name, "difference": min_val}