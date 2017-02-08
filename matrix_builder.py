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
from sompy import SOM
from scipy import array

default_destiny = "obtencionPruebas/MATRIX/"
default_origin  = "obtencionPruebas/LEMMA/"
default_reunir_file = "obtencionPruebas/MATRIX/all_words.txt"
#default_number_of_doc = len(os.listdir(default_origin)) -1
default_test_doc = "obtencionPruebas/LEMMA/100011-0.txt"


class WeightedMatrix:
	"""docstring for WeightMatrix"""
	def __init__(self):
		self.number_of_documents = 0 				#integer
		self.number_distinct_words = 0 				#integer
		self.number_total_words = 0 				#integer
		self.number_of_words_in_document = []		#list of integer (size: number of documents)
		self.document_list = []						#list of strings (size: number of documents)
		self.word_total_frequency = []				#list of integer (size: number of distinct words)
		self.word_list = []							#list of strings (size: number of distinct words)
		self.document_frequency = []				#list of integer (size: number of distinct words)
		self.TF_IDF_matrix = []						#list of list of floats (size: number of documents x number of words)
		self.word_frequency_matrix = []				#list of list of integer (size: number of documents x number of words)
		self.question_frequency_vector = []			#list of floats (size: number of distinct words)
		self.question_TF_IDF_vector = []			#list of floats (size: number of distinct words)
		self.SOM_cluster = None							#one SOM object
		self.document_coordinates = []				#list of x , y pairs
		self.document_coordinates_counter = []
		self.question_coordinates = None
		self.min_distance_cluster = None
		self.documents_in_cluster_indexes = []		#list of integer(size of the recall)
		self.most_similar_document_indexes = []



	def __str__(self):
		return """Weighted Matrix
		number_of_documents = """ + str(self.number_of_documents) + """
		number_distinct_words = """ + str(self.number_distinct_words) + """
		number_total_words = """ + str(self.number_total_words) + """
		number_of_words_in_document = """ + str(self.number_of_words_in_document) + """
		word_total_frequency = """ + str(self.word_total_frequency) + """
		question_frequency_vector = """ + str(self.question_frequency_vector)




	def insert_values(self,dir_fuente=default_origin):
		list_files = os.listdir(dir_fuente)
		set_words = set()
		for file_ in list_files:
			if file_ != ".DS_Store":
				self.number_of_documents += 1
				self.document_list.append(file_)
				f = open(dir_fuente + file_)
				word_list = f.read().split()
				print len(word_list)
				self.number_of_words_in_document.append(int(len(self.word_list)))
				self.number_total_words += len(self.word_list)
				set_words |= set(word_list)
		#print self.number_of_words_in_document
		self.word_list = list(set_words)
		self.number_distinct_words = len(self.word_list)
		self.document_frequency = [0]*self.number_distinct_words
		self.word_total_frequency = [0]*self.number_distinct_words
		for file_ in self.document_list:
			new_row = [0]*self.number_distinct_words
			f = open(dir_fuente + file_)
			word_list = f.read().split()
			counter_word = Counter(word_list)
			for word in counter_word:
				new_row[self.word_list.index(word)] = counter_word[word]
				self.document_frequency[self.word_list.index(word)] += 1
				self.word_total_frequency[self.word_list.index(word)] += counter_word[word]

			self.word_frequency_matrix.append(new_row)
		self.insert_TF_IDF_matrix()
		#print self
		#exit(-1)

	def insert_TF_IDF_matrix(self):
		for x in range(self.number_of_documents):
			new_row = []
			for y in range(self.number_distinct_words):
				new_row.append(0)
			self.TF_IDF_matrix.append(new_row)
		for x in range(len(self.TF_IDF_matrix)):
			for y in range(len(self.TF_IDF_matrix[x])):
				if self.word_frequency_matrix[x][y]:
					self.TF_IDF_matrix[x][y] = (1+math.log(float(self.word_frequency_matrix[x][y])))*(math.log((float(self.number_of_documents)/(float(self.document_frequency[y])))))
				else:
					self.TF_IDF_matrix[x][y] = 0


	def normalize_TF_IDF(self):
		for x in range(len(self.TF_IDF_matrix)):
			min_ = min(self.TF_IDF_matrix[x])
			for y in range(len(self.TF_IDF_matrix[x])):
				self.TF_IDF_matrix[x][y] = self.TF_IDF_matrix[x][y] - min_
			sum_ = sum(self.TF_IDF_matrix[x])
			for y in range(len(self.TF_IDF_matrix[x])):
				self.TF_IDF_matrix[x][y] = self.TF_IDF_matrix[x][y] / sum_
		for x in range(len(self.TF_IDF_matrix)):
			print sum(self.TF_IDF_matrix[x])
	

	def remove_words_with_frequency(self,f):
		size_ = len(self.document_frequency)
		x = 0
		while x < size_:
			if self.document_frequency[x] == f:
				size_ -= 1
				self.document_frequency = self.document_frequency[:x] + self.document_frequency[x+1:]
				self.word_list = self.word_list[:x] + self.word_list[x+1:]
				self.number_distinct_words += -1
				self.word_total_frequency = self.word_total_frequency[:x] + self.word_total_frequency[x+1:]
				for y in range(len(self.word_frequency_matrix)):
					self.number_total_words += -1*self.word_frequency_matrix[y][x]
					self.number_of_words_in_document[y] += -1*self.word_frequency_matrix[y][x]
					self.TF_IDF_matrix[y] = self.TF_IDF_matrix[y][:x] + self.TF_IDF_matrix[y][x+1:]
					self.word_frequency_matrix[y] = self.word_frequency_matrix[y][:x] + self.word_frequency_matrix[y][x+1:]
			else:
				x += 1

	def insert_question_vector(self,question_lemma_document):
		self.insert_new_document(question_lemma_document,'question')
		self.question_vector = self.word_frequency_matrix[-1]
		#print self.word_frequency_matrix[-1]
		for word_index in range(len(self.word_frequency_matrix[-1])):
			self.question_TF_IDF_vector.append(self.TF_IDF_value(-1,word_index))
		min_ = min(self.question_TF_IDF_vector)
		for x in range(len(self.question_TF_IDF_vector)):
			self.question_TF_IDF_vector[x] = self.question_TF_IDF_vector[x] - min_
		sum_ = sum(self.question_TF_IDF_vector)
		for x in range(len(self.question_TF_IDF_vector)):
			self.question_TF_IDF_vector[x] = self.question_TF_IDF_vector[x] / sum_

	def TF_IDF_value(self,doc_index,word_index):
		#print "doc_index " + str(doc_index)
		#print "word_index " + str(word_index)
		#print "len(word_frequency_matrix) " + str(len(self.word_frequency_matrix))
		#print "len(word_frequency_matrix["+str(doc_index)+"]) " + str(len(self.word_frequency_matrix[doc_index]))
		#print "self.document_frequency " + str(len(self.document_frequency))
		#print "return (1+math.log(float( " + str(self.word_frequency_matrix[doc_index][word_index]) + " )))*(math.log((float(" +  str(self.number_of_documents) + ")/(float( " + str(self.document_frequency[word_index]) + " )))))"
		#print
		#print
		if self.word_frequency_matrix[doc_index][word_index]:
			print "    TF_IDF mayor que 0:   " + str((1+math.log(float(self.word_frequency_matrix[doc_index][word_index])))*(math.log((float(self.number_of_documents)/(float(self.document_frequency[word_index]))))))
			print self.word_list[word_index]
			return (1+math.log(float(self.word_frequency_matrix[doc_index][word_index])))*(math.log((float(self.number_of_documents)/(float(self.document_frequency[word_index])))))
		else:
			return 0

	def insert_word(self,word,document_name,frequency=1):
		doc_index = self.document_list.index(document_name)

		if word not in self.word_list:
			word_index = len(self.word_list)
			self.word_list.append(word)
			self.number_distinct_words += 1
			self.word_total_frequency.append(frequency)
			self.word_list.append(word)
			self.document_frequency.append(1)
			for row_index in range(len(self.word_frequency_matrix)):
				self.word_frequency_matrix[row_index].append(0)
		else:
			word_index = self.word_list.index(word)
			self.word_total_frequency[word_index] += frequency
			if self.word_frequency_matrix[doc_index][word_index] == 0:
				self.document_frequency[word_index] += 1
		self.number_of_words_in_document[doc_index] += frequency
		self.number_total_words += frequency
		self.word_frequency_matrix[doc_index][word_index] += frequency
			

	

	def insert_new_document(self,document, name):
		print "IS GONNA BE INSERTED A NEW DOCUMENT"
		f = open(document)
		words = f.read().split()
		print words
		self.number_of_documents += 1
		self.document_list.append(name)
		self.word_frequency_matrix.append([0]*self.number_distinct_words)
		self.number_of_words_in_document.append(0)
		for word in words:
			self.insert_word(word,name)



	def question_cluster_distance(self):
		(q_x,q_y) = self.SOM_cluster.best_match(self.question_TF_IDF_vector)
		min_ = 1000
		min_x = -1
		min_y = -1
		for (x,y) in self.document_coordinates:
			distance = math.sqrt((q_x -x)**2 + (q_y - y)**2)
			if distance < min_:
				min_ = distance
				min_x = x
				min_y = y
		print "Resultado Distancia:"
		print "		(x,y) = (" + str(min_x) + ", " + str(min_y) + ")"
		self.min_distance_cluster = (min_x,min_y)
		return (min_x,min_y)


	def recall_document_result(self):
		for i in range(len(self.document_coordinates)):
			if self.document_coordinates[i] == self.min_distance_cluster:
				self.documents_in_cluster_indexes.append(i)



	def create_SOM(self,x,y,I,LR=0.05):
		if self.SOM_cluster == None:
			self.SOM_cluster = SOM(x,y,self.number_distinct_words,LR)
		self.SOM_cluster.train(I,self.TF_IDF_matrix)


	def test(self):
		coor_y = []
		coor_x = []
		clusters = []
		if  self.question_TF_IDF_vector == []:
			print "ERROR, Vector TF_IDF de pregunta aun no creado."
		else:
			for row in range(len(self.TF_IDF_matrix[:-1])):
				(x,y) = self.SOM_cluster.best_match(array(self.TF_IDF_matrix[row]))
				self.document_coordinates.append((x,y))
				coor_y.append(y)
				coor_x.append(x)
			self.question_coordinates = self.SOM_cluster.best_match(array(self.question_TF_IDF_vector))
		self.document_coordinates_counter = Counter(self.document_coordinates)
		self.question_cluster_distance()
		self.recall_document_result()
		print "Cantidad de documentos en el cluster mas cercano: " + str(self.document_coordinates_counter[self.min_distance_cluster])
		print "Documentos contenidos dentro del cluster mas cercano"
		for i in self.documents_in_cluster_indexes:
			print "Nombre del documento: " + self.document_list[i]
			print
			print "Matriz de peso TF-IDF"
			print self.TF_IDF_matrix[i]
		print "Porcentaje que representa estos documentos: " + str(float(self.document_coordinates_counter[self.min_distance_cluster])/float(self.number_of_documents)*100.0) + " %"


	def similarity_measure_jacard(self):
		max_sim_number = -1000
		max_document_index = -1
		disordered_list = []
		for j in range(len(self.TF_IDF_matrix[:-1])):
			sum_wq_wj = float(sum([a*b for a,b in zip(self.TF_IDF_matrix[j],self.question_TF_IDF_vector)]))
			sum_wq_2 = float(sum([a**2 for a in self.question_TF_IDF_vector]))
			sum_wj_2 = float(sum([a**2 for a in self.TF_IDF_matrix[j]]))
			jacard_sim_ = sum_wq_wj / (sum_wq_2 + sum_wj_2 - sum_wq_wj)
			disordered_list.append((j,self.document_list[j],jacard_sim_))
			if jacard_sim_ > max_sim_number:
				max_sim_number = jacard_sim_
				max_document_index = j
		#print "El documento con mayor Jacard similitud es: " + self.document_list[max_document_index]
		#print "Con un valor de similitud de: " + str(max_sim_number)
		self.most_similar_document_indexes = sorted(disordered_list, key= lambda similarity: similarity[2],reverse=True)

	def similarity_measure_cosine(self):
		max_sim_number = -1000
		max_document_index = -1
		disordered_list = []
		for j in range(len(self.TF_IDF_matrix[:-1])):
			sum_wq_wj = float(sum([a*b for a,b in zip(self.TF_IDF_matrix[j],self.question_TF_IDF_vector)]))
			sum_wq_2 = float(sum([a**2 for a in self.question_TF_IDF_vector]))
			sum_wj_2 = float(sum([a**2 for a in self.TF_IDF_matrix[j]]))
			jacard_sim_ = sum_wq_wj / (sum_wq_2 * sum_wj_2)**.5
			disordered_list.append((j,self.document_list[j],jacard_sim_))
			if jacard_sim_ > max_sim_number:
				max_sim_number = jacard_sim_
				max_document_index = j
		print "El documento con mayor Cosine similitud es: " + self.document_list[max_document_index]
		print "Con un valor de similitud de: " + str(max_sim_number)
		self.most_similar_document_indexes = sorted(disordered_list, key= lambda similarity: similarity[2],reverse=True)









if __name__ == '__main__':
	matriz_de_pesos = WeightedMatrix()
	matriz_de_pesos.insert_values()
	matriz_de_pesos.normalize_TF_IDF()
