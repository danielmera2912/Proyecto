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
class conecta(QMainWindow):
    def __init__(self):
        super().__init__()
        self.puntuacion=100
        self.space = " "
        self.figura1 = "|x|"
        self.figura2 = "|o|"
        self.jugador1 = 1
        self.jugador2 = 2
        self.conecta = 4
        self.setWindowTitle("Conecta4")

        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)
    def pedir_columna(self,figura):
        while True:
            try:
                respuesta= True
                while(respuesta):
                    fila= int(input("Ingresa la columna para ubicar tu ficha: "+figura+" "))-1
                    if(0<=fila<7):
                        respuesta=False
                return fila
            except:
                continue

    def pedir_fila(self,columna,tablero):
        fila_libre=5
        while True:
            try:
                respuesta= True
                while(respuesta):
                    if(tablero[fila_libre][columna]!="|-|"):
                        fila_libre=fila_libre-1
                    elif(tablero[fila_libre][columna]=="|-|"):
                        fila= fila_libre
                        respuesta=False
                return fila
            except:
                return -1

    def crear_tablero(self):
        tablero = []
        for fila in range(6):
            tablero.append([])
            for columna in range(7):
                tablero[fila].append("|-|")
        return tablero


    def mostrar_tablero(self,tablero):
        for i in range(6):
            print("")
            for j in range(7):
                print(tablero[i][j], end="")
        print("")
        print("---------------------")
        print("|1||2||3||4||5||6||7|")
        print("")
        

    def colocar_pieza(self, tablero, jugador, figura):
        fila=-1
        while(fila==-1):
            columna = self.pedir_columna(figura)
            fila= self.pedir_fila(columna,tablero)
        if(fila<=6 and columna<=7):
            if(tablero[fila][columna]=="|-|"):
                if(jugador==1):
                    tablero[fila][columna]="|x|"
                else:
                    tablero[fila][columna]="|o|"
            else:
                print("Columna no válida")
        else:
            print("Columna no válida")
        self.mostrar_tablero(tablero)


   

    def obtener_conteo(self,fila, columna, figura, tablero):
        ...

    def comprobar_ganador(self,jugador, tablero):
        ...

    def juegoFin(self,tablero):
        for columna in range(len(tablero[0])):
            if self.pedir_fila(columna, tablero) != -1:
                return False
        return True

    def juego(self):
        self.puntuacion=100
        tablero= self.crear_tablero()
        self.mostrar_tablero(tablero)
        figura=self.figura1
        cont=1
        while True:
            if(cont%2):
                self.colocar_pieza(tablero,self.jugador1,figura)
                figura=self.figura2
            else:
                self.colocar_pieza(tablero,self.jugador2,figura)
                figura=self.figura1
            cont=cont+1
            if(self.juegoFin(tablero)==True):
                    print("Juego finalizado porque el tablero está lleno.")
                    break
            else:
                eleccion = input("¿Volver a colocar ficha? (s/n) "+figura+" ").lower()
                if eleccion == "s":
                    ...
                elif eleccion == "n":
                    break
    def obtenerPuntuacion(self):
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
