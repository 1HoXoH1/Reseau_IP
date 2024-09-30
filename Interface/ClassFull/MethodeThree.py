from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
import ipaddress
import math


class Methode_Three(QWidget):
    def __init__(self):
        super().__init__()

        self.input_group = QGroupBox("Choix de la découpe")
        self.radio_SR = QRadioButton("Découpe en sous réseaux", self)
        self.radio_IP = QRadioButton("Découpe en IP", self)

        self.radio_SR.setChecked(True)

        self.radio_IP.toggled.connect(self.gerer_fonction_a_afficher)

        self.boxRadio = QHBoxLayout()
        self.boxRadio.addWidget(self.radio_SR)
        self.boxRadio.addWidget(self.radio_IP)

        self.input_group.setLayout(self.boxRadio)

        # Master VBOX
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)  # Alignement en haut

        # Correction: utilisez addWidget pour ajouter le QGroupBox
        self.Master_Layout.addWidget(self.input_group)

        # Ajout du séparateur
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.Master_Layout.addWidget(self.separator)

        # Création du 2ème groupe avec un titre
        self.input_group2 = QGroupBox("Données de découpe")  # Ajoutez un titre pour le groupe

        # Création du layout pour les champs de saisie
        self.HLine = QHBoxLayout()
        self.HLine.setAlignment(Qt.AlignCenter)

        self.nbSR = QLineEdit(self)
        self.nbSR.setPlaceholderText('Nombre de sous réseau')
        self.nbHote = QLineEdit(self)
        self.nbHote.setPlaceholderText('Nombre total d\'hôtes')
        self.AD_RS = QLineEdit(self)
        self.AD_RS.setPlaceholderText('Adresse réseau')

        # Expression régulière pour les hôtes et IP
        nb_regex = QRegExp(r'^\d*$')

        # Expression régulière pour un masque CIDR valide
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$')

        # Ajout des validateurs pour bloquer les caractères sur les champs
        self.nbSR_validateur = QRegExpValidator(nb_regex, self.nbSR)
        self.nbHote_validateur = QRegExpValidator(nb_regex, self.nbHote)
        self.nbSR.setValidator(self.nbSR_validateur)
        self.nbHote.setValidator(self.nbHote_validateur)

        # Ajout du validateur pour l'adresse réseau
        self.AD_RS_validateur = QRegExpValidator(adress_regex, self.AD_RS)
        self.AD_RS.setValidator(self.AD_RS_validateur)

        self.btn_generate = QPushButton('Vérification', self)

        self.HLine.addWidget(self.nbSR)
        self.HLine.addWidget(self.nbHote)
        self.HLine.addWidget(self.AD_RS)
        self.HLine.addWidget(self.btn_generate)

        # Ajout dans le groupe puis à la vue
        self.input_group2.setLayout(self.HLine)
        self.Master_Layout.addWidget(self.input_group2)  # Utilisez addWidget ici aussi

        # Séparateur entre la section d'entrée et la section des résultats
        self.separator2 = QFrame()
        self.separator2.setFrameShape(QFrame.HLine)
        self.separator2.setFrameShadow(QFrame.Sunken)
        self.Master_Layout.addWidget(self.separator2)

        # Création du groupbox pour les labels et tableaux
        self.group_labels_tableaux = QGroupBox("Découpe IP et Sous-Réseaux")

        # Ajout des labels qui seront sous les QLineEdit
        self.lbl_nbTotHotes = QLabel('Nombre total d\'hotes : ', self)
        self.lbl_decoupeSR = QLabel('Possibilité de découpe en fonction des sous réseaux ? : ', self)

        # Table pour afficher les sous-réseaux (cachée au début)
        self.tableauSR = QTableWidget(self)
        self.tableauSR.setColumnCount(5)
        self.tableauSR.setMinimumHeight(370)
        self.tableauSR.setMaximumHeight(370)
        self.tableauSR.verticalHeader().setDefaultSectionSize(40)
        self.tableauSR.setHorizontalHeaderLabels(
            ['Adresse réseau', 'Première IP', 'Dernière IP', 'Broadcast', "Nombre d'hôtes"])

        # Permet de remplir tout l'espace
        header = self.tableauSR.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Tableau inéditable
        self.tableauSR.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.lbl_decoupeIP = QLabel('Possibilité de découpe en fonction des IPs ? : ', self)

        # Table pour afficher les sous-réseaux (cachée au début)
        self.tableauIP = QTableWidget(self)
        self.tableauIP.setColumnCount(5)
        self.tableauIP.setMinimumHeight(370)
        self.tableauIP.setMaximumHeight(370)
        self.tableauIP.verticalHeader().setDefaultSectionSize(40)
        self.tableauIP.setHorizontalHeaderLabels(
            ['Adresse réseau', 'Première IP', 'Dernière IP', 'Broadcast', "Nombre d'hôtes"])

        # Permet de remplir tout l'espace
        header = self.tableauIP.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Tableau inéditable
        self.tableauIP.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Cacher les tableaux et certains éléments au début
        self.tableauIP.hide()
        self.tableauSR.hide()
        self.nbHote.hide()
        self.lbl_decoupeIP.hide()

        # Ajout des labels à la VLine (sous les champs de saisie)
        self.VLineGroup = QVBoxLayout()  # Nouveau layout vertical pour le groupbox
        self.VLineGroup.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Ajouter les labels dans le layout vertical
        self.VLineGroup.addWidget(self.lbl_nbTotHotes)
        self.VLineGroup.addWidget(self.lbl_decoupeSR)
        self.VLineGroup.addWidget(self.tableauSR)
        self.VLineGroup.addWidget(self.lbl_decoupeIP)
        self.VLineGroup.addWidget(self.tableauIP)

        # Gérer l'alignement
        self.VLineGroup.setAlignment(self.lbl_nbTotHotes, Qt.AlignTop)
        self.VLineGroup.setAlignment(self.tableauSR, Qt.AlignTop)
        self.VLineGroup.setAlignment(self.tableauIP, Qt.AlignTop)

        # Appliquer le layout au QGroupBox
        self.group_labels_tableaux.setLayout(self.VLineGroup)

        # Ajouter le groupbox au layout principal (Master_Layout)
        self.Master_Layout.addWidget(self.group_labels_tableaux)

        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.lancer_prog)
        # # Style général de la fenêtre
        self.setStyleSheet(open("Style/styleLog.css").read())

    def gerer_fonction_a_afficher(self):
        if self.radio_SR.isChecked():
            self.afficher_decoupe_SR()
        else:
            self.afficher_decoupe_IP()

    def afficher_decoupe_SR(self):
        self.nbHote.hide()
        self.nbSR.show()
        self.tableauIP.hide()
        self.lbl_decoupeIP.hide()
        self.nbHote.setText("")
        self.lbl_decoupeSR.show()

        return

    def afficher_decoupe_IP(self):
        self.nbSR.hide()
        self.nbHote.show()
        self.tableauSR.hide()
        self.lbl_decoupeSR.hide()
        self.nbSR.setText("")
        self.lbl_decoupeIP.show()
        return


    def lancer_prog(self):
        self.calc_nb_total_hotes()
        self.verifier_decoupe_sr()
        self.verifier_decoupe_ip()

    def calculer_masque_initial(self):
        # Récupérer l'adresse IP
        adresse_reseau = self.AD_RS.text()
        octets = list(map(int, adresse_reseau.split('.')))

        # Vérifier la validité de l'adresse réseau
        if len(octets) != 4 or any(o < 0 or o > 255 for o in octets):
            raise ValueError("Adresse IP non valide.")

        # Déterminer le masque en fonction de la tranche d'adresse réseau
        if 0 <= octets[0] < 128:
            masque = 8  # Classe A
        elif 128 <= octets[0] < 192:
            masque = 16  # Classe B
        elif 192 <= octets[0] < 224:
            masque = 24  # Classe C
        else:
            raise ValueError("Adresse réseau non valide pour les classes A, B ou C.")

        return masque

    def calc_nb_total_hotes(self):
        try:
            if not self.AD_RS.text().strip():
                self.lbl_nbTotHotes.setText("Nombre total d\'hotes : Champ vide.")
                return


            masque = self.calculer_masque_initial()

            # Calculer le nombre total d'hôtes
            total_hotes = 2 ** (32 - masque) - 2  # -2 pour les adresses réservées (réseau et broadcast)

            # Afficher le nombre total d'hôtes
            self.lbl_nbTotHotes.setText(f"Nombre total d'hôtes : {total_hotes}")

        except ValueError as e:
            self.lbl_nbTotHotes.setText(f"Erreur : {str(e)}")

    def verifier_decoupe_sr(self):
        try:
            # Convertir l'adresse réseau de départ en entier
            adresse_reseau = self.AD_RS.text()
            reseau = ipaddress.IPv4Network(adresse_reseau, strict=False)

            if reseau.is_reserved or reseau.is_private:
                self.lbl_decoupeSR.setText("L'adresse renseignée est privée.")
                self.lbl_nbTotHotes.hide()
                return

            if not self.nbSR.text().strip():
                self.tableauSR.hide()
                self.lbl_decoupeSR.setText("Possibilité de découpe en fonction des sous réseaux ? : Champ vide.")
                return

            if not self.AD_RS.text().strip():
                self.tableauSR.hide()
                self.lbl_decoupeSR.setText("Possibilité de découpe en fonction des sous réseaux ? : Aucune adresse réseau.")
                return


            # Récupérer les valeurs saisies
            nombre_sr = int(self.nbSR.text())
            masque_initial = self.calculer_masque_initial()

            # Calculer le nombre de bits disponibles
            bits_disponibles = 32 - masque_initial

            # Calculer le nombre de bits nécessaires pour le nombre de sous-réseaux demandé
            if nombre_sr <= 0:
                raise ValueError("Le nombre de sous-réseaux doit être supérieur à 0.")

            bits_necessaires = math.ceil(math.log2(nombre_sr))

            # Vérifier si la découpe est possible
            if bits_necessaires > bits_disponibles:
                self.lbl_decoupeSR.setText(
                    f"Impossible de réaliser la découpe. Bits nécessaires : {bits_necessaires}, Bits disponibles : {bits_disponibles}")
                self.tableauSR.hide()
                return

            # Calculer le nombre de sous-réseaux possibles
            max_sous_reseaux_possibles = 2 ** bits_necessaires

            # Vérifier si le nombre de sous-réseaux demandés dépasse le maximum possible
            if nombre_sr > max_sous_reseaux_possibles:
                self.lbl_decoupeSR.setText(
                    f"Impossible de réaliser la découpe. Nombre de sous-réseaux demandés : {nombre_sr}, Max possibles : {max_sous_reseaux_possibles}")
                self.tableauSR.hide()
                return

            # Calculer le nouveau masque
            nouveau_masque = masque_initial + bits_necessaires

            #Vérification si le masque est au dessus de 30
            if (nouveau_masque >= 31):
                self.lbl_decoupeSR.setText(
                    f"Impossible de réaliser la découpe. Le masque ne peut pas être supérieur à 30. Masque actuel : {nouveau_masque}")
                self.tableauSR.hide()
                return

            # Calculer la taille de chaque sous-réseau
            taille_sous_reseau = 2 ** (32 - nouveau_masque)  # Nombre d'adresses dans chaque sous-réseau


            adresse_entier = int(reseau.network_address)

            self.lbl_decoupeSR.setText(
                f"Découpe possible. Masque nécessaire : /{nouveau_masque}, Max d\'hôtes : {taille_sous_reseau-2}")


            # Réinitialiser et montrer le tableau
            self.tableauSR.setRowCount(nombre_sr)
            self.tableauSR.show()

            # Boucle pour générer chaque sous-réseau
            for i in range(nombre_sr):
                # Créer un sous-réseau à chaque itération
                sous_reseau = ipaddress.IPv4Network((adresse_entier, nouveau_masque), strict=False)
                adresse_reseau = sous_reseau.network_address
                adresse_broadcast = sous_reseau.broadcast_address
                premiere_ip = sous_reseau.network_address + 1
                derniere_ip = sous_reseau.broadcast_address - 1
                nombre_hotes = taille_sous_reseau - 2  # Retirer réseau et broadcast

                # Remplir le tableau avec les informations de chaque sous-réseau
                self.tableauSR.setItem(i, 0, QTableWidgetItem(str(sous_reseau.network_address)))
                self.tableauSR.setItem(i, 1, QTableWidgetItem(str(premiere_ip)))
                self.tableauSR.setItem(i, 2, QTableWidgetItem(str(derniere_ip)))
                self.tableauSR.setItem(i, 3, QTableWidgetItem(str(adresse_broadcast)))
                self.tableauSR.setItem(i, 4, QTableWidgetItem(str(nombre_hotes)))

                # Incrémenter l'adresse réseau de la taille d'un sous-réseau
                adresse_entier += taille_sous_reseau


        except ValueError as e:
            self.lbl_decoupeSR.setText(f"Erreur : {str(e)}")
        except Exception as e:
            self.lbl_decoupeSR.setText(f"Erreur inattendue : {str(e)}")  # Capture toutes les autres erreurs

    def verifier_decoupe_ip(self):
        try:

            adresse_reseau = ipaddress.IPv4Network(self.AD_RS.text(), strict=False)

            if adresse_reseau.is_private or adresse_reseau.is_reserved:
                self.lbl_decoupeIP.setText("L'adresse renseignée est privée.")
                self.lbl_nbTotHotes.hide()
                return

            if not self.nbHote.text().strip():
                self.tableauIP.hide()
                self.lbl_decoupeIP.setText("Possibilité de découpe en fonction des IPs ? : Champ vide.")
                return

            if not self.AD_RS.text().strip():
                self.tableauIP.hide()
                self.lbl_decoupeIP.setText("Possibilité de découpe en fonction des IPs ? : Aucune adresse réseau.")
                return

            # Récupérer les valeurs saisies
            nombre_ip_par_sr = int(self.nbHote.text())
            masque_initial = self.calculer_masque_initial()

            # Calculer le nombre total d'hôtes
            total_hotes = 2 ** (32 - masque_initial) - 2  # -2 pour les adresses réservées

            # Vérifier si le nombre d'IP par sous-réseau est valide
            if nombre_ip_par_sr <= 0 or nombre_ip_par_sr >= total_hotes:
                raise ValueError("Le nombre d'IP par sous-réseau doit être compris entre 1 et {}".format(total_hotes))

            # Calculer le masque nécessaire pour le nombre d'IP par sous-réseau
            masque_nouveau = 32 - math.ceil(math.log2(nombre_ip_par_sr + 2))  # +2 pour réseau et broadcast

            # Vérifier que le masque n'est pas inférieur au masque initial
            if masque_nouveau < masque_initial:
                raise ValueError("Le masque nécessaire ne peut pas être inférieur au masque initial.")

            # Calculer le nombre de sous-réseaux possibles
            # C'est ici que le calcul doit être corrigé
            max_sous_reseaux_possibles = 2 ** (masque_nouveau - masque_initial)

            # Afficher les résultats
            self.lbl_decoupeIP.setText(
                f"Découpe Possible. Masque nécessaire : /{masque_nouveau}, Max sous-réseaux possibles : {max_sous_reseaux_possibles}")

            if max_sous_reseaux_possibles <= 0:
                self.lbl_decoupeIP.setText("Impossible de réaliser la découpe avec le nombre d'IP demandé.")
                return

            # Vider le tableau avant de le remplir
            self.tableauIP.setRowCount(0)


            for i in range(max_sous_reseaux_possibles):
                # Créer un sous-réseau
                sous_reseau = ipaddress.IPv4Network((str(adresse_reseau.network_address), masque_nouveau), strict=False)
                premiere_ip = sous_reseau.network_address + 1
                derniere_ip = sous_reseau.broadcast_address - 1
                adresse_broadcast = sous_reseau.broadcast_address
                nombre_hotes = 2 ** (32 - masque_nouveau) - 2  # -2 pour réseau et broadcast

                # Ajouter une nouvelle ligne au tableau
                self.tableauIP.insertRow(i)

                # Remplir le tableau avec les informations de chaque sous-réseau
                self.tableauIP.setItem(i, 0, QTableWidgetItem(str(sous_reseau.network_address)))
                self.tableauIP.setItem(i, 1, QTableWidgetItem(str(premiere_ip)))
                self.tableauIP.setItem(i, 2, QTableWidgetItem(str(derniere_ip)))
                self.tableauIP.setItem(i, 3, QTableWidgetItem(str(adresse_broadcast)))
                self.tableauIP.setItem(i, 4, QTableWidgetItem(str(nombre_hotes)))

                # Incrémenter l'adresse pour le prochain sous-réseau
                # Vérifier que la prochaine adresse ne dépasse pas 255.255.255.255
                if adresse_reseau.broadcast_address >= ipaddress.IPv4Address('255.255.255.255'):
                    break  # Sortir de la boucle si nous avons atteint la limite des adresses IPv4

                # Incrémenter l'adresse pour le prochain sous-réseau
                adresse_reseau = ipaddress.IPv4Network((str(adresse_reseau.broadcast_address + 1), masque_initial),
                                                       strict=False)

            # Afficher le tableau après l'avoir rempli
            self.tableauIP.show()

        except ValueError as e:
            self.lbl_decoupeIP.setText(f"Erreur : {str(e)}")
        except Exception as e:
            self.lbl_decoupeIP.setText(f"Erreur inattendue : {str(e)}")
