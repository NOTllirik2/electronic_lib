import model
import autorisation
import mainElements
import mysql.connector
from mysql.connector import Error


from datetime import datetime, timezone
import sys, os
import subprocess
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow, QLabel, QPushButton, QLineEdit, \
    QApplication, QWidget, QVBoxLayout, QCheckBox, QScrollArea, QComboBox, QTextEdit, QToolBar, QAction, QFileDialog, \
    QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, QSize, QPropertyAnimation, QRect, Qt

def test_connection(host, user, password, database=None):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            server_info = connection.get_server_info()
            print(f"Успешное подключение к серверу MySQL версии {server_info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            current_db = cursor.fetchone()
            print(f"Подключен к базе данных: {current_db[0] if current_db else 'нет базы данных'}")
            cursor.close()

    except Error as e:
        print(f"Ошибка подключения: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Подключение закрыто.")

def run_mysqlsh_script():
    mysqlsh_path = "mysqlsh"

    script_path = "createCopy.py"

    try:
        # Выполнение MySQL Shell с указанным скриптом
        subprocess.run([mysqlsh_path, "--python", "--file", script_path], check=True)
        print("Скрипт MySQL Shell успешно выполнен!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении скрипта: {e}")
    except FileNotFoundError:
        print("MySQL Shell не найден. Убедитесь, что он установлен и доступен в PATH.")

class dataBaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("база данных")
        self.setGeometry(0, 0, 1500, 900)

        self.user = model.User
        self.id = 0
        self.name = ""
        self.password = ""

        mode = 2
        if mode == 1:
            self.testUser()
        elif mode == 2:
            self.testAdmin()
        elif mode == 3:
            self.aut = autorisation.autorisationWindow(self)

    def userWasAutorized(self):
        self.switch_connection(self.user.role)
        self.aut.setVisible(False)

        #self.switch_connection("admin")
        #self.user = model.session.query(model.User).filter(model.User.username == "Kirill").first()
        self.mainEl = mainElements.mainElements(self)
        self.mainEl.setVisible(True)
        print(self.user)

    def testAdmin(self):
        self.switch_connection("admin")
        self.user = model.session.query(model.User).filter(model.User.username == "Kirill").first()
        self.mainEl = mainElements.mainElements(self)
        self.mainEl.setVisible(True)

    def testUser(self):
        self.switch_connection("user")
        self.user = model.session.query(model.User).filter(model.User.username == "a").first()
        self.mainEl = mainElements.mainElements(self)
        self.mainEl.setVisible(True)

    def switch_connection(self, role):
        if model.session:
            model.session.close()
        if role.lower() == "admin":
            model.create_session("127.0.0.1", "root", "6547", "my_library")
            print("admin")
        elif role.lower() == "user":
            model.create_session("127.0.0.1", "user", "65478", "my_library")
            print('user')
        else:
            QMessageBox.warning(self, "Ошибка", "Неизвестная роль")
            self.close()



if __name__ == "__main__":
    #backup_mysql_db("root", "6547", "my_library", "C:/backup")
    test_connection("127.0.0.1", "user", "65478", "my_library")
    app = QApplication(sys.argv)
    window = dataBaseWindow()
    window.show()
    sys.exit(app.exec_())
