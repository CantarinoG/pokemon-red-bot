import tkinter as tk

class GUILogger:

    def __init__(self):
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
        self.label.config(text=message)
        self.root.update()
