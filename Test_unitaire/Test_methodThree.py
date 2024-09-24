import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from ipaddress import IPv4Network
import math
from Projet_1.Interface.ClassFull.MethodeThree import Methode_Three # Remplacer 'your_module' par le nom de votre fichier contenant la classe

app = QApplication([])


class TestMethodeThree(unittest.TestCase):

    def setUp(self):
        self.window = Methode_Three()

    # def test_initial_radio_buttons(self):
    #     """ Test initial des boutons radio """
    #     self.assertTrue(self.window.radio_SR.isChecked())
    #     self.assertFalse(self.window.radio_IP.isChecked())

    def test_toggle_radio_buttons(self):
        """ Test du changement entre découpe en sous-réseaux et en IPs """
        QTest.mouseClick(self.window.radio_IP, Qt.LeftButton)
        self.assertTrue(self.window.radio_IP.isChecked())
        self.assertFalse(self.window.radio_SR.isChecked())
        self.assertFalse(self.window.nbSR.isVisible())
        self.assertTrue(self.window.nbHote.isVisible())

        QTest.mouseClick(self.window.radio_SR, Qt.LeftButton)
        self.assertTrue(self.window.radio_SR.isChecked())
        self.assertFalse(self.window.radio_IP.isChecked())
        self.assertTrue(self.window.nbSR.isVisible())
        self.assertFalse(self.window.nbHote.isVisible())

    def test_invalid_ip_input(self):
        """ Test d'entrée d'une adresse IP non valide """
        self.window.AD_RS.setText("999.999.999.999")
        self.window.btn_generate.click()
        self.assertIn("Erreur", self.window.lbl_nbTotHotes.text())

    def test_valid_ip_input(self):
        """ Test d'entrée d'une adresse IP valide """
        self.window.AD_RS.setText("192.168.1.0")
        self.window.btn_generate.click()
        self.assertIn("Nombre total d'hôtes", self.window.lbl_nbTotHotes.text())

    def test_invalid_sous_reseau_input(self):
        """ Test d'entrée non valide pour le nombre de sous-réseaux """
        self.window.AD_RS.setText("192.168.1.0")
        self.window.nbSR.setText("-1")
        self.window.btn_generate.click()
        self.assertIn("Erreur", self.window.lbl_decoupeSR.text())

    def test_valid_sous_reseau_input(self):
        """ Test d'entrée valide pour la découpe en sous-réseaux """
        self.window.AD_RS.setText("192.168.1.0")
        self.window.nbSR.setText("4")
        self.window.btn_generate.click()
        self.assertIn("Découpe possible", self.window.lbl_decoupeSR.text())

    def test_calcul_nombre_hotes(self):
        """ Test du calcul correct du nombre total d'hôtes """
        self.window.AD_RS.setText("192.168.1.0")
        self.window.calc_nb_total_hotes()
        self.assertIn("254", self.window.lbl_nbTotHotes.text())  # /24 => 254 hôtes disponibles

    def test_verifier_decoupe_sr_valid(self):
        """ Test de la vérification de découpe SR avec des entrées valides """
        self.window.AD_RS.setText("192.168.1.0")
        self.window.nbSR.setText("2")
        self.window.verifier_decoupe_sr()
        self.assertIn("Découpe possible", self.window.lbl_decoupeSR.text())
        self.assertEqual(self.window.tableauSR.rowCount(), 2)

    def test_verifier_decoupe_sr_invalid(self):
        """ Test de la vérification de découpe SR avec des entrées invalides """
        self.window.AD_RS.setText("192.168.1.0")
        self.window.nbSR.setText("10000")  # Trop de sous-réseaux demandés
        self.window.verifier_decoupe_sr()
        self.assertIn("Impossible de réaliser la découpe", self.window.lbl_decoupeSR.text())

    def test_verifier_decoupe_ip_valid(self):
        """ Test de la découpe IP avec des entrées valides """
        self.window.radio_IP.setChecked(True)
        self.window.AD_RS.setText("192.168.1.0")
        self.window.nbHote.setText("50")
        self.window.verifier_decoupe_ip()
        self.assertIn("Découpe Possible", self.window.lbl_decoupeIP.text())
        self.assertEqual(self.window.tableauIP.rowCount(), 4)

    def test_verifier_decoupe_ip_invalid(self):
        """ Test de la découpe IP avec des entrées invalides """
        self.window.radio_IP.setChecked(True)
        self.window.AD_RS.setText("192.168.1.0")
        self.window.nbHote.setText("300")
        self.window.verifier_decoupe_ip()
        self.assertIn("Impossible de réaliser la découpe", self.window.lbl_decoupeIP.text())


if __name__ == "__main__":
    unittest.main()
