from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class Encodage(QWidget):
    def __init__(self):
        super().__init__()

        # Splitter pour le dashboard rétractable
        self.splitter = QSplitter(Qt.Horizontal)

        # Dashboard (panneau latéral rétractable)
        self.dashboard = QGroupBox("Dashboard")
        self.dashboard_layout = QVBoxLayout()

        # Ajouter des boutons au dashboard
        self.dashboard_button1 = QPushButton("Action 1")
        self.dashboard_button2 = QPushButton("Action 2")
        self.dashboard_button3 = QPushButton("Action 3")

        self.dashboard_layout.addWidget(self.dashboard_button1)
        self.dashboard_layout.addWidget(self.dashboard_button2)
        self.dashboard_layout.addWidget(self.dashboard_button3)
        self.dashboard_layout.addStretch()  # Pour ajouter de l'espace en bas
        self.dashboard.setLayout(self.dashboard_layout)

        # Onglets
        self.tab_widget = QTabWidget()

        # Onglet 1
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.lbl_tab1 = QLabel("Contenu de l'onglet 1")
        self.tab1_layout.addWidget(self.lbl_tab1)
        self.tab1.setLayout(self.tab1_layout)

        # Onglet 2
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.lbl_tab2 = QLabel("Contenu de l'onglet 2")
        self.tab2_layout.addWidget(self.lbl_tab2)
        self.tab2.setLayout(self.tab2_layout)

        # Ajouter les onglets au QTabWidget
        self.tab_widget.addTab(self.tab1, "Onglet 1")
        self.tab_widget.addTab(self.tab2, "Onglet 2")

        # Ajouter le dashboard et les onglets au splitter
        self.splitter.addWidget(self.dashboard)  # Dashboard à gauche
        self.splitter.addWidget(self.tab_widget)  # Onglets à droite

        # Définir les tailles initiales des panneaux du splitter
        self.splitter.setStretchFactor(1, 1)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.splitter)
        self.setLayout(self.main_layout)

        # Bouton pour rétracter/afficher le dashboard
        self.toggle_button = QPushButton("Cacher/Montrer Dashboard")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.clicked.connect(self.toggle_dashboard)

        # Ajouter le bouton en bas
        self.main_layout.addWidget(self.toggle_button)

    def toggle_dashboard(self):
        if self.toggle_button.isChecked():
            self.dashboard.show()  # Montrer le dashboard
        else:
            self.dashboard.hide()  # Cacher le dashboard


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Encodage()
    window.show()
    sys.exit(app.exec_())
# # Master Layout
# self.Master_Layout = QVBoxLayout()
# self.Master_Layout.setAlignment(Qt.AlignTop)
# self.Master_Layout.setContentsMargins(20, 20, 20, 20)
#
# # GroupBox pour les champs d'entrée
# self.input_group = QGroupBox("Paramètres IP")
# self.input_layout = QHBoxLayout()
#
# # Adresse IP
# self.AD_IP = QLineEdit(self)
# self.AD_IP.setPlaceholderText('Adresse IP')
# self.AD_IP.setFixedWidth(150)
#
# # Masque de sous-réseau
# self.masque = QComboBox(self)
# self.masque.addItems(['255.0.0.0', '255.255.0.0', '255.255.255.0'])
# self.masque.setFixedWidth(150)
#
# # Bouton de génération
# self.btn_generate = QPushButton('Generate', self)
# self.btn_generate.setFixedWidth(100)
#
# # Ajout des widgets dans la ligne d'entrée
# self.input_layout.addWidget(self.AD_IP)
# self.input_layout.addWidget(self.masque)
# self.input_layout.addWidget(self.btn_generate)
#
# self.input_group.setLayout(self.input_layout)
#
# # Ajout de la GroupBox dans le layout principal
# self.Master_Layout.addWidget(self.input_group)
#
# # Séparateur (ligne horizontale)
# self.separator = QFrame()
# self.separator.setFrameShape(QFrame.HLine)
# self.separator.setFrameShadow(QFrame.Sunken)
# self.Master_Layout.addWidget(self.separator)
#
# # Labels pour afficher les résultats
# self.result_group = QGroupBox("Résultats")
# self.result_layout = QVBoxLayout()
#
# self.lbl_AD_reseau = QLabel('Adresse Réseau:', self)
# self.lbl_Broadcast_IP = QLabel('Adresse Broadcast:', self)
# self.lbl_SR_Reseau_IP = QLabel('Adresse sous-réseau:', self)
# self.lbl_SR_Broadcast_IP = QLabel('Adresse Broadcast (SR):', self)
#
# # Ajouter les labels dans le layout vertical des résultats
# self.result_layout.addWidget(self.lbl_AD_reseau)
# self.result_layout.addWidget(self.lbl_Broadcast_IP)
# self.result_layout.addWidget(self.lbl_SR_Reseau_IP)
# self.result_layout.addWidget(self.lbl_SR_Broadcast_IP)
#
# self.result_group.setLayout(self.result_layout)
#
# # Ajout du groupe de résultats au layout principal
# self.Master_Layout.addWidget(self.result_group)
#
#
# # Ajout de la 2ème partie du prog
# self.input_group_2 = QGroupBox("Appertenance Réseau")
# self.input_layout_2 = QHBoxLayout()
#
# #Adresse Ip
# self.AD_IP_2 = QLineEdit(self)
# self.AD_IP_2.setPlaceholderText('Adresse IP')
# self.AD_IP_2.setFixedWidth(150)
#
# # Masque de sous-réseau
# self.masque_2 = QComboBox(self)
# self.masque_2.addItems(['255.0.0.0', '255.255.0.0', '255.255.255.0'])
# self.masque_2.setFixedWidth(150)
#
# #Adresse réseau
# self.AD_RESEAU = QLineEdit(self)
# self.AD_RESEAU.setPlaceholderText('Adresse Réseau')
# self.AD_RESEAU.setFixedWidth(150)
#
# # Bouton de génération
# self.btn_generate_2 = QPushButton('Generate', self)
# self.btn_generate_2.setFixedWidth(100)
#
# # Ajout des widgets dans la ligne d'entrée
# self.input_layout_2.addWidget(self.AD_IP_2)
# self.input_layout_2.addWidget(self.masque_2)
# self.input_layout_2.addWidget(self.AD_RESEAU)
# self.input_layout_2.addWidget(self.btn_generate_2)
#
# self.input_group_2.setLayout(self.input_layout_2)
#
# self.Master_Layout.addWidget(self.input_group_2)
#
#
# # Labels pour afficher les résultats
# self.result_group_2 = QGroupBox("Résultats")
# self.result_layout_2 = QVBoxLayout()
#
# self.lbl_rep = QLabel('Réponse :', self)
#
# # Ajouter les labels dans le layout vertical des résultats
# self.result_layout_2.addWidget(self.lbl_rep)
#
# self.result_group_2.setLayout(self.result_layout_2)
#
# # Ajout du groupe de résultats au layout principal
# self.Master_Layout.addWidget(self.result_group_2)
#
# # Appliquer le layout principal
# self.setLayout(self.Master_Layout)
#
# # Connecter le bouton au générateur d'adresse IP
# self.btn_generate.clicked.connect(self.generator_Ip_ClassFull)
# self.btn_generate_2.clicked.connect(self.SameNetwork)