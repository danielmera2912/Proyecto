# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGroupBox,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTableView, QToolBar, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionInsertar = QAction(MainWindow)
        self.actionInsertar.setObjectName(u"actionInsertar")
        icon = QIcon()
        icon.addFile(u":/icons/database--plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionInsertar.setIcon(icon)
        self.actionModificar = QAction(MainWindow)
        self.actionModificar.setObjectName(u"actionModificar")
        icon1 = QIcon()
        icon1.addFile(u":/icons/database--arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionModificar.setIcon(icon1)
        self.actionEliminar = QAction(MainWindow)
        self.actionEliminar.setObjectName(u"actionEliminar")
        icon2 = QIcon()
        icon2.addFile(u":/icons/database--minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionEliminar.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        #self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.nombreText = QLineEdit(self.groupBox)
        self.nombreText.setObjectName(u"nombreText")

        #self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nombreText)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        #self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.scoreText = QLineEdit(self.groupBox)
        self.scoreText.setObjectName(u"scoreText")

        #self.formLayout.setWidget(1, QFormLayout.FieldRole, self.scoreText)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        #self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.juegoText = QLineEdit(self.groupBox)
        self.juegoText.setObjectName(u"juegoText")

        #self.formLayout.setWidget(2, QFormLayout.FieldRole, self.juegoText)




        #self.verticalLayout_2.addWidget(self.groupBox)

        self.tabla = QTableView(self.centralwidget)
        self.tabla.setObjectName(u"tabla")

        self.verticalLayout_2.addWidget(self.tabla)

        MainWindow.setCentralWidget(self.centralwidget)

        # self.toolBar.addAction(self.actionModificar)
        # self.toolBar.addAction(self.actionEliminar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))

