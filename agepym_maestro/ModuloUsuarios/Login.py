'''
Created on 27/08/2013

@author: Kath
'''

from PySide import QtCore # @UnresolvedImport
from PySide.QtGui import QMainWindow, QApplication # @UnresolvedImport
from Ventanas.LoginWindow import Ui_LogInWindow
from ModuloUsuarios.Sesion import Sesion
from Utils.Constantes import absPath
import sys

class LoginWindow(QMainWindow, Ui_LogInWindow):
    """
        Clase controladora de la ventana Login
    """

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.sesion = Sesion()
        #conecciones 
        self.connect(self.aceptarBtn, QtCore.SIGNAL('clicked()'), self.aceptar)
        self.connect(self.cancelarBtn, QtCore.SIGNAL('clicked()'), self.cancelar)
        self.connect(self.usuarioTxt, QtCore.SIGNAL('editingFinished()'), self.cargarImagen)
        
    def cargarImagen(self):
        #self.label.setText("Carga de imagen")
        nombre = self.usuarioTxt.text()
        self.sesion = Sesion(username=nombre)
        if self.sesion._esValida == True :
            self.fotoLbl.setPixmap(absPath(self.sesion.Usuario.dir_foto))
        
    def aceptar(self):
        #verificacion password
        #self.label.setText("Aceptar")
        password = self.contraTxt.text()
        self.sesion.verificarPassword(password)
        if self.sesion.esValida() :
            self.label.setText("Usuario valido")
            self.limpiar()
            #redirigir a ventana principal, con sesion

    def cancelar(self):
        self.limpiar()
    
    def limpiar(self):
        self.usuarioTxt.setText(" ")
        self.contraTxt.setText(" ")
        
def pruebaLogin():
    print("INICIO DE PRUEBAS\n")
    app = QApplication(sys.argv)
    frame = LoginWindow()
    frame.show()
    app.exec_()

if __name__ == "__main__":
    pruebaLogin() 
        