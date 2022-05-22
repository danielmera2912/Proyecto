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
class battleship(QMainWindow):
    def __init__(self):
        super().__init__()
        self.puntuacion=0
        self.barcos_totales=0
        self.barcos_rotos1=0
        self.barcos_rotos2=0
        self.tablero1 = []
        self.tablero2 = []
        self.tablero_botones1 = []
        self.tablero_botones2 = []
        self.tablero_botones = []
        self.space = " "
        self.figura0 = "| |"
        self.figura1 = "|·|"
        self.figura2 = "|o|"
        self.jugador1 = 1
        self.jugador2 = 2
        self.barcos_rotos1=0
        self.barcos_rotos2=0
        self.barcos_totales=0
        self.acierto=False
        self.botones_usados= []
        self.setWindowTitle("Battleship")
        self.turno = QPushButton("Comienza el jugador que desee")
        self.layoutH = QHBoxLayout()
        self.fin = QPushButton("Fin del juego")
        self.fin.setEnabled(False)
        self.layoutPrincipal = QVBoxLayout()
        self.layoutSecundario = QHBoxLayout()
        self.tablero1_visible= self.crear_tablero_visible(1)
        self.tablero2_visible= self.crear_tablero_visible(2)
        self.tablero1_no_visible= self.crear_tablero_no_visible()
        self.tablero2_no_visible= self.crear_tablero_no_visible()
        self.establecer_barcos(self.tablero1_no_visible)
        self.establecer_barcos(self.tablero2_no_visible)
        self.barcos_totales=self.barcos_totales/2
        self.layoutSecundario.addLayout(self.tablero1_visible)
        self.layoutSecundario.addLayout(self.tablero2_visible)
        self.cabecera = QHBoxLayout()
        self.texto1 = QPushButton("Tablero del Jugador 1")
        self.texto2 = QPushButton("Tablero del Jugador 2")
        self.cabecera.addWidget(self.texto1)
        self.cabecera.addWidget(self.texto2)
        self.layoutH3 = QHBoxLayout()
        self.layoutH3.addWidget(self.fin)
        self.layoutH3.addWidget(self.turno)
        self.datos_jugador1 = QPushButton("Jugador 1 posee "+str(int(self.barcos_totales))+" fragmentos de barcos.")
        self.datos_jugador2 = QPushButton("Jugador 2 posee "+str(int(self.barcos_totales))+" fragmentos de barcos.")
        self.layoutH4 = QHBoxLayout()
        self.layoutH4.addWidget(self.datos_jugador1)
        self.layoutH4.addWidget(self.datos_jugador2)
        self.layoutPrincipal.addLayout(self.cabecera)
        self.layoutPrincipal.addLayout(self.layoutSecundario)
        self.layoutPrincipal.addLayout(self.layoutH3)
        self.layoutPrincipal.addLayout(self.layoutH4)
        self.contenedor= QWidget()
        self.contenedor.setLayout(self.layoutPrincipal)
        figura=self.figura1
        self.jugador= self.jugador2
        self.cont=1
        self.setCentralWidget(self.contenedor)
        
        for fila in range(10):
            for columna in range(10):
                self.tablero_botones1[fila][columna].clicked.connect(self.colocar_pieza_tablero)
                self.tablero_botones1[fila][columna].fila= fila
                self.tablero_botones1[fila][columna].columna= columna
                self.tablero_botones1[fila][columna].jugador= 1
                self.tablero_botones2[fila][columna].clicked.connect(self.colocar_pieza_tablero)
                self.tablero_botones2[fila][columna].fila= fila
                self.tablero_botones2[fila][columna].columna= columna
                self.tablero_botones2[fila][columna].jugador= 2
    def comenzar_juego(self):
        while True:
            if(self.cont%2):
                while True:
                    for fila in range(10):
                        for columna in range(10):
                             self.tablero_botones1[fila][columna].setEnabled(True)
                             self.tablero_botones2[fila][columna].setEnabled(False)
                    if(self.acierto==False):
                        self.jugador= self.jugador1
                        break
                    elif(self.barcos_rotos2==self.barcos_totales):
                        break
            else:
                while True:
                    for fila in range(10):
                        for columna in range(10):
                             self.tablero_botones1[fila][columna].setEnabled(False)
                             self.tablero_botones2[fila][columna].setEnabled(True)
                    if(self.acierto==False):
                        self.jugador= self.jugador2
                        break
                    elif(self.barcos_rotos1==self.barcos_totales):
                        break
            
    def crear_tablero_visible(self, jugador):
        self.layoutV = QVBoxLayout()
        layoutH2= QHBoxLayout()
        layoutH2.addWidget(QPushButton(str("A")))
        layoutH2.addWidget(QPushButton(str("B")))
        layoutH2.addWidget(QPushButton(str("C")))
        layoutH2.addWidget(QPushButton(str("D")))
        layoutH2.addWidget(QPushButton(str("E")))
        layoutH2.addWidget(QPushButton(str("F")))
        layoutH2.addWidget(QPushButton(str("G")))
        layoutH2.addWidget(QPushButton(str("H")))
        layoutH2.addWidget(QPushButton(str("I")))
        layoutH2.addWidget(QPushButton(str("J")))
        self.layoutV.addLayout(layoutH2)
        for fila in range(10):
            layoutH = QHBoxLayout()
            layoutH.addWidget(QPushButton(str(fila+1)))
            
            if(jugador==1):
                self.tablero1.append([])
                self.tablero_botones1.append([])
            else:
                self.tablero2.append([])
                self.tablero_botones2.append([])
            for columna in range(10):
               
                if(jugador==1):
                    self.tablero1[fila].append("F"+str(fila+1)+".C"+str(columna+1))
                    # vacio = QPushButton()
                    vacio = QPushButton(self.tablero1[fila][columna])
                    self.tablero_botones1[fila].append(vacio)
                else:
                    self.tablero2[fila].append("F"+str(fila+1)+".C"+str(columna+1))
                    # vacio = QPushButton()
                    vacio = QPushButton(self.tablero2[fila][columna])
                    self.tablero_botones2[fila].append(vacio)
                layoutH.addWidget(vacio)
            self.layoutV.addLayout(layoutH)
        return self.layoutV
    def crear_tablero_no_visible(self):
        tablero = []
        for fila in range(10):
            tablero.append([])
            for columna in range(10):
                tablero[fila].append("| |")
        return tablero

    def colocar_pieza_tablero(self):
        button = self.sender()
        if(button.jugador==1):
            self.botones_usados.append(self.tablero_botones1[button.fila][button.columna])
            if(self.tablero1_no_visible[button.fila][button.columna]=="| |"):
                self.tablero1[button.fila][button.columna]="|·|"
                self.acierto=False
                self.tablero_botones1[button.fila][button.columna].setText("·")
                self.tablero_botones1[button.fila][button.columna].setStyleSheet("background-color: red")
                self.cont=self.cont+1
            else:
                self.tablero1[button.fila][button.columna]="|X|"
                self.tablero_botones1[button.fila][button.columna].setText("X")
                self.tablero_botones1[button.fila][button.columna].setStyleSheet("background-color: green")
                self.acierto=True
                self.barcos_rotos1=self.barcos_rotos1+1
                self.cont=self.cont+1
                self.datos_jugador1.setText("Jugador 1 posee "+str(int(self.barcos_totales-self.barcos_rotos1))+" fragmentos de barcos.")
                self.datos_jugador2.setText("Jugador 2 posee "+str(int(self.barcos_totales-self.barcos_rotos2))+" fragmentos de barcos.")
            if(self.comprobar_ganador()==False):
                if(self.acierto==False):
                    for fila in range(10):
                        for columna in range(10):
                                self.tablero_botones1[fila][columna].setEnabled(False)
                                self.tablero_botones2[fila][columna].setEnabled(True)
                    
                    self.turno.setText("Turno del jugador 1")
                else:
                    for fila in range(10):
                        for columna in range(10):
                                self.tablero_botones1[fila][columna].setEnabled(True)
                                self.tablero_botones2[fila][columna].setEnabled(False)
                    self.turno.setText("Turno del jugador 2")
                for i in range(len(self.botones_usados)):
                        self.botones_usados[i].setEnabled(False)
        elif(button.jugador==2):
            self.botones_usados.append(self.tablero_botones2[button.fila][button.columna])
            if(self.tablero2_no_visible[button.fila][button.columna]=="| |"):
                self.tablero2[button.fila][button.columna]="|·|"
                self.acierto=False
                self.tablero_botones2[button.fila][button.columna].setText("·")
                self.tablero_botones2[button.fila][button.columna].setStyleSheet("background-color: red")
                self.cont=self.cont+1
            else:
                self.tablero2[button.fila][button.columna]="|X|"
                self.tablero_botones2[button.fila][button.columna].setText("X")
                self.tablero_botones2[button.fila][button.columna].setStyleSheet("background-color: green")
                self.acierto=True
                self.barcos_rotos2=self.barcos_rotos2+1
                self.cont=self.cont+1
                self.datos_jugador1.setText("Jugador 1 posee "+str(int(self.barcos_totales-self.barcos_rotos1))+" fragmentos de barcos.")
                self.datos_jugador2.setText("Jugador 2 posee "+str(int(self.barcos_totales-self.barcos_rotos2))+" fragmentos de barcos.")
            if(self.comprobar_ganador()==False):
                if(self.acierto==False):
                    for fila in range(10):
                        for columna in range(10):
                                self.tablero_botones1[fila][columna].setEnabled(True)
                                self.tablero_botones2[fila][columna].setEnabled(False)
                    self.turno.setText("Turno del jugador 2")
                else:
                    for fila in range(10):
                        for columna in range(10):
                                self.tablero_botones1[fila][columna].setEnabled(False)
                                self.tablero_botones2[fila][columna].setEnabled(True)
                    self.turno.setText("Turno del jugador 1")
                for i in range(len(self.botones_usados)):
                        self.botones_usados[i].setEnabled(False)
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
        layoutH2= QHBoxLayout()
        layoutH2.addWidget(QPushButton(str("A")))
        layoutH2.addWidget(QPushButton(str("B")))
        layoutH2.addWidget(QPushButton(str("C")))
        layoutH2.addWidget(QPushButton(str("D")))
        layoutH2.addWidget(QPushButton(str("E")))
        layoutH2.addWidget(QPushButton(str("F")))
        layoutH2.addWidget(QPushButton(str("G")))
        layoutH2.addWidget(QPushButton(str("H")))
        layoutH2.addWidget(QPushButton(str("I")))
        layoutH2.addWidget(QPushButton(str("J")))
        self.layoutV.addLayout(layoutH2)
        for fila in range(10):
            layoutH = QHBoxLayout()
            layoutH.addWidget(QPushButton(str(fila+1)))
            self.tablero1.append([])
            for columna in range(10):
                self.tablero1[fila].append("F"+str(fila+1)+".C"+str(columna+1))
                # vacio = QPushButton()
                vacio = QPushButton(self.tablero[fila][columna])
                layoutH.addWidget(vacio)
            self.layoutV.addLayout(layoutH)
    def establecer_barcos_solo(self, tablero):
        salida=-1
        while(salida==-1):
            fila= random.randint(0, 9)
            columna = random.randint(0, 9)
            if(tablero[fila][columna]=="| |"):
                tablero[fila][columna]="|z|"
                salida=0
        self.barcos_totales=self.barcos_totales+1
    def establecer_barcos_dos_horizontal(self, tablero):
        salida=-1
        while(salida==-1):
            columna= random.randint(0, 9)
            if(columna==9):
                columna2=8
            elif(columna==0):
                columna2=1
            else:
                columna2=columna-1
            fila = random.randint(0, 9)
            if(tablero[fila][columna]=="| |" and tablero[fila][columna2]=="| |"):
                tablero[fila][columna]="|z|"
                tablero[fila][columna2]="|z|"
                salida=0
        self.barcos_totales=self.barcos_totales+2
    def establecer_barcos_dos_vertical(self, tablero):
        salida=-1
        while(salida==-1):
            fila= random.randint(0, 9)
            if(fila==9):
                fila2=8
            elif(fila==0):
                fila2=1
            else:
                fila2=fila-1
            columna = random.randint(0, 9)
            if(tablero[fila][columna]=="| |" and tablero[fila2][columna]=="| |"):
                tablero[fila][columna]="|z|"
                tablero[fila2][columna]="|z|"
                salida=0
        self.barcos_totales=self.barcos_totales+2
    def establecer_barcos_tres_horizontal(self, tablero):
        salida=-1
        while(salida==-1):
            columna= random.randint(0, 9)
            if(columna==9):
                columna2=8
                columna3=7
            elif(columna==0):
                columna2=1
                columna3=2
            else:
                columna2=columna-1
                columna3=columna+1
            fila = random.randint(0, 9)
            if(tablero[fila][columna]=="| |" and tablero[fila][columna2]=="| |" and tablero[fila][columna3]=="| |"):
                tablero[fila][columna]="|z|"
                tablero[fila][columna2]="|z|"
                tablero[fila][columna3]="|z|"
                salida=0
        self.barcos_totales=self.barcos_totales+3
    def establecer_barcos_tres_vertical(self, tablero):
        salida=-1
        while(salida==-1):
            fila= random.randint(0, 9)
            if(fila==9):
                fila2=8
                fila3=7
            elif(fila==0):
                fila2=1
                fila3=2
            else:
                fila2=fila-1
                fila3=fila+1
            columna = random.randint(0, 9)
            if(tablero[fila][columna]=="| |" and tablero[fila2][columna]=="| |" and tablero[fila3][columna]=="| |"):
                tablero[fila][columna]="|z|"
                tablero[fila2][columna]="|z|"
                tablero[fila3][columna]="|z|"
                salida=0
        self.barcos_totales=self.barcos_totales+3
    def establecer_barcos(self, tablero):
        self.establecer_barcos_dos_vertical(tablero)
        self.establecer_barcos_dos_vertical(tablero)
        self.establecer_barcos_dos_horizontal(tablero)
        self.establecer_barcos_dos_horizontal(tablero)
        self.establecer_barcos_tres_vertical(tablero)
        self.establecer_barcos_tres_horizontal(tablero)
        self.establecer_barcos_solo(tablero)
        self.establecer_barcos_solo(tablero)
        self.establecer_barcos_solo(tablero)


    def comprobar_ganador(self):
        if(self.barcos_rotos1==self.barcos_totales):
            self.turno.setText("Gana el jugador 1")
            self.puntuacion= 100-(self.barcos_rotos2*2)
            self.fin.setEnabled(True)
            for fila in range(10):
                for columna in range(10):
                        self.tablero_botones1[fila][columna].setEnabled(False)
                        self.tablero_botones2[fila][columna].setEnabled(False)
            return True
        elif(self.barcos_rotos2==self.barcos_totales):
            self.turno.setText("Gana el jugador 2")
            self.puntuacion= 100-(self.barcos_rotos1*2)
            self.fin.setEnabled(True)
            for fila in range(10):
                for columna in range(10):
                        self.tablero_botones1[fila][columna].setEnabled(False)
                        self.tablero_botones2[fila][columna].setEnabled(False)
            return True
        else:
            return False

    def obtener_puntuacion(self):
        return self.puntuacion
    def rejugar(self):
        while True:
            eleccion = input("¿Quieres jugar otra partida? (s/n) ").lower()
            if eleccion == "s":
                return True
            elif eleccion == "n":
                return False


    def main(self):
        while True:
            juego = self.juego()
            if not self.rejugar():
                break
