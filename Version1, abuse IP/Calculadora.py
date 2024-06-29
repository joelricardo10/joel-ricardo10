import sys
import ipaddress
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class CalculadoraGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Calculadora.ui", self)
        self.btn_mostrar.clicked.connect(self.mostrarDatos)
        self.printWidgetNames()

    def printWidgetNames(self):
        for widget in self.findChildren(QWidget):
            print(widget.objectName())

    def mostrarDatos(self):
        ip_address = f"{self.le_IP_primer.text()}.{self.le_IP_segun.text()}.{self.le_IP_tercer.text()}.{self.le_IP_cuarto.text()}"
        subnet_mask = f"{self.le_MC_primer.text()}.{self.le_MC_segun.text()}.{self.le_MC_tercer.text()}.{self.le_MC_cuarto.text()}"

        # Calcular el prefijo de la máscara de subred
        try:
            mask_octets = [int(octet) for octet in subnet_mask.split('.')]
            mask_binary = ''.join(f"{octet:08b}" for octet in mask_octets)
            prefix_length = mask_binary.count('1')
        except ValueError as e:
            print(f"Error: {e}")
            return

        # Calcular los datos de la red
        try:
            network = ipaddress.IPv4Network(f"{ip_address}/{prefix_length}", strict=False)
        except ValueError as e:
            print(f"Error: {e}")
            return

        red = network.network_address
        broadcast = network.broadcast_address
        first_usable_ip = network.network_address + 1
        last_usable_ip = network.broadcast_address - 1
        numero_hosts = network.num_addresses
        numero_hosts_utilizables = numero_hosts - 2
        wildcard_mask = ipaddress.IPv4Address(int(network.hostmask))
        
        bin_red = '.'.join(f"{int(octet):08b}" for octet in str(network.network_address).split('.'))

        # Class red
        clase_red = self.claseRed(network.network_address)

        # Crear el modelo para el QTableView
        self.tb_capturar_calculadora.setModel(self.crearModelo([
            ("Dirección IP", ip_address),
            ("Máscara de Subred", f"{subnet_mask}/{prefix_length}"),
            ("Dirección de Red", str(red)),
            ("Dirección de Broadcast", str(broadcast)),
            ("Primera Dirección IP Utilizable", str(first_usable_ip)),
            ("Última Dirección IP Utilizable", str(last_usable_ip)),
            ("Número de Hosts", numero_hosts),
            ("Número de Hosts Utilizables", numero_hosts_utilizables),
            ("Máscara Wildcard", str(wildcard_mask)),
            ("Primer cuarteto de la representación binaria de la red", bin_red.split('.')[0]),
            ("Segundo cuarteto de la representación binaria de la red", bin_red.split('.')[1]),
            ("Tercer cuarteto de la representación binaria de la red", bin_red.split('.')[2]),
            ("Cuarto cuarteto de la representación binaria de la red", bin_red.split('.')[3]),
            ("Clase de Red", clase_red)
        ]))

    def crearModelo(self, data):
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(["Atributo", "Valor"])
        for atributo, valor in data:
            modelo.appendRow([QStandardItem(atributo), QStandardItem(str(valor))])
        return modelo

    def claseRed(self, ip):
        primer_octeto = int(str(ip).split('.')[0])
        if 1 <= primer_octeto <= 126:
            return "Clase A"
        elif 128 <= primer_octeto <= 191:
            return "Clase B"
        elif 192 <= primer_octeto <= 223:
            return "Clase C"
        elif 224 <= primer_octeto <= 239:
            return "Clase D"
        else:
            return "Clase E"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = CalculadoraGUI()
    GUI.show()
    sys.exit(app.exec_())
