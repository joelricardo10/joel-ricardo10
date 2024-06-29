import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextBrowser

def leer_log(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            logs = archivo.readlines()
        return logs
    except FileNotFoundError:
        print("El archivo no existe. Asegúrate de que el nombre del archivo sea correcto.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

def filtrar_logs(logs, criterio):
    logs_filtrados = [log for log in logs if criterio.lower() in log.lower()]
    return logs_filtrados

class LogAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("LogViewer.ui", self)
        
        self.btn_leer.clicked.connect(self.leer_archivo)
        self.btn_filtrar_severidad.clicked.connect(self.filtrar_por_severidad)
        self.btn_mostrar.clicked.connect(self.mostrar_todo)
        self.btn_salir.clicked.connect(self.close)

        self.btn_filtrar_fecha.clicked.connect(self.filtrar_por_fecha)
        self.btn_filtrar_hora.clicked.connect(self.filtrar_por_hora)
        self.btn_filtrar_severidad.clicked.connect(self.filtrar_por_severidad)

        self.logs = []

    def leer_archivo(self):
        self.logs = leer_log('router_log.txt')
        if self.logs:
            self.tb_router.clear()
            self.tb_router.append("Se leyeron {} entradas del log.".format(len(self.logs)))
            self.tb_router.append("".join(self.logs))
        else:
            self.tb_router.clear()
            self.tb_router.append("No se encontraron entradas en el log.")

    def filtrar_logs_por_criterio(self, criterio):
        logs_filtrados = [log for log in self.logs if criterio in log]
        return logs_filtrados

    def filtrar_por_severidad(self):
        severidad = self.le_filtrar_severidad.text().strip().upper()
        if severidad:
            logs_filtrados = self.filtrar_logs_por_criterio(f"{severidad}:")
            self.mostrar_resultados_filtrados(logs_filtrados, f"severidad '{severidad}'")
        else:
            self.mostrar_mensaje_error("Por favor, ingrese una severidad para filtrar.")

    def filtrar_por_fecha(self):
        fecha = self.le_filtrar_fecha.text().strip()
        if fecha:
            criterio = f"{fecha}"
            logs_filtrados = self.filtrar_logs_por_criterio(criterio)
            self.mostrar_resultados_filtrados(logs_filtrados, f"fecha '{criterio}'")
        else:
            self.mostrar_mensaje_error("Por favor, ingrese una fecha completa para filtrar.")

    def filtrar_por_hora(self):
        hora = self.le_filtrar_hora.text().strip()
        if hora:
            criterio = f"{hora}"
            logs_filtrados = self.filtrar_logs_por_criterio(criterio)
            self.mostrar_resultados_filtrados(logs_filtrados, f"hora '{criterio}'")
        else:
            self.mostrar_mensaje_error("Por favor, ingrese una hora completa para filtrar.")

    def mostrar_todo(self):
        if self.logs:
            self.tb_router.clear()
            self.tb_router.append("Mostrando todas las entradas del log:")
            self.tb_router.append("".join(self.logs))
        else:
            self.tb_router.clear()
            self.tb_router.append("No se han leído entradas del log aún.")

    def mostrar_resultados_filtrados(self, logs_filtrados, criterio):
        self.tb_router.clear()
        if logs_filtrados:
            self.tb_router.append(f"Entradas del log filtradas por {criterio}:")
            self.tb_router.append("".join(logs_filtrados))
        else:
            self.tb_router.append(f"No se encontraron entradas que coincidan con {criterio}.")

    def mostrar_mensaje_error(self, mensaje):
        self.tb_router.clear()
        self.tb_router.append(mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogAnalyzer()
    window.show()
    sys.exit(app.exec_())