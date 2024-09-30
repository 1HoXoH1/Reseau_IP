from Projet_1.Interface.ClassFull.ClassFull import *
from Projet_1.Interface.ClassLess.ClassLess import *


class PageZero(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Reseau IP')

        self.resize(1200, 800)
        #self.showFullScreen()

        # Layout principal
        self.main_layout = QVBoxLayout(self)

        # création des pages de navigation
        self.tabs = QTabWidget()

        # Ajout des pages
        self.full = Encodage()
        self.less = EncodageLess()

        self.tabs.addTab(self.full, "ClassFull")
        self.tabs.addTab(self.less, "ClassLess")

        self.main_layout.addWidget(self.tabs)
        # # Style général de la fenêtre
        self.setStyleSheet(open("Style/styleLog.css").read())




