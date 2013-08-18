'''
Created on 15/08/2013

@author: Lennin
'''

class BaseEntidad():
    '''
    Clase que debera ser implementada por entidades como:
    asociado, beneficiario, pagaduria , etc
    '''
        
    @classmethod
    def agregar(cls,ent):
        raise NotImplementedError()
    
    @classmethod
    def modificar(cls,ent):
        raise NotImplementedError()
    
    @classmethod
    def eliminar(cls,cod):
        raise NotImplementedError()
    
    @classmethod
    def consultarUno(cls,cod):
        raise NotImplementedError()
    
    @classmethod
    def consultarTodos(cls):
        raise NotImplementedError()
    
    @classmethod
    def consultarN(cls,N=3):
        raise NotImplementedError()