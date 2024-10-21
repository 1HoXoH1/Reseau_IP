import os
import sys

import bcrypt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox


class Database():
    def __init__(self):

        self.database_name = "Reseau_ip.db"
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName(self.database_name)

        # Vérifie si la base de données existe
        if os.path.exists(self.database_name):
            if not self.database.open():
                QMessageBox.critical(None, "Database Error", "Database could not be opened")
                sys.exit(1)
        else:
            # Si la base de données n'existe pas, on essaie de l'ouvrir et de créer la table
            if not self.database.open():
                QMessageBox.critical(None, "Database Error", "Database could not be opened")
                sys.exit(1)
            self.createTable()


    def createTable(self):

        query = QSqlQuery()
        query.exec_("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)

    def insertUser(self, name, email, password):
        query = QSqlQuery()
        query.prepare("SELECT email FROM user")

        if query.exec_():
            while query.next():
                # Vérifiez la première colonne
                if query.value(0).strip().lower() == email.strip().lower():
                    return QMessageBox.warning(None, "Error", "Email already registered")
        else:
            print("Erreur d'exécution de la requête :", query.lastError().text())

        new_password = self.hash_password(password)

        query.prepare("INSERT INTO user (name, email, password) VALUES (?, ?, ?)")
        query.addBindValue(name)
        query.addBindValue(email)
        query.addBindValue(new_password)

        if not query.exec_():
            raise Exception("Failed to insert record: " + query.lastError().text())

    def get_data(self):
        query = QSqlQuery()
        query.prepare("SELECT * FROM user")

        if query.exec_():
            # Récupérer les résultats et les imprimer
            while query.next():
                user_id = query.value(0)
                name = query.value(1)
                email = query.value(2)
                password = query.value(3)
                print(f"ID: {user_id}, Name: {name}, Email: {email}, Password: {password}")
        else:
            print("Query execution failed:", query.lastError().text())

    def close(self):
        self.database.close()


    def hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode("utf-8")




    def change_password(self, email, new_password) -> bool:
        # Vérifie si l'utilisateur existe dans la base de données avant de changer le mot de passe
        query = QSqlQuery()
        query.prepare("SELECT email FROM user WHERE email = ?")
        query.addBindValue(email)

        if not query.exec_():
            QMessageBox.warning(None, "Database Error", "Erreur lors de la vérification de l'utilisateur: "+ query.lastError().text())
            return False

        if not query.next():
            QMessageBox.warning(None, "Database Error", "Email non trouvé dans la base de données.")
            return False

        # Si l'email existe, on continue à changer le mot de passe
        query = QSqlQuery()
        hashed_password = self.hash_password(new_password)
        query.prepare("UPDATE user SET password = ? WHERE email = ?")
        query.addBindValue(hashed_password)
        query.addBindValue(email)

        if not query.exec_():
            QMessageBox.warning(None, "Database error", "Échec de la mise à jour du mot de passe:" +query.lastError().text())
            return False

        return True



