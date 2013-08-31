#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on 16/08/2013

@author: Lennin

funciones varias que permiten manejar mas facilmente las imagenes
Usos:

from Utils.Imagenes import *

path_img = "C:/PATH_A_IMAGEN/img.jpg"

# convertir a binario un archivo de imagen
img = readImage(path_img)

# convertir de imagen a binario compatible con posgresql-psycopg2
binario = convertirImagen(img)

# obtener una cadena aleatoria de N caracteres
N = 10
cadenaAleatoria = nombreAleatorio(N) # obtiene N caracteres aleatorios

# guardar un binario de imagen a un archivo:
path_img = os.path.realpath(os.path.join("C:/PATH_A_IMAGEN/" ,cadenaAleatoria + ".jpg"))
writeImage(img,path_img) # se guarda en "C:/PATH_A_IMAGEN/"+cadenaAleatoria+".jpg" 

# para guardar la imagen en el directorio temporal y con un nombre aleatorio:
nuevo_directorio = writeImage(img) # nuevo directorio tiene el camino hacia la imagen guardada

# para obtener la direccion absoluta de un icono
direccion = obtenerPathIcono('add.png')

'''
import psycopg2 # @UnresolvedImport
import sys
import random
import string
import os

from ConectorBD import ConexionBD

from Constantes import DIRECTORIO_TEMPORAL, absPath, DIRECTORIO_PROYECTO
from Configuracion import Configuracion

def obtenerPathIcono(nombreIcono):
    if nombreIcono == "user.png":
        return absPath("archivos/Iconos/user.png")
    cnf = Configuracion()
    temaIconos = cnf.obtenerValor("TEMAICONOS")
    if temaIconos is not None and temaIconos in cnf.obtenerValor("TEMASICONOSDISPONIBLES"):
        return absPath("archivos/Iconos/"+temaIconos+"/"+nombreIcono)
    else:
        return None

def convertirImagen(img):
    return psycopg2.Binary(img)

def nombreAleatorio(N = 5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))  # @UnusedVariable

def readImage(path):
    try:
        fin = open(path, "rb")
        img = fin.read()
        return img
    except IOError, e:
        print("Error %d: %s" % (e.args[0],e.args[1]))
        sys.exit(1)
    finally:
        if fin:
            fin.close()

def writeImage(data,path=None):
    if path is None:
        # guardar la imagen en un directorio temporal
        path = os.path.realpath(os.path.join(DIRECTORIO_TEMPORAL ,nombreAleatorio() + ".jpg"))
        print(path)
    # guardar imagen en HDD y retornar nada
    try:
        fout = open(path,'wb')
        fout.write(data)
    except IOError, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        if fout:
            fout.close()
    return path


def pruebaImagenes():
    path_prueba_lectura = os.path.realpath(os.path.join(DIRECTORIO_TEMPORAL ,"prueba.jpg"))

    SQL_prueba_insert = 'INSERT INTO imagenes("IMAGE") VALUES(%s);'
    SQL_prueba_select = 'SELECT "IMAGE" FROM imagenes ORDER BY "ID" DESC;'

    # PARTE INSERCION BD:
    Cnn = ConexionBD(SQL_prueba_insert,(convertirImagen(readImage(path_prueba_lectura)),))
    Cnn.ejecutar()

    # PARTE GUARDADO EN HDD DESDE BD
    Cnn = ConexionBD(SQL_prueba_select)
    img = Cnn.obtenerUno()[0]
    pth = writeImage(img)
    
    print("PATH LECTURA: " + path_prueba_lectura )
    
    print("PATH ESCRITURA: " + pth)
    # PRUEBA FINAL
    assert readImage(pth) == readImage(path_prueba_lectura)
    
    # Busqueda de un icono
    direct = obtenerPathIcono('add.png')
    print(direct)
    assert direct  == os.path.realpath(os.path.join(DIRECTORIO_PROYECTO ,"archivos/Iconos/elementary/add.png"))
    
    # Busqueda de icono user.png
    direct = obtenerPathIcono('user.png')
    print(direct)
    assert direct  == os.path.realpath(os.path.join(DIRECTORIO_PROYECTO ,"archivos/Iconos/user.png"))
    print("****** PRUEBA IMAGEN FINALIZADA SATISFACTORIAMENTE ******")


if __name__ == '__main__':
    pruebaImagenes()