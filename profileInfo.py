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

class profileInfo(QWidget):
    def __init__(self, parent):
        super().__init__(parent.parent)
        self.parent = parent
        self.user = parent.user
        self.setGeometry(0,
                         0,
                         1000,
                         1000)

        # Layout для меню
        self.menu_layout = QVBoxLayout(self)
        self.setLayout(self.menu_layout)

        # Элемент QLabel для фона (если он нужен)
        self.background = QLabel(self)
        self.background.setStyleSheet("background-color: rgb(201, 201, 201);")
        self.menu_layout.addWidget(self.background)

        self.name = QLabel(self.user.username, self)
        self.name.setGeometry(30, 30, 400, 100)
        self.name.setFont(QFont('Arial', 30))

        #===========================================
        self.nBookBack = QLabel(self)
        self.nBookBack.setGeometry(50, 150, 500, 300)
        self.nBookBack.setStyleSheet("background-color: rgb(255, 255, 255);")

        book_count = (
            model.session.query(func.count(model.user_book_association.c.book_id))
            .filter(model.user_book_association.c.user_id == self.user.id)
            .scalar()
        )

        self.nBookTitle = QLabel("Количетсво книг: ", self)
        self.nBookTitle.setGeometry(75, 175, 400, 70)
        self.nBookTitle.setFont(QFont('Arial', 30))

        self.nBook = QLabel(str(book_count), self)
        self.nBook.setGeometry(225, 300, 200, 50)
        self.nBook.setFont(QFont('Arial', 37))
        #===========================================
        self.nBookBack = QLabel(self)
        self.nBookBack.setGeometry(600, 150, 500, 300)
        self.nBookBack.setStyleSheet("background-color: rgb(255, 255, 255);")

        user_rank_query = (
            model.session.query(
                model.User.id,
                func.count(model.user_book_association.c.book_id).label('book_count')
            )
            .join(model.user_book_association, model.user_book_association.c.user_id == model.User.id)
            .group_by(model.User.id)
            .order_by(desc('book_count'))
            .subquery()
        )

        rank_query = (
            model.session.query(
                func.rank().over(order_by=user_rank_query.c.book_count.desc()).label('rank'),
                user_rank_query.c.id,
                user_rank_query.c.book_count
            )
            .filter(user_rank_query.c.id == self.parent.user.id)
        ).first()



        self.nBookTitle = QLabel("Топ по количеству книг: ", self)
        self.nBookTitle.setGeometry(625, 175, 500, 70)
        self.nBookTitle.setFont(QFont('Arial', 25))

        if not (rank_query is None):
            self.nBook = QLabel(str(rank_query[0]), self)
        else:
            self.nBook = QLabel("-", self)

        self.nBook.setGeometry(775, 300, 200, 50)
        self.nBook.setFont(QFont('Arial', 37))
        #===========================================
        self.nBookBack = QLabel(self)
        self.nBookBack.setGeometry(50, 500, 500, 300)
        self.nBookBack.setStyleSheet("background-color: rgb(255, 255, 255);")

        comment_count = (
            model.session.query(func.count(model.Comment.id))
            .filter(model.Comment.user_id == self.parent.user.id)
            .scalar()
        )

        self.nBookTitle = QLabel("Количество комментариев: ", self)
        self.nBookTitle.setGeometry(60, 510, 500, 70)
        self.nBookTitle.setFont(QFont('Arial', 22))

        if comment_count is None:
            self.nBook = QLabel("0", self)
        else:
            self.nBook = QLabel(str(comment_count), self)

        self.nBook.setGeometry(225, 650, 200, 50)
        self.nBook.setFont(QFont('Arial', 37))
        #===========================================
        self.nBookBack = QLabel(self)
        self.nBookBack.setGeometry(600, 500, 500, 300)
        self.nBookBack.setStyleSheet("background-color: rgb(255, 255, 255);")

        money_count = (
            model.session.query(func.sum(model.Transaction.amount))
            .filter(model.Transaction.user_id == self.user.id)
            .scalar()
        )


        self.nBookTitle = QLabel("Денег потрачено: ", self)
        self.nBookTitle.setGeometry(625, 525, 400, 70)
        self.nBookTitle.setFont(QFont('Arial', 30))

        if money_count is None:
            self.nBook = QLabel(f"0.00", self)
        else:
            self.nBook = QLabel(f"{money_count:.2f}", self)

        self.nBook.setGeometry(725, 650, 300, 50)
        self.nBook.setFont(QFont('Arial', 37))