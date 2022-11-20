import tkinter as tk

translation = ["fr", "en", "es"]

class EcranChoixDeLangue(tk.Frame):
    def __init__(self, parent, controller, translate):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        titleGame = tk.Label(self, text=translate('CHOICE_YOUR_LANGUAGE'))
        titleGame.pack(padx=30, pady=30)

        gridPagesFrame = tk.Frame(self)
        gridPagesFrame.pack(expand=True, anchor=tk.CENTER, padx=30, pady=30)

        for idx, data in enumerate(translation):
            buttons = tk.Button(gridPagesFrame, text=translate(data.upper()), command=lambda data=data: self.startGame(data))
            buttons.grid(row=(idx // 9),
                         column=(idx % 9),
                         padx=10, pady=10)

    def startGame(self, data):
        self.controller.setGameTranslation(data)
        self.controller.HomeFrame()
