# Herramienta para el Sistema de Busqueda de Respuestas: Lemmatizador en WordNet
# Creado por: Charles Ochoa 
"""
Este programa tiene la funcion de tomar las listas proporcionadas por Ludovic Denoyer y Patrick Gallinari en "The Wikipedia XML corpus". Estas listas proporcionan informacion de las categorias usadas por Wikipedia. El programa procesa estos datos y busca conseguir todos los documentos que tienen alguna relacion con categorias de tecnologia.

Modificaciones pendientes:
	- 


Uso:
python lemmatizadorWordnet.py Directorio/de/Entrada/ Directorio/de/Salida/

"""	

import re
from sets import Set
import shutil
import os
import time
directorio = "../Wikipedia/Wikipedia2006/english-categories/"
categories_name = "../Wikipedia/Wikipedia2006/english-categories/categories_name.csv"
categories_hierarchy = "../Wikipedia/Wikipedia2006/english-categories/categories_hcategories.csv"
documents_categories = "../Wikipedia/Wikipedia2006/english-categories/categories_categories.csv"
fuente = "../Wikipedia/Wikipedia2006/2006TXT/"
destino = "../Wikipedia/Wikipedia2006/Reducted-2006TXT/"


def merge(lista):
	if len(lista)==1:
		return Set([lista[0]])
	elif len(lista)==0:
		return Set()
	else:
		return merge(lista[:len(lista)/2]) | merge(lista[len(lista)/2:])

t = time.time()

technology = re.compile(r'technology|Technology')
pairForm_cat_name = re.compile(r'([0-9]+),(".+?")', re.DOTALL)
erre = re.compile(r'\r')
f = open(categories_name)
print "abri el primero"
cat_name = dict(re.findall(pairForm_cat_name,f.read()))
f.close()

f = open(categories_hierarchy)
temp = [x.split(',') for x in re.sub(erre,'',f.read()).split('\n')]
temp = temp[1:len(temp)-1]
cat_hier = {}
for elem in temp:
	cat_hier.setdefault(int(elem[0]),[]).append(int(elem[1]))
print len(cat_hier)


print "abri el segundo"

f.close()
f = open(documents_categories)
doc_cat = [x.split(',') for x in re.sub(erre,'',f.read()).split('\n')]
doc_cat = dict(doc_cat[1:len(doc_cat)-1])

print "abri el tercero"
f.close()

Tech_Categories = []
Tech_Documents = Set()

for x in cat_name:
	if re.findall(technology,cat_name[x]) != []:
		Tech_Categories.append(x)

Tech_Categories = Set(Tech_Categories)
#new = herarquia(Tech_Categories)

otroNivel = True

old_len = 0
print len(Tech_Categories)
while(old_len != len(Tech_Categories)):
	print len(Tech_Categories)
	old_len = len(Tech_Categories)
	new = list(Tech_Categories)

	for cat in Tech_Categories:


		if int(cat) in cat_hier:
			new.extend(cat_hier[int(cat)])
	new2 = Set(new)

	Tech_Categories = Tech_Categories | new2


carpetas_internas = os.listdir(fuente)[1:]
x = 1

for carpeta in carpetas_internas:
	try:
		os.mkdir(destino + carpeta)
	except:
		pass
	documentos_internos = os.listdir(fuente+carpeta + "/")[1:]
	for documento in documentos_internos:
		#print carpeta + "/" +documento
		if int(documento[:len(documento)-4]) in Tech_Categories:
			shutil.copy(fuente+carpeta + "/" + documento,destino+carpeta + "/" + documento)
			print "Documento " + documento + " numero " + str(x) + " ha sido copiado en el directorio:"
			print destino+carpeta + "/" + documento
			x += 1


print str(time.time() - t)










