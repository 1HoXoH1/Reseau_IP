from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QApplication, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from Projet_1.Database.DataBase import Database
import re

from Projet_1.Interface.MainPage import PageZero

class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.db.get_data()

        # Paramètres de la fenêtre
        self.setWindowTitle('Login')
        self.resize(600, 600)

        # Layout principal (Vertical)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Titre de la page
        self.label_title = QLabel("Connectez-vous")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        # Ligne pour nom d'utilisateur
        self.Line_Name_username = QLineEdit(self)
        self.Line_Name_username.setPlaceholderText("Nom d'utilisateur")
        self.Line_Name_username.setStyleSheet(self.input_style())

        # Ligne pour le mot de passe
        self.Line_Name_password = QLineEdit(self)
        self.Line_Name_password.setPlaceholderText("Mot de passe")
        self.Line_Name_password.setEchoMode(QLineEdit.Password)  # Masquer le mot de passe
        self.Line_Name_password.setStyleSheet(self.input_style())

        # Bouton de connexion
        self.btn_login = QPushButton("Connexion", self)
        self.btn_login.setStyleSheet(self.button_style())
        self.btn_login.clicked.connect(self.CanIConnexion)

        # Phrase cliquable pour créer un compte
        self.label_create_account = QLabel("<a href='#'>Créer un compte</a>", self)
        self.label_create_account.setAlignment(Qt.AlignCenter)
        self.label_create_account.setStyleSheet(self.link_style())
        self.label_create_account.setOpenExternalLinks(False)

        # Phrase cliquable pour réinitialiser le mot de passe
        self.label_forgot_password = QLabel("<a href='#'>Mot de passe oublié ?</a>", self)
        self.label_forgot_password.setAlignment(Qt.AlignCenter)
        self.label_forgot_password.setStyleSheet(self.link_style())
        self.label_forgot_password.setOpenExternalLinks(False)

        # Ajouter les widgets au layout principal
        self.main_layout.addWidget(self.label_title)
        self.main_layout.addWidget(self.Line_Name_username)
        self.main_layout.addWidget(self.Line_Name_password)
        self.main_layout.addWidget(self.btn_login)
        self.main_layout.addWidget(self.label_create_account)
        self.main_layout.addWidget(self.label_forgot_password)

        # Centrer le layout
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Style général de la fenêtre
        self.setStyleSheet("""
            QWidget {
                background-color: #F3F4F6;
            }
        """)

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
        """ Style CSS pour le bouton de connexion """
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

    def link_style(self):
        """ Style CSS pour les labels cliquables (lien) """
        return """
            QLabel {
                font-size: 14px;
                color: #42A5F5;
                margin-top: 10px;
            }
            QLabel:hover {
                color: #1E88E5;
                cursor: pointer;
            }
        """

    def closeEvent(self, event):
        """ Ferme la connexion à la base de données avant de fermer la fenêtre """
        self.db.close()  # Appelle la méthode close() de ta classe Database
        event.accept()  # Accepte l'événement de fermeture

    def CanIConnexion(self):
        username = self.Line_Name_username.text()
        password = self.Line_Name_password.text()
        self.Connexion(username, password)

    def Connexion(self, name, pswd):

        regex = r'\b[A-za-z0-9.\%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, name):
            value = True
        else:
            value = False

        val = self.ConnexionBd(value, name, pswd)
        if val:
            QMessageBox.information(None, "Connexion réussi", "L'user est inscrit dans la bd")
            self.main_page = PageZero()  # Créer une instance de PageZero
            self.main_page.show()  # Afficher la page principale

            self.close()
        else:
            QMessageBox.warning(None, "Error log", "This user does not a account")

    def ConnexionBd(self, value, name, pswd):
        #si email
        if value:
            query = QSqlQuery()
            query.prepare("SELECT * FROM user WHERE email=? and password=?")
            query.addBindValue(name)
            query.addBindValue(pswd)
            if query.exec_():
                if query.next():  # Vérifie si un résultat est trouvé
                    return True
            else:
                print("Query execution failed:", query.lastError().text())  # Affiche l'erreur dans la console

            return False  # Renvoie False si aucun utilisateur n'est trouvé ou si la requête échoue

        else:
            query = QSqlQuery()
            query.prepare("SELECT * FROM user WHERE name=? and password=?")
            query.addBindValue(name)
            query.addBindValue(pswd)
            if query.exec_():
                if query.next():  # Vérifie si un résultat est trouvé
                    return True
            else:
                print("Query execution failed:", query.lastError().text())  # Affiche l'erreur dans la console

            return False  # Renvoie False si aucun utilisateur n'est trouvé ou si la requête échoue


# Exécution de l'application
if __name__ == '__main__':
    app = QApplication([])
    login = Login()
    login.show()
    app.exec_()
