#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on 26/08/2013

@author: usuario
'''
from Utils.Entidad import BaseEntidad
from Utils.ConectorBD import ConexionBD

class Departamento(BaseEntidad):
    '''
    classdocs
    TABLA USADA EN LA BD: 
    
        create table DEPARTAMENTO (
           idDepto              INTEGER              not null,
           nom_depto            VARCHAR(70)          not null,
           constraint PK_DEPTO primary key (idDepto)
        );
    
    '''
    SENTENCIA_SELECT_TODOS = "SELECT * FROM DEPARTAMENTO;"
    
    SENTENCIA_SELECT_UNO = "SELECT * FROM DEPARTAMENTO WHERE idDepto=%(idDepto)s;"
    
    SENTENCIA_INSERT = """INSERT INTO DEPARTAMENTO(idDepto, nomDepto)
                            VALUES (%(idDepto)s,%(nomDepto)s;"""
                                                        
    SENTENCIA_UPDATE ="""UPDATE DEPARTAMENTO SET nomDepto=%(nomDepto)s
                                WHERE idDepto=%(idDepto)s;"""
                                                             
    SENTENCIA_DELETE = "DELETE FROM DEPARTAMENTO WHERE idDepto=%(idDepto)s;"


    def __init__(self,idDepto,nomDepto):
        '''
        Constructor
        
        '''
        self.idDepto=idDepto
        self.nomDepto=nomDepto
        
    @classmethod
    def consultarUno(cls,cod):
        d={}
        d["idDepto"]=cod
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
    
    @classmethod
    def agregar(cls,ent):
        d={}
        d['idDepto']=ent.idDepto
        d['nomDepto']= ent.nomDepto
        cnn = ConexionBD(Departamento.SENTENCIA_INSERT,d,ConexionBD.INSERT)
        cnn.ejecutar()
    
    @classmethod
    def modificar(cls,ent):
        d={}
        d['idDepto']=ent.idDepto
        d['nomDepto']= ent.nomDepto
        cnn = ConexionBD(Departamento.SENTENCIA_UPDATE,d,ConexionBD.UPDATE)
        cnn.ejecutar()
    
    @classmethod
    def eliminar(cls,cod):
        d={}
        d['idDepto']=cod
        cnn = ConexionBD(Departamento.SENTENCIA_DELETE,d,ConexionBD.DELETE)
        cnn.ejecutar()
    