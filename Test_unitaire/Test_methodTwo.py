import unittest
from PyQt5.QtWidgets import QApplication
from Projet_1.Interface.ClassFull.MethodeTwo import Methode_Two  # Assure-toi que ce chemin est correct
import ipaddress

# Configuration pour que les tests fonctionnent dans PyQt5
app = QApplication([])


class TestMethodeTwo(unittest.TestCase):
    def setUp(self):
        # Crée une instance du widget pour chaque test
        self.widget = Methode_Two()

    def test_ip_in_network(self):
        # Tester si l'IP est dans le réseau
        self.widget.AD_IP_2.setText("192.168.1.10")
        self.widget.masque_2.setText("255.255.255.0")
        self.widget.AD_RESEAU.setText("192.168.1.0")

        self.widget.SameNetwork()
        self.assertEqual(self.widget.lbl_rep.text(), "L'adresse IP 192.168.1.10 est dans le réseau 192.168.1.0/24.")

    def test_ip_not_in_network(self):
        # Tester si l'IP n'est pas dans le réseau
        self.widget.AD_IP_2.setText("192.168.2.10")
        self.widget.masque_2.setText("255.255.255.0")
        self.widget.AD_RESEAU.setText("192.168.1.0")

        self.widget.SameNetwork()
        self.assertEqual(self.widget.lbl_rep.text(), "L'adresse IP 192.168.2.10 n'est pas dans le réseau 192.168.1.0/24.")

    def test_invalid_ip(self):
        # Tester si une IP invalide est fournie
        self.widget.AD_IP_2.setText("300.168.1.10")
        self.widget.masque_2.setText("255.255.255.0")
        self.widget.AD_RESEAU.setText("192.168.1.0")

        self.widget.SameNetwork()
        self.assertEqual(self.widget.lbl_rep.text(), "Erreur dans l'IP, le masque ou l'adresse réseau.")

    def test_invalid_mask(self):
        # Tester si un masque invalide est fourni
        self.widget.AD_IP_2.setText("192.168.1.10")
        self.widget.masque_2.setText("255.255.0.256")
        self.widget.AD_RESEAU.setText("192.168.1.0")

        self.widget.SameNetwork()
        self.assertEqual(self.widget.lbl_rep.text(), "Erreur dans l'IP, le masque ou l'adresse réseau.")

    def test_invalid_network(self):
        # Tester si une adresse réseau invalide est fournie
        self.widget.AD_IP_2.setText("192.168.1.10")
        self.widget.masque_2.setText("255.255.255.0")
        self.widget.AD_RESEAU.setText("192.168.300.0")

        self.widget.SameNetwork()
        self.assertEqual(self.widget.lbl_rep.text(), "Erreur dans l'IP, le masque ou l'adresse réseau.")


if __name__ == '__main__':
    unittest.main()
