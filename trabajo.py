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
from estadisticas import AnotherWindow
from informe import AnotherWindow2
from game21 import Game21
from Conecta4 import conecta
from battleship import battleship
# La aplicación consistiría en pulsar a jugar y se elige el juego que se desea jugar,
#  saltaría la pantalla del juego y al acabar, salta el asistente para registrar tu puntuación en un informe
# en estadísticas se guarda las estadísticas locales en una base de datos, y el botón salir sale
basedir = os.path.dirname(__file__)
db = QSqlDatabase("QSQLITE")
db.setDatabaseName("chinook.sqlite")

db.open()
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'sg.ico')))
        #app.setWindowIcon(QtGui.QIcon('sg.ico'))
        self.setWindowTitle("App SimpGam")
        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.button1 = QPushButton("Jugar")
        self.button2 = QPushButton("Estadísticas")
        self.button3 = QPushButton("Salir")
        self.button5 = QPushButton("21Game")
        self.button6 = QPushButton("Conecta4")
        self.button7 = QPushButton("Destruir la flota")
        self.text_label = QLabel()
        self.text_label.setText("Hello World!")
        self.button1.setStyleSheet("border:7px solid #ff0000")
        self.button2.setStyleSheet("border:7px solid #ff0000")
        self.button3.setStyleSheet("border:7px solid #ff0000")
        self.button5.setStyleSheet("border:7px solid #ff0000")
        self.button6.setStyleSheet("border:7px solid #ff0000")
        self.button7.setStyleSheet("border:7px solid #ff0000")
        self.button1.setMinimumSize(50,50)
        self.button2.setMinimumSize(50,50)
        self.button3.setMinimumSize(50,50)
        self.button5.setMinimumSize(50,50)
        self.button6.setMinimumSize(50,50)
        self.button7.setMinimumSize(50,50)
        self.button1.clicked.connect(self.button_clicked)
        self.button2.clicked.connect(self.button2_clicked)
        self.button3.clicked.connect(self.button3_clicked)
        self.button5.clicked.connect(self.button5_clicked)
        self.button6.clicked.connect(self.button6_clicked)
        self.button7.clicked.connect(self.button7_clicked)
        self.w = AnotherWindow()
        self.w2 = AnotherWindow2()
        
        self.w3= Game21()
        self.w4= conecta()
        self.w5= battleship()
        #self.w3.juego()
        self.button4 = QPushButton()
        self.button4.setText("Salir")
        self.button4.clicked.connect(self.button4_clicked)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button5)
        self.layout.addWidget(self.button6)
        self.layout.addWidget(self.button7)
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)

        
        self.wizard = QWizard()

        self.wizard.setWizardStyle(QWizard.ModernStyle)

        self.wizard.setPixmap(QWizard.WatermarkPixmap,QPixmap('Watermark.png'))
        self.wizard.setPixmap(QWizard.LogoPixmap,QPixmap('Logo.png'))
        self.wizard.setPixmap(QWizard.BannerPixmap,QPixmap('Banner.png'))

        page1 = QWizardPage()
        page1.setTitle('Introduzca tu nombre y el juego jugado')
        self.nombre = QLineEdit()
        self.juegoB= QComboBox()
        query = QSqlQuery("SELECT DISTINCT juego FROM estadisticas",db=db)
        while query.next():
            self.juegoB.addItem(query.value(0))
        hLayout1 = QHBoxLayout(page1)
        hLayout1.addWidget(self.nombre)
        hLayout1.addWidget(self.juegoB)
        page1.registerField('miCampo1*', self.nombre,self.nombre.text(),'textChanged')
        page1.registerField('miCampo1.2', self.juegoB,self.juegoB.currentText())
        self.wizard.addPage(page1)

        page2 = QWizardPage()
        page2.setTitle('Nivel de dificultad elegido')
        dificultadN = random.randint(1, 3)
        if(dificultadN==1):
            self.dificultad = QLabel("Fácil")
        elif(dificultadN==2):
            self.dificultad = QLabel("Normal")
        else:
            self.dificultad = QLabel("Difícil")
        hLayout2 = QHBoxLayout(page2)
        hLayout2.addWidget(self.dificultad)

        self.wizard.addPage(page2)

        page3 = QWizardPage()
        page3.setTitle('Puntuación obtenida')
        self.score = str(random.randint(0, 300))
        self.puntuacion = QLabel(self.score)
        hLayout3 = QHBoxLayout(page3)
        hLayout3.addWidget(self.puntuacion)
        
        self.wizard.addPage(page3)

        page4 = QWizardPage()
        page4.setTitle('Tiemplo empleado en la partida')
        tiempoH = str(random.randint(0, 3))
        tiempoM= str(random.randint(0, 59))
        tiempoS= str(random.randint(0, 59))
        self.tiempoTotal= (tiempoH*60)+tiempoM
        formato= tiempoH+":"+tiempoM+":"+tiempoS
        self.tiempo = QLabel(formato)
        hLayout4 = QHBoxLayout(page4)
        hLayout4.addWidget(self.tiempo)
        page4.setFinalPage(True)

        next = self.wizard.button(QWizard.NextButton)

        finish = self.wizard.button(QWizard.FinishButton)
        finish.clicked.connect(self.generate)

        self.wizard.addPage(page4)
        
    def generate(self):
        self.puntMax = QSqlQuery("SELECT MAX(score) FROM estadisticas WHERE juego='"+self.juegoB.currentText()+"'",db=db)
        self.puntMax.next()
        self.data = {
            'nombre': self.nombre.text(),
            'dificultad': self.dificultad.text(),
            'puntuacion': self.puntuacion.text(),
            'tiempo': self.tiempo.text(),
            'juego': self.juegoB.currentText(),
            'puntuación máxima del juego': str(self.puntMax.value(0))
        }
        query = QSqlQuery("SELECT score FROM estadisticas",db=db)
        
        query.next()
        scor1= query.value(0)
        query.next()
        scor2= query.value(0)
        query.next()
        scor3= query.value(0)
        if(scor1 is None):
            scor1=0
        if(scor2 is None):
            scor2=0
        if(scor3 is None):
            scor3=0
        plt = pg.plot([scor1,scor2,scor3,int(self.score)])

        # Creamos una instancia de exportación con el ítem que queremos exportar
        exporter = pg.exporters.ImageExporter(plt.plotItem)

        # Establecemos los parámetros de la exportación (anchura)
        exporter.parameters()['width'] = 100   # (afecta a la altura de forma proporcional)

        # Elegimos el nombre del archivo en el que exportamos la gráfica como imagen
        exporter.export('graphic.png')

        outfile = "result.pdf"

        template = PdfReader("template.pdf", decompress=False).pages[0]
        template_obj = pagexobj(template)

        canvas = Canvas(outfile)

        xobj_name = makerl(canvas, template_obj)
        canvas.doForm(xobj_name)

        ystart = 820
        today = datetime.today()
        canvas.drawString(510, ystart, today.strftime('%F'))

        canvas.drawString(165, ystart-57, self.data['nombre'])
        canvas.drawString(165, ystart-97, self.data['dificultad'])
        canvas.drawString(165, ystart-137, self.data['puntuacion'])
        canvas.drawString(165, ystart-177, self.data['tiempo'])
        canvas.drawString(165, ystart-220, self.data['juego'])
        canvas.drawString(300, ystart-265, self.data['puntuación máxima del juego'])
        canvas.drawImage("graphic.png", 50, ystart-350, width=None,height=None,mask=None)






        canvas.save()
        layout2 = QVBoxLayout()
        
        self.web = QWebEngineView()
        
        plt.hide()
        self.web.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        
        #rutaConPDF = Path("template.pdf")
        #self.web.load(QUrl(rutaConPDF.absolute().as_uri()))
        #layout2.addWidget(self.web)
        #layout2.addWidget(self.button4)
        #contenedor2= QWidget()
        #contenedor2.setLayout(layout2)
        #self.setCentralWidget(contenedor2)
        
        QMessageBox.information(self, "Finalizado", "Se ha generado el PDF")
        self.w2.show()
        
    def button_clicked(self, s):
        self.wizard.show()
    def button2_clicked(self, checked):
        
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()
    def button3_clicked(self, s):
        self.close()
    def button4_clicked(self,s):
        self.setCentralWidget(self.contenedor)
    def button5_clicked(self,s):
        if self.w3.isVisible():
            self.w3.hide()

        else:
            self.w3.show()
            self.w3.main()
    def button6_clicked(self,s):
        if self.w4.isVisible():
            self.w4.hide()

        else:
            self.w4.show()
            self.w4.main()
    def button7_clicked(self,s):
        if self.w5.isVisible():
            self.w5.hide()

        else:
            self.w5.show()
            self.w5.main()