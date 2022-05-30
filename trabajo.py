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
from PySide6.QtMultimedia import QSoundEffect
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
        self.sonido_victoria = QSoundEffect()
        self.sonido_victoria.setSource(QUrl.fromLocalFile("victoria.wav"))
        self.sonido_victoria.setVolume(0.25)
        self.sonido_musica = QSoundEffect()
        self.sonido_musica.setSource(QUrl.fromLocalFile("music.wav"))
        self.sonido_musica.setVolume(0.01)
        self.sonido_musica.setLoopCount(QSoundEffect.Infinite)
        self.sonido_musica.play()
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
        self.button7 = QPushButton("Hundir la flota")
        self.button8 = QPushButton("Ahorcado")
        self.button9 = QPushButton("Atrás")
        self.button5.setVisible(False)
        self.button6.setVisible(False)
        self.button7.setVisible(False)
        self.button8.setVisible(False)
        self.button9.setVisible(False)
        self.text_label = QLabel()
        self.text_label.setText("Hello World!")
        self.button1.setStyleSheet("border:7px solid #ff0000")
        self.button2.setStyleSheet("border:7px solid #ff0000")
        self.button3.setStyleSheet("border:7px solid #ff0000")
        self.button5.setStyleSheet("border:7px solid #ff0000")
        self.button6.setStyleSheet("border:7px solid #ff0000")
        self.button7.setStyleSheet("border:7px solid #ff0000")
        self.button8.setStyleSheet("border:7px solid #ff0000")
        self.button9.setStyleSheet("border:7px solid #ff0000")
        self.button1.setMinimumSize(50,50)
        self.button2.setMinimumSize(50,50)
        self.button3.setMinimumSize(50,50)
        self.button5.setMinimumSize(50,50)
        self.button6.setMinimumSize(50,50)
        self.button7.setMinimumSize(50,50)
        self.button8.setMinimumSize(50,50)
        self.button9.setMinimumSize(50,50)
        self.button1.clicked.connect(lambda: self.visibilidad_menu(0))
        self.button2.clicked.connect(self.button2_clicked)
        self.button3.clicked.connect(self.close)
        self.button5.clicked.connect(self.button5_clicked)
        self.button6.clicked.connect(self.button6_clicked)
        self.button7.clicked.connect(self.button7_clicked)
        self.button8.clicked.connect(self.button8_clicked)
        self.button9.clicked.connect(lambda: self.visibilidad_menu(1))
        self.w2 = AnotherWindow2()
    
        #self.button4.clicked.connect(self.button4_clicked)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button5)
        self.layout.addWidget(self.button6)
        self.layout.addWidget(self.button7)
        self.layout.addWidget(self.button8)
        self.layout.addWidget(self.button9)
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)
    def visibilidad_menu(self, accion):
        if(accion==0):
            self.button1.setVisible(False)
            self.button2.setVisible(False)
            self.button3.setVisible(False)
            self.button5.setVisible(True)
            self.button6.setVisible(True)
            self.button7.setVisible(True)
            self.button8.setVisible(True)
            self.button9.setVisible(True)
        else:
            self.button1.setVisible(True)
            self.button2.setVisible(True)
            self.button3.setVisible(True)
            self.button5.setVisible(False)
            self.button6.setVisible(False)
            self.button7.setVisible(False)
            self.button8.setVisible(False)
            self.button9.setVisible(False)
    def button_clicked(self, s, puntuacion, juego):
        self.wizard = QWizard()
        self.wizard.setWizardStyle(QWizard.ModernStyle)
        self.watermark  = QPixmap("sg.png")
        self.watermark = self.watermark.scaledToWidth(270)
        self.wizard.setPixmap(QWizard.WatermarkPixmap,self.watermark)
        self.wizard.setFixedSize(600,360)
        #self.wizard.setPixmap(QWizard.LogoPixmap,QPixmap('sg.png'))
        #self.wizard.setPixmap(QWizard.BannerPixmap,QPixmap('sg.png'))

        page1 = QWizardPage()
        page1.setTitle('Introduzca tu nombre')
        self.nombre = QLineEdit()
        hLayout1 = QHBoxLayout(page1)
        hLayout1.addWidget(self.nombre)
        page1.registerField('miCampo1*', self.nombre,self.nombre.text(),'textChanged')
        self.wizard.addPage(page1)

        page2 = QWizardPage()
        page2.setTitle('Juego elegido')
        self.juego_elegido = QLabel(juego)
        hLayout2 = QHBoxLayout(page2)
        hLayout2.addWidget(self.juego_elegido)

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
        juego=self.juego_elegido.text()
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
        self.w3.button3.clicked.connect(lambda: self.asistente(s, self.w3, "BlackJack"))
    def button6_clicked(self,s):
        self.w4= conecta()
        self.w4.showMaximized()
        self.w4.fin.clicked.connect(lambda: self.asistente(s, self.w4, "Conecta4"))
    def button7_clicked(self,s):
        self.w5= battleship()
        self.w5.showMaximized()
        self.w5.fin.clicked.connect(lambda: self.asistente(s, self.w5, "BattleShip"))
    def button8_clicked(self,s):
        self.w6= hangman()
        self.w6.showMaximized()
        self.w6.fin.clicked.connect(lambda: self.asistente(s, self.w6, "Hangman"))
    def asistente(self,s, ventana, nombre_juego):
        if(nombre_juego=="Conecta4"):
            self.sonido_victoria.play()
        ventana.close()
        puntuacion= ventana.obtener_puntuacion()
        self.button_clicked(s, puntuacion, nombre_juego)
    def closeEvent(self, event):
            print("---")