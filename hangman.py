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
class hangman(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hangman")
        self.puntuacion= 0
        self.diccionario= ["HARRY POTTER", "LAS CRONICAS DE NARNIA", "ABECEDARIO", "DICCIONARIO", "COCHE", "VEHICULO AEREO", "BOTELLA DE AGUA", "RECICLAJE", "COLORES", "TETERA", "CHOCOLATE BLANCO", "PIZZA DE CUATRO QUESOS"]
        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)
    def introducir_palabra_secreta(self):
        palabra= str(input("Introduce la palabra secreta: "))
        palabra = palabra.upper()
        return palabra
    def palabra_aleatoria(self):
        numero= random.randrange(len(self.diccionario))
        return self.diccionario[numero]
    def pedir_letra(self):
        letras = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        while(True):
            letra= str(input("Introduce una letra: ")).upper()
            if(len(letra)!=1 or letra not in letras):
                print("Vuelve a intentarlo")
            else:
                return letra
    def juego(self):
        self.puntuacion=0
        letrasUsadas= []
        palabra_secreta= self.palabra_aleatoria()
        palabra_oculta= []
        espacios= 0
        for x in range(len(palabra_secreta)):
            if(palabra_secreta[x]==" "):
                palabra_oculta.append(" ")
                espacios=espacios+1
            else:
                palabra_oculta.append("_")
        palabra_secreta.find(" ")
        vidas= 3
        acierto= espacios
        print(" ".join(palabra_oculta))
        while(True):
            if(vidas==0 or acierto==len(palabra_secreta)):
                break
            else:
                letra= self.pedir_letra()
            if(letra in letrasUsadas):
                print("Letra repetida")
                print("Letras usadas: ")
                print(", ".join(letrasUsadas))
            
            else:
                letrasUsadas.append(letra)
                if(letra in palabra_secreta):
                    contador=0
                    for i in palabra_secreta:
                        if(i==letra):
                            palabra_oculta[contador]=letra
                            acierto=acierto+1
                        contador=contador+1
                    print("Letra acertada.")
                    print(" ".join(palabra_oculta))
                    print("Letras usadas: ")
                    print(", ".join(letrasUsadas))
                else:
                    print("Letra no acertada.")
                    print(" ".join(palabra_oculta))
                    print("Letras usadas: ")
                    print(", ".join(letrasUsadas))
                    vidas=vidas-1
                    print("Te quedan "+str(vidas)+" vidas")
        if(acierto==len(palabra_secreta)):
                    print("Victoria, la palabra secreta SÍ era "+palabra_secreta)
                    self.puntuacion= (vidas*5)+(acierto*3)
        else:
            print("Derrota, la palabra secreta era "+palabra_secreta)
            self.puntuacion=0
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
