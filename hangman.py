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
        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)
    def introducir_palabraSecreta(self):
        palabra= str(input("Introduce la palabra secreta: "))
        palabra = palabra.upper()
        return palabra
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
        palabraSecreta= self.introducir_palabraSecreta()
        palabraOculta= []
        espacios= 0
        for x in range(len(palabraSecreta)):
            if(palabraSecreta[x]==" "):
                palabraOculta.append(" ")
                espacios=espacios+1
            else:
                palabraOculta.append("_")
        palabraSecreta.find(" ")
        vidas= 3
        acierto= espacios
        print(" ".join(palabraOculta))
        while(True):
            if(vidas==0 or acierto==len(palabraSecreta)):
                break
            else:
                letra= self.pedir_letra()
            if(letra in letrasUsadas):
                print("Letra repetida")
                print("Letras usadas: ")
                print(", ".join(letrasUsadas))
            
            else:
                letrasUsadas.append(letra)
                if(letra in palabraSecreta):
                    contador=0
                    for i in palabraSecreta:
                        if(i==letra):
                            palabraOculta[contador]=letra
                            acierto=acierto+1
                        contador=contador+1
                    print("Letra acertada.")
                    print(" ".join(palabraOculta))
                    print("Letras usadas: ")
                    print(", ".join(letrasUsadas))
                else:
                    print("Letra no acertada.")
                    print(" ".join(palabraOculta))
                    print("Letras usadas: ")
                    print(", ".join(letrasUsadas))
                    vidas=vidas-1
                    print("Te quedan "+str(vidas)+" vidas")
        if(acierto==len(palabraSecreta)):
                    print("Victoria, la palabra secreta SÍ era "+palabraSecreta)
                    self.puntuacion= (vidas*5)+(acierto*3)
        else:
            print("Derrota, la palabra secreta era "+palabraSecreta)
            self.puntuacion=0
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
