from datetime import datetime
from pathlib import Path
import random
import sys, os
import textwrap
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel, QWidget, QAbstractItemView, QVBoxLayout, QMessageBox, QFormLayout, QTextEdit, QSpinBox
from Qt import QtGui
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel
from design import Ui_MainWindow
import pyqtgraph as pg
import pyqtgraph.exporters
from PySide6 import QtWidgets, QtGui
class AnotherWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Informe")
        self.web = QWebEngineView()
        self.web.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        ruta = Path("result.pdf")
        ruta.absolute().as_uri()
        self.web.load(QUrl(ruta.absolute().as_uri()))
        self.setCentralWidget(self.web)