#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
Created on 15/08/2013

@author: Lennin
'''

import psycopg2  # @UnresolvedImport
from psycopg2.extras import DictCursor, RealDictCursor, NamedTupleCursor # @UnresolvedImport
from psycopg2 import errorcodes # @UnresolvedImport
from Configuracion import Configuracion
from Utils import Constantes

def obtenerConexion():
    cnf = Configuracion()._dic["CONFIGURACIONES"]["BASEDATOS"]
    host = cnf["HOST"]
    db = cnf["DATABASE"]
    port = cnf["PORT"]
    user = cnf["USER"]
    pasw = cnf["PASS"]
    conexion = psycopg2.connect(database=db, user=user, 
                            password=pasw, port=port, host=host)
    return conexion

class ConexionBD():
    '''
    Clase que permite hacer consultas a la base de datos, esta clase es de bajo nivel
    de preferencia usar las clases entidades si se trabaja directamente con las tablas
    de la Base de Datos.
    
    Uso:
    from utils.ConectorBD import ConexionBD
    
    # CONSULTA SELECT:
    sql = "SELECT * FROM TABLA where(param1=%(p1)s);"
    d = {}
    d['p1'] = param1
    cnn = ConexionBD(sql,d,ConexionBD.SELECT)
    l = cnn.obtenerTodos()     # obtiene una lista de tuplas
    l = cnn.obtenerUno()       # obtiene una lista con una tupla mejor uso: obtenerUno()[0]
    lg = cnn.obtenerN(N=3)     # obtiene un generador de listas de N elementos
    
    # Uso avanzado de las funciones "obtener":
    l = cnn.obtenerTodos(conversor=ConexionBD.DICCIONARIO) 
        # retona una lista de (pseudo)diccionarios en los que cada elemento del diccionario es una columna de la seleccion
    l = cnn.obtenerTodos(conversor=ConexionBD.DICCIONARIO_REAL)
        # retona una lista de diccionarios en los que cada elemento del diccionario es una columna de la seleccion
    l = cnn.obtenerTodos(conversor=ConexionBD.TUPLA_NOMBRADA)
        # retona una lista de tuplas nombradas en los que se accesa a las columnas de la seleccion como si fuera un atributo de objeto
    
    # tambien se pueden definir nuevos conversores ejemplo:
    #    Ejemplo diccionario simple:
    def conversorTupla2Dic(tupla):
        d = {}
        d['col1'] = tupla[0]
        d['col2'] = tupla[3]
        d['col3'] = tupla[5]
        ...
        return d
    
    l = cnn.obtenerTodos(conversor=conversorTupla2Dic)
        # retornar� una lista de diccionarios con llaves ['col1','col2','col3']
    
    #    Ejemplo objeto definido por el usuario:
    
    class Objeto():
        def __init__(self,col1,col2,col3):
            self.col1 = col1
            self.col2 = col2
            self.col3 = col3
        
        @classmethod
        def tupla2Object(cls,tupla):
            obj = Objeto(tupla[0],tupla[3],tupla[5])
            return obj
    
    l = cnn.obtenerTodos(conversor=Objeto.tupla2Object)
        # Retornará una lista de objetos del tipo Objeto
    
    # Nota todas las funciones soportan el parametro conversor.
    
    
    # CONSULTAS INSERT, DELETE y UPDATE:
    sql = "UPDATE TABLA SET param2=0 WHERE (param1=%(p1)s);"
    d = {}
    d['p1'] = param1
    cnn = ConexionBD(sql,d,ConexionBD.SELECT)
    l = cnn.ejecutar() # se ejecuta la consulta.
    
    # Cerrar la conexion a la bd luego de una consulta
    
    # Esta clase abre la conexion a la base de datos antes de hacer una consulta
    # en los metodos obtenerTodos, obtenerUno, ObtenerVarios y Ejecutar, por defecto
    # al finalizar la consulta (ocurriendo o nó un error) se cierra la conexion, 
    # si es necesario mantener la conexion abierta, se envia un parametro a las funciones
    # antes listadas de esta forma:
    
    cnn.obtenerTodos(cerrarAlFinalizar = True) # cierra la conexion luego de hacer la consulta
    
    
    cnn.obtenerTodos(cerrarAlFinalizar = False) # mantiene la conexion abierta luego de finalizar la consulta
    
    # Esto aplica para las funciones: (obtenerTodos, obtenerUno, obtenerVarios y ejecutar).
    '''
    
    # TIPOS SENTENCIA
    SELECT = "SENTENCIA SELECT"
    INSERT = "SENTENCIA INSERT"
    DELETE = "SENTENCIA DELETE"
    UPDATE = "SENTENCIA UPDATE"
    
    #TIPOS CURSOR
    DICCIONARIO = DictCursor
    DICCIONARIO_REAL = RealDictCursor
    TUPLA_NOMBRADA = NamedTupleCursor
    
    
    
    def __init__(self, consulta,params = None, tipoConsulta=None):
        self.conexion = obtenerConexion()
        self.sentencia = consulta
        self.parametros = params
        if tipoConsulta is None: tipoConsulta = ConexionBD.SELECT
        self.tipoConsulta = tipoConsulta
        
    def abrir(self):
        self.conexion.open()
    
    def cerrar(self):
        if not self.cursor.closed: self.cursor.close()
        if not self.conexion.closed : self.conexion.close()
        
    def ejecutar(self,cerrarAlFinalizar = True):
        self.cursor = self.conexion.cursor()
        if Constantes._DEBUG: print(self.cursor.mogrify(self.sentencia, self.parametros))
        self.cursor.execute(self.sentencia, self.parametros)
        self.conexion.commit()
        if cerrarAlFinalizar: self.cerrar()
        
    def obtenerTodos(self,cursor_factory=None, cerrarAlFinalizar = True, conversor= None):
        self.__crearCursor(cursor_factory)
        valores = self.cursor.fetchall()
        if cerrarAlFinalizar: self.cerrar()
        if conversor is not None: valores = [conversor(valor) for valor in valores]
        return valores
    
    def obtenerUno(self, cursor_factory=None, cerrarAlFinalizar = True, conversor= None):
        self.__crearCursor(cursor_factory)
        valor = self.cursor.fetchone()
        if cerrarAlFinalizar: self.cerrar()
        if conversor is not None: valor = conversor(valor)
        return valor
    
    def obtenerVarios(self, cant, cursor_factory = None, cerrarAlFinalizar = True, conversor= None):
        self.__crearCursor(cursor_factory)
        while True:
            valores = self.cursor.fetchmany(cant)
            if not valores: 
                if cerrarAlFinalizar: self.cerrar()
                break
            if conversor is not None: valores = [conversor(valor) for valor in valores]
            yield valores
    
    def __crearCursor(self, cursor_factory = None):
        if cursor_factory is None or not (cursor_factory is ConexionBD.DICCIONARIO or 
                                          cursor_factory is ConexionBD.DICCIONARIO_REAL or 
                                          cursor_factory is ConexionBD.TUPLA_NOMBRADA):
            self.cursor = self.conexion.cursor()
        else:
            self.cursor = self.conexion.cursor(cursor_factory)        
        if Constantes._DEBUG: print(self.cursor.mogrify(self.sentencia, self.parametros))
        self.cursor.execute(self.sentencia, self.parametros)
        
def pruebaConectorBD():
    SQL_PRUEBA = """SELECT table_name FROM information_schema.tables 
                    WHERE table_type = 'BASE TABLE' AND table_schema = 'public' 
                    ORDER BY table_type, table_name;"""
                    
    try:
        print("********************* PRUEBA PARA OBTENER TODOS *********************")
        cnn = ConexionBD(SQL_PRUEBA, params = None, tipoConsulta= ConexionBD.SELECT)
        print(cnn.obtenerTodos())

        print("********************* PRUEBA PARA OBTENER VARIOS *********************")
        cnn = ConexionBD(SQL_PRUEBA, params = None, tipoConsulta= ConexionBD.SELECT)
        for e in cnn.obtenerVarios(2):
            print(e)
        
        print("********************* PRUEBA PARA OBTENER UNO *********************")
        cnn = ConexionBD(SQL_PRUEBA, params = None, tipoConsulta= ConexionBD.SELECT)
        print(cnn.obtenerUno())
        
        print("PRUEBAS A CONECTORBD HECHAS SATISFACTORIAMENTE")
    except Exception, e:
        print(e)
        print(errorcodes.lookup(e.pgcode[:2]))
        print(errorcodes.lookup(e.pgcode))
        print("ERROR EN PRUEBAS A CONECTORBD")


if __name__ == '__main__':
    pruebaConectorBD()
    