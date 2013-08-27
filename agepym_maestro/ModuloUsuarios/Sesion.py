#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on 23/08/2013

@author: Lennin
'''

from Utils.Singleton import Singleton
from ModuloUsuarios.Usuario import Usuario
from Utils.ConectorBD import ConexionBD

class Sesion(Singleton):
    '''
    Clase Singleton que manejara la sesion Actual, permitiendo el acceso a 
    un usuario que ya existe en memoria, o que se conozca su nombre de 
    usuario y contrasena o que solamente se conozca su nombre de usuario
    (teniendo que ceder la contrasena en un futuro para obtener acceso)
    
    USOS:
     1- Si el usuario ya esta instanciado
         user = Usuario(....) # Usuario ya instanciado
         sesion = Sesion(usuario=user)
         tieneAcceso = sesion.esValida() # True
    
    2- Si se conoce nombre y password del usuario
        nombre = "Lennin"
        passw = "_prueba_"
        sesion = Sesion(username=nombre,password=passw)
        tieneAcceso = sesion.esValida() # True
        
    3- Si se tiene nada mas el nombre de usuario y en un futuro se dara el password
        nombre = "Lennin"
        sesion = Sesion(username=nombre) # El password aun no se ha ingresado
        tieneAcceso = sesion.esValida() # False
        passw = "_prueba_"
        sesion.verificarPassword(passw) # Se ingresa el password
        tieneAcceso = sesion.esValida() # True
        
    4- Si en cualquier momento de ejecucion se necesita conocer los datos de sesion 
    actual:
        from ModuloUsuarios.Sesion import Sesion
        
        sesion = Sesion()
        
    5- Si es necesario conocer el objeto usuario vinculado a la sesion:
        from ModuloUsuarios.Sesion import Sesion
        
        sesion = Sesion()
        usuario = sesion.Usuario
        dirFoto = usuario.dir_foto # Direccion de la foto del usuario en el directorio temporal
    '''


    def __init__(self,  *a, **kw):
        '''
        Constructor
        '''
        if "usuario" in kw:
            # Utilizar el objeto usuario e iniciar sesion
            self._esValida = True
            self.Usuario = kw["usuario"]
            self._verificarPassword = False
        elif "username" in kw and "password" in kw :
            # Crear el objeto usuario e iniciar sesion
            self._esValida = False
            user = Sesion.verificarUsuario(kw["username"],kw["password"])
            if user is None:
                self._esValida = False
                self._verificarPassword = True
            else:
                self._esValida= True
                self.Usuario = user
                self._verificarPassword = False
        elif "username" in kw and "password" not in kw :
            # Obtener el objeto Usuario y pedir verificacion de password
            user = Usuario.consultarUno(kw["username"])
            self._esValida= True
            self.Usuario = user
            self._verificarPassword = True
        else:
            # No hacer nada y salir
            self._esValida = False
            self._verificarPassword = True
            
    
    def esValida(self):
        return self._esValida and not self._verificarPassword
    
    def debeVerificarPassword(self):
        return self._verificarPassword
    
    def verificarPassword(self,password):
        user = Sesion.verificarUsuario(self.Usuario.user,password)
        if user is None:
            self._esValida = False
            self._verificarPassword = True
        else:
            self._esValida= True
            self.Usuario = user
            self._verificarPassword = False
            
    def cerrarSesion(self):
        Sesion.borrar()
        self.Usuario = None
        self._esValida= False
        self._verificarPassword = True
    
    @classmethod
    def borrar(cls):
        cls._instance = None
    
    
    @classmethod
    def verificarUsuario(cls,username,password):
        sql = """SELECT COUNT(*) FROM usuario WHERE usuario=%(usuario)s and (contrasena=%(passw)s or contrasena=encode(digest(%(passw)s, 'sha256'),'hex'));"""
        d = {"usuario":username,"passw":password}
        count = 0 
        # Verificacion de cantidad de usuarios:
        try:
            # Tratar de insertar el usuario con la contrasena encriptada
            cnn  = ConexionBD(sql, d)
            count = cnn.obtenerUno()[0]
        except Exception, e1:
            count = 0
            print(e1) 
                
        if count>0:
            # si la cantidad de usuarios es mayor a cero retornar usuario
            return Usuario.consultarUno(username)
        else:
            return None

def pruebasSesion():
    print("INICIO DE PRUEBAS\n")
    #print("\n ************************ Prueba usuario cargado ************************ ")
    user = "Lennin"
    user = Usuario.consultarUno(user)
    s = Sesion(usuario=user)
    assert s.Usuario == user
    assert s.esValida() == True
    assert s.debeVerificarPassword() == False
    assert s==Sesion()
    s.cerrarSesion()
    
    #print("\n ************************ Prueba usando username y password incorrecto ************************ ")
    s = Sesion(username="Lennin2",password="_prueba3_")
    assert s.esValida() == False
    assert s.debeVerificarPassword() == True
    assert s==Sesion()
    s.cerrarSesion()
    
    #print("\n ************************ Prueba usando username y password ************************ ")
    s = Sesion(username="Lennin2",password="_prueba2_")
    assert s.esValida() == True
    assert s.debeVerificarPassword() == False
    assert s==Sesion()
    s.cerrarSesion()
    
    #print("\n ************************ Prueba con usuario sin pass ************************ ")
    s = Sesion(username="Lennin3")
    assert s.esValida() == False
    assert s.debeVerificarPassword() == True
    # VERIFICANDO EL PASS INCORRECTO
    s.verificarPassword("_prueba2_")
    assert s.esValida() == False
    assert s.debeVerificarPassword() == True
    # VERIFICANDO EL PASS CORRECTO
    s.verificarPassword("_prueba3_")
    assert s.esValida() == True
    assert s.debeVerificarPassword() == False
    # VERIFICANDO EL PASS INCORRECTO
    s.verificarPassword("_prueba2_")
    assert s.esValida() == False
    assert s.debeVerificarPassword() == True
    assert s==Sesion()
    s.cerrarSesion()
    
    print("\n PRUEBAS EJECUTADAS CON EXITO")
    
    
    
    
if __name__ == "__main__":
    pruebasSesion()    
        
        
        