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
import random
from copy import deepcopy
from PySide6.QtMultimedia import QSoundEffect

from juego import Juego
class conecta(QMainWindow, Juego):
    def __init__(self):
        super().__init__()
        stylesheet = """
            QMainWindow {
                background-image: url("fondo4.png"); 
                background-repeat: no-repeat; 
                background-position: center;
            }
        """
        self.setStyleSheet(stylesheet)
        self.circulo_blanco  = QPixmap("circulo_blanco.png")
        self.circulo_rojo  = QPixmap("circulo_rojo.png")
        self.circulo_amarillo  = QPixmap("circulo_amarillo.png")
        self.circulo_blanco= self.circulo_blanco.scaledToWidth(20)
        self.circulo_rojo= self.circulo_rojo.scaledToWidth(20)
        self.circulo_amarillo= self.circulo_amarillo.scaledToWidth(20)
        self.hueco= QLabel()
        self.hueco.setPixmap(self.circulo_blanco)
        self.sonido_victoria = QSoundEffect()
        self.sonido_victoria.setSource(QUrl.fromLocalFile("victoria.wav"))
        self.sonido_victoria.setVolume(0.25)
        self.sonido_derrota = QSoundEffect()
        self.sonido_derrota.setSource(QUrl.fromLocalFile("derrota.wav"))
        self.sonido_derrota.setVolume(0.25)
        self.sonido_acierto = QSoundEffect()
        self.sonido_acierto.setSource(QUrl.fromLocalFile("acierto.wav"))
        self.sonido_acierto.setVolume(0.25)
        self.sonido_fallo = QSoundEffect()
        self.sonido_fallo.setSource(QUrl.fromLocalFile("fallo.wav"))
        self.sonido_fallo.setVolume(0.25)
        self.sonido_click = QSoundEffect()
        self.sonido_click.setSource(QUrl.fromLocalFile("click.wav"))
        self.sonido_click.setVolume(0.25)
        self.turno_texto= "Es el turno del jugador "
        self.puntuacion=100
        self.tablero = []
        self.space = " "
        self.figura1 = "|x|"
        self.figura2 = "|o|"
        self.figura0= "|-|"
        self.conecta = 4
        self.jugador=1
        self.setWindowTitle("Conecta4")
        self.layoutV = QVBoxLayout()
        self.b1 = QPushButton("1")
        self.b1.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")     
        self.b2 = QPushButton("2")
        self.b2.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")     
        self.b3 = QPushButton("3")
        self.b3.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")     
        self.b4 = QPushButton("4")
        self.b4.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")     
        self.b5 = QPushButton("5")
        self.b5.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")     
        self.b6 = QPushButton("6")
        self.b6.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")     
        self.b7 = QPushButton("7")
        self.b7.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")     
        self.fin = QPushButton(self.texto_cerrar)
        self.fin.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        if(self.jugador==1):
            figura=" (x)"
        else:
            figura=" (o)"
        self.turno = QPushButton(str(self.turno_texto)+str(self.jugador)+str(figura))
        self.turno.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.contenedor= QWidget()
        self.contenedor.setLayout(self.crear_tablero())
        self.b1.clicked.connect(lambda: self.colocar_ficha(0, self.jugador))
        self.b2.clicked.connect(lambda: self.colocar_ficha(1, self.jugador))
        self.b3.clicked.connect(lambda: self.colocar_ficha(2,self.jugador))
        self.b4.clicked.connect(lambda: self.colocar_ficha(3,self.jugador))
        self.b5.clicked.connect(lambda: self.colocar_ficha(4,self.jugador))
        self.b6.clicked.connect(lambda: self.colocar_ficha(5,self.jugador))
        self.b7.clicked.connect(lambda: self.colocar_ficha(6,self.jugador))
        self.setCentralWidget(self.contenedor)
    def colocar_ficha(self,columna,jugador):
        self.sonido_click.play()
        fila= self.pedir_fila(columna)
        if(self.tablero[fila][columna]==self.figura0):
            if(jugador==1):
                self.tablero[fila][columna]=self.figura1
                self.jugador=2
            else:
                self.tablero[fila][columna]=self.figura2
                self.jugador=1
        else:
            print("Columna no válida")
        
        self.actualizar_tablero()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    if(widget!=self.fin):
                        widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
    def actualizar_tablero(self):
        self.clearLayout(self.layoutV)
        for fila in range(6):
            layoutH = QHBoxLayout()
            for columna in range(7):
                if(self.tablero[fila][columna]==self.figura1):
                    hueco= QLabel()
                    hueco.setPixmap(self.circulo_amarillo)
                    layoutH.addWidget(hueco, 0, Qt.AlignCenter)
                elif(self.tablero[fila][columna]==self.figura2):
                    hueco= QLabel()
                    hueco.setPixmap(self.circulo_rojo)
                    layoutH.addWidget(hueco, 0, Qt.AlignCenter)
                else:
                    hueco= QLabel()
                    hueco.setPixmap(self.circulo_blanco)
                    layoutH.addWidget(hueco, 0, Qt.AlignCenter)
            self.layoutV.addLayout(layoutH)
        if(self.jugador==1):
            figura=" (x)"
        else:
            figura=" (o)"
        if(self.juegoFin()==True):
            self.turno = QPushButton("Juego finalizado porque el tablero está lleno.")
            self.turno.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        else:
            self.turno = QPushButton(str(self.turno_texto)+str(self.jugador))
            if(self.jugador==1):
                self.turno.setStyleSheet("background-color: #1520A6;"
                                            "color: orange;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
            else:
                self.turno.setStyleSheet("background-color: #1520A6;"
                                            "color: red;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.b1 = QPushButton("1")
        self.b1.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;") 
        self.b2 = QPushButton("2")
        self.b2.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;") 
        self.b3 = QPushButton("3")
        self.b3.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;") 
        self.b4 = QPushButton("4")
        self.b4.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;") 
        self.b5 = QPushButton("5")
        self.b5.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;") 
        self.b6 = QPushButton("6")
        self.b6.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;") 
        self.b7 = QPushButton("7")
        self.b7.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: red;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;") 
        # self.fin = QPushButton("Fin del juego")
        self.b1.clicked.connect(lambda: self.colocar_ficha(0, self.jugador))
        self.b2.clicked.connect(lambda: self.colocar_ficha(1, self.jugador))
        self.b3.clicked.connect(lambda: self.colocar_ficha(2,self.jugador))
        self.b4.clicked.connect(lambda: self.colocar_ficha(3,self.jugador))
        self.b5.clicked.connect(lambda: self.colocar_ficha(4,self.jugador))
        self.b6.clicked.connect(lambda: self.colocar_ficha(5,self.jugador))
        self.b7.clicked.connect(lambda: self.colocar_ficha(6,self.jugador))
        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(self.b1)
        layoutH2.addWidget(self.b2)
        layoutH2.addWidget(self.b3)
        layoutH2.addWidget(self.b4)
        layoutH2.addWidget(self.b5)
        layoutH2.addWidget(self.b6)
        layoutH2.addWidget(self.b7)
        layoutH3= QHBoxLayout()
        layoutH3.addWidget(self.turno)
        layoutH3.addWidget(self.fin)
        self.layoutV.addLayout(layoutH2)
        self.layoutV.addLayout(layoutH3)
    def pedir_fila(self,columna):
        fila_libre=5
        while True:
            try:
                respuesta= True
                while(respuesta):
                    if(self.tablero[fila_libre][columna]!="|-|"):
                        fila_libre=fila_libre-1
                    elif(self.tablero[fila_libre][columna]=="|-|"):
                        fila= fila_libre
                        respuesta=False
                return fila
            except:
                return -1

    def crear_tablero(self):
        
        
        for fila in range(6):
            layoutH = QHBoxLayout()
            self.tablero.append([])
            for columna in range(7):
                self.tablero[fila].append(self.figura0)
                vacio = QLabel(self.tablero[fila][columna])
                hueco= QLabel()
                hueco.setPixmap(self.circulo_blanco)
                layoutH.addWidget(hueco, 0, Qt.AlignCenter)
            self.layoutV.addLayout(layoutH)
        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(self.b1)
        layoutH2.addWidget(self.b2)
        layoutH2.addWidget(self.b3)
        layoutH2.addWidget(self.b4)
        layoutH2.addWidget(self.b5)
        layoutH2.addWidget(self.b6)
        layoutH2.addWidget(self.b7)
        self.layoutV.addLayout(layoutH2)
        layoutH3 = QHBoxLayout()
        layoutH3.addWidget(self.turno)
        layoutH3.addWidget(self.fin)
        self.layoutV.addLayout(layoutH3)
        return self.layoutV
    def juegoFin(self):
        for columna in range(len(self.tablero[0])):
            if self.pedir_fila(columna) != -1:
                return False
        return True

    def rejugar(self):
        while True:
            eleccion = input("¿Quieres jugar otra partida? (s/n) ").lower()
            if eleccion == "s":
                return True
            elif eleccion == "n":
                return False
