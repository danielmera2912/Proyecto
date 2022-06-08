from datetime import datetime
from pathlib import Path
import random
import sys, os
import textwrap
from tkinter import CENTER
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QTabWidget, QSplitter, QComboBox, QMainWindow, QPushButton, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel, QWidget, QAbstractItemView, QVBoxLayout, QMessageBox, QFormLayout, QTextEdit, QSpinBox
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
from estadisticas import Estadisticas
from BlackJack import BlackJack
from Conecta4 import conecta
from battleship import battleship
from hangman import hangman
from PySide6.QtHelp import QHelpEngine
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtMultimedia import QSoundEffect
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

class HelpWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Ayuda del programa")
        
        # Creamos una instancia de QHelpEngine con el contenido del archivo de ayuda generado
        self.helpEngine = QHelpEngine("mycollection.qhc")
        # Con setupData cargamos los datos
        self.helpEngine.setupData()

        # Creamos un widget de pestañas en el que añadimos el índice de contenido y el índice de palabras clave
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.helpEngine.contentWidget(), "Contenido")

        # Creamos el visor web donde se mostrará la ayuda
        self.helpBrowser = QWebEngineView()

        # Cuando se haga doble clic en una palabra clave, se carga la url correspondiente
        self.helpEngine.indexWidget().linkActivated.connect(self.cargarUrl)
        # Cuando se haga doble clic en un capítulo, se carga la url correspondiente
        self.helpEngine.contentWidget().linkActivated.connect(self.cargarUrl)

        # Establecemos el contenido del navegador en la página principal de la ayuda
        self.helpBrowser.setContent(self.helpEngine.fileData(QUrl("qthelp://"+self.helpEngine.registeredDocumentations()[0]+"/doc/index.html")),"text/html")

        # Creamos un separador en el que ponemos las pestañas y el contenido
        self.splitter = QSplitter()
        self.splitter.insertWidget(0, self.tabWidget)
        self.splitter.insertWidget(1, self.helpBrowser)

        layout.addWidget(self.label)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
    
    # Método que recoge la url que emite la señal y la carga en el navegador
    def cargarUrl(self,url):
        self.helpBrowser.setContent(self.helpEngine.fileData(url),"text/html")
        print(url)

class HelpElementWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Ayuda del elemento")
        
        # Creamos una instancia de QHelpEngine con el contenido del archivo de ayuda generado
        self.helpEngine = QHelpEngine("mycollection.qhc")
        # Con setupData cargamos los datos
        self.helpEngine.setupData()

        # Creamos un widget de pestañas en el que añadimos el índice de contenido y el índice de palabras clave
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.helpEngine.contentWidget(), "Contenido")

        # Creamos el visor web donde se mostrará la ayuda
        self.helpBrowser = QWebEngineView()

        # Cuando se haga doble clic en una palabra clave, se carga la url correspondiente
        self.helpEngine.indexWidget().linkActivated.connect(self.cargarUrl)
        # Cuando se haga doble clic en un capítulo, se carga la url correspondiente
        self.helpEngine.contentWidget().linkActivated.connect(self.cargarUrl)

        

        # Creamos un separador en el que ponemos las pestañas y el contenido
        self.splitter = QSplitter()
        self.splitter.insertWidget(0, self.tabWidget)
        self.splitter.insertWidget(1, self.helpBrowser)

        layout.addWidget(self.label)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
    
    def cargarUrl(self,url):
        self.helpBrowser.setContent(self.helpEngine.fileData(url),"text/html")
        print(url)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sonido_victoria = QSoundEffect()
        self.sonido_victoria.setSource(QUrl.fromLocalFile("sonido/victoria.wav"))
        self.sonido_victoria.setVolume(0.25)
        self.sonido_musica = QSoundEffect()
        self.sonido_musica.setSource(QUrl.fromLocalFile("sonido/music.wav"))
        self.sonido_musica.setVolume(0.01)
        self.sonido_musica.setLoopCount(QSoundEffect.Infinite)
        self.sonido_musica.play()
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'logo/sg.ico')))
        self.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        self.setWindowTitle("SimpleGames")
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
        self.w = HelpWindow()
        #self.h = HelpElementWindow()
        self.w.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        #self.h.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        self.w.setWindowTitle("Ayuda")
        #self.h.setWindowTitle("Ayuda")
        self.ayuda = QPushButton("Ayuda")
        self.ayuda.clicked.connect(self.toggle_helpwindow)
        self.ayuda.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
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
        self.layout.addWidget(self.ayuda, 0, Qt.AlignRight)
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
    def toggle_helpwindow(self, checked):
        
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()

    # def toggle_elementhelpwindow(self, checked):
        
    #     if self.h.isVisible():
    #         self.h.hide()

    #     else:
    #         self.h.show()
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
    def agregar_estadistica(self, s, puntuacion, juego):
        self.wizard = QWizard()
        self.wizard.setWizardStyle(QWizard.ModernStyle)
        self.wizard.setWindowTitle("Agrega nueva puntuación")
        self.wizard.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        self.watermark  = QPixmap("logo/sg5.png")
        self.wizard.setPixmap(QWizard.WatermarkPixmap,self.watermark)
        self.wizard.setFixedSize(700,400)
        self.wizard.setPixmap(QWizard.LogoPixmap,QPixmap('logo/sg4.png'))
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
        self.estadisticas = Estadisticas()
        self.estadisticas.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        self.estadisticas.setWindowTitle("Estadísticas")
        if self.estadisticas.isVisible():
            self.estadisticas.hide()
        else:
            self.estadisticas.show()
    def boton_blackjack_clicked(self,s):
        juego= BlackJack()
        juego.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        juego.showMaximized()
        juego.fin.clicked.connect(lambda: self.asistente(s, juego, "BlackJack"))
    def boton_conecta_clicked(self,s):
        juego= conecta()
        juego.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        juego.showMaximized()
        juego.fin.clicked.connect(lambda: self.asistente(s, juego, "Conecta4"))
    def boton_battleship_clicked(self,s):
        juego= battleship()
        juego.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        juego.showMaximized()
        juego.fin.clicked.connect(lambda: self.asistente(s, juego, "BattleShip"))
    def boton_hangman_clicked(self,s):
        juego= hangman()
        juego.setWindowIcon(QtGui.QIcon('logo/sg.ico'))
        juego.showMaximized()
        juego.fin.clicked.connect(lambda: self.asistente(s, juego, "Hangman"))
    def asistente(self,s, ventana, nombre_juego):
        if(nombre_juego=="Conecta4"):
            self.sonido_victoria.play()
        ventana.close()
        puntuacion= ventana.obtener_puntuacion()
        self.agregar_estadistica(s, puntuacion, nombre_juego)
    def closeEvent(self, event):
            print("---")