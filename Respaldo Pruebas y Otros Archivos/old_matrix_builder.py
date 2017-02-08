
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

default_destiny = "obtencionPruebas/MATRIX/"
default_origin  = "obtencionPruebas/LEMMA/"
default_reunir_file = "obtencionPruebas/MATRIX/all_words.txt"
default_number_of_doc = len(os.listdir(default_origin)) -1
default_test_doc = "obtencionPruebas/LEMMA/100011-0.txt"




def add_document_list(self, dir_fuente):

	list_files = os.listdir(dir_fuente)
	for file_ in list_files:
		if file_ != ".DS_Store":
			self.document_list.append(file_)
		
	f = open(dir_destino+ "all_words.txt")
	all_words = list(Set(f.read().split()))
	numb_of_words = len(all_words)
	self.word_list = all_words
	number_of_documents = len(list_files)
	if list_files[0] == ".DS_Store":
		number_of_documents+= -1
	for file_ in list_files:
		if file_ != ".DS_Store":
			self.document_list.append(file_)
			multico_file = multicount_in_one_file(dir_fuente + file_)
			new_row = [0]*numb_of_words
			tfidf = TF_IDF(dir_fuente, multico_file,dir_fuente + file_,number_of_documents)
			for term,value in tfidf:
				new_row[all_words.index(term)] = value
			self.matrix.append(new_row)
		else:
			number_of_documents += -1




# Esta funcion lee de un archivo, una lista de palabras con una respectiva frecuencia para ser introducidas en un multiconjunto
def create_multicon_from_multicon_archive(file_):
	f = open(file_)
	contenido = f.read()
	f.close()
	lista = contenido.split()
	c = Counter()
	for l in lista:
		tupla = l.split(",")
		c[tupla[0]] = tupla[1]
	return c


# De una lista de documentos, cuenta en cuantos documentos aparece una determinada palabra
def document_frequency_fun(dir_fuente=default_origin):
	list_files = os.listdir(dir_fuente)
	ret = []
	doc_counter = Counter()
	for file_ in list_files:
		if file_ != ".DS_Store":
			dir_fuente_doc = dir_fuente + file_
			f = open(dir_fuente_doc,'r')
			content = f.read()
			f.close()
			list_ = list(Set(content.split()))
			for word in list_:
				doc_counter[word] += 1
	return doc_counter		

# Esta funcion mezcla una lista de multiconjuntos en un solo multiconjunto
def merge(multicon_list):
	if len(multicon_list) >= 2:
		multicon_1 = merge(multicon_list[:(len(multicon_list)/2)])
		multicon_2 = merge(multicon_list[(len(multicon_list)/2):])
		return  multicon_1 + multicon_2
	elif len(multicon_list) == 1:
		return multicon_list[0]

# Esta funcion reune todas las palabras de una lista de documentos en un solo documento
def reunir(dir_fuente=default_origin, dir_destino=default_destiny):
	list_files = os.listdir(dir_fuente)
	d = open(dir_destino+ "all_words.txt",'w')
	for file_ in list_files:
		if file_ != ".DS_Store":
			dir_fuente_doc = dir_fuente + file_
			f = open(dir_fuente_doc,'r')
			d.write(f.read())
			f.close()
	d.close()

# Esta funcion lee un archivo y lo convierte en un multiconjunto
def multicount_in_one_file(file_=default_reunir_file):
	f = open(file_)
	content = f.read()
	content = content.split()
	multi = Counter(content)
	return multi

# Funcion que calcula el valor TF-IDF
def TF_IDF(dir_fuente,multicon_doc_freq,file_=default_test_doc,number_of_documents=default_number_of_doc):
	f = open(file_)
	content = f.read()
	content = content.split()
	total_of_terms = len(content)
	all_terms_and_frequencies = Counter(content)
	multi_doc_frec = document_frequency_fun(dir_fuente)
	TF_IDF_list = []
	for term in all_terms_and_frequencies:
		term_frequency = all_terms_and_frequencies[term]
		document_frequency = multi_doc_frec[term]
		tfidf = (float(term_frequency)/float(total_of_terms))*(1.0 + math.log((float(document_frequency)/float(number_of_documents)))) + 1
		TF_IDF_list.append([term,tfidf])
	TF_IDF_list.sort()
	return TF_IDF_list


def frequency_matrix(dir_fuente=default_origin,dir_destino=default_destiny):
	list_files = os.listdir(dir_fuente)
	f = open(dir_destino+ "all_words.txt")
	all_words = list(Set(f.read().split()))
	numb_of_words = len(all_words)
	matrix = []
	matrix.append([None] + all_words)
	for file_ in list_files:
		if file_ != ".DS_Store":
			new_row = [0]*numb_of_words
			multico_file = multicount_in_one_file(dir_fuente + file_)
			for term in multico_file:
				new_row[all_words.index(term)] = multico_file[term]
			matrix.append([file_] + new_row)
	return matrix


def save_as_csv(matrix, destiny_path = default_destiny + "default_matrix.csv"):
	string_ = ""
	for row in matrix:
		for box in row:
			if box is not None:
				string_+= str(box) + ", "
			else:
				string_+= "  , "
		string_= string_[:len(string_)-2] + "\n"
	f = open(destiny_path,'w')
	f.write(string_)
	f.close()

def generate_matrix(dir_o,dir_d):
	reunir(dir_o,dir_d)
	return WeightedMatrix(dir_o,dir_d)

def main():
	reunir()
	multi = create_multicon_from_list_archive()
	for c in multi:
		print c + ", " + str(multi[c])
	print "------------------------"
	doc_ = document_frequency()
	for d in doc_:
		print d + ", " + str(doc_[d])
	mat = frequency_matrix()
	save_as_csv(mat)
	exit(-1)
	for m in mat:
		print m

