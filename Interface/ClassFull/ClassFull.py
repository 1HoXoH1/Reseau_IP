from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import ipaddress

from Projet_1.Interface.ClassFull.MethodeOne import Methode_One
from Projet_1.Interface.ClassFull.MethodeThree import Methode_Three
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
        self.methode_three = Methode_Three()

        self.tabs.addTab(self.methode_one, "Information réseau")
        self.tabs.addTab(self.methode_two, "Appartenance réseau")
        self.tabs.addTab(self.methode_three, "Découpe réseau")


        self.main_layout.addWidget(self.tabs)

