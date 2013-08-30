#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on 26/08/2013

@author: usuario
'''
from Utils.Entidad import BaseEntidad
from Utils.ConectorBD import ConexionBD

class Promotora(BaseEntidad):
    '''
    classdocs
    
    create table PROMOTORA (
       IDPROMOTORA          INT4                 not null,
       IDMUNICIPIO          INT4                 not null,
       NOM_PROMOTORA        VARCHAR(25)          not null,
       constraint PK_PROMOTORA primary key (IDPROMOTORA)
    );
    '''
    SENTENCIA_SELECT_TODOS = "SELECT * FROM PROMOTORA;"
    
    SENTENCIA_SELECT_UNO = "SELECT * FROM PROMOTORA WHERE idPromotora=%(parametroID)s;"
    
    SENTENCIA_INSERT = """INSERT INTO PROMOTORA(idPromotora, idMunicipio, nomPromotora)
                            VALUES (%(idPromotora)s,%(idMunicipio)s, %(nomPromotora)s;"""
                                                        
    SENTENCIA_UPDATE ="""UPDATE PROMOTORA SET idMunicipio=%(idMunicipio)s, nomPromotora=%(nomPromotora)s
                                WHERE idPromotora=%(idPromotora)s;"""
                                                             
    SENTENCIA_DELETE = "DELETE FROM DEPARTAMENTO WHERE idDepto=%(idDepto)s;"

    def __init__(self,idPromotora,idMunicipio,nomPromotora):
        '''
        Constructor
        '''
        self.idPromotora=idPromotora
        self.idMunicipio=idMunicipio
        self.nomPromotora=nomPromotora
        
    @classmethod
    def tupla2Promotora(cls,tupla):
        idPromotora = tupla[0]
        idMunicipio = tupla[1]
        nomPromotora = tupla[2]        
        return Promotora(idPromotora,idMunicipio,nomPromotora)
    
    @classmethod
    def consultarUno(cls,cod):
        d={}
        d["idPromotora"]=cod
        cnn=ConexionBD(Promotora.SENTENCIA_SELECT_UNO, d, ConexionBD.SELECT)
        pro=cnn.obtenerUno(conversor=Promotora.tupla2Promotora)
        return pro
    
    @classmethod
    def consultarTodos(cls):
        cnn=ConexionBD(Promotora.SENTENCIA_SELECT_TODOS)
        return cnn.obtenerTodos(conversor=Promotora.tupla2Promotora)
    
    @classmethod
    def consultarN(cls,N=3):
        cnn = ConexionBD(Promotora.SENTENCIA_SELECT_TODOS)
        return cnn.obtenerVarios(N, conversor=Promotora.tupla2Promotora)
    
    @classmethod
    def agregar(cls,ent):
        d={}
        d["idPromotora"]=ent.idPromotora
        d["idMunicipio"]=ent.idMunicipio
        d['nomPromotora']=ent.nomPromotora
        cnn=ConexionBD(Promotora.SENTENCIA_INSERT, d, ConexionBD.INSERT)
        cnn.ejecutar()
    
    @classmethod
    def modificar(cls,ent):
        d={}
        d['idPromotora']=ent.idPromotora
        d['idMunicipio']= ent.idMunicipio
        d['nomPromotora']= ent.nomPromotora
        cnn = ConexionBD(Promotora.SENTENCIA_UPDATE,d,ConexionBD.UPDATE)
        cnn.ejecutar()
    
    @classmethod
    def eliminar(cls,cod):
        d={}
        d['idPromotora']=cod
        cnn = ConexionBD(Promotora.SENTENCIA_DELETE,d,ConexionBD.DELETE)
        cnn.ejecutar()