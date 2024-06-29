import sys
import psutil
import sqlite3
import time
import threading
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class InformacionSistema(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("AnalisisPC.ui", self)
        self.db_connection = sqlite3.connect('AnalisisPC.db', check_same_thread=False)
        self.create_tables()
        self.btn_capturar.clicked.connect(self.captura_tiempo_real)
        self.btn_mostrar.clicked.connect(self.mostrar_datos)
        self.btn_salir.clicked.connect(self.salir)
        self.stop_event = threading.Event()

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sistema (
                            id INTEGER PRIMARY KEY,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                            cpu REAL,
                            memoria_total REAL,
                            memoria_utilizada REAL,
                            disco_total REAL,
                            disco_utilizado REAL,
                            temperatura REAL
                          )''')
        self.db_connection.commit()

    def capturar_datos(self):
        cpu = psutil.cpu_percent(interval=1)
        memoria = psutil.virtual_memory()
        disco = psutil.disk_usage('/')
        temperatura = self.info_temperatura()

        cursor = self.db_connection.cursor()
        cursor.execute('''INSERT INTO sistema (cpu, memoria_total, memoria_utilizada, disco_total, disco_utilizado, temperatura)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (cpu, memoria.total / (1024 ** 2), memoria.used / (1024 ** 2),
                        disco.total / (1024 ** 3), disco.used / (1024 ** 3), temperatura))
        self.db_connection.commit()

    def info_temperatura(self):
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                # Supongamos que tomamos la temperatura del primer sensor encontrado
                return temps[list(temps.keys())[0]][0].current
        return 0.0

    def captura_tiempo_real(self):
        start_time = time.time()
        while time.time() - start_time < 6:
            self.capturar_datos()
            time.sleep(2)
        print("Captura en tiempo real completada.")

    def mostrar_datos(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT AVG(cpu), AVG(memoria_utilizada), AVG(disco_utilizado), AVG(temperatura) FROM sistema')
        avg_cpu, avg_memoria, avg_disco, avg_temperatura = cursor.fetchone()

        # Crear el modelo para el QTableView
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(["Atributo", "Valor"])

        def agregar_fila(atributo, valor):
            modelo.appendRow([QStandardItem(atributo), QStandardItem(str(valor))])

        agregar_fila("Espacio en el disco duro", f"{avg_disco:.2f} GB")
        if avg_disco >= 300:
            agregar_fila("Funcionamiento", "El equipo funciona en óptimas condiciones")
        else:
            agregar_fila("Funcionamiento", "El equipo no funciona en óptimas condiciones")
        agregar_fila("Uso de CPU", f"{avg_cpu:.2f}%")
        agregar_fila("Memoria RAM utilizada", f"{avg_memoria:.2f} MB")
        agregar_fila("Temperatura medida", f"{avg_temperatura:.2f} °C")

        self.tb_mostrar.setModel(modelo)

    def salir(self):
        self.db_connection.close()
        QApplication.instance().quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InformacionSistema()
    ventana.show()
    sys.exit(app.exec_())
