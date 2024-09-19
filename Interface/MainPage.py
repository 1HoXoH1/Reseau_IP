from Projet_1.Interface.ClassFull.ClassFull import *
from Projet_1.Interface.ClassLess.ClassLess import *
class PageZero(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Reseau IP')
        self.resize(800, 600)

        #Layout principal
        self.main_layout = QVBoxLayout(self)

        #création des pages de navigation
        self.tabs = QTabWidget()

        #Ajout des pages
        self.full = Encodage()
        self.less = EncodageLess()

        self.tabs.addTab(self.full, "ClassFull")
        self.tabs.addTab(self.less, "ClassLess")


        self.main_layout.addWidget(self.tabs)

if __name__ == '__main__':
    app = QApplication([])
    dashboard = PageZero()
    dashboard.show()
    app.exec_()