from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import ipaddress

from Projet_1.Interface.ClassFull.MethodeOne import Methode_One
from Projet_1.Interface.ClassFull.MethodeTwo import Methode_Two


class Encodage(QWidget):
    def __init__(self):
        super().__init__()

        #Layout principal
        self.main_layout = QVBoxLayout(self)

        #création des pages de navigation
        self.tabs = QTabWidget()

        #Ajout des pages
        self.methode_one = Methode_One()
        self.methode_two = Methode_Two()

        self.tabs.addTab(self.methode_one, "Classique")
        self.tabs.addTab(self.methode_two, "Complexe")


        self.main_layout.addWidget(self.tabs)

