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
from estadisticas import AnotherWindow
from informe import AnotherWindow2
from game21 import Game21
from Conecta4 import conecta
from battleship import battleship
from hangman import hangman
# La aplicación consistiría en pulsar a jugar y se elige el juego que se desea jugar,
#  saltaría la pantalla del juego y al acabar, salta el asistente para registrar tu puntuación en un informe
# en estadísticas se guarda las estadísticas locales en una base de datos, y el botón salir sale
basedir = os.path.dirname(__file__)
db = QSqlDatabase("QSQLITE")
db.setDatabaseName("chinook.sqlite")

db.open()
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'sg.ico')))
        #app.setWindowIcon(QtGui.QIcon('sg.ico'))
        self.setWindowTitle("App SimpGam")
        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.button1 = QPushButton("Jugar")
        self.button2 = QPushButton("Estadísticas")
        self.button3 = QPushButton("Salir")
        self.button5 = QPushButton("21Game")
        self.button6 = QPushButton("Conecta4")
        self.button7 = QPushButton("Destruir la flota")
        self.button8 = QPushButton("Ahorcado")
        self.text_label = QLabel()
        self.text_label.setText("Hello World!")
        self.button1.setStyleSheet("border:7px solid #ff0000")
        self.button2.setStyleSheet("border:7px solid #ff0000")
        self.button3.setStyleSheet("border:7px solid #ff0000")
        self.button5.setStyleSheet("border:7px solid #ff0000")
        self.button6.setStyleSheet("border:7px solid #ff0000")
        self.button7.setStyleSheet("border:7px solid #ff0000")
        self.button8.setStyleSheet("border:7px solid #ff0000")
        self.button1.setMinimumSize(50,50)
        self.button2.setMinimumSize(50,50)
        self.button3.setMinimumSize(50,50)
        self.button5.setMinimumSize(50,50)
        self.button6.setMinimumSize(50,50)
        self.button7.setMinimumSize(50,50)
        self.button8.setMinimumSize(50,50)
        # self.button1.clicked.connect(self.button_clicked)
        self.button2.clicked.connect(self.button2_clicked)
        self.button3.clicked.connect(self.close)
        self.button5.clicked.connect(self.button5_clicked)
        self.button6.clicked.connect(self.button6_clicked)
        self.button7.clicked.connect(self.button7_clicked)
        self.button8.clicked.connect(self.button8_clicked)
        
        self.w2 = AnotherWindow2()
        
        self.button4 = QPushButton()
        self.button4.setText("Salir")
        self.button4.clicked.connect(self.button4_clicked)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button5)
        self.layout.addWidget(self.button6)
        self.layout.addWidget(self.button7)
        self.layout.addWidget(self.button8)
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)
    def button_clicked(self, s, puntuacion, juego):
        self.wizard = QWizard()
        self.wizard.setWizardStyle(QWizard.ModernStyle)

        self.wizard.setPixmap(QWizard.WatermarkPixmap,QPixmap('Watermark.png'))
        self.wizard.setPixmap(QWizard.LogoPixmap,QPixmap('Logo.png'))
        self.wizard.setPixmap(QWizard.BannerPixmap,QPixmap('Banner.png'))

        page1 = QWizardPage()
        page1.setTitle('Introduzca tu nombre')
        self.nombre = QLineEdit()
        hLayout1 = QHBoxLayout(page1)
        hLayout1.addWidget(self.nombre)
        page1.registerField('miCampo1*', self.nombre,self.nombre.text(),'textChanged')
        self.wizard.addPage(page1)

        page2 = QWizardPage()
        page2.setTitle('Juego elegido')
        self.juegoElegido = QLabel(juego)
        hLayout2 = QHBoxLayout(page2)
        hLayout2.addWidget(self.juegoElegido)

        self.wizard.addPage(page2)

        page3 = QWizardPage()
        page3.setTitle('Puntuación obtenida')
        self.score = str(puntuacion)
        self.puntuacion = QLabel(self.score)
        hLayout3 = QHBoxLayout(page3)
        hLayout3.addWidget(self.puntuacion)
        page3.setFinalPage(True)
        next = self.wizard.button(QWizard.NextButton)

        finish = self.wizard.button(QWizard.FinishButton)
        self.wizard.addPage(page3)
        
        finish.clicked.connect(self.insertar)
        self.wizard.show()
    def insertar(self):
        nombre=self.nombre.text()
        puntuacion=self.puntuacion.text()
        juego=self.juegoElegido.text()
        self.modelo = QSqlRelationalTableModel(db=db)
        self.modelo.setTable("estadisticas")
        self.modelo.select()
        nuevaFila = self.modelo.rowCount()
        self.modelo.insertRow(nuevaFila)
        self.modelo.setData(self.modelo.index(nuevaFila, 0), nombre)
        self.modelo.setData(self.modelo.index(nuevaFila, 1), puntuacion)
        self.modelo.setData(self.modelo.index(nuevaFila, 2), juego)
        self.modelo.submit()
    def button2_clicked(self, checked):
        self.w = AnotherWindow()
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()
    def button4_clicked(self,s):
        self.setCentralWidget(self.contenedor)
    def button5_clicked(self,s):
        self.w3= Game21()
        self.w3.showMaximized()
        self.w3.button3.clicked.connect(self.asistente)
            
    def asistente(self,s):
        self.w3.close()
        puntuacion= self.w3.obtenerPuntuacion()
        self.button_clicked(s, puntuacion, "BlackJack")
    def closeEvent(self, event):
        print("---")
    def button6_clicked(self,s):
        self.w4= conecta()
        self.w4.showMaximized()
    def button7_clicked(self,s):
        self.w5= battleship()
        if self.w5.isVisible():
            self.w5.hide()
            self.w5.close()

        else:
            self.w5.show()
            self.w5.main()
        puntuacion= self.w5.obtenerPuntuacion()
        self.button_clicked(s, puntuacion, "Battleship")
        self.w5.close()
    def button8_clicked(self,s):
        self.w6= hangman()
        if self.w6.isVisible():
            self.w6.hide()
            self.w6.close()

        else:
            self.w6.show()
            self.w6.main()
        puntuacion= self.w6.obtenerPuntuacion()
        self.button_clicked(s, puntuacion, "Hangman")
        self.w6.close()