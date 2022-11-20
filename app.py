import json
import tkinter as tk
from screen.Accueil import MainScreen
from screen.ChoixLangue import EcranChoixDeLangue
from version_one import wikiRequest, getPageTitle, getHyperLinks, pagination


class windows(tk.Tk):
    windowWidth = 1080
    windowHeight = 600
    currentFrame = None
    round = 1

    page = 1
    startPage = wikiRequest()
    currentPage = startPage
    endPage = wikiRequest()
    translation = 'fr'

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()

        self.centerX = int(self.screenWidth / 2 - self.windowWidth / 2)
        self.centerY = int(self.screenHeight / 2 - self.windowHeight / 2)

        # Adding a title to the window
        self.wm_title("TP-python")

        self.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, self.centerX,
                                           self.centerY))  # set the size and pos of the windows
        self.defaultSize = self.geometry()

        # creating a frame and assigning it to container
        self.container = tk.Frame(self)
        # specifying the region where the frame is packed in root
        self.container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Using a method to switch frames
        self.show_frame(EcranChoixDeLangue)

    def HomeFrame(self):
        self.show_frame(MainScreen)

    def show_frame(self, cont):
        self.currentFrame = cont
        frame = self.currentFrame(self.container, self, self.translate)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def updateRound(self):
        self.round += 1
        self.refreshFrame()

    def refreshFrame(self):
        self.show_frame(self.currentFrame)

    def getStartPage(self):
        return getPageTitle(self.startPage)

    def getCurrentPage(self):
        return getPageTitle(self.currentPage)

    def getEndPage(self):
        return getPageTitle(self.endPage)

    def getRound(self):
        return self.round

    def getItemsList(self):
        return [(idx + 1, page.get('title')) for idx, page in enumerate(getHyperLinks(self.currentPage))]

    def getPaginateList(self):
        return pagination(self.getItemsList(), self.page, 20)

    def changePage(self, page):
        self.page = page
        self.refreshFrame()

    def switchPage(self, newPage):
        self.currentPage = newPage
        self.updateRound()
        self.refreshFrame()

    def translate(self, key):
        file = open('translation/{}.json'.format(self.translation), encoding="utf-8")
        data = json.load(file)
        file.close()
        if key in data:
            return data[key]
        return key

    def setGameTranslation(self, translation):
        self.translation = translation


if __name__ == "__main__":
    app = windows()
    app.mainloop()
