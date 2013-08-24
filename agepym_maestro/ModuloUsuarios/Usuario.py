#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
Created on 17/08/2013

@author: Lennin
'''
from Utils import Entidad, Imagenes, Constantes
from Utils.ConectorBD import ConexionBD
import os

class Usuario(Entidad.BaseEntidad):
    '''
    Clase entidad Usuario, manejará  las operaciones básicas de un usuario 
    en la BD (agregar, consultar, modificar y eliminar usuarios)
    
    Uso: 
    username = 'username'
    contrasena = 'password'
    nombre = 'nombre completo'
    nivel = 1
    cargo = 'Secretaria'
    foto = 'C:/DIRECCION_A_LA_FOTO/foto.jpg'
    u = Usuario(username, contrasena, nombre, nivel, cargo, foto)
    
    Usuario.agregar(u) # agrega el usuario a la BD
    
    nuevo_nombre = "NUEVO NOMBRE"
    u.nombre = nuevo_nombre
    
    Usuario.modificar(u) # actualiza el usuario en la BD
    
    Usuario.eliminar(u.user) # elimina el usuario de la BD
    
    username = "user"
    u = Usuario.consultarUno(username) # obtiene el usuario de la BD
    
    l = Usuario.consultarTodos() # obtiene todos los usuarios de la BD en una lista de objetos Usuario
    
    N = 5
    lg = Usuario.consultarN(N) # obtiene un iterador que contiene N usuarios por iteración
    
    # Una forma de usarlo
    for l in lg:        # recorre el generador "lg" e itera guardando en "l"
        for u in l:     # recorre la lista "l" e itera guardando en "u"
            print(u)    # imprime el usuario "u"
            
    # otro uso:
    l = lg.next()       # obtiene los primeros N usuarios y los guarda en "l"
    for u in l:
        hacerAlgo(u)    # hace algo con el usuario "u"
        
    l = lg.next()       # obtiene los siguientes N usuarios y los guarda en "l"
    
    hacerOtraCosa(l)    # hace otra cosa con la lista "l" (que contiene objetos usuario)
    
    # lg.next() se puede utilizar hasta que no se puedan generar mas listas,
    # si se llega a la cantidad maxima de generaciones emitirá una excepcion.
    
    # NOTA: De las formas anteriores de usar el iterador, solo se puede utilizar una
    
    
    # Modificar imagen del usuario
    nuevo_path = "C:/NUEVAIMAGEN.jpg"
    u.cambiarImagen(nuevo_path,alterarBD=True) 
    # con alterarBD se cambia la imagen en la BD (dejar vacío y tomará valor por defecto True)
    
    #Modificar password del usuario
    nuevo_pass = "_nueva_pass_123123@"
    u.cambiarPassword(nuevo_pass) #cambia el pasword en la BD tambien
    
    
    TABLA USADA EN LA BD: 
    
    create table USUARIO (
       USUARIO              VARCHAR(25)          not null,
       CONTRASENA           VARCHAR(70)          not null,
       NOM_COMPLETO         VARCHAR(30)          not null,
       NIVEL                INT4                 not null,
       CARGO_USUARIO        VARCHAR(20)          not null,
       FOTO                 BYTEA  ,
       constraint PK_USUARIO primary key (USUARIO)
    );
    '''
    

    SENTENCIA_SELECT_TODOS = "SELECT * FROM usuario;"
    
    SENTENCIA_SELECT_UNO = "SELECT * FROM usuario WHERE usuario=%(usuario)s;"
    
    SENTENCIA_INSERT = """INSERT INTO usuario(usuario, contrasena, nom_completo, nivel, cargo_usuario, foto)
                            VALUES (%(usuario)s, encode(digest(%(passw)s, 'sha256'), 'hex'), %(nombre)s, %(nivel)s, %(cargo)s, %(foto)s);"""
                                                        
    SENTENCIA_UPDATE ="""UPDATE usuario SET nom_completo=%(nombre)s, nivel=%(nivel)s, cargo_usuario=%(cargo)s, 
                                foto=%(foto)s WHERE usuario=%(usuario)s;"""
                                                             
    SENTENCIA_DELETE = "DELETE FROM usuario WHERE usuario=%(usuario)s;"
    
    SENTENCIA_ACTUALIZAR_PASS = "UPDATE usuario set contrasena= encode(digest(%(passw)s, 'sha256'), 'hex') where usuario=%(usuario)s;"
    
    def obtenerDiccionarioDatos(self):
        d = {}
        d["usuario"] = self.user
        d["passw"] = self.contrasena
        d["nombre"] = self.nombre
        d["nivel"] = self.nivel
        d["cargo"] = self.cargo
        d["foto"] = Imagenes.convertirImagen(self.foto)
        return d
    
    def __init__(self,usuario,contrasena,nom_completo,nivel,cargo,dir_foto):
        '''
        Constructor
        '''
        self.user = usuario
        self.contrasena = contrasena
        self.nombre = nom_completo
        self.nivel = nivel
        self.cargo = cargo
        self.foto = Imagenes.readImage(dir_foto)
        self.dir_foto = dir_foto
        
    def __str__(self):
        return str(self.obtenerDiccionarioDatos())
    
    def __unicode__(self):
        return unicode(str(self.obtenerDiccionarioDatos()))
    
    def __repr__(self):
        return str(self.obtenerDiccionarioDatos())
    
    def cambiarImagen(self,pathImagen,alterarBD=True):
        self.foto = Imagenes.readImage(pathImagen)
        self.dir_foto = pathImagen
        if alterarBD: Usuario.modificar(self)
        
    def cambiarPassword(self,nuevoPass):
        self.contrasena = nuevoPass
        d = {"passw":nuevoPass,"usuario":self.user}
        try:
            cnn = ConexionBD(Usuario.SENTENCIA_ACTUALIZAR_PASS,d,ConexionBD.UPDATE)
            cnn.ejecutar(cerrarAlFinalizar=True)
        except Exception, e1:
            print(e1)
        
            
    @classmethod
    def agregar(cls,ent):
        d = ent.obtenerDiccionarioDatos()
        try:
            # Tratar de insertar el usuario con la contrasena encriptada
            cnn  = ConexionBD(cls.SENTENCIA_INSERT, d,ConexionBD.INSERT)
            cnn.ejecutar()
        except Exception, e1:
            print(e1)
        
    
    @classmethod
    def modificar(cls,ent):
        d = ent.obtenerDiccionarioDatos()
        try:
            cnn  = ConexionBD(cls.SENTENCIA_UPDATE, d,ConexionBD.INSERT)
            cnn.ejecutar()
        except Exception, e1:
            print(e1)
    
    @classmethod
    def eliminar(cls,user):
        d= {}
        d["usuario"] = user
        cnn = ConexionBD(cls.SENTENCIA_DELETE, d)
        cnn.ejecutar()
    
    @classmethod
    def consultarUno(cls,user,cursor_factory=None):
        d= {}
        d["usuario"] = user
        cnn = ConexionBD(cls.SENTENCIA_SELECT_UNO, d)
        return cnn.obtenerUno(cursor_factory,conversor=Usuario.tuplaToUsuario)
    
    @classmethod
    def consultarTodos(cls,cursor_factory=None):
        cnn = ConexionBD(cls.SENTENCIA_SELECT_TODOS)
        return cnn.obtenerTodos(cursor_factory,conversor=Usuario.tuplaToUsuario)
    
    @classmethod
    def consultarN(cls,N=3,cursor_factory=None):
        cnn = ConexionBD(cls.SENTENCIA_SELECT_TODOS)
        return cnn.obtenerVarios(N,cursor_factory,conversor=Usuario.tuplaToUsuario)
    
    @classmethod
    def tuplaToUsuario(cls,tupla):
        if tupla is not None: 
            return Usuario(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], Imagenes.writeImage(tupla[5]))

def pruebasUsuario():
    user = "Lennin"
    pasw = "_prueba_"
    nom = "Lennin Hernandez"
    nivel = 1
    cargo = "Desarrollador"
    imagen = os.path.realpath(os.path.join(Constantes.DIRECTORIO_TEMPORAL ,"prueba.jpg"))
    user = Usuario(user, pasw, nom, nivel, cargo, imagen)
    Usuario.agregar(user)
    
    
    user = "Lennin2"
    pasw = "_prueba2_"
    nom = "Lennin2 Hernandez2"
    nivel = 1
    cargo = "Desarrollador"
    imagen = os.path.realpath(os.path.join(Constantes.DIRECTORIO_TEMPORAL ,"prueba.jpg"))
    user = Usuario(user, pasw, nom, nivel, cargo, imagen)
    Usuario.agregar(user)
    
    user = "Lennin3"
    pasw = "_prueba3_"
    nom = "Lennin3 Hernandez3"
    nivel = 1
    cargo = "Desarrollador"
    imagen = os.path.realpath(os.path.join(Constantes.DIRECTORIO_TEMPORAL ,"prueba.jpg"))
    user = Usuario(user, pasw, nom, nivel, cargo, imagen)
    Usuario.agregar(user)
    
    userE = "_borrar_prueba"
    pasw = "_prueba4_"
    nom = "Prueba de borrado"
    nivel = 1
    cargo = "Desarrollador"
    imagen = os.path.realpath(os.path.join(Constantes.DIRECTORIO_TEMPORAL ,"prueba.jpg"))
    user = Usuario(userE, pasw, nom, nivel, cargo, imagen)
    Usuario.agregar(user)
    
    print(Usuario.consultarTodos())
    
    Usuario.eliminar(userE)
    
    assert Usuario.consultarUno(userE) is None
    
if __name__ == "__main__":
    pruebasUsuario()
    
    
    