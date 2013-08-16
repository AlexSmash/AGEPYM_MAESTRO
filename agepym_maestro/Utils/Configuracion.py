'''
Created on 15/08/2013

@author: Lennin
'''

import json


from Singleton import Singleton

from Constantes import ARCHIVO_CONFIGURACION

def busquedaProfundidadDic(dic,llave):
    if llave in dic: return dic[llave]
    elif isinstance(dic,dict):
        for key, val in dic.items():
            if key == llave:
                return val
            if isinstance(val, dict):
                item = busquedaProfundidadDic(val,llave)
                if item is not None:
                    return item
        return None
    else:
        return None

def modificarProfundidadDic(dic, nuevo, llave):
    if llave in dic: dic[llave] = nuevo
    elif isinstance(dic,dict):
        for key, val in dic.items():
            if key == llave:
                dic[key] = nuevo
                return None
            if isinstance(val, dict):
                modificarProfundidadDic(val, nuevo, llave)
        return None
    else:
        return None


class Configuracion(Singleton):
    _dic = {}
    def __init__(self):
        self._dic = json.load(open(ARCHIVO_CONFIGURACION))

    def obtenerValor(self,llave = "CONFIGURACIONES",busquedaProfundidad= True):
        llave = unicode(llave.upper())
        if busquedaProfundidad:
            return busquedaProfundidadDic(self._dic,llave)
        else:
            if llave in self._dic:
                return self._dic[llave]
            else:
                return None

    def modificarValor(self, nuevo, llave, busquedaProfundidad= True):
        llave = unicode(llave.upper())
        if busquedaProfundidad:
            return modificarProfundidadDic(self._dic, nuevo,llave)
        else:
            if llave in self._dic:
                self._dic[llave] = nuevo

    def guardarArchivo(self):
        json.dump(self._dic,open(ARCHIVO_CONFIGURACION,mode="w"),indent=4)

def pruebaPatronSingleton():
    cnf = Configuracion()
    cnf2 = Configuracion()
    cnf2.modificarValor("90","PORT")
    cnf.modificarValor("5432","PORT")
    cnf2.guardarArchivo()
    assert cnf is cnf2
    print("PRUEBAS A CONFIGURACION HECHAS SATISFACTORIAMENTE")

if __name__ == '__main__':
    pruebaPatronSingleton()
