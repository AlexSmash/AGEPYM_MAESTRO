'''
Created on 26/08/2013

@author: usuario
'''
from Utils.Entidad import BaseEntidad
from Utils.ConectorBD import ConexionBD

class Departamento(BaseEntidad):
    '''
    classdocs
    '''
    SENTENCIA_SELECT_TODOS = "SELECT * FROM DEPARTAMENTO;"
    
    SENTENCIA_SELECT_UNO = "SELECT * FROM DEPARTAMENTO WHERE idDepto=%(parametroID)s;"
    
    SENTENCIA_INSERT = """INSERT INTO usuario(usuario, contrasena, nom_completo, nivel, cargo_usuario, foto)
                            VALUES (%(usuario)s, encode(digest(%(passw)s, 'sha256'), 'hex'), %(nombre)s, %(nivel)s, %(cargo)s, %(foto)s);"""
                                                        
    SENTENCIA_UPDATE ="""UPDATE usuario SET nom_completo=%(nombre)s, nivel=%(nivel)s, cargo_usuario=%(cargo)s, 
                                foto=%(foto)s WHERE usuario=%(usuario)s;"""
                                                             
    SENTENCIA_DELETE = "DELETE FROM usuario WHERE usuario=%(usuario)s;"


    def __init__(self,idDepto,nom_depto):
        '''
        Constructor
        TABLA USADA EN LA BD: 
    
        create table DEPARTAMENTO (
           idDepto              INTEGER              not null,
           nom_depto            VARCHAR(70)          not null,
           constraint PK_DEPTO primary key (idDepto)
        );
        '''
        self.idDepto=idDepto
        self.nom_depto=nom_depto
        
    @classmethod
    def consultarUno(cls,cod):
        d={}
        d["parametroID"]=cod
        cnn=ConexionBD(Departamento.SENTENCIA_SELECT_UNO, d, ConexionBD.SELECT)
        dep = cnn.obtenerUno(conversor=Departamento.tupla2Departamento) # print(dep) >> (1,"Santa Ana")
        return dep
    
    @classmethod
    def tupla2Departamento(cls,tupla):
        cod = tupla[0]
        nombre = tupla[1]        
        return Departamento(cod,nombre)
    
    @classmethod
    def consultarN(cls,N=3):
        cnn = ConexionBD(Departamento.SENTENCIA_SELECT_TODOS)
        return cnn.obtenerVarios(N, conversor=Departamento.tupla2Departamento)
    
    @classmethod
    def consultarTodos(cls):
        cnn = ConexionBD(Departamento.SENTENCIA_SELECT_TODOS)
        return cnn.obtenerTodos(conversor=Departamento.tupla2Departamento)