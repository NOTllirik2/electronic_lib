import sys, os
import model

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow, QLabel, QPushButton, QLineEdit, \
    QApplication, QWidget, QVBoxLayout, QCheckBox, QScrollArea, QComboBox, QTextEdit, QToolBar, QAction, QFileDialog, \
    QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, QSize, QPropertyAnimation, QRect, Qt
from functools import partial

from sqlalchemy import (
    Column, Integer, String, Date, BigInteger, ForeignKey, CheckConstraint,
    Boolean, DECIMAL, UniqueConstraint, create_engine, insert, delete, and_, or_, select, update, func, select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional, List, Tuple


class autorisationWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(int(self.parent.width() / 3), int(self.parent.height() / 3) - 100, int(self.parent.width() / 3),
                         int(self.parent.height() / 3) + 100)

        # Layout для меню
        self.menu_layout = QVBoxLayout(self)
        self.setLayout(self.menu_layout)

        # Элемент QLabel для фона (если он нужен)
        self.background = QLabel(self)
        self.background.setStyleSheet("background-color: rgb(221, 221, 221);")
        self.menu_layout.addWidget(self.background)

        self.label1 = QLabel("Введите email:", self)
        self.label1.setGeometry(30, 20, 200, 30)

        self.text1 = QTextEdit(self)
        self.text1.setGeometry(30, 60, 200, 30)

        self.label2 = QLabel("Введите имя пользователя:", self)
        self.label2.setGeometry(30, 100, 200, 30)

        self.text2 = QTextEdit(self)
        self.text2.setGeometry(30, 140, 200, 30)

        self.label3 = QLabel("Введите пароль:", self)
        self.label3.setGeometry(30, 190, 200, 30)

        self.text3 = QTextEdit(self)
        self.text3.setGeometry(30, 220, 200, 30)

        self.okButton = QPushButton("Ok", self)
        self.okButton.setGeometry(30, 270, 70, 40)
        self.okButton.clicked.connect(self.okButtonPressed)

        self.buttonLogin = QPushButton("Вход", self)
        self.buttonLogin.setGeometry(9, 345, 240, 50)
        self.buttonLogin.clicked.connect(self.buttonLoginPressed)
        self.buttonLogin.setStyleSheet("background-color: lightBlue;")

        self.buttonAut = QPushButton("Авторизация", self)
        self.buttonAut.setGeometry(245, 345, 245, 50)
        self.buttonAut.clicked.connect(self.buttonAutPressed)
        self.buttonAut.setStyleSheet("background-color: white;")

        self.isLogin = 1
        self.buttonLoginPressed()

    def okButtonPressed(self):
        email = self.text1.toPlainText()

        t = email.split('@')
        if len(t) != 2:
            self.show_message("неверный формат email")
            return

        name = self.text2.toPlainText()
        password = self.text3.toPlainText()

        session = model.session
        User = model.User

        if self.isLogin == 1:
            user = session.query(User).filter(User.email == email, User.password_hash == password).first()
            if user == None:
                 self.show_message("Неверный логин или пароль")
            else:
                self.parent.user = user
                self.parent.userWasAutorized()
        else:
            user = session.query(User).filter(User.email == email).first()
            if user != None:
                self.show_message("email уже занят")
                return

            user2 = session.query(User).filter(User.username == name).first()
            if user2 != None:
                self.show_message("имя уже занято")
                return

            user = model.User(email=email, username=name, password_hash=password, role="User")
            session.add(user)
            session.commit()

            user = session.query(User).filter(User.email == email, User.password_hash == password).first()
            self.parent.user = user
            self.parent.userWasAutorized()

    def show_message(self, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def buttonLoginPressed(self):
        self.buttonLogin.setStyleSheet("background-color: lightBlue;")
        self.buttonAut.setStyleSheet("background-color: white;")
        self.isLogin = 1
        self.text1.clear()
        self.text2.clear()
        self.text3.clear()
        self.label2.setVisible(False)
        self.text2.setVisible(False)

        self.label1.setGeometry(30, 40, 200, 30)
        self.text1.setGeometry(30, 80, 200, 30)
        self.label3.setGeometry(30, 130, 200, 30)
        self.text3.setGeometry(30, 170, 200, 30)

        self.okButton.setGeometry(30, 270, 70, 40)

    def buttonAutPressed(self):
        self.buttonLogin.setStyleSheet("background-color: white;")
        self.buttonAut.setStyleSheet("background-color: lightBlue;")
        self.isLogin = 0
        self.text1.clear()
        self.text2.clear()
        self.text3.clear()
        self.label2.setVisible(True)
        self.text2.setVisible(True)

        self.label1.setGeometry(30, 20, 200, 30)
        self.text1.setGeometry(30, 60, 200, 30)
        self.label2.setGeometry(30, 100, 200, 30)
        self.text2.setGeometry(30, 140, 200, 30)
        self.label3.setGeometry(30, 190, 200, 30)
        self.text3.setGeometry(30, 220, 200, 30)

        self.okButton.setGeometry(30, 270, 70, 40)