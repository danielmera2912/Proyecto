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
        self.space = " "
        self.figura1 = "|·|"
        self.figura2 = "|o|"
        self.jugador1 = 1
        self.jugador2 = 2
        self.barcos_rotos1=0
        self.barcos_rotos2=0
        self.acierto=False
        self.setWindowTitle("Conecta4")

        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)
    def pedir_columna(self,tablero_visible):
        while True:
            try:
                respuesta= True
                while(respuesta):
                    columna= int(input("Ingresa la columna para ubicar tu ficha: "))-1
                    if(0<=columna<10 and (tablero_visible[0][columna]=="| |" or tablero_visible[1][columna]=="| |" or tablero_visible[2][columna]=="| |" or tablero_visible[3][columna]=="| |" or tablero_visible[4][columna]=="| |" or tablero_visible[5][columna]=="| |" or tablero_visible[6][columna]=="| |" or tablero_visible[7][columna]=="| |" or tablero_visible[8][columna]=="| |" or tablero_visible[9][columna]=="| |")):
                        respuesta= False
                    else:
                        respuesta=True
                return columna
            except:
                continue

    def pedir_fila(self,columna, tablero_visible):
        while True:
            try:
                respuesta= True
                while(respuesta):
                    fila= int(input("Ingresa la fila para ubicar tu ficha:"))-1
                    if(0<=fila<10 and tablero_visible[fila][columna]=="| |"):
                        respuesta=False
                return fila
            except:
                continue

    def crear_tablero(self):
        tablero = []
        for fila in range(10):
            tablero.append([])
            for columna in range(10):
                tablero[fila].append("| |")
        return tablero


    def mostrar_tablero(self,tablero,jugador):
        if(jugador==1):
            print("Tablero del jugador 1. Ha perdido "+str(self.barcos_rotos1)+" barcos. Y le queda "+str(17-self.barcos_rotos1)+" barcos.")
        else:
            print("Tablero del jugador 2. Ha perdido "+str(self.barcos_rotos2)+" barcos. Y le queda "+str(17-self.barcos_rotos2)+" barcos.")
        print("")
        print("|0 ||A||B||C||D||E||F||G||H||I||J|")
        for i in range(10):
            if(i+1<10):
                print(str("|"+str(i+1)+" |"), end="")
            else:
                print(str("|"+str(i+1)+"|"), end="")
            for j in range(10):
                print(tablero[i][j], end="")
            print("")
        print("")


    def colocar_pieza(self, tablero, tablero_visible, jugador):
        fila=-1
        while(fila==-1):
            print("Tu turno jugador "+str(jugador))
            columna = self.pedir_columna(tablero_visible)
            fila= self.pedir_fila(columna, tablero_visible)
        if(fila<=10 and columna<=10):
            if(tablero[fila][columna]=="| |"):
                tablero_visible[fila][columna]="|·|"
                self.acierto=False
            else:
                tablero_visible[fila][columna]="|X|"
                self.acierto=True
                if(jugador==1):
                    self.barcos_rotos1=self.barcos_rotos1+1
                else:
                    self.barcos_rotos2=self.barcos_rotos2+1
        else:
            print("Columna no válida")

    def establecer_barcos_solo(self, tablero):
        salida=-1
        while(salida==-1):
            fila= random.randint(0, 9)
            columna = random.randint(0, 9)
            if(tablero[fila][columna]=="| |"):
                tablero[fila][columna]="|z|"
                salida=0
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
        if(self.barcos_rotos1==17):
            print("Gana el jugador 1")
            return True
        elif(self.barcos_rotos2==17):
            print("Gana el jugador 2")
            return True
        else:
            return False


    def juego(self):
        tablero1= self.crear_tablero()
        tablero_visible1 = self.crear_tablero()
        tablero2= self.crear_tablero()
        tablero_visible2 = self.crear_tablero()
        self.establecer_barcos(tablero1)
        self.establecer_barcos(tablero2)
        self.mostrar_tablero(tablero_visible1,self.jugador1)
        self.mostrar_tablero(tablero_visible2,self.jugador2)
        figura=self.figura1
        jugador= self.jugador2
        cont=1
        while True:
            if(cont%2):
                while True:
                    self.colocar_pieza(tablero1, tablero_visible1,jugador)
                    self.mostrar_tablero(tablero_visible1,self.jugador1)
                    self.mostrar_tablero(tablero_visible2,self.jugador2)
                    
                    if(self.acierto==False):
                        jugador= self.jugador1
                        break
                    elif(self.barcos_rotos2==17):
                        break
            else:
                while True:
                    self.colocar_pieza(tablero2,tablero_visible2,jugador)
                    self.mostrar_tablero(tablero_visible1,self.jugador1)
                    self.mostrar_tablero(tablero_visible2,self.jugador2)
                    if(self.acierto==False):
                        jugador= self.jugador2
                        break
                    elif(self.barcos_rotos1==17):
                        break
            cont=cont+1
            if(self.comprobar_ganador()==False):
                eleccion = input("¿Volver a colocar ficha? (s/n) jugador"+str(jugador)+" ").lower()
                if eleccion == "s":
                    ...
                elif eleccion == "n":
                    break
            else:
                break
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
