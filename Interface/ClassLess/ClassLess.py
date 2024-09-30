from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import ipaddress


from Projet_1.Interface.ClassLess.CLMethodOne import CLMethod_One
from Projet_1.Interface.ClassLess.CLMethodTwo import CLMethod_Two


class EncodageLess(QWidget):
    def __init__(self):
        super().__init__()

        #Layout principal
        self.main_layout = QVBoxLayout(self)

        #création des pages de navigation
        self.tabs = QTabWidget()

        #Ajout des pages
        self.methode_one = CLMethod_One()
        self.methode_two = CLMethod_Two()

        self.tabs.addTab(self.methode_one, "Calcul Adresse")
        self.tabs.addTab(self.methode_two, "Appartenance au réseau")



        self.main_layout.addWidget(self.tabs)
        # # Style général de la fenêtre
        self.setStyleSheet(open("Style/styleLog.css").read())


