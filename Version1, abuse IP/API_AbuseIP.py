import sys
import requests
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

API_KEY = '4df9bce33f09f71edaf250d1dd4db9e66ca7fd01fc7d818b190e6b5a1bfd033d55b4ca369f479584'
API_URL = 'https://api.abuseipdb.com/api/v2/'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("abuseip.ui", self)

        self.btn_api_leer.clicked.connect(self.api_read)
        self.btn_api_obtener.clicked.connect(self.api_history)
        self.btn_api_verif.clicked.connect(self.api_load)
        
        self.btn_db_actualizar.clicked.connect(self.db_update)
        self.btn_db_del.clicked.connect(self.db_delete)

        self.setup_db()
        self.load_table()

    def setup_db(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('abuseipdb.db')
        if not self.db.open():
            QMessageBox.critical(None, "Database Error", self.db.lastError().text())
        
        query = QSqlDatabase.database().exec(
            '''
            DROP TABLE IF EXISTS reports
            '''
        )
        query = QSqlDatabase.database().exec(
            '''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ipAddress TEXT,
                isPublic TEXT,
                ipVersion INTEGER,
                reportDetails TEXT
            )
            '''
        )

    def load_table(self):
        self.model = QSqlTableModel(self)
        self.model.setTable('reports')
        self.model.select()
        self.tb_mostrar.setModel(self.model)

    def api_read(self):
        response = requests.get(API_URL + 'blacklist', headers={'Key': API_KEY, 'Accept': 'application/json'})
        if response.status_code == 200:
            data = response.json()
        # No hay mensajes emergentes

    def api_history(self):
        ip = "8.8.8.8"  # Example IP
        response = requests.get(API_URL + f'check?ipAddress={ip}', headers={'Key': API_KEY, 'Accept': 'application/json'})
        if response.status_code == 200:
            data = response.json()
        # No hay mensajes emergentes

    def api_load(self):
        ip = "8.8.8.8"  # Example IP
        response = requests.get(API_URL + f'check?ipAddress={ip}', headers={'Key': API_KEY, 'Accept': 'application/json'})
        if response.status_code == 200:
            data = response.json()['data']
            conn = sqlite3.connect('abuseipdb.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reports (ipAddress, isPublic, ipVersion, reportDetails) VALUES (?, ?, ?, ?)", 
                           (data['ipAddress'], str(data['isPublic']), data['ipVersion'], str(data)))
            conn.commit()
            conn.close()
            self.load_table()
        # No hay mensajes emergentes

    def db_update(self):
        # Implement update logic here
        pass

    def db_delete(self):
        keyword = self.le_db_del.text().strip()
        if keyword:
            conn = sqlite3.connect('abuseipdb.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reports WHERE reportDetails LIKE ?", ('%' + keyword + '%',))
            conn.commit()
            conn.close()
            self.load_table()
            # QMessageBox.information(self, "Delete", "Record deleted successfully.")
        else:
            # QMessageBox.warning(self, "Delete", "Please enter a keyword to delete.")
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
