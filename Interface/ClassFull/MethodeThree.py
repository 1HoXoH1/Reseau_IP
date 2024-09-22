import math

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
import ipaddress
import math


class Methode_Three(QWidget):
    def __init__(self):
        super().__init__()
        # master VBOX
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)  # Alignement en haut

        # Création du layout pour les champs de saisie
        self.HLine = QHBoxLayout()
        self.HLine.setAlignment(Qt.AlignCenter)

        self.nbSR = QLineEdit(self)
        self.nbSR.setPlaceholderText('Nombre de sous réseau')
        self.nbHote = QLineEdit(self)
        self.nbHote.setPlaceholderText('Nombre d\'hôtes')
        self.AD_RS = QLineEdit(self)
        self.AD_RS.setPlaceholderText('Adresse réseau')

        # Expression régulière pour un masque CIDR valide
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\/(3[0-2]|[1-2]?[0-9])$')


        # ajout du validateur pour l'adresse réseau
        self.AD_RS_validator = QRegExpValidator(adress_regex, self.AD_RS)
        self.AD_RS.setValidator(self.AD_RS_validator)

        self.btn_generate = QPushButton('Vérification', self)

        self.HLine.addWidget(self.nbSR)
        self.HLine.addWidget(self.nbHote)
        self.HLine.addWidget(self.AD_RS)
        self.HLine.addWidget(self.btn_generate)

        # Ajout des labels qui seront sous les QLineEdit
        self.lbl_nbTotHotes = QLabel('Nomber total d\'hotes : ', self)
        self.lbl_decoupeSR = QLabel('Possibilité de découpe en fonction des sous réseaux ? : ', self)
        self.lbl_decoupeIP = QLabel('Possibilité de découpe en fonction des IPs ? : ', self)



        # Ajout des labels à la VLine (sous les champs de saisie)
        self.VLine = QVBoxLayout()
        self.VLine.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Ajouter les labels dans le layout vertical
        self.VLine.addWidget(self.lbl_nbTotHotes)
        self.VLine.addWidget(self.lbl_decoupeSR)
        self.VLine.addWidget(self.lbl_decoupeIP)


        # Ajout du layout horizontal (pour les QLineEdit) et vertical (pour les labels) dans le layout principal
        self.Master_Layout.addLayout(self.HLine)  # Les QLineEdit en haut
        self.Master_Layout.addLayout(self.VLine)  # Les labels en dessous

        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.lancer_prog)

    def lancer_prog(self):
        self.calc_nb_total_hotes()
        self.verifier_decoupe_sr()



    def calculer_masque_initial(self):
        # Récupérer l'adresse IP
        adresse_reseau = self.AD_RS.text()
        octets = list(map(int, adresse_reseau.split('.')))

        # Vérifier la validité de l'adresse IP
        if len(octets) != 4 or any(o < 0 or o > 255 for o in octets):
            raise ValueError("Adresse IP non valide.")

        # Déterminer le masque en fonction de la tranche d'adresse IP
        if 0 <= octets[0] < 128:
            masque = 8  # Classe A
        elif 128 <= octets[0] < 192:
            masque = 16  # Classe B
        elif 192 <= octets[0] < 224:
            masque = 24  # Classe C
        else:
            raise ValueError("Adresse IP non valide pour les classes A, B ou C.")

        return masque



    def calc_nb_total_hotes(self):
        try:
            masque = self.calculer_masque_initial()

            # Calculer le nombre total d'hôtes
            total_hotes = 2 ** (32 - masque) - 2  # -2 pour les adresses réservées (réseau et broadcast)

            # Afficher le nombre total d'hôtes
            self.lbl_nbTotHotes.setText(f"Nombre total d'hôtes : {total_hotes}")

        except ValueError as e:
            self.lbl_nbTotHotes.setText(f"Erreur : {str(e)}")

    def verifier_decoupe_sr(self):
        try:
            # Récupérer les valeurs saisies
            nombre_sr = int(self.nbSR.text())
            masque_initial = self.calculer_masque_initial()

            # Calculer le nombre de bits disponibles
            bits_disponibles = 32 - masque_initial

            # Calculer le nombre de bits nécessaires pour le nombre de sous-réseaux demandé
            if nombre_sr <= 0:
                raise ValueError("Le nombre de sous-réseaux doit être supérieur à 0.")

            bits_nécessaires = math.ceil(math.log2(nombre_sr))

            # Afficher le nombre de bits disponibles et nécessaires
            self.lbl_decoupeSR.setText(f"Bits disponibles : {bits_disponibles}, Bits nécessaires : {bits_nécessaires}")

            # Vérifier si la découpe est possible
            if bits_nécessaires > bits_disponibles:
                self.lbl_decoupeSR.setText(
                    f"Impossible de réaliser la découpe. Bits nécessaires : {bits_nécessaires}, Bits disponibles : {bits_disponibles}")
                return

            # Calculer le nombre de sous-réseaux possibles
            max_sous_reseaux_possibles = 2 ** bits_nécessaires

            # Vérifier si le nombre de sous-réseaux demandés dépasse le maximum possible
            if nombre_sr > max_sous_reseaux_possibles:
                self.lbl_decoupeSR.setText(
                    f"Impossible de réaliser la découpe. Nombre de sous-réseaux demandés : {nombre_sr}, Max possibles : {max_sous_reseaux_possibles}")
                return

            # Calculer le nouveau masque
            nouveau_masque = masque_initial + bits_nécessaires

            # Calculer la taille de chaque sous-réseau
            taille_sous_reseau = 2 ** (32 - nouveau_masque)  # Nombre d'adresses dans chaque sous-réseau

            # Calculer l'adresse de départ
            adresse_reseau = self.AD_RS.text()
            adresse_sous_reseau = ipaddress.IPv4Network((adresse_reseau, nouveau_masque), strict=False)

            # Liste pour stocker les adresses des sous-réseaux
            plan_adressage = []

            # Liste des sous-réseaux
            sous_reseaux = list(adresse_sous_reseau.subnets(new_prefix=nouveau_masque))

            for i in range(nombre_sr):
                # Assurez-vous que l'index est dans la plage
                if i < len(sous_reseaux):
                    plan_adressage.append(str(sous_reseaux[i].network_address))
                else:
                    break  # Sortir de la boucle si l'index dépasse la longueur de la liste



            #a vérif car seulement 1 adresse généré


            print("Sous-réseaux générés :", sous_reseaux)

            # Afficher le plan d'adressage **en dehors de la boucle**
            self.lbl_decoupeSR.setText(f"Plan d'adressage : {', '.join(plan_adressage)}")

        except ValueError as e:
            self.lbl_decoupeSR.setText(f"Erreur : {str(e)}")
        except Exception as e:
            self.lbl_decoupeSR.setText(f"Erreur inattendue : {str(e)}")  # Capture toutes les autres erreurs









