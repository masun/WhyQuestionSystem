# Herramienta para el Sistema de Busqueda de Respuestas: Creador de Matriz de frecuencias
# Creado por: Charles Ochoa 
"""
Este programa tiene por objetivo tomar una lista de directorios, en donde internamente contienen documentos con listas de palabras. El objetivo es generar una matriz de documentos en funcion de las palabras que contienen, tomando como ese valor el resultado de la funcion TF_IDF (term frequency, inteverse document frequency)

Modificaciones pendientes:
	- Reducir el numero de palabras relevantes por documento
	- 
	- 


Uso Ejemplo:
python matrixCreation.py ../Directorio/Fuente/ ../Directorio/Destino/ ../Directorio/Respaldo/

Uso Actual:
python matrixCreation.py ../Wikipedia/Wikipedia2006/Pruebas/fuente/ ../Wikipedia/Wikipedia2006/Pruebas/destino/ ../Wikipedia/Wikipedia2006/Pruebas/respaldo/

"""	

import os 
import re
import sys
from sets import Set
from collections import Counter
import shutil
import math


def TF_IDF(tf, ttf, df, nd):
	#print tf
	#print ttf
	#print df
	#print nd
	return (float(tf)/float(ttf))*(1.0 + math.log((float(df)/float(nd))))

#Esta funcion toma las palabras encontradas en "contenido" y retorna un multiconjunto, o un diccionario de palabras con su frecuencia
def createMultiset(contenido):
	lista = contenido.split()
	c = Counter()
	for elem in lista:
		c[elem] += 1
	return c

#Esta funcion toma las palabras encontradas en "contenido" y retorna un multiconjunto, o un diccionario de palabras con su frecuencia, sin embargo asignando a cada frecuencia el valor de 1
def createListFrec1(contenido):
	lista = contenido.split()
	c = Counter()
	for elem in lista:
		c[elem] = 1
	return c
	

#La variable contenido contiene una lista de palabras por frecuencia. Esta funcion transforma esa informacion en un diccionario de frecuencias o en un multiconjunto
def leerDeMultiset(contenido):
	lista = contenido.split()
	c = Counter()
	for l in lista:
		tupla = l.split(",")
		c[tupla[0]] = tupla[1]
	return c
	
#La variable contenido contiene una lista de palabras por frecuencia. Esta funcion transforma esa informacion en una lista de palabras, ignorando su frecuencia
def leerDeMultisetAsLista(contenido):
	lista = contenido.split()
	c = []
	for l in lista:
		tupla = l.split(",")
		c.append(tupla[0])
	return c

#Esta funcion primero lee un archivo, que contiene una lista de palabras. Luego con esa informacion puede crear 2 cosas: un multiconjunto, o un conjunto con apariencia de multiconjunto. Este segundo es usado para luego contar en cuantos documentos ha aparecido la palabra
def listaAMulticonjunto(i,o,frecValid):
	fi = open(i,'r')
	content = fi.read()
	fi.close()
	if frecValid:
		multi = createMultiset(content)
	else:
		multi = createListFrec1(content)
	fo = open(o,'w')
	for elem in multi:
		fo.write(elem+","+str(multi[elem])+"\n")
	fo.close()

#Esta funcion vierte la informacion de un multiconjunto en el archivo ubicado en "directorio"
def escribirMulticonjunto(multi,directorio):
	f = open(directorio,'w')
	for e in multi:
		f.write(str(e)+","+str(multi[e])+"\n")
	f.close()

#Esta funcion regresa una lista de multiconjuntos proveniente de todos los archivos contenidos en "lista"
def devolverMulticonjuntos(lista):
	nueva = []
	for e in lista:
		f = open(e,'r')
		c = leerDeMultiset(f.read())
		f.close()
		nueva.append(c)
	return nueva

def recorreListaAMulticonjunto(inFolder, outFolder, respaldo):
	#print inFolder
	lista = os.listdir(inFolder)
	nuevaLista = []
	for doc in lista[1:]:
		#print "   " + doc
		if doc[len(doc)-3:] != "txt":
			raise NameError("Wrong extention: "+doc)
		dirI = inFolder + doc
		dirO = outFolder + doc[:len(doc)-3] + "csv"
		dirR = respaldo + doc[:len(doc)-3] + "csv"
		listaAMulticonjunto(dirI,dirO,1)
		shutil.copyfile(dirO,dirR)
		nuevaLista.append(dirO)
	return nuevaLista

def recorreListaAMulticonjunto2(inFolder, outFolder, respaldo):
	#print inFolder
	lista = os.listdir(inFolder)
	nuevaLista = []
	for doc in lista[1:]:
		#print "   " + doc
		if doc[len(doc)-3:] != "txt":
			raise NameError("Wrong extention: "+doc)
		dirI = inFolder + doc
		dirO = outFolder + doc[:len(doc)-3] + "csv"
		listaAMulticonjunto(dirI,dirO,0)
		nuevaLista.append(dirO)
	return nuevaLista


def merge2(dir1,dir2):
	#print "merge" + dir1
	f1 = open(dir1)
	c1 = leerDeMultiset(f1.read())
	f1.close()
	f2 = open(dir2)
	c2 = leerDeMultiset(f2.read())
	f2.close()
	for e in c2:
		c1[e] = int(c1[e]) + int(c2[e])
	escribirMulticonjunto(c1,dir1)
	os.remove(dir2)
	return dir1

def mergeAll(listaDir):
	if len(listaDir) > 2:
		dir1 = mergeAll(listaDir[:(len(listaDir)/2)])
		dir2 = mergeAll(listaDir[(len(listaDir)/2):])
		return merge2(dir1,dir2)
	elif len(listaDir) == 2:
		return merge2(listaDir[0],listaDir[1])
	elif len(listaDir) == 1:
		return listaDir[0]
	
def regresarListaArchivos(directorio):
	nueva = []
	lista = os.listdir(directorio)[1:]
	for l in lista:
		#print l
		l2 = os.listdir(directorio + l + "/")[1:]
		if l2[0][len(l2[0])-4] == '.':
			for l3 in l2:
				nueva.append(directorio + l + "/" + l3)
	return nueva

# Regresa una lista de todos los archivos, desde su raiz de carpetas "part-xxxx" donde xxxx representa un nombre
def creacionTablaDocumentos(directorioDestino, directorioFuente,directorioRespaldo,listFiles):
	f = open(directorioDestino+"listaDocumentos.csv",'w')
	for l in listFiles:
		fuenteIn = directorioFuente+l+"/"
		lista = os.listdir(fuenteIn)
		if lista[0] == ".DS_Store":
			lista = lista[1:]
		for doc in lista:
			#print doc
			archivo = open(fuenteIn + doc,'r')
			f.write(l+"/"+ doc + "," + str(len(archivo.read().split()))+"\n")
			archivo.close()
	f.close()

def creacionMatriz(dirDestino,dirPalabraFrec,dirCuantosDoc,documentoTam,dirRespaldo):
	pf = open(dirPalabraFrec,'r')
	dt = open(documentoTam,'r')
	cd = open(dirCuantosDoc,'r')
	conPF = pf.read()
	tablaPalFre = leerDeMultiset(conPF)
	listaPalabra = leerDeMultisetAsLista(conPF)
	pf.close()
	del pf
	tablaDocTam = leerDeMultiset(dt.read())
	dt.close()
	del dt
	tablaPalDoc = leerDeMultiset(cd.read())
	cd.close()
	del cd
	numeroTotalDoc = len(tablaDocTam)
	matriz = open(dirDestino + "matriz.csv" , 'w')
	x=0
	for e in tablaDocTam:
		dms = open(dirRespaldo + e[:len(e)-3] + "csv",'r')
		docMultiset = leerDeMultiset(dms.read())
		dms.close()
		for palabra in docMultiset:
			y = listaPalabra.index(palabra)
			frecuenciaPalabra = docMultiset[palabra]
			frecuenciaEnDocumentos = tablaPalDoc[palabra]
			frecuenciaEnCorpus = tablaPalFre[palabra]
			value = TF_IDF(int(frecuenciaPalabra),int(frecuenciaEnCorpus),int(frecuenciaEnDocumentos),int(numeroTotalDoc))
			matriz.write(str(x)+","+str(y)+","+str(value)+"\n")
		x=x+1
	matriz.close()
		
	
	
if __name__ == '__main__':
	#python matrixCreation.py ../Wikipedia/Wikipedia2006/Pruebas/fuente/ ../Wikipedia/Wikipedia2006/Pruebas/destino/ ../Wikipedia/Wikipedia2006/Pruebas/respaldo/
	#dirFuente = sys.argv[1]
	#dirDestino = sys.argv[2]
	#dirRespaldo = sys.argv[3]
	dirFuente = "../Wikipedia/Wikipedia2006/Pruebas/fuente/"
	dirDestino = "../Wikipedia/Wikipedia2006/Pruebas/destino/"
	dirRespaldo = "../Wikipedia/Wikipedia2006/Pruebas/respaldo/"
	listFiles = os.listdir(dirFuente)[1:]
	#final = Counter()
	listaCompletaArchivosCSV = []
	listaCompletaConjuntosCSV = []
	frecDoc = dirDestino +"/frecDoc/"
	try:
		os.mkdir(frecDoc)
	except:
		pass	

	for l in listFiles:
		bigs = len(listFiles)
		
		# Creacion de archivos en nueva lista
		
		try:
			os.mkdir(dirDestino+l)
		except:
			pass
		try:
			os.mkdir(dirRespaldo+l)
		except:
			pass
		try:
			os.mkdir(frecDoc + l)
		except:
			pass
		listaCompletaArchivosCSV.extend( recorreListaAMulticonjunto(dirFuente+l+"/",dirDestino+l+"/",dirRespaldo+l+"/") )
		listaCompletaConjuntosCSV.extend( recorreListaAMulticonjunto2(dirFuente+l+"/",frecDoc+l+"/",dirRespaldo+l+"/") )
	
	#En este primer merge, se realizara la combinacion de los archivos que tengan una lista correspondiente al multiconjunto de frecuencia de cada documento.
	print "Se realizara el merge 1"
	result = mergeAll(listaCompletaArchivosCSV)
	dirPalabraFrec = dirDestino+"frecuenciaTotal.csv" # es el directorio en donde se encuentra el multiconjunto de palabras
	os.rename(result,dirPalabraFrec)
	#En el segundo merge, se realizara la combinacion de los archivos que tengan una lista correspondiente a los multiconjuntos creados con frecuencia 1, para contar en cuantos documentos aparece cada palabra.
	print "Se realizara el merge 2"
	result = mergeAll(listaCompletaConjuntosCSV)
	dirPalabraFrecEnDoc = dirDestino+"frecuenciaEnDocumentos.csv" # es el directorio en donde se encuentra el multiconjunto de palabras
	os.rename(result,dirPalabraFrecEnDoc)

	print "Lista la combinacion de archivos. Resultado: multiconjunto.csv creado"
	creacionTablaDocumentos(dirDestino,dirFuente,dirRespaldo,listFiles)
	documentoTam = dirDestino + "listaDocumentos.csv" # es el directorio en donde se encuentra la lista de documentos con el numero de palabras
	creacionMatriz(dirDestino,dirPalabraFrec,dirPalabraFrecEnDoc,documentoTam,dirRespaldo)



	