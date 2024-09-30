import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
import sys
from PyQt5 import Qt
from Projet_1.Database.DataBase import Database



class PageInscription(QWidget):
    def __init__(self):
        super().__init__()

        #appel db
        self.db = Database()
        self.db.get_data()

        #appel login
        self.log = None


        self.setWindowTitle('Inscription')
        self.resize(600, 600)

        layout = QVBoxLayout()
        layout.setSpacing(20)  # Espace entre les widgets

        # Titre
        self.label_title = QLabel("Créer un compte")
        layout.addWidget(self.label_title)

        # Label et champ pour le nom utilisation
        self.label_username = QLabel("Nom d'utilisateur:")
        self.input_username = QLineEdit(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        # Label et champ pour l'e-mail
        self.label_email = QLabel("E-mail:")
        self.input_email = QLineEdit(self)
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)

        # Label et champ pour le mot de passe
        self.label_password = QLabel("Mot de passe:")
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)  # Masquer le mot de passe
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        # Bouton pour créer un compte
        self.btn_create = QPushButton("Créer", self)
        self.btn_create.clicked.connect(self.create_account)
        layout.addWidget(self.btn_create)

        # Bouton pour revenir à la page précédente
        self.btn_back = QPushButton("Retour", self)
        self.btn_back.clicked.connect(self.go_back)  # Ferme la fenêtre actuelle
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

        # # Style général de la fenêtre
        self.setStyleSheet(open("Style/styleLog.css").read())




    def create_account(self):
        username = self.input_username.text()
        email = self.input_email.text()
        regex = r'\b[A-za-z0-9.\%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, email):
            QMessageBox.warning(None, 'Inscription Invalide', "Veuillez remplir un email correct \n"
                                                              "test@test.com ")
            return 0

        password = self.input_password.text()
        if username:
            if email:
                if not password:
                    QMessageBox.warning(None, 'Inscription Invalide', "Veuillez remplir le champ 'mot de passe' ")
                    return 0
            else:
                QMessageBox.warning(None, 'Inscription Invalide', "Veuillez remplir tout le champ 'email' ")
                return 0
        else:
            QMessageBox.warning(None, 'Inscription Invalide', "Veuillez remplir tout le champ 'username'")
            return 0
        self.db.insertUser(username, email, password)
        self.go_back()

    def go_back(self):
        from Projet_1.Interface.PageConnexion.Login import Login
        try:
            self.log  = Login()  # Vérifiez que PageInscription est correctement défini
            self.log .show()
            self.close()  # Assurez-vous que cela ne cause pas de problème
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

