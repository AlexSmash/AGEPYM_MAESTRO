'''
Created on 15/08/2013

@author: Lennin
'''

class BaseEntidad():
    '''
    Clase que deberá ser implementada por entidades como:
    asociado, beneficiario, pagaduría , etc
    '''
        
    @classmethod
    def agregar(cls,ent):
        raise NotImplementedError()
    
    @classmethod
    def modificar(cls,ent):
        raise NotImplementedError()
    
    @classmethod
    def eliminar(cls,ent):
        raise NotImplementedError()
    
    @classmethod
    def consultarUno(cls,ent):
        raise NotImplementedError()
    
    @classmethod
    def consultarTodos(cls,ent):
        raise NotImplementedError()
    
    @classmethod
    def consultarN(cls,ent):
        raise NotImplementedError()