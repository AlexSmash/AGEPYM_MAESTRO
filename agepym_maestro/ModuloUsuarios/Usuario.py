'''
Created on 17/08/2013

@author: Lennin
'''
from Utils import Entidad, Imagenes, Constantes
from Utils.ConectorBD import ConexionBD
import os

class Usuario(Entidad.BaseEntidad):
    '''
    Clase entidad Usuario
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
    
    SENTENCIA_INSERT_HASHED = """INSERT INTO usuario(usuario, contrasena, nom_completo, nivel, cargo_usuario, foto)
                            VALUES (%(usuario)s, encode(digest(%(passw)s, 'sha256'), 'hex'), %(nombre)s, %(nivel)s, %(cargo)s, %(foto)s);"""
                            
    SENTENCIA_INSERT = """INSERT INTO usuario(usuario, contrasena, nom_completo, nivel, cargo_usuario, foto)
                            VALUES (%(usuario)s, %(passw)s, %(nombre)s, %(nivel)s, %(cargo)s, %(foto)s);"""
                            
    SENTENCIA_UPDATE ="""UPDATE usuario SET nom_completo=%(nombre)s, nivel=%(nivel)s, cargo_usuario=%(cargo)s, 
                                foto=%(foto)s WHERE usuario=%(usuario)s;"""
                                                             
    SENTENCIA_DELETE = "DELETE FROM usuario WHERE usuario=%(usuario)s;"
    
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
        return self.obtenerDiccionarioDatos()
    
    def __unicode__(self):
        return self.obtenerDiccionarioDatos()
    
    def __repr__(self):
        return str(self.obtenerDiccionarioDatos())
            
    @classmethod
    def agregar(cls,ent):
        d = ent.obtenerDiccionarioDatos()
        try:
            # Tratar de insertar el usuario con la contrasena encriptada
            cnn  = ConexionBD(cls.SENTENCIA_INSERT_HASHED, d,ConexionBD.INSERT)
            cnn.ejecutar()
        except Exception, e1:
            try:
                # Tratar de insertar el usuario con la contrasena en texto plano
                cnn  = ConexionBD(cls.SENTENCIA_INSERT, d,ConexionBD.INSERT)
                cnn.ejecutar()
            except Exception, e2:
                print(e1)
                print(e2)
        
    
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
    
    print(Usuario.consultarTodos())
    
if __name__ == "__main__":
    pruebasUsuario()
    
    
    