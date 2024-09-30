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
        self.label_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(self.label_title)

        # Label et champ pour le nom utilisation
        self.label_username = QLabel("Nom d'utilisateur:")
        self.label_username.setStyleSheet("font-size: 16px; color: #555;")
        self.input_username = QLineEdit(self)
        self.input_username.setStyleSheet(self.input_style())
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        # Label et champ pour l'e-mail
        self.label_email = QLabel("E-mail:")
        self.label_email.setStyleSheet("font-size: 16px; color: #555;")
        self.input_email = QLineEdit(self)
        self.input_email.setStyleSheet(self.input_style())
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)

        # Label et champ pour le mot de passe
        self.label_password = QLabel("Mot de passe:")
        self.label_password.setStyleSheet("font-size: 16px; color: #555;")
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)  # Masquer le mot de passe
        self.input_password.setStyleSheet(self.input_style())
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        # Bouton pour créer un compte
        self.btn_create = QPushButton("Créer", self)
        self.btn_create.setStyleSheet(self.button_style())
        self.btn_create.clicked.connect(self.create_account)
        layout.addWidget(self.btn_create)

        # Bouton pour revenir à la page précédente
        self.btn_back = QPushButton("Retour", self)
        self.btn_back.setStyleSheet(self.button_style())
        self.btn_back.clicked.connect(self.go_back)  # Ferme la fenêtre actuelle
        layout.addWidget(self.btn_back)

        self.setLayout(layout)
        self.setStyleSheet(self.window_style())

    def window_style(self):
        return """
            QWidget {
                background-color: #F3F4F6;
            }
        """

    def input_style(self):
        """ Style CSS pour les QLineEdit (input) """
        return """
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                border: 2px solid #B0BEC5;
                border-radius: 5px;
                margin: 10px 0;
                background-color: #FFFFFF;
            }
            QLineEdit:focus {
                border-color: #42A5F5;
            }
        """

    def button_style(self):
        """ Style CSS pour les boutons """
        return """
            QPushButton {
                padding: 10px;
                font-size: 16px;
                color: white;
                background-color: #42A5F5;
                border: none;
                border-radius: 5px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #1E88E5;
                cursor: pointer;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """

    def create_account(self):
        username = self.input_username.text()
        email = self.input_email.text()
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

