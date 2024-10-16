import sys
import os
import time
import requests
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QIcon

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.png'))
        # Configuration de la fenêtre principale
        self.setWindowTitle("Systel  POCSAG Tester")
        self.setGeometry(100, 100, 400, 200)

        # Création d'un widget central et layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Ajout d'un champ de texte pour l'adresse IP
        self.ip_label = QLabel("Adresse IP :", self)
        self.layout.addWidget(self.ip_label)
        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Entrez l'adresse IP")
        self.layout.addWidget(self.ip_input)

        # Ajout d'un QComboBox pour des options (systel)
        self.systel_label = QLabel("Systel :", self)
        self.layout.addWidget(self.systel_label)
        self.systel_combobox = QComboBox(self)
        self.systel_combobox.addItems(["SysBOX", "Tempo100-IP"])
        self.layout.addWidget(self.systel_combobox)

        # Ajout d'un QSpinBox pour définir un nombre de boucles
        self.nbrloop_label = QLabel("Nombre de boucles :", self)
        self.layout.addWidget(self.nbrloop_label)
        self.nbrloop_spinbox = QSpinBox(self)
        self.nbrloop_spinbox.setRange(1, 100)  # Définir la plage de 1 à 100
        self.layout.addWidget(self.nbrloop_spinbox)

        # Ajout d'un bouton pour envoyer les données
        self.button = QPushButton("Envoyer", self)
        self.layout.addWidget(self.button)

        # Connexion du bouton à une méthode qui enverra les données en multi-threading
        self.button.clicked.connect(self.on_button_click)
        multiprocessing = threading.Thread(target=self.on_button_click)
        # Ajout d'un label pour afficher les réponses ou informations
        self.response_label = QLabel("", self)
        self.layout.addWidget(self.response_label)

    def on_button_click(self):
        # Récupérer les données saisies dans les champs
        ip_value = self.ip_input.text()
        nbrloop_value = self.nbrloop_spinbox.value()
        systel_value = self.systel_combobox.currentText()

        # Affichage des valeurs dans le label (tu peux ici appeler une fonction qui envoie les données)
        self.response_label.setText(f"IP: {ip_value}, Boucles: {nbrloop_value}, Systel: {systel_value}")
        if systel_value == "SysBOX":
            for i in range(nbrloop_value):
                url = 'http://' + ip_value + ':8000/api/testPOCSAG'
                payload = {'id': 0}
                try:
                    response = requests.put(url, json=payload)
                    if response.status_code == 200:
                        self.response_label.setText(f"Test Réussi, Boucle {i+1}/{nbrloop_value}")
                        time.sleep(26)
                    else:
                        self.response_label.setText(f"Test Echoué, Boucle {i+1}/{nbrloop_value}")
                except requests.exceptions.ConnectionError:
                    show_error_message(f"Erreur : Impossible de se connecter à l'IP {ip_value}.")
                except requests.exceptions.Timeout:
                    show_error_message("Erreur : La requête a expiré (timeout).")
                except requests.exceptions.RequestException as e:
                    show_error_message(f"Erreur lors de la requête : {e}")
                

def show_error_message(message):
    # Fonction pour afficher un message d'erreur
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setWindowIcon(QIcon('icon.png'))
    error_dialog.setWindowTitle("Erreur")
    error_dialog.setText(message)
    error_dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()