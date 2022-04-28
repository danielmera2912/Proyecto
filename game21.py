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
class Mano():
    def __init__(self, baraja, info):
        super().__init__()
        self.valor=0
        self.mano= []
        self.cartas= baraja
        self.cartas.barajar()
        self.info=info
    def comienzoPartida(self):
        for i in range(3):
            robo= self.cartas.cartas.pop()
            self.mano.append(robo)
    def robarCarta(self):
        try:
            robo= self.cartas.cartas.pop()
            self.mano.append(robo)
            if(self.info is True):
                robo.infoCarta()
            suma= 0
            for x in self.mano:
                suma+= x.numero
                self.valor=suma
        except:
            print("No se pueden robar más cartas, no hay mazo.")
    def enseñarMano(self):
        for x in range(0,len(self.mano)):
            self.mano[x].infoCarta()
    def infoMano(self):
        if(self.info is True):
            print("El valor de tus cartas son de "+str(self.valor))
class Carta():
    def __init__(self, numero, palo):
        super().__init__()
        self.numero=numero
        self.palo=palo
        self.paloT= ""
    def infoCarta(self):
        if(self.palo=="O"):
            self.paloT="Oro"
        elif(self.palo=="C"):
            self.paloT="Copas"
        elif(self.palo=="E"):
            self.paloT="Espadas"
        elif(self.palo=="B"):
            self.paloT="Bastos"
        print(str(self.numero)+" de "+self.paloT)
class BarajaCartas():
    def __init__(self):
        super().__init__()
        self.cartasB= []
        self.cartasE= []
        self.cartasC= []
        self.cartasO= []
        self.cartas= []
        for x in range(1,13):
            self.cartasB.append(Carta(x,"B"))
            self.cartasE.append(Carta(x,"E"))
            self.cartasC.append(Carta(x,"C"))
            self.cartasO.append(Carta(x,"O"))
        self.cartas= self.cartasO+self.cartasB+self.cartasC+self.cartasE
    
    def barajar(self):
        lista = self.cartas[:]
        longitud_lista = len(lista)
        for i in range(longitud_lista):
            indice_aleatorio = random.randint(0, longitud_lista - 1)
            temporal = lista[i]
            lista[i] = lista[indice_aleatorio]
            lista[indice_aleatorio] = temporal
        self.cartas=lista
    def mostrarBaraja(self):
        for x in range(0,len(self.cartas)):
            self.cartas[x].infoCarta()
class Game21(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("21 Game")

        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)


        #print(random.randrange(10))
        #self.cartas.append(self.crearCarta(1,"B"))
        #self.layout.addWidget(self.cartas[0])
        #self.layout.addWidget(self.cartas[x-1])
        #self.cartas= BarajaCartas()
        #self.cartas.barajar()
        #self.cartas.mostrarBaraja()
        #self.baraja= self.cartas.cartas
        


        
        
    def juego(self):
        self.baraja= BarajaCartas()
        self.mano = Mano(self.baraja, True)
        self.mano2 = Mano(self.baraja, False)
        #self.mano.comienzoPartida()
        self.mano.robarCarta()
        self.mano2.robarCarta()
        respuesta='s'
        while(respuesta=='s'):
            respuesta= input("¿Quieres robar una carta? (s/n): ")
            if(respuesta=='s'):
                self.mano.robarCarta()
                self.mano.infoMano()
                if(self.mano2.valor<=self.mano.valor and self.mano2.valor<21):
                    if(self.mano2.valor<10):
                        print("IA ha robado carta")
                        self.mano2.robarCarta()
                        self.mano2.infoMano()
                    elif(self.mano2.valor>10 and self.mano2.valor<15):
                        chances= random.randrange(10)
                        if(chances>4):
                            print("IA ha robado carta")
                            self.mano2.robarCarta()
                            self.mano2.infoMano()
                    elif(self.mano2.valor>15 and self.mano2.valor<20):
                        chances= random.randrange(3)
                        if(chances==2):
                            print("IA ha robado carta")
                            self.mano2.robarCarta()
                            self.mano2.infoMano()
                    elif(self.mano2.valor==20):
                        chances= random.randrange(10)
                        if(chances==5):
                            print("IA ha robado carta")
                            self.mano2.robarCarta()
                            self.mano2.infoMano()
        print("Mano del jugador:")
        self.mano.enseñarMano()
        print(self.mano.valor)
        print("Mano de la IA")
        self.mano2.enseñarMano()
        print(self.mano2.valor)
        if(self.mano.valor==21 and self.mano2.valor!=21):
            print("Jugador ha ganado")
        elif(self.mano.valor==21 and self.mano2.valor==21):
            print("Empate")
        elif(self.mano2.valor==21 and self.mano.valor==21):
            print("IA ha ganado")
        else:
            if(self.mano.valor>21 and self.mano2.valor<21):
                print("IA ha ganado")
            elif(self.mano2.valor>21 and self.mano.valor<21):
                print("Jugador ha ganado")
            else:
                if(self.mano.valor>21 and self.mano2.valor>21):
                    if(self.mano.valor<self.mano2.valor):
                        print("Jugador ha ganado")
                    elif(self.mano2.valor<self.mano.valor):
                        print("IA ha ganado")
                elif(self.mano.valor<21 and self.mano2.valor<21):
                    if(self.mano.valor>self.mano2.valor):
                        print("Jugador ha ganado")
                    elif(self.mano2.valor>self.mano.valor):
                        print("IA ha ganado")
        
        
        
    def crearCarta(self, numeroCarta, paloCarta):
        card1 = QLabel()
        card1.setText(str(numeroCarta)+paloCarta)
        card1.setStyleSheet("border:7px solid #ff0000")
        card1.setMaximumSize(38,40)
        return card1

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