import tkinter as tk

class GUILogger:
    """
    Classe responsável por exibir uma janela flutuante com informações do estado do jogo.
    
    Cria uma janela transparente e sempre visível que exibe mensagens de status
    atualizadas durante a execução do bot.
    """

    def __init__(self):
        """
        Inicializa a janela do logger com as configurações visuais.
        
        Cria uma janela Tkinter com fundo semi-transparente, sem bordas e sempre
        visível, contendo um label para exibir as mensagens.
        """
        root = tk.Tk()
        root.attributes('-topmost', True)
        root.attributes('-alpha', 0.8)
        root.overrideredirect(True)
        root.geometry('300x350+50+50')  
        label = tk.Label(root, 
                        text="...",
                        font=('Arial', 14),
                        bg='black',
                        fg='white',
                        wraplength=280, 
                        justify='left',
                        padx=10,
                        pady=10)
        label.pack(expand=True, fill='both')

        self.root = root 
        self.label = label

    def display(self, message: str) -> None:
        """
        Atualiza o texto exibido na janela.
        
        Args:
            message: String contendo a mensagem a ser exibida
        """
        self.label.config(text=message)
        self.root.update()
