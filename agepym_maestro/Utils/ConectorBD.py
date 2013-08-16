'''
Created on 15/08/2013

@author: Lennin
'''

import psycopg2  # @UnresolvedImport
from psycopg2.extras import DictCursor, RealDictCursor, NamedTupleCursor # @UnresolvedImport
from psycopg2 import errorcodes # @UnresolvedImport
from Configuracion import Configuracion

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
        self.cursor.execute(self.sentencia, self.parametros)
        self.conexion.commit()
        if cerrarAlFinalizar: self.cerrar()
        
    def obtenerTodos(self,cursor_factory=None, cerrarAlFinalizar = True):
        self.__crearCursor(cursor_factory)
        valores = self.cursor.fetchall()
        if cerrarAlFinalizar: self.cerrar()
        return valores
    
    def obtenerUno(self, cursor_factory=None, cerrarAlFinalizar = True):
        self.__crearCursor(cursor_factory)
        valor = self.cursor.fetchone()
        if cerrarAlFinalizar: self.cerrar()
        return valor
    
    def obtenerVarios(self, cant, cursor_factory = None, cerrarAlFinalizar = True):
        self.__crearCursor(cursor_factory)
        while True:
            valores = self.cursor.fetchmany(cant)
            if not valores: 
                if cerrarAlFinalizar: self.cerrar()
                break
            yield valores
    
    def __crearCursor(self, cursor_factory = None):
        if cursor_factory is None or not (cursor_factory is ConexionBD.DICCIONARIO or 
                                          cursor_factory is ConexionBD.DICCIONARIO_REAL or 
                                          cursor_factory is ConexionBD.TUPLA_NOMBRADA):
            self.cursor = self.conexion.cursor()
        else:
            self.cursor = self.conexion.cursor(cursor_factory)
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
        for e in cnn.obtenerVarios(1):
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
    