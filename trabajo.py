from datetime import datetime
from pathlib import Path
import random
import sys, os
import textwrap
from tkinter import CENTER
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel, QWidget, QAbstractItemView, QVBoxLayout, QMessageBox, QFormLayout, QTextEdit, QSpinBox
from Qt import QtCore, QtGui
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
from BlackJack import BlackJack
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
        self.titulo = QLabel("SimpleGames")
        self.titulo.setStyleSheet("background-color: #64C5DA;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 74px;"
                                        "min-width: 10em;"
                                        "margin:80px;"
                                        "padding: 6px;")
        self.titulo.setAlignment(Qt.AlignCenter)
        # self.titulo.setMaximumWidth(30)
        self.creditos = QLabel("Creado por Daniel Mera Sachse")
        self.creditos.setStyleSheet("background-color: #64C5DA;"
                                        "color: white;"
                                    "border-style: outset;"
                                    "border-width: 2px;"
                                    "border-radius: 210px;"
                                    "border-color: blue;"
                                    "font: 8px;"
                                    "min-width: 10em;"
                                    "margin:80px;"
                                    "padding: 6px;")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.ayuda = QPushButton("Ayuda")
        self.boton_jugar = QPushButton("Jugar")
        self.boton_estadisticas = QPushButton("Estadísticas")
        self.boton_salir = QPushButton("Salir")
        self.boton_blackjack = QPushButton("BlackJack")
        self.boton_conecta = QPushButton("Conecta4")
        self.boton_battleship = QPushButton("Battleship")
        self.boton_hangman = QPushButton("Hangman")
        self.boton_back = QPushButton("Atrás")
        self.boton_blackjack.setVisible(False)
        self.boton_conecta.setVisible(False)
        self.boton_battleship.setVisible(False)
        self.boton_hangman.setVisible(False)
        self.boton_back.setVisible(False)
        self.boton_jugar.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.boton_estadisticas.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.boton_salir.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.boton_blackjack.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.boton_conecta.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.boton_battleship.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.boton_hangman.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.boton_back.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
 
        self.boton_jugar.clicked.connect(lambda: self.visibilidad_menu(0))
        self.boton_estadisticas.clicked.connect(self.boton_estadisticas_clicked)
        self.boton_salir.clicked.connect(self.close)
        self.boton_blackjack.clicked.connect(self.boton_blackjack_clicked)
        self.boton_conecta.clicked.connect(self.boton_conecta_clicked)
        self.boton_battleship.clicked.connect(self.boton_battleship_clicked)
        self.boton_hangman.clicked.connect(self.boton_hangman_clicked)
        self.boton_back.clicked.connect(lambda: self.visibilidad_menu(1))

        self.layout.addWidget(self.titulo)
        self.layout.addWidget(self.boton_jugar, 0, Qt.AlignCenter)
        self.layout.addWidget(self.boton_estadisticas, 0, Qt.AlignCenter)
        self.layout.addWidget(self.boton_salir, 0, Qt.AlignCenter)
        self.layout.addWidget(self.boton_blackjack, 0, Qt.AlignCenter)
        self.layout.addWidget(self.boton_conecta, 0, Qt.AlignCenter)
        self.layout.addWidget(self.boton_battleship, 0, Qt.AlignCenter)
        self.layout.addWidget(self.boton_hangman, 0, Qt.AlignCenter)
        self.layout.addWidget(self.boton_back, 0, Qt.AlignCenter)
        self.layout.addWidget(self.creditos, 0, Qt.AlignRight)
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)
    def visibilidad_menu(self, accion):
        if(accion==0):
            self.boton_jugar.setVisible(False)
            self.boton_estadisticas.setVisible(False)
            self.boton_salir.setVisible(False)
            self.boton_blackjack.setVisible(True)
            self.boton_conecta.setVisible(True)
            self.boton_battleship.setVisible(True)
            self.boton_hangman.setVisible(True)
            self.boton_back.setVisible(True)
            self.creditos.setVisible(True)
        else:
            self.boton_jugar.setVisible(True)
            self.boton_estadisticas.setVisible(True)
            self.boton_salir.setVisible(True)
            self.boton_blackjack.setVisible(False)
            self.boton_conecta.setVisible(False)
            self.boton_battleship.setVisible(False)
            self.boton_hangman.setVisible(False)
            self.boton_back.setVisible(False)
            self.creditos.setVisible(True)
    def button_clicked(self, s, puntuacion, juego):
        self.wizard = QWizard()
        self.wizard.setWizardStyle(QWizard.ModernStyle)
        self.wizard.setWindowTitle("Agrega nueva puntuación")
        self.watermark  = QPixmap("sg5.png")
        self.wizard.setPixmap(QWizard.WatermarkPixmap,self.watermark)
        self.wizard.setFixedSize(700,400)
        self.wizard.setPixmap(QWizard.LogoPixmap,QPixmap('sg4.png'))
        page1 = QWizardPage()
        page1.setTitle('Acabas de finalizar una partida, regístrelo en estadísticas')
        page1.setSubTitle('Has sacado una puntuación de '+str(puntuacion)+" en el juego de "+juego)
        self.label_nombre = QLabel()
        self.label_nombre.setText("Introduce tu nombre")
        self.nombre = QLineEdit()
        hLayout1 = QHBoxLayout(page1)
        hLayout1.addWidget(self.label_nombre)
        hLayout1.addWidget(self.nombre)
        
        page1.registerField('miCampo1*', self.nombre,self.nombre.text(),'textChanged')
        self.wizard.addPage(page1)
        self.juego_elegido = QLabel(juego)
        self.score = str(puntuacion)
        self.puntuacion = QLabel(self.score)
        page1.setFinalPage(True)
        finish = self.wizard.button(QWizard.FinishButton)
        finish.clicked.connect(self.insertar)
        self.wizard.show()
    def insertar(self):
        nombre_limpio = self.nombre.text()
        nombre_limpio=nombre_limpio.replace('"','')
        nombre_limpio=nombre_limpio.replace(';','')
        nombre_limpio=nombre_limpio.replace("'","")
        nombre_limpio=nombre_limpio.replace('?','')
        nombre_limpio=nombre_limpio.replace('-','')
        nombre_limpio=nombre_limpio.replace('!','')
        nombre=nombre_limpio
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
    def boton_estadisticas_clicked(self, checked):
        self.estadisticas = AnotherWindow()
        if self.estadisticas.isVisible():
            self.estadisticas.hide()
        else:
            self.estadisticas.show()
    def button4_clicked(self,s):
        self.setCentralWidget(self.contenedor)
    def boton_blackjack_clicked(self,s):
        juego= BlackJack()
        juego.showMaximized()
        juego.fin.clicked.connect(lambda: self.asistente(s, juego, "BlackJack"))
    def boton_conecta_clicked(self,s):
        juego= conecta()
        juego.showMaximized()
        juego.fin.clicked.connect(lambda: self.asistente(s, juego, "Conecta4"))
    def boton_battleship_clicked(self,s):
        juego= battleship()
        juego.showMaximized()
        juego.fin.clicked.connect(lambda: self.asistente(s, juego, "BattleShip"))
    def boton_hangman_clicked(self,s):
        juego= hangman()
        juego.showMaximized()
        juego.fin.clicked.connect(lambda: self.asistente(s, juego, "Hangman"))
    def asistente(self,s, ventana, nombre_juego):
        if(nombre_juego=="Conecta4"):
            self.sonido_victoria.play()
        ventana.close()
        puntuacion= ventana.obtener_puntuacion()
        self.button_clicked(s, puntuacion, nombre_juego)
    def closeEvent(self, event):
            print("---")