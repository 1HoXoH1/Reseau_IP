from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication, QMessageBox
from PyQt5.QtCore import Qt



class forgive_mdp(QWidget):
    def __init__(self):
        super().__init__()

        self.db = None
        self.log = None
        self.setWindowTitle("Change MDP")
        self.resize(600, 600)

        # Master layout
        self.master_layout = QVBoxLayout(self)
        self.setLayout(self.master_layout)

        # Labels et inputs pour l'email, le nouveau mdp et la confirmation
        self.lbl_email = QLabel("Nom d'utilisateur", self)
        self.Ln_email = QLineEdit(self)

        self.lbl_new_password = QLabel("Nouveau mot de passe", self)
        self.Ln_new_password = QLineEdit(self)
        self.Ln_new_password.setEchoMode(QLineEdit.Password)

        self.lbl_confirm_new_password = QLabel("Confirmer le nouveau mot de passe", self)
        self.Ln_confirm_new_password = QLineEdit(self)
        self.Ln_confirm_new_password.setEchoMode(QLineEdit.Password)
        self.Ln_confirm_new_password.editingFinished.connect(self.IsSame)

        # Boutons pour soumettre ou annuler
        self.btn_submit = QPushButton("Soumettre")
        self.btn_submit.setDisabled(True)
        self.btn_submit.clicked.connect(self.change_password)
        self.btn_cancel = QPushButton("Annuler")

        # Ajouter les composants au layout
        self.master_layout.addWidget(self.lbl_email)
        self.master_layout.addWidget(self.Ln_email)
        self.master_layout.addWidget(self.lbl_new_password)
        self.master_layout.addWidget(self.Ln_new_password)
        self.master_layout.addWidget(self.lbl_confirm_new_password)
        self.master_layout.addWidget(self.Ln_confirm_new_password)
        self.master_layout.addWidget(self.btn_submit)
        self.master_layout.addWidget(self.btn_cancel)

        # Appliquer le style CSS
        self.setStyleSheet(self.style())

    def change_password(self):
        from Projet_1.Interface.PageConnexion.Login import Login

        value = self.go_change_password(email=self.Ln_email.text(), new_password=self.Ln_new_password.text())
        if value:
            try:
                self.log = Login()
                self.log.show()
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")
        else:
            QMessageBox.warning(None, "Error log", "The user is not in data base")

    def go_change_password(self, email, new_password) -> bool:
        from Projet_1.Database.DataBase import Database
        self.db = Database()
        value =self.db.change_password(email, new_password)
        return value



    def IsSame(self):
        first_pswd = self.Ln_new_password.text()
        second_pswd = self.Ln_confirm_new_password.text()
        email = self.Ln_email.text().strip()

        if first_pswd == second_pswd and email:
            self.btn_submit.setDisabled(False)
        else:
            self.btn_submit.setDisabled(True)



    def style(self):
        return """
            QWidget {
                background-color: #F0F4F7;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 10px;
            }
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                border: 2px solid #B0BEC5;
                border-radius: 5px;
                margin-bottom: 20px;
                background-color: #FFFFFF;
            }
            QLineEdit:focus {
                border-color: #42A5F5;
            }
            QPushButton {
                padding: 10px;
                font-size: 16px;
                color: white;
                background-color: #42A5F5;
                border: none;
                border-radius: 5px;
                margin-top: 10px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QPushButton:disabled {
                background-color: #B0BEC5;
                color: #ECEFF1;
                cursor: not-allowed;
            }
        """


# Lancer l'application
# if __name__ == '__main__':
#     app = QApplication([])
#     login = forgive_mdp()
#     login.show()
#     app.exec_()
