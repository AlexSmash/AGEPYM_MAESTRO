'''
Created on 15/08/2013

@author: Lennin
'''
import os

configuracion = """
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

ARCHIVO_CONFIGURACION = os.path.realpath(os.path.join(DIRECTORIO_PROYECTO ,"archivos/configuracion.json"))

DIRECTORIO_TEMPORAL = os.path.realpath(os.path.join(DIRECTORIO_PROYECTO ,"archivos/TMP/"))

_DEBUG = False
