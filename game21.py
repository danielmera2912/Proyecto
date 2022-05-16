from datetime import datetime
from pathlib import Path
import random
import sys, os
import textwrap
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel, QWidget, QAbstractItemView, QVBoxLayout, QMessageBox, QFormLayout, QTextEdit, QSpinBox
from Qt import QtGui, Signal
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from PySide6.QtCore import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel
from design import Ui_MainWindow
import pyqtgraph as pg
import pyqtgraph.exporters
from PySide6 import QtWidgets, QtGui, QtCore
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
        self.textCard= (palo+str(numero))
        self.cartaJugable = self.crearCarta(self.textCard)
        self.cartaNoJugable = self.crearCarta("dorso")
    def crearCarta(self, textCard):
        card= QLabel()
        cartaCompleta= 'img/'+textCard+'.png'
        pixmap2  = QPixmap(cartaCompleta)
        pixmap = pixmap2.scaledToWidth(100)
        card.setPixmap(pixmap)
        return card
    def infoCarta(self):
        if(self.palo=="d"):
            self.paloT="Diamante"
        elif(self.palo=="c"):
            self.paloT="Corazón"
        elif(self.palo=="p"):
            self.paloT="Pica"
        elif(self.palo=="t"):
            self.paloT="Trébol"
        print(str(self.numero)+" de "+self.paloT)

class BarajaCartas():
    def __init__(self):
        super().__init__()
        self.cartasD= []
        self.cartasP= []
        self.cartasC= []
        self.cartasT= []
        self.cartas= []
        for x in range(1,9):
            self.cartasD.append(Carta(x,"d"))
            self.cartasP.append(Carta(x,"p"))
            self.cartasC.append(Carta(x,"c"))
            self.cartasT.append(Carta(x,"t"))
        self.cartas= self.cartasT+self.cartasD+self.cartasC+self.cartasP
        self.numeroCartas= len(self.cartas)
    
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
        self.puntuacion=0
        self.ganador=True
        self.contenedor= QWidget()
        self.cartasRival = QHBoxLayout()
        self.vacio1 = QHBoxLayout()
        self.cartasRobar = QHBoxLayout()
        self.vacio2 = QHBoxLayout()
        self.misCartas = QHBoxLayout()
        self.robar = QHBoxLayout()
        self.baraja= BarajaCartas()
        self.victoria = QLabel("Enhorabuena, ¡Has ganado!")
        self.derrota = QLabel("Lo siento, ¡Has perdido!")
        self.button1 = QPushButton("Robar carta")
        self.button2 = QPushButton("No robar carta")
        self.button3 = QPushButton("Salir del juego")
        self.button1.setStyleSheet("border:7px solid #ff0000")
        self.button2.setStyleSheet("border:7px solid #ff0000")
        self.button3.setStyleSheet("border:7px solid #ff0000")
        self.victoria.setStyleSheet("border:7px solid #ff0000")
        self.derrota.setStyleSheet("border:7px solid #ff0000")
        self.button1.setMinimumSize(50,50)
        self.button2.setMinimumSize(50,50)
        self.button3.setMinimumSize(50,50)
        self.victoria.setMinimumSize(50,50)
        self.derrota.setMinimumSize(50,50)
        self.robar.addWidget(self.button1)
        self.robar.addWidget(self.button2)
        self.robar.addWidget(self.button3)
        self.mano1 = Mano(self.baraja, True)
        self.mano2 = Mano(self.baraja, False)
        self.mano1.robarCarta()
        self.mano2.robarCarta()
        self.numeroCartasRestantes= (self.baraja.numeroCartas)-2
        self.cartasRestantes= QLabel()
        self.cartasRestantesTexto= QLabel(str(self.numeroCartasRestantes))
        dorso  = QPixmap("img/dorso.png")
        dorsoD = dorso.scaledToWidth(100)
        self.cartasRestantes.setPixmap(dorsoD)
        self.cartasRobar.addWidget(self.cartasRestantes)
        self.cartasRobar.addWidget(self.cartasRestantesTexto)
        for x in range(0,len(self.mano1.mano)):
            self.misCartas.addWidget(self.mano1.mano[x].cartaJugable)
        for x in range(0,len(self.mano2.mano)):
            self.cartasRival.addWidget(self.mano2.mano[x].cartaNoJugable)
        self.button1.clicked.connect(self.robo)
        self.button2.clicked.connect(self.fin)    
        self.pagelayout = QVBoxLayout()
        self.pagelayout.addLayout(self.cartasRival)
        self.pagelayout.addLayout(self.vacio1)
        self.pagelayout.addLayout(self.cartasRobar)
        self.pagelayout.addLayout(self.vacio2)
        self.pagelayout.addLayout(self.misCartas)
        self.pagelayout.addLayout(self.robar)
        self.contenedor.setLayout(self.pagelayout)
        self.setCentralWidget(self.contenedor)
    def robo(self):
        self.mano1.robarCarta()
        for i in reversed(range(self.cartasRobar.count())): 
            self.cartasRobar.itemAt(i).widget().setParent(None)
        if(self.numeroCartasRestantes>0):
            self.numeroCartasRestantes= self.numeroCartasRestantes-1
        self.cartasRestantesTexto= QLabel(str(self.numeroCartasRestantes))
        self.cartasRobar.addWidget(self.cartasRestantes)
        self.cartasRobar.addWidget(self.cartasRestantesTexto)
        self.mano1.infoMano()
        for x in range(0,len(self.mano1.mano)):
            self.misCartas.addWidget(self.mano1.mano[x].cartaJugable)
        if(self.mano2.valor<=self.mano1.valor and self.mano2.valor<21):
                    if(self.mano2.valor<10):
                        self.mano2.robarCarta()
                        for i in reversed(range(self.cartasRobar.count())): 
                            self.cartasRobar.itemAt(i).widget().setParent(None)
                        self.numeroCartasRestantes= self.numeroCartasRestantes-1
                        self.cartasRestantesTexto= QLabel(str(self.numeroCartasRestantes))
                        self.cartasRobar.addWidget(self.cartasRestantes)
                        self.cartasRobar.addWidget(self.cartasRestantesTexto)
                        self.mano2.infoMano()
                        for x in range(0,len(self.mano2.mano)):
                            self.cartasRival.addWidget(self.mano2.mano[x].cartaNoJugable)
                    elif(self.mano2.valor>10 and self.mano2.valor<15):
                        chances= random.randrange(10)
                        if(chances>4):
                            self.mano2.robarCarta()
                            for i in reversed(range(self.cartasRobar.count())): 
                                self.cartasRobar.itemAt(i).widget().setParent(None)
                            self.numeroCartasRestantes= self.numeroCartasRestantes-1
                            self.cartasRestantesTexto= QLabel(str(self.numeroCartasRestantes))
                            self.cartasRobar.addWidget(self.cartasRestantes)
                            self.cartasRobar.addWidget(self.cartasRestantesTexto)
                            self.mano2.infoMano()
                            for x in range(0,len(self.mano2.mano)):
                                self.cartasRival.addWidget(self.mano2.mano[x].cartaNoJugable)
                    elif(self.mano2.valor>15 and self.mano2.valor<20):
                        chances= random.randrange(3)
                        if(chances==2):
                            self.mano2.robarCarta()
                            for i in reversed(range(self.cartasRobar.count())): 
                                self.cartasRobar.itemAt(i).widget().setParent(None)
                            self.numeroCartasRestantes= self.numeroCartasRestantes-1
                            self.cartasRestantesTexto= QLabel(str(self.numeroCartasRestantes))
                            self.cartasRobar.addWidget(self.cartasRestantes)
                            self.cartasRobar.addWidget(self.cartasRestantesTexto)
                            self.mano2.infoMano()
                            for x in range(0,len(self.mano2.mano)):
                                self.cartasRival.addWidget(self.mano2.mano[x].cartaNoJugable)
                    elif(self.mano2.valor==20):
                        chances= random.randrange(10)
                        if(chances==5):
                            self.mano2.robarCarta()
                            for i in reversed(range(self.cartasRobar.count())): 
                                self.cartasRobar.itemAt(i).widget().setParent(None)
                            self.numeroCartasRestantes= self.numeroCartasRestantes-1
                            self.cartasRestantesTexto= QLabel(str(self.numeroCartasRestantes))
                            self.cartasRobar.addWidget(self.cartasRestantes)
                            self.cartasRobar.addWidget(self.cartasRestantesTexto)
                            self.mano2.infoMano()
                            for x in range(0,len(self.mano2.mano)):
                                self.cartasRival.addWidget(self.mano2.mano[x].cartaNoJugable)
    def fin(self):
        print("Mano del jugador:")
        self.mano1.enseñarMano()
        print(self.mano1.valor)
        print("Mano de la IA")
        self.mano2.enseñarMano()
        print(self.mano2.valor)
        if(self.mano1.valor==21 and self.mano2.valor!=21):
            print("Jugador ha ganado")
            self.puntuacion=100
        elif(self.mano1.valor==21 and self.mano2.valor==21):
            print("Empate")
            self.ganador=False
            self.puntuacion= 30
        elif(self.mano2.valor==21 and self.mano1.valor!=21):
            print("IA ha ganado")
            self.ganador=False
            self.puntuacion= 0
        else:
            if(self.mano1.valor>21 and self.mano2.valor<21):
                print("IA ha ganado")
                self.ganador=False
                self.puntuacion= 0
            elif(self.mano2.valor>21 and self.mano1.valor<21):
                print("Jugador ha ganado")
                self.puntuacion= 80
            else:
                if(self.mano1.valor>21 and self.mano2.valor>21):
                    if(self.mano1.valor<self.mano2.valor):
                        print("Jugador ha ganado")
                        self.puntuacion= 50
                    elif(self.mano2.valor<self.mano1.valor):
                        print("IA ha ganado")
                        self.ganador=False
                        self.puntuacion= 0
                elif(self.mano1.valor<21 and self.mano2.valor<21):
                    if(self.mano1.valor>self.mano2.valor):
                        print("Jugador ha ganado")
                        self.puntuacion= 80
                    elif(self.mano2.valor>self.mano1.valor):
                        print("IA ha ganado")
                        self.ganador=False
                        self.puntuacion= 0
                else:
                    print("EMPATE")
                    self.ganador=False
                    self.puntuacion=30
        for i in reversed(range(self.cartasRival.count())): 
            self.cartasRival.itemAt(i).widget().setParent(None)
        for x in range(0,len(self.mano2.mano)):
            self.cartasRival.addWidget(self.mano2.mano[x].cartaJugable)
        self.celebrar()
    def celebrar(self):
        puntuacionLabel= QLabel("La puntuación obtenida es "+str(self.puntuacion))
        puntuacionLabel.setStyleSheet("border:7px solid #ff0000")
        puntuacionLabel.setMinimumSize(50,50)
        for i in reversed(range(self.robar.count())): 
            self.robar.itemAt(i).widget().setParent(None)
        if(self.ganador):
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.button3.setEnabled(True)
            self.robar.addWidget(self.victoria)
            self.robar.addWidget(puntuacionLabel)
            self.robar.addWidget(self.button3)
        else:
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.button3.setEnabled(True)
            self.robar.addWidget(self.derrota)
            self.robar.addWidget(puntuacionLabel)
            self.robar.addWidget(self.button3)
    def juego(self):
        self.puntuacion=0
        self.baraja= BarajaCartas()
        self.mano1 = Mano(self.baraja, True)
        self.mano2 = Mano(self.baraja, False)
        self.mano1.robarCarta()
        self.mano2.robarCarta()
        respuesta='s'
        while(respuesta=='s'):
            respuesta= input("¿Quieres robar una carta? (s/n): ")
            if(respuesta=='s'):
                self.mano1.robarCarta()
                self.mano1.infoMano()
                if(self.mano2.valor<=self.mano1.valor and self.mano2.valor<21):
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
        self.mano1.enseñarMano()
        print(self.mano1.valor)
        print("Mano de la IA")
        self.mano2.enseñarMano()
        print(self.mano2.valor)
        if(self.mano1.valor==21 and self.mano2.valor!=21):
            print("Jugador ha ganado")
            self.puntuacion=100
        elif(self.mano1.valor==21 and self.mano2.valor==21):
            print("Empate")
            self.puntuacion= 30
        elif(self.mano2.valor==21 and self.mano1.valor!=21):
            print("IA ha ganado")
            self.puntuacion= 0
        else:
            if(self.mano1.valor>21 and self.mano2.valor<21):
                print("IA ha ganado")
                self.puntuacion= 0
            elif(self.mano2.valor>21 and self.mano1.valor<21):
                print("Jugador ha ganado")
                self.puntuacion= 80
            else:
                if(self.mano1.valor>21 and self.mano2.valor>21):
                    if(self.mano1.valor<self.mano2.valor):
                        print("Jugador ha ganado")
                        self.puntuacion= 50
                    elif(self.mano2.valor<self.mano1.valor):
                        print("IA ha ganado")
                        self.puntuacion= 0
                elif(self.mano1.valor<21 and self.mano2.valor<21):
                    if(self.mano1.valor>self.mano2.valor):
                        print("Jugador ha ganado")
                        self.puntuacion= 80
                    elif(self.mano2.valor>self.mano1.valor):
                        print("IA ha ganado")
                        self.puntuacion= 0
                else:
                    print("EMPATE")
                    self.puntuacion=30
        
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