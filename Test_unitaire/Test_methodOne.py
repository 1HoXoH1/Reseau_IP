import unittest

import unittest

from Projet_1.Interface.ClassFull.MethodeOne import Methode_One

import sys
from PyQt5.QtWidgets import QApplication

# Crée une application pour gérer les widgets PyQt
app = QApplication(sys.argv)


class Test_methodeOne(unittest.TestCase):

    def setUp(self):
        # Crée une instance de la classe Methode_One pour chaque test
        self.widget = Methode_One()

    def test_calc_data_valid(self):
        self.widget.AD_IP.setText('192.168.1.10')  # Simule la saisie de cette IP
        self.widget.masque.setText('255.255.255.0')  # Simule la saisie de ce masque
        result_reseau, result_broadcast = self.widget.Calc_data()
        self.assertEqual(result_reseau, '192.168.1.0')  # Vérifie que l'adresse réseau est correcte
        self.assertEqual(result_broadcast, '192.168.1.255')  # Vérifie l'adresse de broadcast

    def test_calc_data_invalid(self):
        # Test avec des entrées invalides (adresse IP non valide)
        self.widget.AD_IP.setText('999.999.999.999')
        self.widget.masque.setText('255.255.255.0')
        result_reseau, result_broadcast = self.widget.Calc_data()
        self.assertEqual(result_reseau, "Erreur dans l'IP ou le masque")
        self.assertEqual(result_broadcast, "Erreur")

    def test_calc_data_sr_private_ip(self):
        # Test avec une adresse privée
        reseau, broadcast = self.widget.Calc_data_sr('192.168.1.10', '255.255.255.0')
        self.assertEqual(reseau, '192.168.1.0')
        self.assertEqual(broadcast, '192.168.1.255')

    def test_calc_data_sr_invalid_ip(self):
        # Test avec une IP non valide
        reseau, broadcast = self.widget.Calc_data_sr('999.999.999.999', '255.255.255.0')
        self.assertEqual(reseau, "Erreur dans l'IP")
        self.assertEqual(broadcast, "Erreur")


if __name__ == '__main__':
    unittest.main(exit=False)  # exit=False pour éviter que l'application ne ferme après le test
    app.exec_()  # Lancer la boucle d'événement PyQt
