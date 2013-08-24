#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on 15/08/2013

@author: Lennin
'''

class Singleton(object):
    '''
    Clase singleton, todas las clases que la hereden
    tendrán  solamente 1 instancia en toda la ejecución.
    
    Uso:
    
    # Creación de la clase:
    class SingletonSubClass(Singleton):
        ...
        def __init__(self):
            # poner inicializadores y otras funciones
            pass
        
    # Instanciación de la clase:
    
    s1 = SingletonSubClass()
    s2 = SingetonSubClass()
    
    # s1 y s2  referencian al mismo objeto
    assert s1 == s2 # Asercion, si ambos no son iguales se produce una excepcion
    
    assert s1 is s2 # Asercion, si ambos no son el mismo se produce una excepcion
    
    '''
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def borrar(cls):
        Singleton._instance = None