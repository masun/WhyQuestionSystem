import sys
import optparse
import re
import os
import experiments
from python_google import *
from wikipedia_url_tagCleaner import transform_from_url, return_paragraph
from lemmatizadorWordnet import lemmatizar_varios_documentos
from utility import extract_paragraph_from_snipp
from matrix_builder import WeightedMatrix
from sompy import SOM
from time import time
from datetime import datetime
from question_processing import question_preprocessing
from collections import Counter

WIKIPEDIA_WEBPAGE = 'http://en.wikipedia.org'
file_name_form = re.compile(r'http://en.wikipedia.org/wiki/(.+)',re.DOTALL)

if __name__ == "__main__":
	t_ = time()
	parser = optparse.OptionParser()
	parser.add_option('-q', help='pregunta a realizar (entre comillas)', default="why is the sky blue", type='string', dest='question')
	parser.add_option('-n', help='numero de paginas de wikipedia para extraer la respuesta', type='int', default=10, dest='page_number')
	parser.add_option('-w', help='tamano de la ventana de oracion', type='int',default=20, dest='window')
	parser.add_option('-x', help='numero de columnas para la red neuronal', type='int',default=10, dest='clusters_x')
	parser.add_option('-y', help='numero de filas para la red neuronal', type='int',default=10, dest='clusters_y')
	parser.add_option('-i', help='numero de iteraciones para el entrenamiento de la red neuronal', type='int',default=10, dest='iterations')
	parser.add_option('-d', help='directorio a crear', type='string', dest='directory')
	parser.add_option('-f', help='usado para remover palabras con una frecuencia igual o menor al numero dado', type='int',default=0, dest='term_frequency')
	parser.add_option('-o', help='usado para pruebas offline, colocar el directorio con la informaccion extraida', type='string', default=False, dest='offline_dir')
	(opts, args) = parser.parse_args()
	mandatories = ['directory']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Falta argumento obligatorio"
			parser.print_help()
			exit(-1)
	day_date = str(datetime.now())
	#print day_date
	#exit(-1)
	if opts.offline_dir:
		onlinetime = 0
		lemmatizetime = 0
		FOLDER_CONTAINER = opts.offline_dir
		FOLDER_XML = FOLDER_CONTAINER + "/XML/"
		FOLDER_TXT = FOLDER_CONTAINER +"/TXT/"
		FOLDER_LEMMA = FOLDER_CONTAINER +"/LEMMA/"
		FOLDER_MATRIX = FOLDER_CONTAINER +"/MATRIX/"
		FOLDER_QUESTION = FOLDER_CONTAINER + "/QUESTION/"
		DATE_TIME = str(datetime.now())
		FOLDER_RESULTS = opts.directory + DATE_TIME +"/RESULTS/"
		print "CREACION DE DIRECTORIOS"
		try:
			os.mkdir(opts.directory)
			print "directory folder created"
		except Exception, e:
			print e
		try:
			os.mkdir(opts.directory + DATE_TIME)
			print "datetime folder created"
		except Exception, e:
			print e
		try:
			os.mkdir(FOLDER_RESULTS)
			print "results folder created"
		except Exception, e:
			print e
	else:
	 	FOLDER_CONTAINER = opts.directory + "/" + day_date
		FOLDER_XML = FOLDER_CONTAINER + "/XML/"
		FOLDER_TXT = FOLDER_CONTAINER +"/TXT/"
		FOLDER_LEMMA = FOLDER_CONTAINER +"/LEMMA/"
		FOLDER_MATRIX = FOLDER_CONTAINER +"/MATRIX/"
		FOLDER_RESULTS = FOLDER_CONTAINER +"/RESULTS/"
		FOLDER_QUESTION = FOLDER_CONTAINER + "/QUESTION/"
		print "CREACION DE DIRECTORIOS"

		try:
			os.mkdir(opts.directory)
		except Exception, e:
			print e
		try:
			os.mkdir(FOLDER_CONTAINER)
		except Exception, e:
			print e
		try:
			os.mkdir(FOLDER_XML)
		except Exception, e:
			print e
		try:
			os.mkdir(FOLDER_LEMMA)
		except Exception, e:
			print e
		try:
			os.mkdir(FOLDER_TXT)
		except Exception, e:
			print e
		try:
			os.mkdir(FOLDER_MATRIX)
		except Exception, e:
			print e
		try:
			os.mkdir(FOLDER_RESULTS)
		except Exception, e:
			print e
		try:
			os.mkdir(FOLDER_QUESTION)
		except Exception, e:
			print e
		identi = 1000
		google_url_list = get_google_url(opts.question,1000,WIKIPEDIA_WEBPAGE)
		i_list = []
		o_list = []
		n = 0
		i = 0
		#print google_url_list
		print "Buscando documentos de wikipedia"
		while n < int(opts.page_number):
			#print n
			wiki_list = get_google_from_one_link(google_url_list[i])
			#print wiki_list
			for l in range(len(wiki_list)):
				if n >= int(opts.page_number):
					#print "se salio?"
					break
				#print l
				x =  wiki_list[l]
				new_archive_txt = FOLDER_TXT + str(identi) + ".txt"
				new_destiny = FOLDER_LEMMA + str(identi) + ".txt"
				identi+=1
				transform_from_url(wiki_list[l][0],new_archive_txt)
				i_list.extend(extract_paragraph_from_snipp(new_archive_txt,x[1]))
				os.remove(new_archive_txt)
				n+=1
				#print n
			i+=1

		onlinetime = time()-t_
		for l in i_list:
			o_list.append(FOLDER_LEMMA + l[len(FOLDER_TXT):])
		print "Lemmatizando"
		lemmatizar_varios_documentos(i_list,o_list)
		lemmatizetime = time() - t_ - onlinetime
	print "Creando matriz de pesos"
	w_matrix = WeightedMatrix()
	w_matrix.insert_values(FOLDER_LEMMA)
	#w_matrix.normalize_TF_IDF()
	if opts.term_frequency > 0:
		for x in range(opts.term_frequency+1):
			w_matrix.remove_words_with_frequency(x)
	print w_matrix.TF_IDF_matrix
	
	for row in w_matrix.TF_IDF_matrix:
		print row
	print
	print
	print
	#exit(-1)
	print "Entrenando la red neuronal"
	w_matrix.create_SOM(int(opts.clusters_x),int(opts.clusters_y),opts.iterations)
	tiempo = time()-t_
	print "Tiempo de prueba: " + str(time()-t_) + " segundos"
	print "Experimentos"
	neural_training_time = time() - t_ - lemmatizetime - onlinetime
	#experiments.documents_location_in_Map(w_matrix.SOM_cluster,w_matrix.TF_IDF_matrix,FOLDER_RESULTS)
	#experiments.percentage_documents_in_cluster(w_matrix.SOM_cluster,w_matrix.TF_IDF_matrix)
	experiments.plot_words_distribution(w_matrix,FOLDER_RESULTS)
	#experiments.plot_weight_distribution(w_matrix.TF_IDF_matrix,FOLDER_RESULTS)

	clusters = experiments.documents_location_in_Map(w_matrix.SOM_cluster,w_matrix.TF_IDF_matrix,FOLDER_RESULTS)
	question_lemma_document = question_preprocessing(opts.question,FOLDER_QUESTION)
	lemma_question_doc = open(question_lemma_document)
	print lemma_question_doc.read()
	w_matrix.insert_question_vector(question_lemma_document)
	experiments.location_of_question_in_map(w_matrix,FOLDER_RESULTS)
	w_matrix.test()
	w_matrix.similarity_measure_jacard()
	print w_matrix.most_similar_document_indexes
	print w_matrix.word_list
	print w_matrix.document_list
	print "Prueba finalizada. Resultados guardados en: " + FOLDER_RESULTS
	if not os.path.isfile(opts.directory +"/results.csv"):
		f = open(opts.directory +"/results.csv",'w')
		s = "CODIGO DE LA PREGUNTA,	PREGUNTA,	TIEMPO DE EJECUCION,	DIMENSION X DE LA MATRIZ,	DIMENSION Y DE LA MATRIZ,	NUMERO DE DOCUMENTOS,	NUMERO DE PALABRAS,	NUMERO DE ITERACIONES UTILIZADAS,	TIEMPO ONLINE,	TIEMPO LEMMATIZACION,	TIEMPO ENTRENAMIENTO,	TIEMPO TOTAL\n"
		f.write(s)
		s = ""
		f.close
	f = open(opts.directory +"/results.csv",'a')
	s = day_date + ",\t" #						CODIGO DE LA PRUEBA
	s = s + opts.question+",\t"    #					PREGUNTA
	s = s + str(tiempo) + ",\t"  #						TIEMPO DE EJECUCION
	s = s + str(opts.clusters_x) + ",\t" #				DIMENSION X DE LA MATRIZ
	s = s + str(opts.clusters_y) + ",\t" #				DIMENSION Y DE LA MATRIZ
	s = s + str(w_matrix.number_of_documents) + ",\t"#	NUMERO DE DOCUMENTOS
	s = s + str(w_matrix.number_distinct_words)+",\t"#	NUMERO DE PALABRAS
	s = s + str(opts.iterations) + ",\t" #				NUMERO DE ITERACIONES UTILIZADAS
	s = s + str(onlinetime) + ",\t"	#					TIEMPO DE EXTRACCION DE PAGINAS EN WIKIPEDIA
	s = s + str(lemmatizetime) + ",\t"	#				TIEMPO DE LEMMATIZACION DE VOCABULARIO
	s = s + str(neural_training_time) + ",\t"	#		TIEMPO DE ENTRENAMIENTO DE LA RED NEURONAL
	s = s + str(tiempo) 		#						TIEMPO TOTAL DE EJECUCION
	s += "\n"
	f.write(s)
	f.close()
	f = open(FOLDER_RESULTS + "matriz_pesos.txt",'w')
	f.write(str(w_matrix.TF_IDF_matrix))






'''
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
'''
















