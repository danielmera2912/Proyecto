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
    def robar_carta(self):
        try:
            robo= self.cartas.cartas.pop()
            self.mano.append(robo)
            if(self.info is True):
                robo.info_carta()
            suma= 0
            for x in self.mano:
                suma+= x.numero
                self.valor=suma
        except:
            print("No se pueden robar más cartas, no hay mazo.")
    def mostrar_mano(self):
        for x in range(0,len(self.mano)):
            self.mano[x].info_carta()
    def info_mano(self):
        if(self.info is True):
            print("El valor de tus cartas son de "+str(self.valor))
class Carta():
    def __init__(self, numero, palo):
        super().__init__()
        self.numero=numero
        self.palo=palo
        self.paloT= ""
        self.textCard= (palo+str(numero))
        self.cartaJugable = self.crear_carta(self.textCard)
        self.cartaNoJugable = self.crear_carta("dorso")
    def crear_carta(self, textCard):
        card= QLabel()
        carta_completa= 'img/'+textCard+'.png'
        pixmap2  = QPixmap(carta_completa)
        pixmap = pixmap2.scaledToWidth(100)
        card.setPixmap(pixmap)
        return card
    def info_carta(self):
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
        self.num_cartas= len(self.cartas)
    
    def barajar(self):
        lista = self.cartas[:]
        longitud_lista = len(lista)
        for i in range(longitud_lista):
            indice_aleatorio = random.randint(0, longitud_lista - 1)
            temporal = lista[i]
            lista[i] = lista[indice_aleatorio]
            lista[indice_aleatorio] = temporal
        self.cartas=lista
    def mostrar_baraja(self):
        for x in range(0,len(self.cartas)):
            self.cartas[x].info_carta()
class Game21(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("21 Game")
        self.puntuacion=0
        self.ganador=True
        self.contenedor= QWidget()
        self.cartas_rival = QHBoxLayout()
        self.vacio1 = QHBoxLayout()
        self.cartas_robar = QHBoxLayout()
        self.vacio2 = QHBoxLayout()
        self.mis_cartas = QHBoxLayout()
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
        self.mano1.robar_carta()
        self.mano2.robar_carta()
        self.num_cartas_restantes= (self.baraja.num_cartas)-2
        self.cartas_restantes= QLabel()
        self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
        dorso  = QPixmap("img/dorso.png")
        dorsoD = dorso.scaledToWidth(100)
        self.cartas_restantes.setPixmap(dorsoD)
        self.cartas_robar.addWidget(self.cartas_restantes)
        self.cartas_robar.addWidget(self.cartas_restantes_texto)
        for x in range(0,len(self.mano1.mano)):
            self.mis_cartas.addWidget(self.mano1.mano[x].cartaJugable)
        for x in range(0,len(self.mano2.mano)):
            self.cartas_rival.addWidget(self.mano2.mano[x].cartaNoJugable)
        self.button1.clicked.connect(self.robo)
        self.button2.clicked.connect(self.fin)    
        self.pagelayout = QVBoxLayout()
        self.pagelayout.addLayout(self.cartas_rival)
        self.pagelayout.addLayout(self.vacio1)
        self.pagelayout.addLayout(self.cartas_robar)
        self.pagelayout.addLayout(self.vacio2)
        self.pagelayout.addLayout(self.mis_cartas)
        self.pagelayout.addLayout(self.robar)
        self.contenedor.setLayout(self.pagelayout)
        self.setCentralWidget(self.contenedor)
    def robo(self):
        self.mano1.robar_carta()
        for i in reversed(range(self.cartas_robar.count())): 
            self.cartas_robar.itemAt(i).widget().setParent(None)
        if(self.num_cartas_restantes>0):
            self.num_cartas_restantes= self.num_cartas_restantes-1
        self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
        self.cartas_robar.addWidget(self.cartas_restantes)
        self.cartas_robar.addWidget(self.cartas_restantes_texto)
        self.mano1.info_mano()
        for x in range(0,len(self.mano1.mano)):
            self.mis_cartas.addWidget(self.mano1.mano[x].cartaJugable)
        if(self.mano2.valor<=self.mano1.valor and self.mano2.valor<21):
                    if(self.mano2.valor<10):
                        self.mano2.robar_carta()
                        for i in reversed(range(self.cartas_robar.count())): 
                            self.cartas_robar.itemAt(i).widget().setParent(None)
                        self.num_cartas_restantes= self.num_cartas_restantes-1
                        self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
                        self.cartas_robar.addWidget(self.cartas_restantes)
                        self.cartas_robar.addWidget(self.cartas_restantes_texto)
                        self.mano2.info_mano()
                        for x in range(0,len(self.mano2.mano)):
                            self.cartas_rival.addWidget(self.mano2.mano[x].cartaNoJugable)
                    elif(self.mano2.valor>10 and self.mano2.valor<15):
                        chances= random.randrange(10)
                        if(chances>4):
                            self.mano2.robar_carta()
                            for i in reversed(range(self.cartas_robar.count())): 
                                self.cartas_robar.itemAt(i).widget().setParent(None)
                            self.num_cartas_restantes= self.num_cartas_restantes-1
                            self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
                            self.cartas_robar.addWidget(self.cartas_restantes)
                            self.cartas_robar.addWidget(self.cartas_restantes_texto)
                            self.mano2.info_mano()
                            for x in range(0,len(self.mano2.mano)):
                                self.cartas_rival.addWidget(self.mano2.mano[x].cartaNoJugable)
                    elif(self.mano2.valor>15 and self.mano2.valor<20):
                        chances= random.randrange(3)
                        if(chances==2):
                            self.mano2.robar_carta()
                            for i in reversed(range(self.cartas_robar.count())): 
                                self.cartas_robar.itemAt(i).widget().setParent(None)
                            self.num_cartas_restantes= self.num_cartas_restantes-1
                            self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
                            self.cartas_robar.addWidget(self.cartas_restantes)
                            self.cartas_robar.addWidget(self.cartas_restantes_texto)
                            self.mano2.info_mano()
                            for x in range(0,len(self.mano2.mano)):
                                self.cartas_rival.addWidget(self.mano2.mano[x].cartaNoJugable)
                    elif(self.mano2.valor==20):
                        chances= random.randrange(10)
                        if(chances==5):
                            self.mano2.robar_carta()
                            for i in reversed(range(self.cartas_robar.count())): 
                                self.cartas_robar.itemAt(i).widget().setParent(None)
                            self.num_cartas_restantes= self.num_cartas_restantes-1
                            self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
                            self.cartas_robar.addWidget(self.cartas_restantes)
                            self.cartas_robar.addWidget(self.cartas_restantes_texto)
                            self.mano2.info_mano()
                            for x in range(0,len(self.mano2.mano)):
                                self.cartas_rival.addWidget(self.mano2.mano[x].cartaNoJugable)
    def fin(self):
        print("Mano del jugador:")
        self.mano1.mostrar_mano()
        print(self.mano1.valor)
        print("Mano de la IA")
        self.mano2.mostrar_mano()
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
        for i in reversed(range(self.cartas_rival.count())): 
            self.cartas_rival.itemAt(i).widget().setParent(None)
        for x in range(0,len(self.mano2.mano)):
            self.cartas_rival.addWidget(self.mano2.mano[x].cartaJugable)
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
        self.mano1.robar_carta()
        self.mano2.robar_carta()
        respuesta='s'
        while(respuesta=='s'):
            respuesta= input("¿Quieres robar una carta? (s/n): ")
            if(respuesta=='s'):
                self.mano1.robar_carta()
                self.mano1.info_mano()
                if(self.mano2.valor<=self.mano1.valor and self.mano2.valor<21):
                    if(self.mano2.valor<10):
                        print("IA ha robado carta")
                        self.mano2.robar_carta()
                        self.mano2.info_mano()
                    elif(self.mano2.valor>10 and self.mano2.valor<15):
                        chances= random.randrange(10)
                        if(chances>4):
                            print("IA ha robado carta")
                            self.mano2.robar_carta()
                            self.mano2.info_mano()
                    elif(self.mano2.valor>15 and self.mano2.valor<20):
                        chances= random.randrange(3)
                        if(chances==2):
                            print("IA ha robado carta")
                            self.mano2.robar_carta()
                            self.mano2.info_mano()
                    elif(self.mano2.valor==20):
                        chances= random.randrange(10)
                        if(chances==5):
                            print("IA ha robado carta")
                            self.mano2.robar_carta()
                            self.mano2.info_mano()
        print("Mano del jugador:")
        self.mano1.mostrar_mano()
        print(self.mano1.valor)
        print("Mano de la IA")
        self.mano2.mostrar_mano()
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