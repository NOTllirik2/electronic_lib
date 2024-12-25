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
    Boolean, DECIMAL, UniqueConstraint, create_engine, insert, delete, and_, or_, select, update, func, select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional, List, Tuple


class bookInfo(QWidget):
    def __init__(self, parent, book):
        super().__init__(parent.parent)
        self.parent = parent
        self.user = parent.user
        self.setGeometry(300,
                         100,
                         self.parent.parent.width() - 300 * 2,
                         self.parent.parent.height() - 100 * 2)

        # Layout для меню
        self.menu_layout = QVBoxLayout(self)
        self.setLayout(self.menu_layout)
        self.book = book

        # Элемент QLabel для фона (если он нужен)
        self.background = QLabel(self)
        self.background.setStyleSheet("background-color: rgb(201, 201, 201);")
        self.menu_layout.addWidget(self.background)

        self.okButton = QPushButton("Ok", self)
        self.okButton.setGeometry(750, 600, 100, 50)
        self.okButton.clicked.connect(self.okButtonClicked)

        self.title = QLabel("title", self)
        self.title.setGeometry(50, 30, 1000, 50)

        font = QFont()
        font.setPointSize(20)
        self.title.setFont(font)

        self.authorsTitle = QLabel("Авторы: ", self)
        self.authorsTitle.setGeometry(70, 100, 1000, 50)
        self.authorsTitle.setFont(QFont("Arial", 17))

        self.authors = QLabel("authors", self)
        self.authors.setGeometry(90, 130, 1000, 50)
        self.authors.setFont(QFont("Arial", 14))

        self.genreTitle = QLabel("жанр: ", self)
        self.genreTitle.setGeometry(470, 100, 1000, 50)
        self.genreTitle.setFont(QFont("Arial", 17))

        self.genre = QLabel("genre", self)
        self.genre.setGeometry(490, 130, 1000, 50)
        self.genre.setFont(QFont("Arial", 14))

        self.descriptionTitle = QLabel("Описание: ", self)
        self.descriptionTitle.setGeometry(70, 200, 1000, 50)
        self.descriptionTitle.setFont(QFont("Arial", 17))

        self.desc = QLabel("descricption", self)
        self.desc.setGeometry(90, 240, 1000, 150)
        self.desc.setFont(QFont("Arial", 14))
        self.desc.setWordWrap(True)
        self.desc.setAlignment(Qt.AlignTop)

        self.comentTitle = QLabel("Коментарии: ", self)
        self.comentTitle.setGeometry(70, 300, 1000, 50)
        self.comentTitle.setFont(QFont("Arial", 17))

        self.comentText = QTextEdit(self)
        self.comentText.setFont(QFont("Arial", 12))
        self.comentText.setGeometry(70, 350, 650, 120)

        self.coment = QListWidget(self)
        self.coment.setGeometry(70, 500, 650, 180)
        self.coment.setSpacing(10)
        self.coment.setWordWrap(True)

        self.coment.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.canComment = 0

        self.addCommentButton = QPushButton("Опубликовать", self)
        self.addCommentButton.setGeometry(750, 420, 100, 50)
        self.addCommentButton.clicked.connect(self.addCommentButtonClicked)

    def loadComents(self):
        res = (model.session.query(model.Comment).
               filter(model.Comment.book_id == self.book.id,
                      model.Comment.user_id == self.user.id).first())

        if res:
            self.comentText.setText(res.content)

        res = (model.session.query(model.Comment.content, model.User.username, model.Comment.created_at).
               join(model.User, model.Comment.user_id == model.User.id).
               filter(model.Comment.book_id == self.book.id).order_by(model.Comment.created_at.desc()).all())

        self.coment.clear()
        for i in res:
            self.add_item_with_wordwrap(i[1], i[0], i[2])

    def addCommentButtonClicked(self):
        if self.canComment:
            res = model.session.query(model.Comment).filter(model.Comment.book_id == self.book.id,
                                                             model.Comment.user_id == self.user.id).first()
            if res:
                res.content = self.comentText.toPlainText()
                res.created_at = datetime.now()

                model.session.flush()
                model.session.commit()

                self.loadComents()
            else:
                text = self.comentText.toPlainText()

                c = model.Comment(
                    content=text,
                    user_id=self.user.id,
                    book_id=self.book.id,
                )

                model.session.add(c)
                model.session.commit()

    def add_item_with_wordwrap(self, name, text, date):
        item = QListWidgetItem()
        self.coment.addItem(item)

        label = QLabel("     " + name + " " * (70 - len(name)) + str(date) + '\n\n' + text, self)
        label.setWordWrap(True)
        label.setStyleSheet("border: none; padding: 5px;")
        label.setFixedWidth(self.coment.width() - 50)
        label.setFont(QFont("Arial", 11))

        item.setSizeHint(label.sizeHint())
        self.coment.setItemWidget(item, label)

    def okButtonClicked(self):
        self.setVisible(False)

    def loadInfo(self):
        self.comentText.setText("")
        self.title.setText(self.book.title)
        authors = model.session.query(model.Author.name).join(
            model.book_author_association, model.book_author_association.c.author_id == model.Author.id
        ).join(
            model.Book, model.Book.id == model.book_author_association.c.book_id
        ).filter(
            model.Book.id == self.book.id
        ).all()

        text = ""
        for i in range(len(authors)):
            text += authors[i][0]
            if i != len(authors) - 1:
                text += ", "

        if len(authors) != 1:
            self.authorsTitle.setText("Авторы: ")
        else:
            self.authorsTitle.setText("Автор: ")

        self.authors.setText(text)

        genre = model.session.query(model.Genre.name).join(
            model.book_genre_association, model.book_genre_association.c.genre_id == model.Genre.id
        ).join(
            model.Book, model.Book.id == model.book_genre_association.c.book_id
        ).filter(
            model.Book.id == self.book.id
        ).all()

        text = ""
        for i in range(len(genre)):
            text += genre[i][0]
            if i != len(genre) - 1:
                text += ", "

        if len(genre) != 1:
            self.genreTitle.setText("Жанры: ")
        else:
            self.genreTitle.setText("Жанр: ")

        self.genre.setText(text)

        self.desc.setText(self.book.description)

        user = self.parent.user
        book = self.book

        stmt = select(model.user_book_association).where(
            model.user_book_association.c.user_id == user.id,
            model.user_book_association.c.book_id == book.id
        )

        result = model.session.execute(stmt).fetchone()

        if result:
            self.comentTitle.setText("Коментарии: ")
            self.canComment = 1
        else:
            self.comentTitle.setText("Коментарии(Купите эту книгу, что-бы оставить коментарий): ")
            self.canComment = 0

        self.loadComents()
