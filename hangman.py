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
class hangman(QMainWindow, Juego):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hangman")
        self.fondo()
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
        self.fase= QLabel()
        self.img1  = QPixmap("img2/fase1.png")
        self.img2  = QPixmap("img2/fase2.png")
        self.img3  = QPixmap("img2/fase3.png")
        self.img4  = QPixmap("img2/fase4.png")
        self.img5  = QPixmap("img2/fase5.png")
        self.img6  = QPixmap("img2/fase6.png")
        self.img7  = QPixmap("img2/fase7.png")
        self.img8  = QPixmap("img2/fase8.png")
        self.fase.setPixmap(self.img1)
        self.texto_letras_usadas = "Letras utilizadas: "
        self.diccionario= ["HARRY POTTER", "LAS CRONICAS DE NARNIA", "ABECEDARIO", "DICCIONARIO", "COCHE", "VEHICULO AEREO", "BOTELLA DE AGUA", "RECICLAJE", "COLORES", "TETERA", "CHOCOLATE BLANCO", "PIZZA DE CUATRO QUESOS"]
        self.palabra_visible= QLabel()
        self.palabra_visible.setStyleSheet("font: bold 54px;")
        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.c1 = QVBoxLayout()
        self.c00 = QHBoxLayout()
        self.c10 = QHBoxLayout()
        self.c11 = QHBoxLayout()
        self.c12 = QHBoxLayout()
        self.c13 = QHBoxLayout()
        self.c2 = QHBoxLayout()
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
        self.actualizador= QPushButton("¡Comienza a jugar!")
        self.actualizador.setStyleSheet("background-color: #1520A6;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
        self.c2.addWidget(self.actualizador)
        self.c2.addWidget(self.fin)

        self.bQ= QPushButton("Q")
        self.bW= QPushButton("W")
        self.bE= QPushButton("E")
        self.bR= QPushButton("R")
        self.bT= QPushButton("T")
        self.bY= QPushButton("Y")
        self.bU= QPushButton("U")
        self.bI= QPushButton("I")
        self.bO= QPushButton("O")
        self.bP= QPushButton("P")
        self.bA= QPushButton("A")
        self.bS= QPushButton("S")
        self.bD= QPushButton("D")
        self.bF= QPushButton("F")
        self.bG= QPushButton("G")
        self.bH= QPushButton("H")
        self.bJ= QPushButton("J")
        self.bK= QPushButton("K")
        self.bL= QPushButton("L")
        self.bÑ= QPushButton("Ñ")
        self.bZ= QPushButton("Z")
        self.bX= QPushButton("X")
        self.bC= QPushButton("C")
        self.bV= QPushButton("V")
        self.bB= QPushButton("B")
        self.bN= QPushButton("N")
        self.bM= QPushButton("M")

        self.c00.addWidget(self.fase, 0, Qt.AlignCenter)
        self.c10.addWidget(self.palabra_visible, 0, Qt.AlignCenter)
        self.c11.addWidget(self.bQ)
        self.c11.addWidget(self.bW)
        self.c11.addWidget(self.bE)
        self.c11.addWidget(self.bR)
        self.c11.addWidget(self.bT)
        self.c11.addWidget(self.bY)
        self.c11.addWidget(self.bU)
        self.c11.addWidget(self.bI)
        self.c11.addWidget(self.bO)
        self.c11.addWidget(self.bP)
        self.c12.addWidget(self.bA)
        self.c12.addWidget(self.bS)
        self.c12.addWidget(self.bD)
        self.c12.addWidget(self.bF)
        self.c12.addWidget(self.bG)
        self.c12.addWidget(self.bH)
        self.c12.addWidget(self.bJ)
        self.c12.addWidget(self.bK)
        self.c12.addWidget(self.bL)
        self.c12.addWidget(self.bÑ)
        self.c13.addWidget(self.bZ)
        self.c13.addWidget(self.bX)
        self.c13.addWidget(self.bC)
        self.c13.addWidget(self.bV)
        self.c13.addWidget(self.bB)
        self.c13.addWidget(self.bN)
        self.c13.addWidget(self.bM)
        self.c1.addLayout(self.c00)
        self.c1.addLayout(self.c10)
        self.c1.addLayout(self.c11)
        self.c1.addLayout(self.c12)
        self.c1.addLayout(self.c13)
        self.letras_usadas= []
        self.palabra_secreta= self.palabra_aleatoria()
        self.palabra_oculta= []
        self.espacios= 0
        for x in range(len(self.palabra_secreta)):
            if(self.palabra_secreta[x]==" "):
                self.palabra_oculta.append(" ")
                self.espacios=self.espacios+1
            else:
                self.palabra_oculta.append("_")
        self.palabra_secreta.find(" ")
        self.vidas= 7
        self.acierto= self.espacios
        self.palabra_visible.setText(" ".join(self.palabra_oculta))
        self.bQ.clicked.connect(lambda: self.descifrar("Q", self.bQ))
        self.bW.clicked.connect(lambda: self.descifrar("W", self.bW))
        self.bE.clicked.connect(lambda: self.descifrar("E", self.bE))
        self.bR.clicked.connect(lambda: self.descifrar("R", self.bR))
        self.bT.clicked.connect(lambda: self.descifrar("T", self.bT))
        self.bY.clicked.connect(lambda: self.descifrar("Y", self.bY))
        self.bU.clicked.connect(lambda: self.descifrar("U", self.bU))
        self.bI.clicked.connect(lambda: self.descifrar("I", self.bI))
        self.bO.clicked.connect(lambda: self.descifrar("O", self.bO))
        self.bP.clicked.connect(lambda: self.descifrar("P", self.bP))
        self.bA.clicked.connect(lambda: self.descifrar("A", self.bA))
        self.bS.clicked.connect(lambda: self.descifrar("S", self.bS))
        self.bD.clicked.connect(lambda: self.descifrar("D", self.bD))
        self.bF.clicked.connect(lambda: self.descifrar("F", self.bF))
        self.bG.clicked.connect(lambda: self.descifrar("G", self.bG))
        self.bH.clicked.connect(lambda: self.descifrar("H", self.bH))
        self.bJ.clicked.connect(lambda: self.descifrar("J", self.bJ))
        self.bK.clicked.connect(lambda: self.descifrar("K", self.bK))
        self.bL.clicked.connect(lambda: self.descifrar("L", self.bL))
        self.bÑ.clicked.connect(lambda: self.descifrar("Ñ", self.bÑ))
        self.bZ.clicked.connect(lambda: self.descifrar("Z", self.bZ))
        self.bX.clicked.connect(lambda: self.descifrar("X", self.bX))
        self.bC.clicked.connect(lambda: self.descifrar("C", self.bC))
        self.bV.clicked.connect(lambda: self.descifrar("V", self.bV))
        self.bB.clicked.connect(lambda: self.descifrar("B", self.bB))
        self.bN.clicked.connect(lambda: self.descifrar("N", self.bN))
        self.bM.clicked.connect(lambda: self.descifrar("M", self.bM))

        self.layout.addLayout(self.c1)
        self.layout.addLayout(self.c2)
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)
    # def introducir_palabra_secreta(self):
    #     palabra= str(input("Introduce la palabra secreta: "))
    #     palabra = palabra.upper()
    #     return palabra
 
    # def pedir_letra(self):
    #     letras = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    #     while(True):
    #         letra= str(input("Introduce una letra: ")).upper()
    #         if(len(letra)!=1 or letra not in letras):
    #             print("Vuelve a intentarlo")
    #         else:
    #             return letra

    def palabra_aleatoria(self):
        numero= random.randrange(len(self.diccionario))
        return self.diccionario[numero]
    def descifrar(self, letra_enviada, boton):
        if(self.vidas==0 or self.acierto==len(self.palabra_secreta)):
            ...
        else:
            letra= letra_enviada

        if(letra in self.letras_usadas):
            self.actualizador.setText("Letra repetida")
            self.sonido_click.play()
        else:
            self.letras_usadas.append(letra)
            if(letra in self.palabra_secreta):
                contador=0
                for i in self.palabra_secreta:
                    if(i==letra):
                        self.palabra_oculta[contador]=letra
                        self.acierto=self.acierto+1
                    contador=contador+1
                self.actualizador.setText("Letra acertada.")
                boton.setStyleSheet("background-color: green")
                self.sonido_acierto.play()
                self.palabra_visible.setText(" ".join(self.palabra_oculta))
            else:
                self.actualizador.setText("Letra no acertada.")
                boton.setStyleSheet("background-color: red")
                self.sonido_fallo.play()
                self.palabra_visible.setText(" ".join(self.palabra_oculta))
                self.vidas=self.vidas-1
                if(self.vidas==6):
                    self.fase.setPixmap(self.img2)
                elif(self.vidas==5):
                    self.fase.setPixmap(self.img3)
                elif(self.vidas==4):
                    self.fase.setPixmap(self.img4)
                elif(self.vidas==3):
                    self.fase.setPixmap(self.img5)
                elif(self.vidas==2):
                    self.fase.setPixmap(self.img6)
                elif(self.vidas==1):
                    self.fase.setPixmap(self.img7)
                elif(self.vidas==0):
                    self.fase.setPixmap(self.img8)
                # print("Te quedan "+str(self.vidas)+" vidas")
        if(self.comprobar_final()==True):
            if(self.acierto==len(self.palabra_secreta)):
                self.actualizador.setText("Victoria, la palabra secreta SÍ era "+self.palabra_secreta)
                self.actualizador.setStyleSheet("background-color: blue;"
                                            "color: black;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
                self.puntuacion= (self.vidas*5)+(self.acierto*3)
                self.sonido_victoria.play()
            else:
                self.actualizador.setText("Derrota, la palabra secreta era "+self.palabra_secreta)
                self.actualizador.setStyleSheet("background-color: red;"
                                            "color: white;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 210px;"
                                        "border-color: blue;"
                                        "font: bold 14px;"
                                        "min-width: 10em;"
                                        "padding: 6px;")
                self.puntuacion=0
                self.sonido_derrota.play()
            self.bQ.setEnabled(False)
            self.bW.setEnabled(False)
            self.bE.setEnabled(False)
            self.bR.setEnabled(False)
            self.bT.setEnabled(False)
            self.bY.setEnabled(False)
            self.bU.setEnabled(False)
            self.bI.setEnabled(False)
            self.bO.setEnabled(False)
            self.bP.setEnabled(False)
            self.bA.setEnabled(False)
            self.bS.setEnabled(False)
            self.bD.setEnabled(False)
            self.bF.setEnabled(False)
            self.bG.setEnabled(False)
            self.bH.setEnabled(False)
            self.bJ.setEnabled(False)
            self.bK.setEnabled(False)
            self.bL.setEnabled(False)
            self.bÑ.setEnabled(False)
            self.bZ.setEnabled(False)
            self.bX.setEnabled(False)
            self.bC.setEnabled(False)
            self.bV.setEnabled(False)
            self.bB.setEnabled(False)
            self.bN.setEnabled(False)
            self.bM.setEnabled(False)
    def comprobar_final(self):
        if(self.acierto==len(self.palabra_secreta)):
            return True
        elif(self.vidas==0):
            return True
        else:
            return False