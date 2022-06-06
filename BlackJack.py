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
from PySide6.QtMultimedia import QSoundEffect

from juego import Juego
class Mano():
    def __init__(self, baraja, info):
        super().__init__()
        self.valor=0
        self.mano= []
        self.cartas= baraja
        self.cartas.barajar()
        self.info=info
        self.sonido_click = QSoundEffect()
        self.sonido_click.setSource(QUrl.fromLocalFile("click.wav"))
        self.sonido_click.setVolume(0.25)
        
    def robar_carta(self, robo_manual):
        if(robo_manual==True):
            self.sonido_click.play()
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
        self.carta_jugable = self.crear_carta(self.textCard)
        self.carta_no_jugable = self.crear_carta("dorso")
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
class BlackJack(QMainWindow, Juego):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BlackJack")
        stylesheet = """
            QMainWindow {
                background-image: url("fondo3.png"); 
                background-repeat: repeat; 
                background-position: center;
            }
        """
        self.setStyleSheet(stylesheet)
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
        self.ganador=True
        self.contenedor= QWidget()
        self.cartas_rival = QHBoxLayout()
        self.cartas_robar = QHBoxLayout()
        self.mis_cartas = QHBoxLayout()
        self.robar = QHBoxLayout()
        self.baraja= BarajaCartas()
        self.victoria = QLabel("Enhorabuena, ¡Has ganado!")
        self.victoria.setStyleSheet("background-color: blue;"
                                            "color: black;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.derrota = QLabel("Lo siento, ¡Has perdido!")
        self.derrota.setStyleSheet("background-color: red;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.pasar_turno = QPushButton("Pasar turno")
        self.pasar_turno.setStyleSheet("background-color: #1520A6;"
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
        self.pasar_turno.setMinimumSize(50,50)
        self.fin.setMinimumSize(50,50)
        self.victoria.setMinimumSize(50,50)
        self.derrota.setMinimumSize(50,50)
        self.robar.addWidget(self.pasar_turno)
        self.robar.addWidget(self.fin)
        self.mano1 = Mano(self.baraja, True)
        self.mano2 = Mano(self.baraja, False)
        self.mano1.robar_carta(False)
        self.mano2.robar_carta(False)
        self.num_cartas_restantes= (self.baraja.num_cartas)-2
        self.cartas_restantes= QPushButton()
        self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
        dorso  = QPixmap("img/dorso2.png")
        dorsoD = dorso.scaledToWidth(100)
        self.cartas_restantes.setIcon(dorsoD)
        self.cartas_restantes.setIconSize(QSize(150, 190))
        self.cartas_restantes.setStyleSheet("QPushButton{border-radius:0px;border: 0px solid #345781;}") 
        self.cartas_robar.addWidget(self.cartas_restantes)
        self.cartas_robar.addWidget(self.cartas_restantes_texto)
        for x in range(0,len(self.mano1.mano)):
            self.mis_cartas.addWidget(self.mano1.mano[x].carta_jugable)
        for x in range(0,len(self.mano2.mano)):
            self.cartas_rival.addWidget(self.mano2.mano[x].carta_no_jugable)
        self.cartas_restantes.clicked.connect(self.robo)
        self.pasar_turno.clicked.connect(self.finalizar_turno)    
        self.pagelayout = QVBoxLayout()
        self.pagelayout.addLayout(self.cartas_rival)
        self.pagelayout.addLayout(self.cartas_robar)
        self.pagelayout.addLayout(self.mis_cartas)
        self.pagelayout.addLayout(self.robar)
        self.contenedor.setLayout(self.pagelayout)
        self.setCentralWidget(self.contenedor)
    def robo(self):
        self.mano1.robar_carta(True)
        for i in reversed(range(self.cartas_robar.count())): 
            self.cartas_robar.itemAt(i).widget().setParent(None)
        if(self.num_cartas_restantes>0):
            self.num_cartas_restantes= self.num_cartas_restantes-1
        self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
        self.cartas_robar.addWidget(self.cartas_restantes)
        self.cartas_robar.addWidget(self.cartas_restantes_texto)
        self.mano1.info_mano()
        for x in range(0,len(self.mano1.mano)):
            self.mis_cartas.addWidget(self.mano1.mano[x].carta_jugable)
        if(self.mano2.valor<=self.mano1.valor and self.mano2.valor<21):
            if(self.mano2.valor<10):
                self.mano2.robar_carta(True)
                for i in reversed(range(self.cartas_robar.count())): 
                    self.cartas_robar.itemAt(i).widget().setParent(None)
                self.num_cartas_restantes= self.num_cartas_restantes-1
                self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
                self.cartas_robar.addWidget(self.cartas_restantes)
                self.cartas_robar.addWidget(self.cartas_restantes_texto)
                self.mano2.info_mano()
                for x in range(0,len(self.mano2.mano)):
                    self.cartas_rival.addWidget(self.mano2.mano[x].carta_no_jugable)
            elif(self.mano2.valor>10 and self.mano2.valor<15):
                chances= random.randrange(10)
                print(chances)
                if(chances>4):
                    self.mano2.robar_carta(True)
                    for i in reversed(range(self.cartas_robar.count())): 
                        self.cartas_robar.itemAt(i).widget().setParent(None)
                    self.num_cartas_restantes= self.num_cartas_restantes-1
                    self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
                    self.cartas_robar.addWidget(self.cartas_restantes)
                    self.cartas_robar.addWidget(self.cartas_restantes_texto)
                    self.mano2.info_mano()
                    for x in range(0,len(self.mano2.mano)):
                        self.cartas_rival.addWidget(self.mano2.mano[x].carta_no_jugable)
            elif(self.mano2.valor>15 and self.mano2.valor<20):
                chances= random.randrange(3)
                print(chances)
                if(chances==2):
                    self.mano2.robar_carta(True)
                    for i in reversed(range(self.cartas_robar.count())): 
                        self.cartas_robar.itemAt(i).widget().setParent(None)
                    self.num_cartas_restantes= self.num_cartas_restantes-1
                    self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
                    self.cartas_robar.addWidget(self.cartas_restantes)
                    self.cartas_robar.addWidget(self.cartas_restantes_texto)
                    self.mano2.info_mano()
                    for x in range(0,len(self.mano2.mano)):
                        self.cartas_rival.addWidget(self.mano2.mano[x].carta_no_jugable)
            elif(self.mano2.valor==20):
                chances= random.randrange(10)
                if(chances==5):
                    self.mano2.robar_carta(True)
                    for i in reversed(range(self.cartas_robar.count())): 
                        self.cartas_robar.itemAt(i).widget().setParent(None)
                    self.num_cartas_restantes= self.num_cartas_restantes-1
                    self.cartas_restantes_texto= QLabel(str(self.num_cartas_restantes))
                    self.cartas_robar.addWidget(self.cartas_restantes)
                    self.cartas_robar.addWidget(self.cartas_restantes_texto)
                    self.mano2.info_mano()
                    for x in range(0,len(self.mano2.mano)):
                        self.cartas_rival.addWidget(self.mano2.mano[x].carta_no_jugable)
        if(self.mano1.valor>=21):
            self.cartas_restantes.setEnabled(False)
            self.pasar_turno.setText("¡Pasa turno! ¡No puedes robar más!")
            self.pasar_turno.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 5px;"
                                        "border-radius: 210px;"
                                        "border-color: green;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")     
    def finalizar_turno(self):
        print("Mano del jugador:")
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
        elif(self.mano1.valor==self.mano2.valor):
            #EMPATE
            self.ganador= False
            self.puntuacion=10
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
        for i in reversed(range(self.cartas_rival.count())): 
            self.cartas_rival.itemAt(i).widget().setParent(None)
        for x in range(0,len(self.mano2.mano)):
            self.cartas_rival.addWidget(self.mano2.mano[x].carta_jugable)
        self.celebrar()
    def celebrar(self):
        for i in reversed(range(self.robar.count())): 
            self.robar.itemAt(i).widget().setParent(None)
        if(self.ganador):
            self.pasar_turno.setEnabled(False)
            self.fin.setEnabled(True)
            self.sonido_victoria.play()
            self.robar.addWidget(self.victoria)
            self.robar.addWidget(self.fin)
        else:
            self.pasar_turno.setEnabled(False)
            self.fin.setEnabled(True)
            self.sonido_derrota.play()
            self.robar.addWidget(self.derrota)
            self.robar.addWidget(self.fin)

    def rejugar(self):
        while True:
            eleccion = input("¿Quieres jugar otra partida? (s/n) ").lower()
            if eleccion == "s":
                return True
            elif eleccion == "n":
                return False