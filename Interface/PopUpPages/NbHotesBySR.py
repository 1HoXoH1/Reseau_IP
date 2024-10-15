from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt

class HotesBySR(QWidget):
    # Signal personnalisé qui transmet la valeur maximale à la première page
    max_value_signal = pyqtSignal(int)

    def __init__(self, NbSr):
        super().__init__()
        self.max_value = 0
        self.NbSr = NbSr
        self.input_fields = []  # Liste pour stocker les références des champs QLineEdit
        self.initUI()

        self.setStyleSheet(open("Style/styleLog.css").read())

    def initUI(self):
        main_layout = QVBoxLayout()  # Layout principal pour la fenêtre
        main_layout.setAlignment(Qt.AlignTop)  # Aligner tous les éléments en haut

        # Créer une zone de défilement (scrollable)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Redimensionner automatiquement le contenu

        # Créer un widget pour contenir tous les QLabel et QLineEdit
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)  # Layout pour les champs d'entrée

        self.create_layout(scroll_layout)  # Ajoute les champs au scroll_layout

        # Définir le widget contenant les labels et input comme contenu de la zone de défilement
        scroll_area.setWidget(scroll_widget)

        # Ajouter la zone de défilement au layout principal
        main_layout.addWidget(scroll_area)

        # Bouton pour récupérer la valeur maximale et fermer la page
        btn_max = QPushButton("Récupérer les valeurs et fermer", self)
        btn_max.clicked.connect(self.take_max_number)
        main_layout.addWidget(btn_max)

        self.setWindowTitle("Nombre d'hôtes par sous-réseau")
        self.resize(600, 600)  # Taille fixe pour la fenêtre
        self.setLayout(main_layout)  # Définir le layout principal pour la fenêtre

    def create_layout(self, layout):
        """Crée dynamiquement les champs d'entrée basés sur NbSr"""
        for i in range(self.NbSr):
            label = QLabel(f"Nombre d'hôtes par sous-réseau, réseau {i + 1}:", self)
            input_field = QLineEdit(self)
            layout.addWidget(label)
            layout.addWidget(input_field)

            # Ajouter le champ QLineEdit dans la liste pour une utilisation ultérieure
            self.input_fields.append(input_field)

    def take_max_number(self):
        try:
            values = [int(field.text()) for field in self.input_fields if field.text().isdigit()]
            if values:  # Si la liste n'est pas vide
                self.max_value = max(values)

                # Émettre le signal avec la valeur maximale
                self.max_value_signal.emit(self.max_value)
                self.close()
            else:
                QMessageBox.warning(self, "Erreur", "Aucune valeur valide n'a été saisie.")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des nombres valides.")
