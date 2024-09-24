from PyQt5.QtWidgets import QApplication

from Projet_1.Interface.PageConnexion.Login import Login

if __name__ == '__main__':
    app = QApplication([])
    login = Login()
    login.show()
    app.exec_()