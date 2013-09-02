# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Chris\Desktop\CICLO VIII\DSI\Windows\LoginWin.ui'
#
# Created: Sun Sep 01 20:10:02 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui # @UnresolvedImport
from Utils.Imagenes import obtenerPathIcono

class Ui_LogInWindow(object):
    def setupUi(self, LogInWindow):
        LogInWindow.setObjectName("LogInWindow")
        LogInWindow.resize(468, 191)
        self.centralwidget = QtGui.QWidget(LogInWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.fotoLbl = QtGui.QLabel(self.centralwidget)
        self.fotoLbl.setMaximumSize(QtCore.QSize(125, 125))
        self.fotoLbl.setAutoFillBackground(True)
        self.fotoLbl.setStyleSheet("")
        self.fotoLbl.setLineWidth(2)
        self.fotoLbl.setText("")
        self.fotoLbl.setPixmap(QtGui.QPixmap(obtenerPathIcono("user.png")))
        self.fotoLbl.setScaledContents(True)
        self.fotoLbl.setObjectName("fotoLbl")
        self.verticalLayout_2.addWidget(self.fotoLbl)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.usuarioTxt = QtGui.QLineEdit(self.centralwidget)
        self.usuarioTxt.setObjectName("usuarioTxt")
        self.verticalLayout.addWidget(self.usuarioTxt)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.contraTxt = QtGui.QLineEdit(self.centralwidget)
        self.contraTxt.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText)
        self.contraTxt.setEchoMode(QtGui.QLineEdit.Password)
        self.contraTxt.setObjectName("contraTxt")
        self.verticalLayout.addWidget(self.contraTxt)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.aceptarBtn = QtGui.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(obtenerPathIcono("dialog-ok.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aceptarBtn.setIcon(icon)
        self.aceptarBtn.setObjectName("aceptarBtn")
        self.horizontalLayout_2.addWidget(self.aceptarBtn)
        self.cancelarBtn = QtGui.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(obtenerPathIcono("dialog-cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelarBtn.setIcon(icon1)
        self.cancelarBtn.setObjectName("cancelarBtn")
        self.horizontalLayout_2.addWidget(self.cancelarBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        LogInWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(LogInWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 468, 21))
        self.menubar.setObjectName("menubar")
        LogInWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(LogInWindow)
        self.statusbar.setObjectName("statusbar")
        LogInWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LogInWindow)
        QtCore.QObject.connect(self.aceptarBtn, QtCore.SIGNAL("clicked()"), LogInWindow.aceptar)
        QtCore.QObject.connect(self.cancelarBtn, QtCore.SIGNAL("clicked()"), LogInWindow.cancelar)
        QtCore.QObject.connect(self.usuarioTxt, QtCore.SIGNAL("editingFinished()"), LogInWindow.cargarImagen)
        QtCore.QMetaObject.connectSlotsByName(LogInWindow)

    def retranslateUi(self, LogInWindow):
        LogInWindow.setWindowTitle(QtGui.QApplication.translate("LogInWindow", "MAESTRO - Iniciar Sesión", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LogInWindow", "Usuario: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LogInWindow", "Contraseña:", None, QtGui.QApplication.UnicodeUTF8))
        self.aceptarBtn.setText(QtGui.QApplication.translate("LogInWindow", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelarBtn.setText(QtGui.QApplication.translate("LogInWindow", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))

