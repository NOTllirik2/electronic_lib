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
