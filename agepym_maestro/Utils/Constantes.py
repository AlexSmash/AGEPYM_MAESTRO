#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on 15/08/2013

@author: Lennin

Contiene valores de constantes a ser utilizadas en el proyecto

Se agregó la funcion absPath(relPath) que retorna 
la direccion absoluta a partir de una direccion relativa
al proyecto
ejemplo:
 realPath = absPath("archivos/configuracion.json")
 print(realPath) # "C:\Proyecto\archivos\configuracion.json"

'''
import os

CONFIGURACION_ORIGINAL = """
{
    "CONFIGURACIONES":{
        "BASEDATOS":{
            "HOST":"localhost",
            "USER":"app",
            "PASS":"asdf",
            "PORT":"5432",
            "DATABASE":"_pruebaQT"
        }
    }
}
""" 

_DIRECCION_ACTUAL = os.path.dirname(os.path.realpath(__file__))

DIRECTORIO_PROYECTO = os.path.realpath(os.path.join(_DIRECCION_ACTUAL ,".."))

def absPath(relativePath):
    return os.path.realpath(os.path.join(DIRECTORIO_PROYECTO ,relativePath))

ARCHIVO_CONFIGURACION = absPath("archivos/configuracion.json")

DIRECTORIO_TEMPORAL = absPath("archivos/TMP/")

_DEBUG = False
