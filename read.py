import sys, os

from sqlalchemy.sql.functions import user

import model

from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow, QLabel, QPushButton, QLineEdit, \
    QApplication, QWidget, QVBoxLayout, QCheckBox, QScrollArea, QComboBox, QTextEdit, QToolBar, QAction, QFileDialog, \
    QHBoxLayout, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QSize, QPropertyAnimation, QRect, Qt
from functools import partial

from sqlalchemy import (
    Column, Integer, String, Date, BigInteger, ForeignKey, CheckConstraint,
    Boolean, DECIMAL, UniqueConstraint, create_engine, insert, delete, and_, or_, select, update, func, select, desc)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional, List, Tuple

class readEl(QWidget):
    def __init__(self, parent, book):
        super().__init__(parent.parent)
        self.parent = parent
        self.user = parent.user
        self.setGeometry(300,
                         0,
                         self.parent.parent.width() - 300 * 2,
                         self.parent.parent.height() - 50)

        # Layout для меню
        self.menu_layout = QVBoxLayout(self)
        self.setLayout(self.menu_layout)
        self.book = book

        # Элемент QLabel для фона (если он нужен)
        self.background = QLabel(self)
        self.background.setStyleSheet("background-color: rgb(201, 201, 201);")
        self.menu_layout.addWidget(self.background)

        self.okButton = QPushButton("Закрыть", self)
        self.okButton.setGeometry(750, 20, 100, 50)
        self.okButton.clicked.connect(self.okButtonClicked)

        self.title = QLabel("title", self)
        self.title.setGeometry(50, 30, 600, 50)

        self.text = QTextEdit(self)
        self.text.setGeometry(50, 100, 800, 700)
        self.text.setFont(QFont("Arial", 14))

        font = QFont()
        font.setPointSize(20)
        self.title.setFont(font)

    def okButtonClicked(self):
        self.setVisible(False)

    def loadInfo(self):
        self.title.setText(self.book.title)
        self.text.setText(self.book.content)