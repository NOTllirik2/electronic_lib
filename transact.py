import sys, os
import model

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow, QLabel, QPushButton, QLineEdit, \
    QApplication, QWidget, QVBoxLayout, QCheckBox, QScrollArea, QComboBox, QTextEdit, QToolBar, QAction, QFileDialog, \
    QHBoxLayout, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QSize, QPropertyAnimation, QRect, Qt
from functools import partial

from sqlalchemy import (
    Column, Integer, String, Date, BigInteger, ForeignKey, CheckConstraint,
    Boolean, DECIMAL, UniqueConstraint, create_engine, insert, delete, and_, or_, select, update, func, select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional, List, Tuple


class buyMenu(QWidget):
    def __init__(self, parent, book):
        super().__init__(parent.parent)
        self.parent = parent
        self.setGeometry(500,
                         200,
                         self.parent.parent.width() - 500 * 2,
                         self.parent.parent.height() - 200 * 2)

        self.menu_layout = QVBoxLayout(self)
        self.setLayout(self.menu_layout)
        self.book = book

        self.background = QLabel(self)
        self.background.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.menu_layout.addWidget(self.background)

        self.okButton = QPushButton("Ok", self)
        self.okButton.setGeometry(370, 420, 100, 50)
        self.okButton.clicked.connect(self.okButtonClicked)

        self.backButton = QPushButton("Назад", self)
        self.backButton.setGeometry(30, 420, 100, 50)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.titleTitle = QLabel("Вы хотите купить: ", self)
        self.titleTitle.setGeometry(50, 20, 1000, 50)
        self.titleTitle.setFont(QFont("Arial", 11))

        self.title = QLabel("title", self)
        self.title.setGeometry(50, 60, 400, 50)
        self.title.setFont(QFont("Arial", 15))

        self.priceTitle = QLabel("Цена покупки:", self)
        self.priceTitle.setGeometry(50, 120, 200, 50)
        self.priceTitle.setFont(QFont("Arial", 13))

        self.price = QLabel(str(self.book.price), self)
        self.price.setGeometry(200, 120, 1000, 50)
        self.price.setFont(QFont("Arial", 13))

        self.cardNumTitle = QLabel("Введите номер карты:", self)
        self.cardNumTitle.setGeometry(50, 200, 200, 50)
        self.cardNumTitle.setFont(QFont("Arial", 11))

        self.cardNum = QTextEdit(self)
        self.cardNum.setGeometry(50, 240, 300, 33)
        self.cardNum.setFont(QFont("Arial", 11))

        self.csvTitle = QLabel("Введите CSV:", self)
        self.csvTitle.setGeometry(50, 300, 280, 50)
        self.csvTitle.setFont(QFont("Arial", 11))

        self.csv = QTextEdit(self)
        self.csv.setGeometry(50, 340, 140, 33)
        self.csv.setFont(QFont("Arial", 11))

        # 00/00
        self.dataTitle = QLabel("Срок действия:", self)
        self.dataTitle.setGeometry(250, 300, 280, 50)
        self.dataTitle.setFont(QFont("Arial", 11))

        self.data = QTextEdit(self)
        self.data.setGeometry(250, 340, 140, 33)
        self.data.setFont(QFont("Arial", 11))

    def checkDataToCorrect(self):
        num = self.cardNum.toPlainText()
        csv = self.csv.toPlainText()
        data = self.data.toPlainText()

        if not num.isdigit() or not len(num) == 16:
            self.show_message("Номер карты не коректен")
            return 0

        if not csv.isdigit() or not len(csv) == 3:
            self.show_message("CSV не коректен")
            return 0

        dat = data.split('/')
        if not len(dat) == 2 or not dat[0].isdigit() or not len(dat[0]) == 2 or not dat[1].isdigit() or not len(
                dat[1]) == 2:
            self.show_message("Срок действия не коректен")
            return 0

        return 1

    def show_message(self, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def setCorrectData(self):
        self.cardNum.setText("1111111111111111")
        self.csv.setText("111")
        self.data.setText("11/11")

    def okButtonClicked(self):
        #self.setCorrectData()
        if self.checkDataToCorrect():

            user = self.parent.user
            book = self.book

            stmt = select(model.user_book_association).where(
                model.user_book_association.c.user_id == user.id,
                model.user_book_association.c.book_id == book.id
            )

            result = model.session.execute(stmt).fetchone()
            if result:
                self.show_message("У тебя уже есть такая книга")
                return

            print(user)
            print(book)
            user.purchased_books.append(book)
            t = model.Transaction(
                user_id=user.id,
                book_id=book.id,
                transaction_type="Online",
                amount=book.price,
                card_num=str(self.cardNum.toPlainText())
            )
            model.session.add(t)
            model.session.commit()
            self.setVisible(False)


    def backButtonClicked(self):
        self.setVisible(False)


    def loadInfo(self):
        self.cardNum.setText("")
        self.csv.setText("")
        self.data.setText("")

        user = self.parent.user
        book = self.book

        stmt = select(model.user_book_association).where(
            model.user_book_association.c.user_id == user.id,
            model.user_book_association.c.book_id == book.id
        )

        result = model.session.execute(stmt).fetchone()
        if result:
            self.show_message("У тебя уже есть такая книга")
            self.setVisible(False)
            return 0

        self.title.setText(self.book.title)
        self.price.setText(str(self.book.price))
        return 1
